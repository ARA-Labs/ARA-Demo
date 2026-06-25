# Algorithm — Math + Pseudocode of the Frontier Levers

Notation follows the run code. `M` = Nesterov momentum of the gradient for a 2-D weight `W` with
shape `(rows, cols)`; `lr(t, role)` = per-role learning rate at step `t`.

## 1. Baseline Muon update (the starting point)

Mathematical form:

```
M_t   = mu * M_{t-1} + g_t                      # momentum buffer
M_nag = g_t + mu * M_t                          # Nesterov lookahead
O     = NS_12(M_nag)                            # Newton-Schulz, 12 iters, (a,b,c)=(2,-1.5,0.5)
U     = O * sqrt(max(1, rows/cols))             # shape-aware scale
W     = (1 - lr*wd) * W - lr * U                # decoupled weight decay + step
```

Newton-Schulz iteration (per step `X_0 = M / ||M||_F`):

```
X_{k+1} = a*X_k + b*(X_k X_k^T) X_k + c*(X_k X_k^T)^2 X_k
```

Pushes singular values of `M` toward 1 (orthogonalization) without an SVD.

## 2. MuonEq — pre-NS per-row normalization (C03)

```
for each row i of M_nag:
    M_nag[i] <- M_nag[i] / (||M_nag[i]||_2 + eps)
O <- NS(M_nag)                                  # NS now sees equalized rows
```

Pre-NS (improves the orthogonalization input) strictly dominates post-NS NorMuon
(`O / sqrt(EMA(row 2nd moment))`), and stacking both double-corrects -> no gain.

## 3. Aurora row-rescale (C04) — interleaved with NS

```
X <- M_nag
for k in range(K_outer):
    X <- NS_inner(X)
    d <- per_row_scale(X, beta=0.25)            # running per-row magnitude
    X <- X / d
O <- X
```

Clamps per-neuron update variance, which is what makes the larger global LR (0.0375, up from 0.025)
stable.

## 4. Contra-Muon — ramping early decorrelation (C08, C14)

```
g_unit       = g_t / ||g_t||_op                 # unit operator-norm raw gradient
contra_coeff = linear_ramp(t, start=-0.2, end=0.0, end_step=1920)
O_contra     = O + contra_coeff * g_unit        # early: subtract a slice of the greedy direction
```

`contra_coeff < 0` early pushes the update *away* from the instantaneous gradient (exploration /
conditioning); anneals to pure Muon by step ~1920, which is where the §8 crossover occurs.

## 5. soft-Muon — endgame orthogonalization softening (C14)

```
soft_blend = linear_ramp(t, start=0.0, end=0.80, start_step=2400, end_step=2890)
O_hard     = NS(M)                              # singular values -> 1
O_soft     = soft_via_NS(M, p=0.1)             # singular values -> s^0.1 (gentler)
O          = (1 - soft_blend)*O_hard + soft_blend*O_soft
```

Near convergence, full orthogonalization is too aggressive; soft-Muon keeps more natural magnitude
structure for fine-tuning. Mechanism partly `[HYP]`.

## 6. SOAP-on-subset preconditioner (C05, C13)

Applied only if `should_soap_param(name)` (MLP `fc`/`proj` and attention `V`):

```
# every step (cheap):
row_gg = beta2*row_gg + (1-beta2)*(U @ U^T)     # left Gram factor
col_gg = beta2*col_gg + (1-beta2)*(U^T @ U)     # right Gram factor
# every SOAP_PRECONDITION_FREQUENCY (=10) steps (expensive):
q_row, _ = QR(row_gg);  q_col, _ = QR(col_gg)   # refresh eigenbasis
# every step:
P        = q_row^T @ U @ q_col                  # project into eigenbasis
exp_avg_sq = beta2*exp_avg_sq + (1-beta2)*P^2   # Adam 2nd moment IN basis
P_hat    = P / (exp_avg_sq^0.5 + eps)           # SOAP_DENOM_POWER = 0.5 (RMS)
S        = q_row @ P_hat @ q_col^T              # project back
S        = S * (||U||_F / ||S||_F)              # norm-preserve: change shape, not magnitude
U_soap   = trust_gate(raw=U, soap=S, grad=g_t)  # per-element stale-basis safety net
```

`trust_gate` accepts `S[ij]` only if it agrees with raw momentum (cos > 0.20) and is at least as
gradient-aligned as raw momentum; else falls back to `U[ij]`. Early trust-floor 0.45 forces SOAP-trust
while gradients are too noisy to measure cosines (fades 1375->1625). V gets a 95%/5% SOAP/raw blend.

## 7. Per-role power-law LR schedule (C06, C13)

```
lr(step, role) = min( flat_lr[role],  power_c[role] * (t_end - step)^power )
power   = FINAL_LR_POWER = 1.2          # convex: hold LR higher, then drop steeply
t_end   = FINAL_SCHEDULE_STEPS = 2985   # schedule horizon
stop    = FINAL_TRAIN_STEPS = 2900      # run halts here; LR(stop) = 0.00069 = 1.8% of flat
power_c = {embed: 4.98e-5, proj: 5.18e-7, scalars: 1.66e-6, muon: 3.32e-6}  # per-role onset
```

Three coupled knobs the linear baseline lacks: cooldown onset (`power_c`), curvature (`power`), and
terminal-LR offset (`t_end != stop`), co-tuned so val lands ~3.279 at ~2885-2900.

## Complexity

- Muon core (momentum + NS + scale): O(rows*cols) per matrix per step, NS adds a constant number of
  matmuls (12 baseline, 5 with Polar-Express).
- SOAP: Gram EMAs O(rows^2 + cols^2) per step; QR eigendecomposition O(rows^3 + cols^3) but only every
  10 steps (amortized). Net per-step cost +~22% wall-clock (157.5 -> 191 ms) — free on a step-counted
  benchmark, a poor trade on a FLOP-budgeted run (C16).
- The cheap v1/v2 levers (MuonEq, train-steps trim, per-role LR/WD) are actually *faster* per step
  (~147 ms) because MuonEq row-norm is cheap and the horizon is shorter.

## Pseudocode: full per-step optimizer

```
for W in muon_params:
    M   = nesterov_momentum(W.grad, mu=mu_schedule(t))
    M   = muoneq_row_norm(M)                              # C03
    O   = aurora_rescale(soft_blend(t, hard=NS(M), soft=soft_NS(M, p=0.1)))   # C04, C14
    O   = O + contra_coeff(t) * unit_op_norm(W.grad)      # C08
    if should_soap(W):                                    # C05
        O = trust_gate(O, soap_precondition(O, W.grad, t), W.grad)
    U   = O * sqrt(max(1, rows/cols))
    lr  = power_law_lr(t, role(W))                        # C06, C13
    W   = (1 - lr*wd(role(W)))*W - lr*U
for P in adamw_params:
    adamw_step(P, lr=power_law_lr(t, role(P)), betas=retuned_betas)   # C06
if t >= 2820: validate_every(5..10)                       # C02 dense late validation
if t == 2900: stop()                                      # horizon-decoupled stop
```
