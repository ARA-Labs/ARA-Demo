# Problem

## Setting

`track_3_optimization` of the modded-nanogpt benchmark fixes the architecture, dataset, batch
size, and the one-forward-backward-per-step contract of a ~124M-parameter GPT, and asks a single
question: **in how few training steps can validation loss reach 3.28?** The optimizer, its
hyperparameters, the learning-rate/weight-decay schedule, and parameter initialization are the
*only* surfaces an entrant may change. The current best at the start of the experiment is **Muon
(lr=0.025, wd=0.0125) at 3500 steps**; an AdamW baseline reaches the same loss only at 5625
steps (`v1/codex/goal.md:3-7`, `v1/codex/AGENTS.md:5-6`).

The agent's standing goal is the open-ended one in `goal.md`: *"Find an optimizer / hyperparameter
/ schedule / init combination that reaches 3.28 validation loss in fewer than 3500 steps … the
current stretch target from the user is below 2800 steps"* (`v1/codex/goal.md:3-6`).

## Observations (with numbers)

- **O1 — The baseline is already close.** Canonical Muon hits 3.28 at 3500 and is only
  `3.28106` at step 3375 — a near-miss a few thousandths above target (v1 journal,
  `v1/.../THREAD.md:142-143`). The headroom per step is therefore *small relative to seed noise*.
- **O2 — Seed noise is comparable to the prize.** The agent's own noise-floor estimate is
  `step_to_target ≈ 50 steps`, `final_val_loss mean ≈ 0.001` (`v1/codex/AGENTS.md:160-163`).
  A 50–100-step "win" can be entirely seed noise.
- **O3 — The literature is unverified and wide.** The benchmark exists because "the optimization
  literature is a sea of unverified SOTA claims … 100s–1000s of optimizer papers; most have never
  been compared head-to-head on the same setup" (`v1/codex/goal.md:12-15`). The search space of
  candidate optimizers/schedules/inits is enormous and mostly untested at this scale.
- **O4 — Wall-clock is irrelevant.** Methods that are slow per step (Shampoo, SOAP, full-matrix
  preconditioners) are admissible if they cut *steps* (`v1/codex/goal.md:33-34`). This widens the
  admissible method set well beyond what a wall-clock speedrun would allow.
- **O5 — The submitted trajectory.** Codex drove the bin from 3500 to
  **3205 → 3037 → 2949** across three promotable waves (`README.md:10`,
  `record_configs/*/README.md`), with one hard-isolated wave producing no promotable submission.

## Gaps

- **G1 — Which methods actually beat Muon here, and do their gains stack?** Most optimizer papers
  under-tune baselines and never test head-to-head; it is unknown which post-Muon ideas survive a
  fair, single-setup comparison, and whether gains from {optimizer, schedule, init, second-order
  preconditioning, EMA} are orthogonal or redundant (`v1/codex/goal.md:36-48`).
- **G2 — Where is the noise floor, and what makes a step-count gain real?** Without a reproduction
  and significance discipline, sub-frontier "wins" are indistinguishable from favorable seeds
  (`v1/codex/goal.md:49-50`).
- **G3 — How much of a near-saturated speedrun is reachable by genuinely novel mechanisms** (as
  opposed to reusing schedule/optimizer tricks already in the literature)? This is the question
  the hard-isolated novelty wave was built to answer.
- **G4 — How should an autonomous agent keep its own ledger honest** when it inherits results from
  another agent or from public PRs whose compliance it cannot take for granted?

## Key insight

The decisive moves in this trajectory are **methodological, not a single magic optimizer**:

1. **Decouple the LR-decay horizon from the optimization horizon.** Holding `schedule_steps`
   longer than `train_steps` keeps the LR warmer at the forced final validation, crossing target
   earlier "for free" — the lever that first beat 3500 and recurs across every wave
   ([C01](claims.md)).
2. **Treat the sub-frontier region as a seed-fragility map governed by a significance gate**, not
   as a monotone frontier to be greedily descended ([C05](claims.md), [C06](claims.md)). Every
   submitted bin is a *fixed-cohort* result that clears `(3.28−μ)·√n ≥ 0.004` over n=16 seeds, not
   a cherry-picked single crossing.
3. **Add levers, then prune them.** Each wave ends with a mandatory leave-one-out pruning round
   that quantifies every component's marginal contribution and drops the redundant ones
   ([C07](claims.md), [C11](claims.md)) — which is how v3's submitted recipe became *simpler*
   (`nosphere`) than its parent.
4. **Quarantine non-compliant inheritance.** A v12 parent inherited from the other agent carried a
   forward-path precision change; once flagged it was quarantined wholesale and the frontier was
   rebuilt on a byte-identical-compliant base ([C08](claims.md)).

The *content* levers that moved the metric most — tail-only weight EMA, factorized second-moment
preconditioning (Muon2F/MuonEq), role-specific LR/WD, outward-radial dampening, and a warm-start
SOAP sidecar — are the subject of [C02](claims.md)–[C04](claims.md), [C09](claims.md),
[C10](claims.md).

## Assumptions

- **A1** — The submitted `record_configs/` READMEs and their `pruning_data.json` are the
  authoritative final results; the per-wave `THREAD.md` journals are the (messier, point-in-time)
  trajectory. Where they disagree, the record governs (see PAPER.md compile note).
- **A2** — `final_val_loss` and the first-crossing step are read from the canonical training log
  for a submitted run; a run "counts" only if `step_to_3.28` actually fired (a run can dip past
  3.28 and back — `v1/codex/AGENTS.md:224-226`).
- **A3** — The noise-floor estimates (`step_to_target ≈ 50`, `final_val_loss ≈ 0.001`) are
  treated as stable across the experiment; they were refreshed from baseline Muon at 3 seeds and
  not recomputed every turn (`v1/codex/plan.md:24-27`).
- **A4** — "Compliant" means the `Architecture` and forward/normalization code of the submitted
  script is byte-identical to baseline `train_gpt_simple.py`; only the `Optimization` and
  `Init & Optim Hyperparams` sections differ (`v2/.../THREAD.md:130`).
