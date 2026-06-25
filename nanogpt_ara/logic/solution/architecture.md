# Architecture — The v3 Frontier Recipe as a Component Graph

The "solution" here is not a model architecture (that is fixed: GPT-124M) but the **optimizer +
schedule recipe** that reaches 3.28 in ~2885 steps. It is a composition of components layered onto
the §0 two-optimizer baseline. Source: `cc_v3/07070-v88-aurora-proj-s2/launched_script.py` (decoded
in INSIGHTS.md §5, §15-§18).

## Top-level: two-optimizer partition

```
parameters
  |-- 1-D / embedding / output / scalar params --> [AdamW group]
  |       (embed.weight lr=0.3, proj.weight lr=1/320 zero-init, scalars lr=0.01,
  |        retuned betas; per-role power-law cooldown onset)
  |
  '-- 2-D block weight matrices (ndim>=2 in model.blocks) --> [Muon group]
          (split further by role: attention vs MLP; further into Q/K vs V vs MLP for SOAP)
```

- **AdamW group** — Purpose: optimize the params Muon does not. Inputs: gradients of 1-D/embedding/
  output/scalar params. Outputs: AdamW updates. Key choices: hand-set per-group LRs; output `proj`
  zero-initialized; betas retuned (LOO ~+45 steps); its own cooldown onset (`ADAM_*_POWER_C`).
- **Muon group** — Purpose: optimize 2-D weight matrices via the orthogonalized-momentum pipeline
  below. Inputs: gradients of block weights. Outputs: orthogonalized, normalized, preconditioned
  updates. Key choices: base LR 0.0375; per-role LR (attn ~0.6x) and WD (attn 0.0275 < MLP 0.03125).

## The Muon update pipeline (per 2-D weight, per step)

Data flow (each box is a component; see `src/execution/muon_pipeline.py` and `soap_subset.py`):

```
grad
  v
[Nesterov momentum]  mu-schedule 0.85 ->0.95 (warmup 0-300) -> 0.85 (2850-2900)
  v
[MuonEq pre-NS row-norm]  per-row L2 normalize momentum            (C03)
  v
[Newton-Schulz / soft-Muon]  hard NS (sing. vals ->1) early;        (concept: NS, soft-Muon)
  |                          blend to soft-Muon (p=0.1) over 2400-2890
  v
[Aurora row-rescale]  K outer NS iters w/ per-row D rescale (beta 0.25)  (C04)
  v
[Contra-Muon term]  + contra_coeff * normalized_grad, coeff -0.2 ->0 by 1920  (C08, C14)
  v
[SOAP-on-subset]  if param in {MLP fc/proj, attn V}:                 (C05, C13)
  |   project to eigenbasis (refreshed every 10 steps) -> Adam 2nd-moment
  |   -> divide by RMS denom -> project back -> norm-preserve
  |   -> trust_gate(raw, soap, grad): accept per-element only if it agrees
  |      with raw momentum (cos>0.20) and is >= as grad-aligned; else fall back
  v
[scale by sqrt(max(1, rows/cols))]
  v
[decoupled weight decay]  p *= 1 - lr(step,role)*wd(role)
  v
weight update, lr from the per-role power-law cooldown controller
```

## Schedule controller (orthogonal to the update pipeline)

- **Per-role power-law cooldown** (`src/execution/schedule.py`): `lr(step) = min(flat_lr, power_c *
  (t_end - step)^1.2)`, per-group `power_c`, `t_end = 2985`, run stops at `2900` (LR then 1.8% of
  flat). Purpose: anneal each parameter group on its own convex curve; the single most critical lever
  (C13). Inputs: step, role. Output: per-group LR multiplier.
- **Horizon decoupling**: the schedule is *computed for* 2985 steps but the run *stops at* 2900,
  harvesting the trajectory while LR is still nonzero (the cc realization of codex's early-stop
  insight).
- **Dense late validation**: validate every 5-10 steps from ~2820 onward to pin the first sub-3.28
  step (de-quantizes `step_to_3_28`, C02).

## Temporal-curriculum view (C14)

The same components, read as three time phases that hand off control:

| Phase | Steps | Active components |
|---|---|---|
| Explore | 0 - ~1625 | mu warmup; flat LR 0.0375; Contra-Muon -0.2->0; attn trust-floor 0.45 |
| Converge | ~1625 - 2400 | hard NS; Contra ~off; data-driven trust gate; convex cooldown underway |
| Soften | 2400 - 2900 | soft-Muon 0->0.80; power cooldown steepens; mu cools; stop at LR=1.8% flat |

## Component interaction summary

- MuonEq, Aurora, and NorMuon all target *per-row update magnitude*; once MuonEq+Aurora are present,
  NorMuon is redundant (C03, C13).
- SOAP supplies the per-direction curvature scaling NS discards, but only where it pays (MLP+V); the
  trust_gate is the safety net that makes its amortized stale basis affordable (C05, C14).
- The power-law cooldown is load-bearing precisely because the target margin is sub-0.001: it is the
  last thing standing between the recipe and the threshold (C13).
- Diagnostics (`src/execution/diagnostics.py`) sit outside the recipe: seed-significance sizing,
  miss-rate, and the early-kill divergence test (C09, C11, C17).
