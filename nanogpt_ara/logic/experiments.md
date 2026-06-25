# Experiments

Directional verification/analysis plans. **No exact numbers** — those live in
[../evidence/](../evidence/). "Experiment" here means a benchmark eval campaign, an ablation
sweep, or a statistical verification. Claims and experiments are many-to-many; a claim that
generalizes across waves lists several experiments in its `Proof`.

Each run is one execution of the canonical `train_gpt_simple.py` (or a `scratchpad/variants/`
copy for diagnostics only); results are filed in [../src/artifacts.md](../src/artifacts.md) (the
8,224 attached run exports) and summarized in [../evidence/](../evidence/).

---

## E01 — Schedule-horizon vs train-step decoupling

**Verifies.** C01.
**Setup.** Baseline Muon on the fixed benchmark; vary `schedule_steps` (LR-decay length)
independently of `train_steps` (optimization length), forcing final validation at `train_steps <
schedule_steps`.
**Procedure.** Establish the baseline crossing; run `horizon<sched>-stop<train>` variants holding a
long schedule while shortening the optimization horizon; reproduce any crossing on a second seed;
map the seed-dependent cliff below which the shortened horizon lags from mid-training.
**Expected outcome.** A long-schedule/short-optimization run crosses target earlier than the
matched-length baseline, down to a seed-dependent floor; directionally the schedule geometry
buys step-count without an optimizer change.
**Evidence.** [../evidence/figures/v1_loss_curves.md](../evidence/figures/v1_loss_curves.md).
**Run.** v1 `horizon*` / `h<sched>-stop<train>` families (`v1/codex/scratchpad/THREAD.md:139-261`).

---

## E02 — Optimizer-family screen against the Muon baseline

**Verifies.** C03, C05.
**Setup.** A breadth screen of post-Muon and older optimizers (NorMuon, Muon2F, MARS-M, Adam-mini,
SOAP/Shampoo, APOLLO, Lookahead, Sophia-F, CAME, LAMB, …) each LR/WD/schedule-tuned against the
Muon baseline bar.
**Procedure.** Coarse log-spaced LR sweep, refine around any peak, sweep WD and schedule shape,
two-seed reproduction at the best cell, kill a family at the stuck-detector threshold; record clean
negatives.
**Expected outcome.** Most families are ruled out (negative or worse than Muon); NorMuon, Muon2F,
and Adam-mini survive as positive; the surviving gains are seed-fragile near the frontier.
**Evidence.** [../evidence/figures/v1_pruning.md](../evidence/figures/v1_pruning.md) (component
contributions of the survivors), [../evidence/tables/v1_pruning_table.md](../evidence/tables/v1_pruning_table.md).
**Run.** v1 optimizer screens and `picklist.md` graveyard (`v1/codex/plan.md:35-71`).

---

## E03 — Tail-EMA vs SWA endpoint smoothing

**Verifies.** C02.
**Setup.** On the v1 Muon2F/Adam-mini stack, compare evaluation-time weight EMA (β≈0.99, late
start) against uniform tail averaging (SWA) and against no smoothing.
**Procedure.** Swap an EMA/SWA average of late weights in for the final validation only, then
restore; sweep β and start step; reproduce across seeds; compare crossing steps.
**Expected outcome.** Tail-EMA converts near-misses into crossings and is the strongest endpoint
lever; SWA is consistently worse than EMA.
**Evidence.** [../evidence/figures/v1_pruning.md](../evidence/figures/v1_pruning.md) (`noTailEMA` is
the top bar).
**Run.** v1 EMA/SWA support jobs (`v1/codex/plan.md:102-104`, `THREAD.md:1745-2030`).

---

## E04 — v1 leave-one-out component pruning

**Verifies.** C02, C03, C07.
**Setup.** The v12iso stack at its 3195-step screen; remove each component in turn.
**Procedure.** For each modifier build a leave-one-out variant, run an n-seed cohort, measure
`Δval when removed`; rank components; drop only those whose removal is within ±0.5× noise.
**Expected outcome.** Tail-EMA and Muon2F dominate; mu-schedule and error-feedback are moderate;
late-LR / momentum-refresh / residual-pulse are net-removable.
**Evidence.** [../evidence/figures/v1_pruning.md](../evidence/figures/v1_pruning.md),
[../evidence/tables/v1_pruning_table.md](../evidence/tables/v1_pruning_table.md),
[../evidence/data/v1_pruning_data.json](../evidence/data/v1_pruning_data.json).
**Run.** v1 `formalprune` / pruning-rerun runs (family `formalprune`, 162 runs in `runs.csv`).

