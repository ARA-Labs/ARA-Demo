# Concepts

Load-bearing terms, defined as this experiment uses them. Grounded in the goals, AGENTS.md, record
configs, submitted scripts, and journals.

## Benchmark & metric

- **`track_3_optimization`** — A fixed-architecture optimizer speedrun on the modded-nanogpt
  `train_gpt_simple.py` benchmark. Architecture, dataset, and batch size are frozen; exactly one
  forward-backward per step; hyperparameters hardcoded in the submitted script. A run counts only if
  validation loss reaches **3.28**.
- **Bin (`step_to_3.28` / `first_step_le_3p28`)** — The metric: the first training step at which the
  (cohort) validation loss crosses 3.28. Lower is better. The Muon baseline bin is 3500; AdamW is 5625.
- **Noise floor** — The per-seed variance scale: ≈50 steps on `step_to_3.28` and ≈0.001 on
  `final_val_loss`, estimated from baseline Muon. A "win" smaller than this is not signal until
  reproduced.
- **Statistical claimability / z-margin** — The submission gate: a fixed-step N-seed cohort passes only
  if `(3.28 − μ)·√n ≥ 0.004` (equivalently z ≥ ~3.08 at σ=0.0013, one-sided p < 0.001). The submitted
  **bin** is the earliest common validation checkpoint whose cohort clears this — not the lowest
  single-seed crossing. → C06.
- **Lawful core** — The six always-binding rules (benchmark hard rules; noise-floor gate; stuck
  detector at 30 same-family runs; ≤3-modifier slug cap; two-seed reproduction; mandatory
  pre-submission pruning). A result violating any is invalid regardless of its loss. → constraints.md.

## Optimizer family (Muon and its descendants)

- **Muon** — The baseline matrix optimizer: orthogonalize the momentum update (via Newton-Schulz) and
  step. The standing SOTA at 3500 steps (lr=0.025, wd=0.0125).
- **Polar / polar factor U** — The orthogonal factor of the momentum matrix `M = U·P`; Muon's update is
  essentially `U`. "Pre-polar" mechanisms perturb `M` before the polar map; the novelty wave's no-op
  laws (C10) are statements about how such perturbations behave under exact `U`.
- **Newton-Schulz (NS) / Polar-Express NS-5** — The iterative orthogonalization used to approximate the
  polar factor. "Polar-Express" is a non-uniform NS-5 variant (external lineage, arXiv:2505.16932).
- **NorMuon / MuonEq** — Row/column-variance–normalized Muon updates (NorMuon-lite, and MuonEq's
  row-normalized update, arXiv:2603.28254). The v1 corridor used NorMuon (β=0.90, lr=0.030).
- **Muon2F (2-factor / factorized preconditioning)** — A factorized preconditioner on the Muon update;
  in v1 it helps the **hidden** (non-`mlp.proj`) matrices specifically. → C03.
- **Contra-Muon** — A Contra update term added to the Muon step (external lineage, PR #275). v3 scales
  the q/k Contra residual.
- **Soft-Muon** — A late-schedule "softened" Muon update (basis stacking, p=0.1, ending at an ~80%
  blend), reached via a Contra → normal → Soft schedule (external lineage, PR #291). Buys tail slope,
  not early loss.
- **Outward-radial dampening** — Scaling the radial (outward) component of the update down and applying
  a post-step weight-radius correction (external lineage, PR #294). Works as a **tail** correction;
  radial-from-step-0 is harmful. → C08.
- **SOAP preconditioning** — A second-order preconditioner (external lineage, PR #278); v3 extends the
  SOAP set to MLP + attention value (V) matrices ("`mlp_plus_v`"). The single most load-bearing v3
  component. → C08.
- **Adam-mini** — A row-wise second-moment AdamW variant used as the auxiliary ("optimizer1") optimizer;
  a genuine v1 signal distinct from tuning.
- **AggMo3 / 2-factor preconditioning** — Aggregated-momentum + two-factor preconditioning on the
  non-`mlp.proj` hidden matrices in v1.

## Schedule, init, and state levers

- **Horizon ≠ stop** — Running with `train_steps` (forced final-validation step) **below**
  `schedule_steps` (LR-decay horizon). The foundational v1/v2 lever. → C01.
- **Power-law LR cooldown (PowerCool)** — `min(flat_lr, c·(t_end − step)^1.2)`; a back-loaded cooldown
  (external lineage, PR #287). Because the cooldown is back-loaded, early-curve loss is **not** a valid
  kill signal on this schedule.
- **Tail-EMA evaluation** — Validating on an exponential moving average of late-training weights (swap
  in for eval, restore the online weights), as opposed to training on them. The strongest v1
  endpoint-smoothing lever; β=0.99 > β=0.995. Distinct from SWA (fixed-window average) and from
  EMA-extrapolated evaluation, both of which were worse. → C02.
- **Muon mu (μ) schedule** — A momentum schedule `0.85 → 0.95` then `0.95 → 0.85` over the last steps;
  the load-bearing isolated lever from the transplanted "v12" idea set, and the largest v2 pruning
  contributor.
- **Role-specific LR / WD** — Per-parameter-role Muon learning-rate and weight-decay multipliers
  (q/k vs v vs attn.proj vs mlp.fc vs mlp.proj) instead of one body-wide value. → C04.
- **Muon lookahead** — Late-training interpolation toward a slow weight copy (start ≈ step 2450,
  interval 25, α=0.35, pull=0.15, with a smoothstep ramp). Moves the crossing step earlier. → C04.
- **LACV (lookahead control variate) / LACV-floor** — A variance-control lever gating q/k/mlp.proj
  updates; introduced in v3 to fix mid-run seed-offset pathology (the high-tail failure mode).
- **Sphere-lookahead pull / tangent-sphere gate** — Two radius-aware lookahead/radial terms in the v3
  stack. Leave-one-out found the **sphere-lookahead pull** redundant ("nosphere") once LACV +
  tangent-sphere are present; the two sphere terms do **not** compose. → C09.
- **CGI gain split / depth-scaled init / embed init ×0.7 / zero-init proj** — Init levers carried into
  the v2/v3 stacks (embedding init scaled by 0.7; depth-scaled `mlp.fc` init; zero-init projection
  weights).

## Process & search concepts

- **Wave** — One autonomous mission slice: **v1** (optimizer/schedule/init screen → 3205), **novelty**
  (hard-isolated, novelty-constrained → negative), **v2** (legal frontier → 3037), **v3** (public-PR
  reproduction + compression + pruning → 2949).
- **Slug / family** — A run's short modifier name; the "family" is its first 1–3 tokens and is the unit
  for the stuck detector (≤3 modifiers before a rename).
- **Leave-one-out (LOO) pruning** — Removing each stack modifier in turn and re-measuring, to find
  redundant components before submission. → C09.
- **The exact-polar no-op law** — For exact polar `U`, input-column norms satisfy `‖U[:,j]‖² = 1`, and
  for square q/k/v and tall mlp.fc targets `UᵀU = I`; therefore many pre-polar perturbations are
  identically zero or collapse to a scalar Nesterov blend. The structural reason the novelty wave was a
  negative result. → C10, novelty_derivation.md.
- **Quarantine** — Marking a set of results invalid (non-compliant) so they are recorded as journey but
  never reported as records — applied to every v12-derived result after the forward-path flag. → C05.
- **Preempt fanout** — Launching parallel benchmark runs into the cluster's `preempt` partition behind
  an idle-node gate, to multiply throughput while the main thread runs one job at a time.
