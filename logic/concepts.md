# Concepts

> **t=0 FRAME.** Domain concepts the Codex agent holds at the start of the experiment, defined
> from the allowed inputs only (AGENTS.md, goal.md, the baseline `launched_script.py`). No
> discovered method or recipe appears here.

## Muon
- **Notation**: optimizer over 2D parameters; canonical t=0 recipe `lr=0.025, weight_decay=0.0125, mu=0.95`.
- **Definition**: A momentum optimizer for matrix-shaped parameters whose update is
  *orthogonalized*: it forms a Nesterov-style momentum buffer of the gradient, then replaces
  the update direction with the (approximate) orthogonal factor of that buffer via a
  Newton–Schulz iteration (`zeropower_via_newtonschulz5`), then rescales by
  `max(1, rows/cols)**0.5`. In the benchmark it is applied to the 2D block parameters
  (`model.blocks`), while embeddings, the unembedding/output projection, and all <2D
  parameters are handled by AdamW. It is the incumbent: SOTA at 3500 steps (lr=.025,
  wd=.0125) at t=0.
- **Boundary conditions**: Applied only to parameters with `ndim >= 2` inside the transformer
  blocks; scalar/vector parameters and the embed/unembed go to AdamW (see `src/environment.md`).
- **Related concepts**: Newton–Schulz orthogonalization (NS5), the lawful core, AdamW
  baseline, recipe family / slug-stack.

## Newton–Schulz orthogonalization (NS5)
- **Notation**: `zeropower_via_newtonschulz5(G)`; quintic coefficients `(a, b, c) = (2, -1.5, 0.5)`; 12 iterations.
- **Definition**: The fixed iterative routine Muon uses to approximate the orthogonal polar
  factor of the momentum matrix. The matrix is first normalized so its spectral norm is ≤ 1
  (`X / (||X|| + 1e-7)`), then the quintic map `X ← aX + (bA + cA²)X` with `A = XXᵀ` is applied
  for 12 iterations in bfloat16. The routine is explicitly "not optimizing for wallclock
  speed."
- **Boundary conditions**: Requires `G.ndim >= 2`; transposes when rows > cols so the iteration
  runs on the smaller dimension.
- **Related concepts**: Muon.

## AdamW baseline / per-group optimizer split
- **Notation**: AdamW with `betas=(0.8, 0.95)`, `eps=1e-10`, `weight_decay=0`, `fused=True`;
  per-group LRs (embed 0.3, output proj 1/320, <2D params 0.01).
- **Definition**: The reference optimizer. As a standalone optimizer it reaches the 3.28 target
  in 5625 steps (the slower baseline). In the t=0 SOTA recipe it is also used as the *second*
  optimizer alongside Muon, owning the embedding, the output projection, and all <2D parameters
  with the per-group learning rates above; Muon owns the 2D block weights.