---

## E05 — v2 compliance audit, quarantine, and compliant rebuild

**Verifies.** C08.
**Setup.** The inherited v12 parent (traced to the Claude/cc agent) used as the v2 backbone.
**Procedure.** Run a code-comparison subagent against the public script; on the flagged
`RMSNorm.forward` / q-k-norm forward-path change, cancel live jobs, quarantine all v12-derived
results, add a launch-time Architecture gate that blocks non-byte-identical forward/norm code, and
rebuild the `legal_v12opt` family from the workspace baseline.
**Expected outcome.** The non-compliant family is excluded from the frontier (even though it
helped); a byte-identical-compliant frontier is re-established and becomes the submission base.
**Evidence.** [../evidence/tables/v2_seed_table.md](../evidence/tables/v2_seed_table.md) (the
compliant submitted cohort).
**Run.** v2 `v12` (quarantined) vs `v12iso`/`legal_v12opt` families (`v2/.../THREAD.md:124-214`).

---

## E06 — v2 role-specific LR/WD + lookahead frontier search

**Verifies.** C04, C05.
**Setup.** The compliant v2 stack; add role-specific LR multipliers, role-specific weight decay,
and Muon lookahead.
**Procedure.** Screen each lever at a fixed step budget, then walk the step frontier by copying a
verified parent with only `train_steps` changed; track single-seed crossings vs cohort means.
**Expected outcome.** Role-LR/WD and lookahead extend the single-seed frontier lower, but the
cohort means at those low steps still miss (motivating E08).
**Evidence.** [../evidence/figures/v2_pruning.md](../evidence/figures/v2_pruning.md),
[../evidence/figures/v2_loss_curves.md](../evidence/figures/v2_loss_curves.md).
**Run.** v2 `rolewd` / `rolelr2` / `lookahead` families (`v2/.../THREAD.md:476-800`).

---

## E07 — v2 leave-one-out pruning at the submitted step budget

**Verifies.** C03, C04, C07.
**Setup.** The submitted `legal_v12opt` stack at its submitted step budget; remove each component.
**Procedure.** Leave-one-out each modifier over an n-seed cohort; rank by `Δval when removed`.
**Expected outcome.** Inherited MuonEq and the mu-schedule are the largest contributors; role-LR is
the largest v2-specific addition; lookahead and role-WD are smaller; Contra-Muon is near-zero.
**Evidence.** [../evidence/figures/v2_pruning.md](../evidence/figures/v2_pruning.md),
[../evidence/tables/v2_pruning_table.md](../evidence/tables/v2_pruning_table.md),
[../evidence/data/v2_pruning_data.json](../evidence/data/v2_pruning_data.json).
**Run.** v2 pruning-rerun cohort (`record_configs/20260515_codex_v2_legal_3037/`).

---

## E08 — Fixed-cohort statistical verification (submission gate)

**Verifies.** C06.
**Setup.** Candidate step budgets from each wave; cohorts of n non-cherry-picked seeds with
distinct `--seed N`.
**Procedure.** Compute the cohort mean and the significance margin; scan all common checkpoints for
the earliest that passes the fixed-cohort threshold (anti-val-spam); reject single-seed crossings
and low-step families whose cohort margin is negative.
**Expected outcome.** Each wave's submitted bin is the earliest common checkpoint passing the gate
over its seed cohort; lower single-seed crossings are rejected by the gate.
**Evidence.** [../evidence/tables/v1_seed_table.md](../evidence/tables/v1_seed_table.md),
[../evidence/tables/v2_seed_table.md](../evidence/tables/v2_seed_table.md),
[../evidence/tables/v3_seed_table.md](../evidence/tables/v3_seed_table.md).
**Run.** v1 stat pass (`v1/.../THREAD.md:2231-2232`), v2 significance cohorts (`v2/.../THREAD.md:802-810`),
v3 `v3prune-w258loo-nosphere` cohort.

---

## E09 — v3 public-PR reproduction (Soft-Muon, radial brake)

