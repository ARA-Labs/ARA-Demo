# Concepts

Technical vocabulary as used in this experiment (not generic dictionary definitions).

## Benchmark / methodology

- **bin** — the submitted `train_steps` value: the step count at which a recipe is claimed to reach
  `val_loss <= 3.28`. Lower is better. The reportable bin is the earliest fixed-step checkpoint whose
  seed cohort passes the significance gate.
- **horizon / stop decoupling** — keeping the LR-decay denominator (`schedule_steps`, the "horizon")
  larger than the training stop step (`train_steps`, the "stop"), so the cooldown is not compressed
  into a shorter run. Notation e.g. `h3375-stop3195`.
- **noise floor** — the empirical run-to-run variability used to gate "real" improvements:
  ~50 steps in `step_to_target` and ~0.001 in final val_loss. A promotion must exceed ~2× this floor.
- **stepping stone** — a rigorously reproduced lower-step hit that is still inside the noise-floor
  gate relative to the current frontier; kept as boundary evidence, not promoted.
- **fixed-step seed cohort / cohort z-test** — the submission gate: run n distinct seeds at a fixed
  bin and require `(3.28 - mean)*sqrt(n) >= 0.004` (with `sigma = 0.0013`, a one-sided z, `p < 0.001`).
- **anti-val-spam** — scoring significance only at validation checkpoints common to all runs, never
  at a per-run cherry-picked lowest validation step (a p-hacking control).
- **leave-one-out (LOO) pruning** — ablating each stacked mechanism singly and keeping only those
  whose removal degrades the statistical boundary; the basis of the per-component "removal delta".
- **seed control** — inserting `torch.manual_seed(seed)` after the validation batch is materialized
  but before model construction, so the validation data is fixed and only init/optimizer state vary.

## Optimizer / update mechanisms

- **Muon (baseline)** — orthogonalizes the momentum update via Newton-Schulz on block matrices;
  canonical recipe `lr=0.025, wd=0.0125, mu=0.95`, NS coefficients `(2,-1.5,0.5)`, 12 iterations.
- **NorMuon** — "normalized Muon": after orthogonalization, divide each row by an EMA of its squared
  norm and globally RMS-rescale to canonical Muon's update scale. Used with a colder beta2 (~0.90).
- **Muon2F / 2-factor preconditioning** — factorized row+column preconditioning of the matrix
  gradient before Newton-Schulz (`pre_eps`, `beta2_pre`).
- **AggMo3** — aggregated-momentum (3 momentum terms) applied to hidden non-`mlp.proj` matrices.
- **error-feedback residual** — reinjecting the residual discarded by orthogonalization on
  `mlp.proj`, so the lost component is not thrown away.
- **tail-EMA** — a full-model EMA shadow started late in training (e.g. step 2000, `beta=0.99`),
  swapped in only for validation under `no_grad`, then restored.
- **Adam-mini** — memory-light Adam variant: rowwise second-moment denominators for embedding/head,
  a single tensorwise denominator for 1-D gains/biases.
- **mu schedule** — a time-varying Muon momentum, e.g. `0.85 → 0.95 → 0.85` (warm up to a plateau,
  then cool down near the end).
- **Muon lookahead** — a slow-weight pull (Lookahead-style) applied to Muon parameters with a
  smoothstep ramp (here from step 2450, interval 25, alpha 0.35, pull 0.15).
- **role-specific LR / WD (RoleLR2 / RoleWD)** — distinct Muon learning-rate multipliers and weight
  decays per parameter role (q/k, v, attn.proj, mlp.fc, mlp.proj) instead of one body-wide value.

## Public-PR mechanisms reproduced in v3

- **Contra-Muon** — a Contra residual update term added to the Muon update (PR #275/#291); v3 scales
  it down to 0.125 for q/k only.
- **MuonEq** — a row-normalized Muon update (arXiv:2603.28254 lineage).
- **Polar Express NS** — a non-uniform 5-coefficient Newton-Schulz iteration for the
  orthogonalization (arXiv:2505.16932 lineage).
- **Soft-Muon** — a Contra → normal → Soft-Muon momentum schedule with basis stacking (p=0.1) ending
  at a blend ceiling (`SOFT_MUON_CEIL`), depending on a Gram-Frobenius / Schatten-4 input-norm
  estimate (PR #291).
- **outward-radial dampening / radial brake** — scaling the outward radial component of the update
  (here 0.45 base, 0.38 in the tail guard window) followed by a post-step weight-radius correction
  (PR #294).
- **SOAP (MLP+V)** — a second-order (Shampoo-family) preconditioner applied to MLP parameters plus
  attention-V (`SOAP_PARAM_MODE="mlp_plus_v"`, V blend 0.95), with an attention SOAP fade window
  (PR #278 / #290 machinery).
- **power-law cooldown** — a back-loaded power-law LR decay (PR #287); its lateness makes early
  trajectory kills invalid.
- **CGI gain split** — a Rademacher channel-gain split on RMSNorm gains (`alpha=0.14`), ported from
  the cross-agent v15/v48 stack.

## v3 codex-specific mechanisms

- **LACV / lookahead-CV gating** — a lookahead control-variate: a seed-offset correction reusing a
  prior worker's lookahead state, gated on q/k/mlp.proj.
- **LACV q/k floor relaxation** — relaxing the u/w-floor that refills the tangent energy LACV
  removes (`LACV_FLOOR_LAMBDA=0.060`, ramp 2550..2900).
- **sphere-lookahead** — a pull (`SPHERE_LOOKAHEAD_PULL`) plus a tangent-sphere radial gate; the
  W258 LOO showed the **pull** is redundant (→ "nosphere") while the tangent term must stay.

## Novelty-wave concepts

- **two-gate rule** — every novelty idea needs both an arXiv/local novelty existence check and a
  benchmark-rule compliance check to PASS before any code is written.
- **refined novelty bar** — an optimizer-level combination counts as novel only if one mechanism's
  output *materially and non-additively* shapes another's; schedule/LR/WD tuning and additive combos
  are "plumbing" and do not count.
- **exact-polar no-op** — for Muon's exact polar factor `U`, `U^T U = I` (and unit input-column
  norms), so a pre-polar perturbation built from disagreement/commutator terms of `U` vanishes
  identically — the most common reason a "clever" novel optimizer idea was killed before code.
- **same-family target-step probe** — a measurement-only step/HP sweep of an already-cleared idea;
  explicitly not a new novelty claim.

## Cross-agent terms

- **cc v12** — a "v12" optimizer stack authored by the Claude/"cc" agent, inherited as v2's parent;
  its rewritten RMSNorm forward path triggered the compliance quarantine (C05).
- **opus v15 / v48** — cross-agent stacks (CGI gain split, AdamW b2=0.99, di-fc init) read as source
  material for v3's faithful reproduction.
- **legal / compliant / byte-identical rebuild** — a variant family rebuilt from the workspace
  `train_gpt_simple.py` with an empty Architecture-block diff, enforced by a launcher-time gate.