- **Boundary conditions**: In the benchmark it never touches the 2D block weights (those are
  Muon's). The goal notes AdamW's best LR at this scale is ~4–8e-3, well above the canonical
  3e-4 — a warning that paper-default LRs are untrustworthy here.
- **Related concepts**: Muon, HP sweeps, fixed-benchmark constraints.

## step_to_3.28 — the "bin" metric
- **Notation**: `step_to_target` / `step_to_3.28`.
- **Definition**: The primary objective: the number of training steps at which validation loss
  first reaches ≤ 3.28. Lower is better. It is a *threshold-crossing* metric, distinct from
  final validation loss — a run can drift past 3.28 and back, so the crossing must be confirmed
  by reading the log, not just the final value. Validation is measured every 125 steps (and at
  the final step), so the metric is read on that grid.
- **Boundary conditions**: Only runs that actually reach 3.28 produce a value; a run that never
  reaches 3.28 is a failed candidate, not a "look how few steps" win. The benchmark hard rule is
  val ≤ 3.28 to count.
- **Related concepts**: final validation loss, noise floor, fixed-benchmark constraints.

## Noise floor / statistical-significance gate
- **Notation**: `step_to_target` noise floor ≈ 50 steps; `final_val_loss` mean noise ≈ 0.001
  (provisional t=0 estimates, to recompute weekly from baseline-Muon at 3 seeds).
- **Definition**: The measured run-to-run variance that determines whether a step-count
  difference is real signal or noise. A candidate is recognized as "passing" only when it runs
  on ≥ 2 distinct seeds AND beats the prior best by ≥ 2× the noise floor (the noise-floor gate,
  lawful core rule 2). Single-seed wins are ideas to reproduce, not new bests; the next launch
  is a 2nd seed of the same recipe, not a new modifier.
- **Boundary conditions**: The estimates are provisional at t=0 and must be re-measured; the
  exact seed budget needed to call a 50 / 100 / 200-step gain significant is itself an open
  question (problem.md G5).
- **Related concepts**: step_to_3.28, two-seed reproduction, lawful core, pruning rounds.

## Two-seed reproduction
- **Notation**: ≥ 2 distinct seeds.
- **Definition**: The requirement that any new "best" be reproduced on a second seed before it
  is recognized (lawful core rule 5). Variance on this benchmark is real, so nothing under
  ~50–100 steps is treated as signal until reproduced.
- **Boundary conditions**: Applies to declaring a new best and to pruning decisions; a borderline
  leave-one-out result triggers a 2nd seed before any drop decision.
- **Related concepts**: noise floor, lawful core, pruning rounds.

## Lawful core
- **Notation**: six always-on rules.
- **Definition**: The six non-negotiable rules that override all other ("default, not law")
  conventions; a run, candidate, or claim that violates any one is invalid regardless of what
  else it achieved: (1) benchmark hard rules — same dataset, batch, architecture as
  `train_gpt_simple.py`, one forward-backward per step, hardcoded HPs, val ≤ 3.28 to count;
  (2) the noise-floor gate; (3) the stuck detector; (4) slug-stack ≤ 3 modifiers; (5) two-seed
  reproduction before any new best; (6) mandatory pre-submission pruning round.
- **Boundary conditions**: Always applies; everything else in AGENTS.md is a default that may be
  deviated from when it serves the work.
- **Related concepts**: noise-floor gate, stuck detector, recipe family / slug-stack, pruning
  rounds, two-seed reproduction, fixed-benchmark constraints.

## Fixed-benchmark constraints
- **Notation**: the "Hard rules — benchmark."
- **Definition**: The non-negotiable invariants of the comparison platform: same dataset, batch
  size, and architecture as `train_gpt_simple.py` (no arch, batch-size, or data changes); one
  forward-backward per step (no grad-accumulation tricks, no multi-step inner loops); a run must
  reach 3.28 val loss to count; modifications are confined to the `Optimization` and
  `Init & Optim Hyperparams` sections (init scaling and optimizer-schedule changes are fair
  game); HPs are hardcoded for any submitted result (no CLI args). Experimental code that breaks
  any of these lives in `scratchpad/variants/` for diagnostics only and is never submitted.
- **Boundary conditions**: Diagnostic instrumentation of the training loop is allowed, but
  submitted runs use the canonical script with HPs hardcoded.
- **Related concepts**: lawful core, src/environment.md, step_to_3.28.

## Recipe family / slug-stack
- **Notation**: slug prefix = first 1–3 tokens; ≤ 3 modifiers beyond the optimizer name.
- **Definition**: A run's identity is a slug describing the variant. The "family" is the slug
  prefix (the optimizer name plus its first modifiers), which keys the stuck-detector counter.
  A slug may carry at most 3 modifiers beyond the optimizer name; adding a 4th means a *new
  family* — rename it, reset its stuck-counter, and give it a fresh picklist entry. Adding a
  modifier to an existing slug does NOT reset the counter.
- **Boundary conditions**: Family membership is the slug prefix, not the full string.
- **Related concepts**: stuck detector, lawful core, pruning rounds.

## Stuck detector
- **Notation**: `consecutive_runs_without_step_to_target_improvement`; thresholds at 15 and 30.
- **Definition**: A per-family counter of consecutive runs that did not improve
  `step_to_target`. At 15 it triggers a "noise floor or pivot?" subagent whose first action is
  a pruning round. At 30, pivoting is mandatory: the family is ruled out, the lesson is logged,
  and the next family is picked. The counter is recomputable from the run index so it survives
  context compaction.
- **Boundary conditions**: Tracked per recipe family (slug prefix), not per individual run.
- **Related concepts**: recipe family / slug-stack, pruning rounds, lawful core.

## Pruning rounds
- **Notation**: leave-one-out per modifier; drop on a 2-seed mean inside ±0.5× noise floor.
- **Definition**: The mechanism for *removing* modifiers from a stack so the slug stays
  attributable. For each modifier, a leave-one-out variant is run (1 seed first): if removal
  worsens validation by ≥ 1× noise floor, the modifier is kept; if removal looks neutral or
  better, a 2nd seed is run and the modifier is dropped only if the 2-seed mean is inside
  ±0.5× the noise floor (a single-seed drop is itself overfitting). Triggered every 10
  successful runs at the current best, when the stuck detector first fires at 15, and before
  promoting any candidate to a submission. A pre-submission pruning round is mandatory (lawful
  core rule 6), and the post-pruning recipe must clear the noise-floor gate as if it were a new
  candidate before submission.
- **Boundary conditions**: The keep-tolerance is deliberately wider than the drop-tolerance;
  borderline is keep, not drop.
- **Related concepts**: noise floor, two-seed reproduction, recipe family / slug-stack, lawful core.

## WSD / stable-then-decay schedule (incumbent schedule)
- **Notation**: `set_hparams(step, cooldown_frac=0.7)`; `eta = 1.0` while `progress < 1 - cooldown_frac`, then `eta = (1 - progress)/cooldown_frac`.
- **Definition**: The learning-rate schedule baked into the t=0 SOTA recipe: a "stable then
  decay" (WSD-style) schedule that holds every optimizer group's LR at its initial value for
  the first `(1 - cooldown_frac)` fraction of training, then linearly decays it to 0 over the
  final `cooldown_frac` fraction. With `cooldown_frac=0.7` the LR is flat for the first 30% of
  steps and decays over the last 70%. There is no warmup in the t=0 recipe. Schedule shape is
  explicitly an open lever (WSD vs cosine vs trapezoid vs multi-stage vs schedule-free; warmup;
  end-of-training averaging).
- **Boundary conditions**: Applies multiplicatively to every optimizer group's `initial_lr`.
- **Related concepts**: step_to_3.28, AdamW baseline, Muon, fixed-benchmark constraints.

## Muon2F (hidden-matrix orthogonalized update variant)
- **Notation**: `muon2fhidden`; on the C01 NorMuon/Adam-mini parent with `b2p095, eps1e3`; applied to optimizer2 (the hidden matrices).
- **Definition**: A variant of the Muon orthogonalized update applied as a *stack-level* change to ONLY the optimizer2 hidden-matrix update/state, leaving optimizer1 (Adam-mini) and optimizer3 (MLP-proj NorMuon) and the residual stack intact, and keeping `GPT.forward` byte-identical. It is the first matrix-side preconditioning change found to HELP this corridor (where APOLLO, OLion, and DION all washed out — staging O15, N38/N46). On its own it is a 3-seed reproduced stepping stone at step_to_3.28 ≈ 3237/3250 (crystallized as part of C02); raw Muon2F at stop3200 misses, and no internal Muon2F modifier (warm-handoff, magnitude-graft, input-covariance, attention-only, preconditioner-exponent, late-MLP-LR, grokfast, SPAM, MARS-diff, gradient-centralization) closes that 3200 gap (N52).
- **Boundary conditions**: Hidden matrices only (optimizer2); compliant under the N16 strict boundary (optimizer-state/update change, no forward/loss/data/batch change). The compression below ~3237 comes from endpoint EMA / mu_schedule layered on top, not from Muon2F alone.
- **Related concepts**: Muon, NorMuon, Newton–Schulz orthogonalization (NS5), endpoint EMA, v12 mu_schedule.

## Endpoint EMA (validation-time weight averaging)
- **Notation**: `ema<beta>s<start>`, e.g. `ema099s2500` (beta=0.99, start step 2500); validation-only swap, restore online weights afterward (under `torch.no_grad()`).
- **Definition**: A run-control / state-level smoothing modifier that maintains an exponential moving average of the model weights from a start step, temporarily swaps the averaged weights in for the periodic validation, then restores the online training weights — leaving online optimization and `GPT.forward` unchanged. It was the strongest endpoint-smoothing signal on the Muon2F-hidden stack (N53): `beta=0.99, start≈2000-2500` narrows the Muon2F stepping stone to step_to_3.28 ≈ 3195-3200 across seeds (part of C02). Fixed uniform tail-averaging (SWA) was consistently worse; extrapolated-EMA eval and matrix-only/MLP-only EMA splits did not beat full-model EMA.
- **Boundary conditions**: A validation-time average only (online weights are restored) — distinct from training-time averaging; sub-~3195 stops are seed-fragile. The first SWA implementation had a `p.copy_` outside `no_grad()` bug (a run-control bug, corrected, not evidence).
- **Related concepts**: WSD / stable-then-decay schedule, Muon2F, two-seed reproduction, noise floor.

## v12 mu_schedule (isolated momentum-schedule lever)
- **Notation**: `v12iso-musched` (isolated lever) vs `v12pack`/`v12simpfix` (the full/simplified package); `h3375` schedule horizon.
- **Definition**: One lever isolated from another agent's "v12" recipe bundle (handed over by the user, N56) — a schedule on the optimizer momentum (`mu`) — applied alone to the active Muon2F/EMA/Adam-mini parent. The full v12 PACKAGE (mu schedule + attention LR 0.6× + cooldown floor + pre-Newton-Schulz row L2 norm + embedding init scale 0.7 + Contra-Muon) washed out, but a leave-one-out factorization showed the mu_schedule lever ALONE carries the gain (N57 pivot): `v12iso-musched-h3375` is a 3-seed reproduced lead with a practical floor walked to stop3170, and `s3220`/`s3195` are the statistically-verified claimable frontiers (C02). The lower 3170 floor was REJECTED by the n-scaled gate (n=15).
- **Boundary conditions**: Compliant optimizer/schedule change (no forward/loss/data/batch change). The gain is the single lever, not the v12 stack; sub-3195 stops are seed-fragile and the 3170 floor fails the statistical gate.
- **Related concepts**: WSD / stable-then-decay schedule, Muon2F, endpoint EMA, noise floor / statistical-significance gate, recipe family / slug-stack.

## Aurora (leverage-aware proj-only Muon-update preconditioner)
- **Notation**: `v3aur2proj` / `v3aur2b035proj` (proj-only); beta strength `b0125/b025/b035/b05`; inserted only in `muon_update` on the C04 compliant stack.
- **Definition**: A leverage-aware row/Stiefel-correction preconditioner that directly attacks Muon's row-leverage collapse in rectangular MLP matrices, transplanted into ONLY the `muon_update` step (square/attention matrices kept on the C04 row-L2 + PE5 path). It is **shape-selective**: applied PROJ-ONLY (to the wide MLP `proj` matrices, m<n, via transpose) it is the FIRST new optimizer mechanism in the lineage to clear the statistical gate — static proj-only beta0.5 n=8 at `ts3037` scores `(3.28−μ)·√8 = +0.006074` (crystallized as C06), beta0.35 +0.005533; applied to the tall MLP `fc` shape (m>n) it HURTS, and the all-rectangular mask (both) is a near-miss (+0.003995). It widens the C04 gate margin at the SAME ts3037 bin (+0.006074 vs C04's +0.004589) but does NOT lower the verified step bin: the lower-step Aurora cohorts (direct ts3025 n=8 −0.001032; ts3035 n=8 +0.003772; the 3025-checkpoint near-misses) all FAIL the gate.
- **Boundary conditions**: Hidden/MLP matrices via the `muon_update` path; compliant under the C05/N16 byte-identical-Architecture rule (optimizer-state/update change, no forward/loss/data/batch change). The gate passes with the proj-only mask; fc-only / all-rect masks do not pass. At v3-001 the gate passed only at the ts3037 endpoint (sub-3037 read as noise-floor artifacts); **at v3-003 ENDPOINT TAIL-TUNING this exact proj-only recipe (a late Aurora-beta ramp 0.35→0.50 + a terminal beta-preload with endpoint-aligned lookahead) lowered the COMMITTED gate-verified bin to ts3027 (C07)** — so the verified Aurora frontier is ts3027 (not ts3037), and the noise-floor-artifact reading now applies BELOW ts3027 (the direct ts3026 port and the entire sub-3000 mechanism hunt fail the gate, N88). The pair-coherent variant (shared hidden-channel scaling across fc rows and proj columns, rho0.25/beta_s0.95/cmax2.0) is viable but no better than simple proj-only. A clean C04-stack-without-Aurora control at matched n (to isolate the proj-only modifier from the C04 base) is still outstanding.
- **Related concepts**: Muon, NorMuon, Newton–Schulz orthogonalization (NS5), Muon2F, Soft-Muon, outward-radial update dampening, noise floor / statistical-significance gate, recipe family / slug-stack.