**Verifies.** C09, C10.
**Setup.** The public modded-nanogpt frontier below the v3 line: PR #294 (radial), PR #291
(Contra→Soft-Muon), PR #290 (KL-SOAP-H), PR #288 (Muown).
**Procedure.** Port each PR onto the v3 backbone with an audit subagent confirming faithfulness;
test radial timing (from-step-zero vs tail-only); test SOAP portability against the zero-init
projections.
**Expected outcome.** PR #294 radial (tail-only) and PR #291 Soft-Muon reproduce and are
load-bearing; PR #290 full KL-SOAP-H is not portable (salvaged only as a warm-start sidecar);
PR #288 Muown is incompatible.
**Evidence.** [../evidence/figures/v3_pruning.md](../evidence/figures/v3_pruning.md) (`noradial`,
`nosoap`, `nosoft` contributions).
**Run.** v3 public-frontier port (`v3/.../THREAD.md:411-552`).

---

## E10 — v3 SOAP / LACV / radial mechanism search (the u2900 worker campaign)

**Verifies.** C05, C10.
**Setup.** The reproduced v48 public-frontier parent; goal reset below the prior frontier.
**Procedure.** A long numbered-worker search over warm-start SOAP-skip, conditional radial guard
windows, q/k Contra scaling, LACV and its q/k floor, radius-preserving lookahead, and schedule-phase
retargeting (keeping the back-loaded PR #287 cooldown rather than truncating it).
**Expected outcome.** A small set of levers (warm SOAP sidecar, tail-radial guard, LACV floor)
converge on a sub-2950 statistically-viable distribution; hard schedule truncation fails.
**Evidence.** [../evidence/figures/v3_loss_curves.md](../evidence/figures/v3_loss_curves.md).
**Run.** v3 `v3u2900-worker*` families (hundreds of runs in `runs.csv`).

---

## E11 — v3 W258 leave-one-out pruning → nosphere

**Verifies.** C07, C09, C10, C11.
**Setup.** The W258 tangent-sphere stack at its statistical boundary; the leave-one-out ablation set
(nosoft, nocontra, noqkcontrascale, noradial, notailradial, nolacv, nolacvfloor, nosphere,
notangentsphere, nosoap, novsoap).
**Procedure.** Run each ablation as an n-seed cohort at the boundary; rank by `Δval when removed`;
identify the only removal that both simplifies and preserves the statistical boundary; test the
combined sphere removal for composition.
**Expected outcome.** SOAP and radial are the largest keeps; `nosphere` (drop the sphere-lookahead
pull) is the only positive-score, submittable simplification; `nosphere_notangent` loses the
boundary (the two sphere terms do not compose).
**Evidence.** [../evidence/figures/v3_pruning.md](../evidence/figures/v3_pruning.md),
[../evidence/tables/v3_pruning_table.md](../evidence/tables/v3_pruning_table.md),
[../evidence/data/v3_pruning_data.json](../evidence/data/v3_pruning_data.json).
**Run.** v3 `v3prune-w258loo-*` runs (16 `nosphere` runs in `runs.csv`),
`v3/.../w258_2940_leave_one_out_pruning_20260513.md`.

---

## E12 — Novelty wave: novelty-constrained mechanism search (negative)

**Verifies.** C05, C12.
**Setup.** Hard-isolated worktree; a novelty bar tightened three times (excluding schedule, then
optimizer+schedule, then merely-additive optimizer couplings); two mandatory pre-code gates (arXiv
novelty + benchmark-rule compliance).
**Procedure.** Generate candidate mechanisms (residual-corrected Muon, init rescales, polar-disagreement
splits, commutator corrections, branch-Gram couplings, …); kill at the gate those that reduce to
known literature or are exact-polar algebraic no-ops; run the survivors; require two-seed
reproduction and ≥ 2× noise-floor improvement to promote.
**Expected outcome.** No promotable submission: the best robust result is a reproduced one-bin gain
below the noise floor; most invented mechanisms are pre-empted by the literature or are no-ops.
**Evidence.** [../evidence/tables/novelty_outcomes.md](../evidence/tables/novelty_outcomes.md).
**Run.** novelty wave (`novelty/codex/scratchpad/THREAD.md`, 254 runs in `runs.csv`,
family-tagged `ngi`/`rsi`/`vfg`/…).
