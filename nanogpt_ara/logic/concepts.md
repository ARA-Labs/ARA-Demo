# Concepts

Formal definitions of the technical terms used across this ARA. Notation follows the run code
(`launched_script.py`) and INSIGHTS.md.

## Muon (orthogonalized-momentum optimizer)
- **Notation**: update `U = NS(M) * max(1, rows/cols)**0.5`, where `M` is Nesterov momentum of the
  gradient and `NS` is Newton-Schulz orthogonalization.
- **Definition**: An optimizer for 2-D weight matrices that takes the Nesterov-momentum gradient,
  orthogonalizes it (drives its singular values toward 1) via a fixed-iteration Newton-Schulz scheme,
  then scales by `sqrt(max(1, rows/cols))`. Applied with decoupled weight decay (`p *= 1 - lr*wd`).
- **Boundary conditions**: Used only for `ndim>=2` block weights inside `model.blocks`; 1-D /
  embedding / output params are handled by AdamW. Baseline HPs: lr 0.025, wd 0.0125, mu 0.95.
- **Related concepts**: Newton-Schulz orthogonalization, MuonEq, NorMuon, soft-Muon, WSD schedule.

## Newton-Schulz orthogonalization (NS)
- **Notation**: `X_{k+1} = a*X_k + b*(X_k X_k^T) X_k + c*(X_k X_k^T)^2 X_k`, baseline
  `(a,b,c)=(2,-1.5,0.5)`, 12 iterations (`zeropower_via_newtonschulz5`).
- **Definition**: An iterative matrix polynomial that approximates the orthogonal polar factor of `M`,
  pushing all singular values toward 1 without an explicit SVD. It is the mechanism that gives Muon a
  well-conditioned update direction.
- **Boundary conditions**: At 124M the 12-iteration version is already converged, so re-tuning the
  coefficients (Polar-Express, 5 iters) is ~neutral on quality; modifying the NS core (fewer iters,
  anisotropic coeffs) degrades the orthogonalization and hurts (novelty wave).
- **Related concepts**: Muon, Polar-Express coefficients, soft-Muon, MuonEq.

## MuonEq (pre-NS per-row normalization)
- **Notation**: `M_row = M / ||M_row||_2` (per-row L2 normalize) applied *before* `NS(M_row)`.
- **Definition**: Equalizes the L2 norm of each row of the momentum matrix before orthogonalization,
  giving NS a better-conditioned input so rows contribute equally to the spectral fit (arXiv 2603.28254).
- **Boundary conditions**: Strongest single Muon-internal lever (dval -0.00484, ~11 sigma); becomes
  redundant with Aurora row-rescale once that is present. Must be applied *before* NS to matter.
- **Related concepts**: NorMuon, Aurora row-rescale, Newton-Schulz orthogonalization.

## NorMuon (post-NS per-row second-moment normalization)
- **Notation**: `U = NS(M) / sqrt(EMA(row 2nd moment) + eps)` (divide *after* NS).
- **Definition**: Per-row 2nd-moment EMA normalization applied to the already-orthogonalized update
  (arXiv 2510.05491 / microsoft/dion). The weaker sibling of MuonEq.
- **Boundary conditions**: dval -0.00155 standalone; stacking with MuonEq over-corrects the same
  imbalance (-> ~no gain); LOO `loo14_no_normuon` -> 2930 (dead weight at the frontier once
  Aurora/MuonEq are present).
- **Related concepts**: MuonEq, Aurora row-rescale.

## SOAP (Shampoo-with-Adam-in-eigenbasis)
- **Notation**: maintain Gram EMAs `row_gg=EMA(g g^T)`, `col_gg=EMA(g^T g)`; eigenbasis `q_row,q_col`
  via QR; `projected = q_row^T U q_col`; per-coordinate Adam 2nd-moment in-basis; divide by
  `denom = exp_avg_sq^0.5`; project back.
- **Definition**: Runs Adam in the eigenbasis of the gradient covariance (Shampoo's left/right
  factors), i.e. a second-order preconditioner (arXiv 2409.11321), benchmarked against AdamW.
- **Boundary conditions**: As a *global* optimizer it fails on top of Muon at 124M (asymptotes ~3.39)
  because NS already supplies the curvature signal; may win at >=350M scale.
- **Related concepts**: SOAP-on-subset, Shampoo, KL-Shampoo, Newton-Schulz orthogonalization.