## Soft-Muon (Gram-Frobenius / Schatten-4 normed Muon, public PR #291)
- **Notation**: `soft` / `soft<ceil>` (Soft-Muon ceiling, e.g. `soft2925`); on the public `v37`/`v48` Contra stack; load-bearing in the C08 step-2940 stack.
- **Definition**: A public modded-nanogpt PR #291 variant of the Muon/Contra update in which the polar/orthogonalization input scaling and norm restorations use a **Gram-Frobenius / Schatten-4** norm (with p=0.1 basis stacking) instead of the hard orthogonalization, producing a "softer" update. Imported (user-directed, N89) onto the architecture-compliant `v37` checkout as one component of the public-frontier stack. On its own it gives good early loss but **insufficient tail slope** (base Soft-only ≈ 3.28345/3.28351 at 2949, not a 2949-step crossing), so it is NOT a standalone frontier; but the leave-one-out pruning round (N90) shows it is **load-bearing** for the gated step-2940 result (removing it — `nosoft` — demotes the 2940 mean to 3.280623). Part of the C08 stat-sig step-2940 stack.
- **Boundary conditions**: Compliant under the C05/N16 byte-identical-Architecture rule (optimizer-update change, no forward/loss/data/batch change). Not a standalone compression lever (insufficient tail slope alone); only gates as part of the coupled Soft-Muon + tail-only-radial + SOAP + V-SOAP + LACV + reduced-q/k-Contra + q/k-LACV-floor + tangent-sphere ensemble (O30). The PR #291 norm switch must be applied to hard Aurora polar input scaling, Contra normalization, Soft-Muon input scaling, and all norm restorations (not only Soft-Muon) to test the recipe faithfully.
- **Related concepts**: Muon, outward-radial update dampening, Newton–Schulz orthogonalization (NS5), noise floor / statistical-significance gate, recipe family / slug-stack.