## SOAP-on-subset (MLP+V eigenbasis preconditioner)
- **Notation**: `SOAP_PARAM_MODE="mlp_plus_v"`, `SOAP_PRECONDITION_FREQUENCY=10`, `SOAP_BETA2=0.90`,
  `SOAP_DENOM_POWER=0.50`, Frobenius-norm-preserving (`precond *= ||U||/||precond||`).
- **Definition**: SOAP applied *only* to MLP `fc`/`proj` and the attention value projection (not Q/K),
  with the eigenbasis refreshed every 10 steps and the output rescaled to preserve the input's
  Frobenius norm so it changes update *shape*, not magnitude.
- **Boundary conditions**: Biggest hitting v3 lever (~+85 steps from MLP-SOAP, ~+35 from V-SOAP);
  helps where curvature is anisotropic/persistent (MLP, V) and duplicates Muon where it is not (Q/K).
- **Related concepts**: SOAP, trust_gate, per-role differentiation.

## trust_gate (stale-basis safety net)
- **Notation**: `trust_gate(raw, soap, grad)` accepts the SOAP update per-element only if it agrees
  with raw momentum (cos > 0.20) AND is at least as gradient-aligned as raw momentum; else fall back
  to plain Muon. Early floor `ATTN_EARLY_TRUST_FLOOR=0.45` fading 1375->1625.
- **Definition**: A cheap per-element correctness check that catches cases where SOAP's stale
  (every-10-steps) eigenbasis would mislead, making amortized SOAP affordable *and* safe.
- **Boundary conditions**: The early trust-floor prevents spurious rejection while early gradients are
  too noisy to measure cosines reliably; gate becomes fully data-driven after ~1625.
- **Related concepts**: SOAP-on-subset, temporal curriculum.

## Contra-Muon (contrastive early-decorrelation term)
- **Notation**: `contra_update = NS(M) + contra_coeff * normalized_grad`, `contra_coeff` ramps
  -0.2 -> 0 by step ~1920 (`CONTRA_TO_NORMAL_END_STEP`).
- **Definition**: Subtracts a ramping fraction of the unit-norm raw-gradient direction from the
  orthogonalized update early in training (decorrelating the update from the greedy gradient), then
  anneals to pure Muon (modded-nanogpt PR275).
- **Boundary conditions**: Active in the Explore phase only; standalone `family=contra` best 3000;
  enabling, not sufficient. Mechanism confirmed from code (§16.4).
- **Related concepts**: temporal curriculum, soft-Muon, lose-early-win-late crossover.

## Aurora row-rescale
- **Notation**: K outer NS iterations with a per-row diagonal `D` rescale between NS calls,
  `_AURORA_BETA=0.25`.
- **Definition**: A per-row magnitude/variance normalization interleaved with the orthogonalization
  that clamps the per-neuron update scale, enabling a larger global LR.
- **Boundary conditions**: Part of the v3 stack; makes MuonEq/NorMuon redundant (same mechanism);
  LOO `aurora` ~+20 steps when removed.
- **Related concepts**: MuonEq, NorMuon, learning-rate headroom.

## soft-Muon (endgame orthogonalization softening)
- **Notation**: raise singular values to a small power `SOFT_MUON_P=0.1` instead of forcing them to 1;
  blend in over steps 2400-2890 to ceiling 0.80 (`soft_via_newtonschulz5`, `soft_blend_for_step`).
- **Definition**: A softened orthogonalization used only in the endgame so updates retain more of
  their natural magnitude structure for gentle fine-tuning near convergence — the optimizer-space
  analogue of LR annealing. Mechanism partly `[HYP]`.
- **Boundary conditions**: Acts only in the final ~1.7% of steps; LOO `softmuon` ~0 (a refinement,
  not load-bearing).
- **Related concepts**: Newton-Schulz orthogonalization, temporal curriculum, power-law cooldown.

## WSD schedule (Warmup-Stable-Decay / stable-then-decay)
- **Notation**: hold `eta=1.0` for the first 30% of steps, then linearly decay to 0 over the final
  70% (`set_hparams(step, cooldown_frac=0.7)`), applied as one multiplier to all groups.
- **Definition**: The baseline learning-rate schedule: a long full-LR stable phase for bulk descent,
  then a linear cooldown into the minimum.
- **Boundary conditions**: Near-optimal *shape* at the baseline (only the *length* is the lever there);
  replaced at the frontier by a per-role power-law cooldown.
- **Related concepts**: power-law cooldown, train_steps, cooldown_frac.

## Power-law cooldown (per-role convex LR decay)
- **Notation**: `lr(step) = min(flat_lr, power_c * (t_end - step)^power)` with `power=FINAL_LR_POWER
  =1.2`, `t_end=FINAL_SCHEDULE_STEPS=2985`, per-group `power_c`; run stops at `FINAL_TRAIN_STEPS=2900`
  (LR then = 0.00069 = 1.8% of flat).
- **Definition**: A convex (power>1) cooldown that holds LR higher through mid-training then drops
  steeply near the end, with a per-role cooldown onset and the schedule horizon *decoupled* from the
  stop step.
- **Boundary conditions**: The single most critical frontier lever — removing it makes all 4 LOO seeds
  miss; exposes three coupled knobs (onset `power_c`, curvature `power`, terminal-LR offset
  `t_end != stop`) co-tuned to land val ~3.279 at ~2885-2900.
- **Related concepts**: WSD schedule, per-role differentiation, train_steps, horizon-decoupling.

## step_to_3_28 (the benchmark metric)
- **Notation**: `step_to_3_28 = min { step : val_loss(step) <= 3.28 }`.
- **Definition**: First training step whose logged validation loss is <= 3.28; the quantity being
  minimized. Lower is better; wall-clock and per-step FLOPs are explicitly free.
- **Boundary conditions**: Quantized to the validation cadence (default every 125 steps), so it
  rounds up to the next logged validation; below ~15 steps it is the wrong metric (rank on
  `min_val_loss` instead). Has a binary miss-rate tail at the frontier (`None` if never hit).
- **Related concepts**: validation cadence, noise floor, min_val_loss.

## Noise floor / miss-rate (seed reproducibility)
- **Notation**: within-config `std(final_val_loss) ~ 0.0004-0.0010`; frontier `std(step_to_3_28) ~
  14-21` steps; miss-rate = fraction of seeds with `step_to_3_28 = None`.
- **Definition**: The seed-to-seed variability of a fixed config. The std of final val loss is the
  same size as a single-lever gain, and ~9-12% of frontier seeds fail to reach 3.28 at all.
- **Boundary conditions**: Coarsely-validated configs read step-std ~0 (cadence hides it); dense
  validation reveals the true ~15-step floor. Seeds needed ~ 8*sigma^2/Delta^2.
- **Related concepts**: step_to_3_28, seed-verified median, validation cadence.

## Per-role differentiation
- **Definition**: Splitting Muon parameter groups by structural role (attention vs MLP, plus the
  AdamW-owned embed/proj/scalars) and assigning each its own learning rate, weight decay, and cooldown
  onset, because attention and MLP matrices differ in scale/curvature/sensitivity.
- **Notation**: attn LR ~0.5-0.6x MLP; attn WD 0.0275 < MLP 0.03125; per-group `power_c`.
- **Boundary conditions**: A recurring frontier theme across three axes (LR, WD, schedule); each axis
  contributes a small-to-mid LOO delta.
- **Related concepts**: power-law cooldown, weight decay, learning-rate.

## Backbone-dependence (the dominant confounder)
- **Definition**: The phenomenon that a lever's *sign and magnitude* depend on what else is in the
  recipe and on which parameter subset it touches, so public-PR gains measured against vanilla Muon do
  not transfer additively.
- **Boundary conditions**: Sharpened to *param-subset*-dependence by SOAP (full fails, MLP+V helps);
  the reason the agents re-tested every lever at the current backbone.
- **Related concepts**: SOAP-on-subset, MuonEq/NorMuon stacking, Muon^2, enabling lever.

## Temporal curriculum (explore -> exploit in optimizer-space)
- **Definition**: A recipe whose levers are *time-scheduled* to hand off across the run — early
  exploration/decorrelation (Contra-Muon, forced SOAP-trust, mu warmup) trading early loss for
  conditioning, then late exploitation (hard NS -> soft-Muon, convex cooldown) — producing an
  engineered lose-early/win-late crossover.
- **Boundary conditions**: The ramp constants bracket the measured crossover (~step 1750); it is the
  mechanism behind the §8 crossover, not an accident.
- **Related concepts**: Contra-Muon, soft-Muon, trust_gate, lose-early-win-late crossover.