## Outward-radial update dampening (public PR #294, tail-correction only)
- **Notation**: `rad<scale>` (e.g. `rad045`) / `tailradgate` / `tailradial<start>`; on the public Soft-Muon/Contra stack; load-bearing in the C08 step-2940 stack.
- **Definition**: A public modded-nanogpt PR #294 update modification that, AFTER the update is formed, decomposes it into radial (parallel-to-weight) and tangential components and DAMPENS the outward-radial part, then applies a post-step radius correction (a WD-aware radius target). Imported (user-directed, N89) onto the compliant `v37` checkout. The audited PR #294 projection/sign/placement math is correct; the agent's only deliberate deviations are **tail activation** (the dampening is gated ON only after ~2400-2500, NOT from step zero) and a WD-aware radius target. **Radial-from-step-zero is a hard KILL** (it tracks the slow radial-only curve, ~0.04 behind Soft-only by step 1000, unrecoverable for under-2950, O31); applied as a TAIL correction it is **load-bearing** for the gated step-2940 result (removing it — `noradial` — demotes the 2940 mean to 3.282580, the most destructive single removal after SOAP). Part of the C08 stat-sig step-2940 stack.
- **Boundary conditions**: Compliant under the C05/N16 byte-identical-Architecture rule (optimizer-update change, no forward/loss/data/batch change). Must be a TAIL correction (gated after ~2400-2500), not from step zero (the radial-from-zero kill). A base PR #294 radial dampening is required (noradial collapses), but an EXTRA tail-tightening knob (`notailradial`) is pruneable/neutral at the 2940 boundary; a tangent-sphere radial GATE is load-bearing while a sphere-lookahead PULL is pruneable (O30). The public Muown (PR #288) post-step norm-growth graft is INCOMPATIBLE as wired (explodes ~5.67 by step 2500), and KL-SOAP-H (PR #290) is far off-target + expensive (O31).
- **Related concepts**: Soft-Muon, Muon, two-seed reproduction, noise floor / statistical-significance gate, pruning rounds, recipe family / slug-stack.
