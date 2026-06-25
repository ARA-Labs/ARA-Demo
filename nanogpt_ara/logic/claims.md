# Claims

Mechanism-level, falsifiable takeaways from the Codex speedrun. Each `Statement` is the reusable
*why*; named recipes, run IDs, bins, and scores live in `Evidence basis`/`Proof`/`Sources`, never
in the `Statement`. `Proof` references experiment IDs in [experiments.md](experiments.md).
Provenance: all claims are `ai-executed` (the agent ran the experiments); the significance and
compliance disciplines (C06, C08) were `user-revised` (the human operator set or tightened the
rule).

Load-bearing numbers are grounded against firsthand-opened sources: the submitted
`record_configs/*/README.md`, their `pruning_data.json` (also mirrored under
[../evidence/data/](../evidence/data/)), and the per-wave `*/codex/scratchpad/THREAD.md` journals.

---

## C01 — Decoupling the LR-decay horizon from the optimization horizon compresses step count

**Statement.** Holding the learning-rate schedule's decay length longer than the number of
optimization steps actually taken keeps the LR warmer at the forced final validation than a
matched-length cosine would, so a near-miss model crosses the target loss earlier without any
change to the optimizer — step-count is recovered "for free" from the schedule geometry alone.

**Conditions.** Holds for the Muon/NorMuon/Muon2F/Adam-mini families on this 124M-GPT speedrun
near the 3.28 threshold, where the matched-length baseline is already a few thousandths above
target. Untested boundary: how far the decay/optimization horizons can diverge before the colder
intermediate LR costs more than the warmer endpoint buys (the agent observed a seed-dependent
cliff below which a too-short optimization horizon lags from mid-training and cannot recover).

**Status.** Supported (corroborated across every wave; it is the first lever that beat 3500 and
recurs as `h<sched>-stop<train>` and `FINAL_SCHEDULE_STEPS`≠`FINAL_TRAIN_STEPS` throughout).

**Falsification criteria.** If, on this benchmark, runs with `schedule_steps > train_steps` cross
3.28 no earlier (within the seed noise floor) than the best matched-length schedule at equal
`train_steps`, the mechanism is refuted. System-level: if the gain disappeared once the
intermediate LR is held fixed, the effect would not be the schedule-horizon decoupling.

**Proof.** E01.

**Evidence basis.** The baseline is `3.28106` at step 3375 vs `3.27658` at 3500, motivating a
forced early validation under the long schedule; `horizon3500-stop3450` then crossed at step 3450,
the first sub-3500 hit, reproduced on a second seed. The same lever (`FINAL_SCHEDULE_STEPS=3025`,
`FINAL_TRAIN_STEPS=3020`) is the backbone of the v3 schedule in `worker192/193`.

**Sources.**
- `3.28106`@3375, `3.27658`@3500 ← `v1/codex/scratchpad/THREAD.md:142` «schedule was `3.28106` at step 3375 and `3.27658` at 3500, so a forced final validation at 3450 may already beat the target without compressing cooldown» [result]
- first sub-3500 hit `3.27844`@3450 ← `v1/codex/scratchpad/THREAD.md:187-189` «Run `horizon3500-stop3450-seed0` hit target: … at step 3450 with `val_loss=3.27844` … This beats the 3500-step baseline» [result]
- schedule≠train in v3 ← `v3/codex/scratchpad/THREAD.md:1039` «`FINAL_SCHEDULE_STEPS` 3025 and 3015 while keeping `FINAL_TRAIN_STEPS=3020`» [input]

---

## C02 — Tail-only weight EMA at evaluation is the single largest step-count lever in the v1 stack; uniform tail averaging is worse

**Statement.** Evaluating on an exponential moving average of the late-training weights (swapped
in for the final validation, then restored) supplies a lower-variance evaluation point than the
still-noisy online weights, converting a near-miss into a crossing without altering the training
trajectory; a uniform (SWA-style) average of the same tail is consistently inferior because it
weights stale early-tail weights as heavily as the most-converged ones.

**Conditions.** Established on the v1 Muon2F/Adam-mini stack with EMA β≈0.99 starting in the late
schedule; it is an evaluation-time transformation, so it cannot move the training dynamics, only
the reported endpoint. Untested boundary: whether the same lever is the *largest* contributor on
stacks (v2/v3) where role-LR/SOAP already dominate.

**Status.** Supported (largest single leave-one-out contribution in the v1 record; SWA dominated
by EMA in direct comparison).

**Falsification criteria.** If removing tail-EMA from the submitted v1 stack and re-running n
seeds changes the crossing step by less than the noise floor, or if a matched uniform-SWA tail
average matches EMA within noise, the claim is refuted.

**Proof.** E03, E04.

**Evidence basis.** In the v1 leave-one-out pruning rerun, removing tail-EMA is the worst single
ablation (`noTailEMA` raises val by `+0.00251`, the top bar), ahead of every other component; the
agent separately recorded that "fixed SWA is consistently worse" and declined to expand it.

**Sources.**
- `noTailEMA` Δval `+0.00251` (largest) ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:113-114` «"label": "noTailEMA" … "mean": 3.28158» (delta `0.0025100000000000122` vs baseline `3.27907`) [result]
- SWA worse ← `v1/codex/scratchpad/THREAD.md:1813` «do not expand SWA because fixed SWA is consistently worse» [result]

**Dependencies.** Builds on C01 (the EMA lever operates at the forced final-validation step set by the schedule decoupling).

---

## C03 — Factorized row/column second-moment preconditioning of the matrix update is a large, reusable optimizer contributor

**Statement.** Replacing the plain Muon matrix update with one that applies row/column-normalized
(factorized two-factor) second-moment preconditioning — the Muon2F / MuonEq family — is among the
largest single optimizer-side step-count gains, independent of and stacking on top of the
schedule and evaluation levers.

**Conditions.** Holds on this benchmark's hidden weight matrices (attention and MLP projections);
in v1 it appears as "Muon2F" hidden-only preconditioning, in the compliant v2 stack as the
"MuonEq" row-normalized update. Untested boundary: whether the two formulations are
interchangeable at equal tuning, and whether the gain persists once SOAP-style preconditioning
(v3) is also present.

**Status.** Supported (second-largest single ablation in v1; largest *inherited* optimizer
ablation in v2).

**Falsification criteria.** If removing the factorized second-moment preconditioning from the v1
or v2 submitted stacks and re-running n seeds moves the crossing step by less than the noise
floor, the contribution is not real.

**Proof.** E02, E04, E07.

**Evidence basis.** v1 leave-one-out: `noMuon2f` is the second-worst ablation (`+0.00229`). v2
leave-one-out: `noMuonEq` is the single largest *content* ablation (`+0.00353`), ahead of every
v2-specific addition.

**Sources.**
- v1 `noMuon2f` Δval `+0.00229` ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:104-106` «"label": "noMuon2f" … "mean": 3.28136» (delta `0.0022899999999999032`) [result]
- v2 `noMuonEq` Δval `+0.00353` ← `record_configs/20260515_codex_v2_legal_3037/pruning_data.json:80-82` «"label": "noMuonEq" … "mean": 3.28238» (delta `0.003530000000000033`) [result]

---

## C04 — Splitting learning rate and weight decay by parameter role is a productive lever once a single body-wide value is saturated

**Statement.** Once a single body-wide Muon LR and weight decay are tuned out, assigning
*role-specific* LR multipliers and weight-decay values to the different parameter groups
(q/k, v, attn.proj, mlp.fc, mlp.proj) recovers further step-count where uniform scalars and plain
reseeding stall — different roles want measurably different effective step sizes near the loss
boundary.

**Conditions.** Established on the compliant v2 stack near the ~3000-step regime; role-LR is the
larger of the two (role-WD is a smaller refinement). Untested boundary: whether the optimal
per-role split transfers to the v3 public-PR backbone, which re-derives its own role structure
(Soft/SOAP on MLP+V).

**Status.** Supported (role-LR is a top-four v2 ablation; role-WD a smaller but positive one).

**Falsification criteria.** If collapsing the role-specific LR/WD vectors back to their best
single body-wide values costs less than the noise floor over n seeds on the v2 stack, the lever is
not real.

**Proof.** E06, E07.

**Evidence basis.** v2 leave-one-out: `noRoleLR` is the largest v2-*specific* ablation
(`+0.00292`, fourth overall behind the inherited mu-schedule, cooldown-floor, and MuonEq);
`noRoleWD` is smaller but positive (`+0.00041`). The submitted record names the per-role
multipliers (q/k `0.61875`, v `0.625`, attn.proj `0.6375`, mlp.fc `1.0125`, mlp.proj `0.9875` of
base LR `0.045`) and per-role WD around `0.027..0.0315`.

**Sources.**
- `noRoleLR` Δval `+0.00292` ← `record_configs/20260515_codex_v2_legal_3037/pruning_data.json:72-74` «"label": "noRoleLR" … "mean": 3.28177» (delta `0.0029200000000000337`) [result]
- `noRoleWD` Δval `+0.00041` ← `record_configs/20260515_codex_v2_legal_3037/pruning_data.json:32-34` «"label": "noRoleWD" … "mean": 3.27926» (delta `0.00041000000000002146`) [result]
- per-role multipliers ← `record_configs/20260515_codex_v2_legal_3037/README.md:8` «Role-specific Muon LR multipliers: q/k `0.61875`, v `0.625`, attn.proj `0.6375`, mlp.fc `1.0125`, mlp.proj `0.9875` of base LR `0.045`» [input]

---

## C05 — Below the formal frontier, the low-step region is a seed-fragility map, not a monotone frontier

**Statement.** Near the loss threshold the per-run outcome (cross / miss) is dominated by seed
noise rather than by the recipe, so a single-seed crossing at a lower step count is overwhelmingly
likely to be the favorable tail of a distribution whose mean still misses — descending the bin one
seed at a time measures noise, not progress.

**Conditions.** This is the central methodological regularity of the whole experiment; it holds in
every wave (v1 lower-stop brackets, v2's sub-2992 frontier, v3's sub-2900 push, and the novelty
wave's single-seed crossings) wherever step counts approach the point where the cohort mean sits
near 3.28. It does not say recipes never help — it says *unreproduced single crossings* are not
evidence that they do.

**Status.** Supported (corroborated across all four waves; the agent's lawful core encodes it as a
two-seed-reproduction requirement).

**Falsification criteria.** If, on this benchmark, single-seed sub-frontier crossings reproduced
on independent seeds at a rate far above chance (so that a lone crossing reliably predicted a
cohort-mean crossing), the "fragility map" framing would be wrong and greedy descent would be
valid.

**Proof.** E02, E06, E10, E12.

**Evidence basis.** v1: a representative lower-stop bracket splits hit/miss across seeds, prompting
the agent's own verdict that the region is "a seed-fragility map, not a promotion path by itself."
v2: every low-step family's *cohort* z-score is negative even where single runs crossed. Novelty:
single-seed crossings (NGI, NDF, VFG) failed second-seed reproduction or were sub-noise-floor.

**Sources.**
- v1 verdict ← `v1/codex/scratchpad/THREAD.md:976` «the lower-stop region is a seed-fragility map, not a promotion path by itself» [result]
- v2 cohorts negative ← `v2/codex/scratchpad/THREAD.md:802` «the low-step frontier families do not pass `(3.28 - mu) * sqrt(n) >= 0.004`: `ts2962` n=38 mean 3.28243 score -0.01496 … `ts2982` n=17 mean 3.28131 score -0.00539» [result]

**Dependencies.** Motivates C06 (the significance gate is the operational response to this fragility).

---

## C06 — A speedrun result is claimable only under a fixed-cohort significance margin, not a single best run

**Statement.** Because of C05, a valid step-count submission must clear a pre-planned fixed-cohort
significance margin over many non-cherry-picked seeds — with an anti-"val-spam" same-checkpoint
scan so the reported bin is the earliest *common* checkpoint whose cohort mean clears the bar —
rather than resting on a single best run; selecting a lone low-tail crossing is p-hacking and is
rejected even when that crossing is real.

**Conditions.** This is the benchmark's acceptance rule as the agent operationalized it; all three
submitted records (v1, v2, v3) were validated at n=16 under it, and lower single-seed crossings
(v1's 3170, v2's 2962/2963) were rejected by it. The threshold constant `0.004` and the
σ≈0.0013 z-conversion are properties of this benchmark's stated rule, not of the optimizer.

**Status.** Supported (the rule selected every submitted bin and rejected every sub-frontier
single-seed crossing).

**Falsification criteria.** Methodological: if a submission that passed `(3.28−μ)·√n ≥ 0.004` at
n=16 systematically failed to reproduce its cohort mean on a fresh independent n=16 draw, the gate
would not be doing its job. If the rejected lower single-seed crossings (e.g. v1 s3170, v2 ts2962)
had instead passed a fresh fixed cohort, the gate would be too conservative.

**Proof.** E08.

**Evidence basis.** v1's statistical pass selects `s3220`/`s3195`/`s3296` as claimable and
explicitly *rejects* `s3170` (negative score). v2 switches "from frontier search to
submission-validity verification," finds the low-step families fail the margin, and certifies the
fixed +75 cohort `ts3037` (mean `3.2783775`, score `0.004589`, z≈3.53, p≈0.000208) as the earliest
common checkpoint that passes. The submitted records report n=16 margins of `0.00411250` (v1),
`0.00588000` (v2), `0.00455500` (v3).

**Sources.**
- v1 rule + rejection ← `v1/codex/scratchpad/THREAD.md:2232` «Claimable by `((3.28 - mu) * sqrt(n) >= 0.004)`: `v12iso-musched-h3375-s3220` `n=12`, `mu=3.278060`, score `0.006720` … Rejected: `v12iso-musched-h3375-s3170` `n=15`, `mu=3.280266`, negative score» [result]
- v2 certification ← `v2/codex/scratchpad/THREAD.md:810` «mean 3.2783775; score `(3.28 - mu) * sqrt(8) = 0.004589` … 3025 does not pass (mean 3.279132, score 0.002454), while final step 3037 is the earliest common validation checkpoint that passes» [result]
- v1 record n=16 margin `0.00411250` ← `record_configs/20260515_codex_v1_v12iso_3205/README.md:21-24` «n = 16 / mean val loss = 3.27897187 / (3.28 - mu) * sqrt(n) = 0.00411250» [result]
- v3 record n=16 margin `0.00455500` ← `record_configs/20260515_codex_v3_nosphere_2949/README.md:21-25` «n = 16 / mean val loss = 3.27886125 / (3.28 - mu) * sqrt(n) = 0.00455500» [result]

**Dependencies.** C05.

---

## C07 — Stacked modifier packages wash out late even when each gains mid-curve; leave-one-out pruning recovers the real stack

**Statement.** Combining many modifiers that each improve the mid-training curve does not
reliably preserve the gain to the final validation — the package can miss where an isolated lever
hits — so an explicit removal mechanism (leave-one-out pruning that measures each component's
marginal contribution and drops the redundant ones) is required for the stack to stay
attributable and to keep its smallest faithful form.

**Conditions.** Holds across the experiment: v1 found stacked "v12 packages" missed while the
isolated mu-schedule lever hit; every wave ends in a mandatory pruning round; v3's submitted
recipe is *simpler* than its parent because pruning removed a redundant component. Untested
boundary: the pruning verdicts are single-/few-seed leave-one-out deltas (n=8 in v1/v2, n=3–16 in
v3), so very small contributions sit within their own noise.

**Status.** Supported (the pruning rounds are first-class artifacts with quantified per-component
deltas; v1 and v2 leave-one-out tables resolve which modifiers are load-bearing vs droppable).

**Falsification criteria.** If a leave-one-out "redundant" component (Δval ≈ 0 within noise) turned
out to cost more than the noise floor when removed in a fresh independent cohort, or if a stacked
package reliably retained all its mid-curve gains at final validation, the claim is wrong.

**Proof.** E04, E07, E11.

**Evidence basis.** v1: stacked `v12pack` packages missed while the isolated mu-schedule lever was
the reproduced lead; the v1 pruning table spans an order of magnitude in per-component Δval (from
`noTailEMA +0.00251` down to `noResPulse −0.00007`, i.e. some components are net-removable). v3:
`nosphere` (C11) is a leave-one-out *removal* that the agent submitted.

**Sources.**
- v1 isolated lever beats package ← `v1/codex/plan.md:12` «Full `v12pack-hbin` missed all completed seed0 stops … Isolated `mu_schedule` is now the reproduced lead» [result]
- removable component (negative Δ) ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:24-29` «"label": "noResPulse" … "delta": -7.00000000000145e-05» [result]

**Dependencies.** Pruning is mandated by the lawful core (see [solution/constraints.md](solution/constraints.md)).

---

## C08 — A cross-agent parent that changes the forward path is non-compliant and must be quarantined regardless of how much it helped

**Statement.** Inheriting a high-performing parent from another agent does not transfer its
validity: when that parent altered the model's forward/normalization path (here, an
`RMSNorm.forward` casting change and routing q/k normalization through the helper), it violates
the no-architecture-change rule, so every result derived from it is invalid and must be excluded
from the frontier — even after confirming the change "materially helped" — and the submittable
frontier must be rebuilt on a byte-identical-compliant base.

**Conditions.** Specific to benchmarks whose rules pin the forward path (here, only the
`Optimization` and `Init & Optim Hyperparams` sections may change; forward/norm code must be
byte-identical). The judgement that the change helped means the quarantine *costs* real
performance — that is the point: epistemic validity outranks the score.

**Status.** Supported (the quarantine was executed: jobs cancelled, the `v2cx` family
disqualified, the prefix switched to `v2cxleg`, the frontier rebuilt; the submitted v2 record is
the compliant `legal_v12opt` stack).

**Falsification criteria.** Methodological: if the flagged `RMSNorm.forward` change were shown to
leave the bf16 forward output bit-identical to baseline across the validation set, it would not be
a forward-path change and the quarantine would be unnecessary. If the rebuilt compliant frontier
matched the quarantined one within noise, the change would not in fact have "materially helped."

**Proof.** E05.

**Evidence basis.** The user flagged the inherited `RMSNorm.forward` precision change as a
forward-path violation; the agent immediately cancelled the live `v2cx` jobs and quarantined all
v12-derived results, while explicitly recording that the invalid change *had* helped the sub-3000
behavior, then rebuilt the compliant `legal_v12opt` family.

**Sources.**
- the flag ← `v2/codex/scratchpad/THREAD.md:126` «User flagged a real architecture/forward-pass violation: every v12-derived codex variant inherited `RMSNorm.forward` as `(norm(x.float()) * self.gains).type_as(x)` instead of the workspace baseline `F.rms_norm(...)` … This is a precision/behavior change in the forward path and is invalid for this track even if mathematically close» [result]
- the quarantine ← `v2/codex/scratchpad/THREAD.md:128` «all v12-derived `v2cx` results are now quarantined and must not be reported as valid frontier improvements» [result]
- it helped (cost of compliance) ← `v2/codex/scratchpad/THREAD.md:154` «the invalid forward-path change materially helped the sub-3000 behavior» [result]

---

## C09 — Outward-radial dampening helps because it preserves the late "catch-up" tail, and only tail-activated

**Statement.** Damping the outward-radial drift of the matrix update after it is formed (with a
post-step radius correction) keeps the optimizer on the productive radius so the back-loaded
cooldown can keep reducing loss into the final steps; the benefit is specifically a preserved
late-training catch-up, which is why applying the same damping from step zero is harmful — it
suppresses early progress the run cannot recover from at low step budgets.

**Conditions.** Established on the v3 public-PR backbone (the KellerJordan PR #294 radial brake) at
low step budgets; the damping is tail-activated (guard window late in training). Untested
boundary: whether the same tail-only timing is optimal at higher step budgets where the cooldown
is less back-loaded.

**Status.** Supported (radial is a top-two v3 ablation; radial-from-step-zero was an explicit
kill).

**Falsification criteria.** If removing tail outward-radial damping from the submitted v3 stack
costs less than the noise floor, the contribution is not real. If radial-from-step-zero performed
no worse than tail-only at equal budget, the "preserves the late catch-up" mechanism is wrong.

**Proof.** E09, E11.

**Evidence basis.** v3 leave-one-out: `noradial` is the second-worst ablation (`+0.00374`), and the
agent's stated reason is that removing it "destroys the tail catch-up rather than merely moving the
crossing later"; separately, radial-from-step-zero was ruled a kill because "under-2950 cannot
recover from a ~0.04 early loss."

**Sources.**
- `noradial` Δval `+0.00374` + mechanism ← `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json:56-58` «"label": "noradial" … "mean": 3.2821599999999997» (delta `0.0037431249999997362`); reason ← `v3/codex/scratchpad/THREAD.md:1186` «removing radial damping destroys the tail catch-up rather than merely moving the crossing later» [result]
- step-zero kill ← `v3/codex/scratchpad/THREAD.md:414` «Early ablation made radial-from-step-zero a kill … under-2950 cannot recover from a ~0.04 early loss» [result]

---

## C10 — A warm-start SOAP-skip sidecar is the single most load-bearing component of the v3 stack; the full SOAP recipe was not portable

**Statement.** Second-moment SOAP-basis preconditioning of the MLP (and attention-V) updates,
warm-started from the first gradient and *skipped* on step 0, is the largest single contributor to
the v3 stack — but only as a norm-matched sidecar behind the Muon/Soft update; the corresponding
*full* SOAP recipe (KL-SOAP-H) was not portable because the benchmark zero-initializes the
projection matrices, so a scale-invariant update tied to `‖W‖` leaves zero-norm projections frozen.

**Conditions.** Holds on the v3 public-PR backbone with `SOAP_PARAM_MODE=mlp_plus_v`. The
zero-init freeze is a property of this benchmark's initialization; the "sidecar, not replacement"
qualification is essential — all-params SOAP did not work.

**Status.** Supported (`nosoap` is the worst v3 ablation; the full KL-SOAP-H branch was killed as
non-portable).

**Falsification criteria.** If removing the SOAP sidecar from the submitted v3 stack costs less
than the noise floor, it is not load-bearing. If full KL-SOAP-H were made to converge on this
zero-init backbone without the warm-start-skip, the portability obstruction would be mischaracterized.

**Proof.** E09, E10, E11.

**Evidence basis.** v3 leave-one-out: `nosoap` is the largest ablation (`+0.00528`), with the
agent's reason "removing SOAP breaks the whole tail"; the full KL-SOAP-H recipe was killed as "not
portable as currently wired into this stack."

**Sources.**
- `nosoap` Δval `+0.00528` ← `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json:65-67` «"label": "nosoap" … "mean": 3.2836999999999996» (delta `0.005283124999999611`); reason ← `v3/codex/scratchpad/THREAD.md:1192` «removing SOAP breaks the whole tail» [result]
- full recipe not portable ← `v3/codex/scratchpad/THREAD.md:424` «PR #290's full KL-SOAP-H recipe is not portable as currently wired into this stack» [result]

---

## C11 — Two substitute "sphere" mechanisms: the lookahead pull is removable given the radial gate, but removing both loses the boundary

**Statement.** When two mechanisms shape the same tail geometry (here a tangent-sphere radial gate
and a sphere-lookahead pull), they act as substitutes rather than complements: keeping one lets the
other be pruned with no loss (and a slight simplification), but removing both together loses the
result — so the canonical pruning move is to drop exactly one, not to greedily drop every
"redundant-looking" component.

**Conditions.** Established in the v3 W258 leave-one-out round; the submitted "nosphere" recipe
removes the sphere-lookahead pull while keeping the tangent-sphere radial gate. The substitution is
specific to this pair on this backbone; it is the reason the submitted recipe is simpler than its
W258 parent.

**Status.** Supported (`nosphere` is the only positive-score leave-one-out and was submitted;
`nosphere_notangent` was demoted).

**Falsification criteria.** If the combined removal `nosphere_notangent` had preserved the 2940/2949
boundary within noise, the two mechanisms would be redundant (not substitutes) and both should be
dropped. If `nosphere` alone had cost more than noise, the pull would not be removable.

**Proof.** E11.

**Evidence basis.** `nosphere` reached statistical viability and "is the only leave-one-out that
both simplifies the stack and preserves the 2940 statistical boundary"; the combined removal
`nosphere_notangent` "closed at N=12 and is clearly worse," with the final rule "the two sphere
removals do not compose."

**Sources.**
- nosphere is the only simplifying+preserving prune ← `v3/codex/scratchpad/THREAD.md:1200` «this is the only leave-one-out that both simplifies the stack and preserves the 2940 statistical boundary» [result]
- non-composition ← `v3/codex/scratchpad/THREAD.md:1206` «keep the tangent-sphere radial gate if sphere-lookahead pull is removed; the canonical prune from this round is `nosphere` only … the two sphere removals do not compose» [result]
- pruning summary ← `v3/codex/scratchpad/w258_2940_leave_one_out_pruning_20260513.md:14` «Do not combine the two sphere removals. `nosphere_notangent` loses the 2940 boundary» [result]

**Dependencies.** C07 (this is the pruning discipline applied to a specific substitute pair).

---

## C12 — Under hard isolation and a tightened novelty bar, an already-saturated optimizer track yields no promotable submission (negative result)

**Statement.** When the only surfaces that move a near-saturated speedrun metric (schedule and
optimizer+schedule combinations) are ruled out as non-novel, the genuinely-new mechanisms that
remain — function-preserving init rescales and "non-additive" optimizer couplings — systematically
fail to produce a reproducible gain: many such couplings reduce to mechanisms already in the Muon
literature or, built from the *exact* polar factor (UᵀU = I), are algebraic no-ops, and the few
that run produce only single-seed or sub-noise-floor effects. Novelty-as-a-constraint, on a
saturated track, predicts a negative result.

**Conditions.** Established in the hard-isolated novelty wave (forbidden from inspecting other
worktrees; novelty bar tightened three times to exclude schedule/optimizer+schedule and then
merely-additive couplings). The claim is about this regime — a track where Muon is already at the
noise floor — not a statement that novel optimizers can never help.

**Status.** Supported as a negative result (the wave produced no promotable submission; its best
robust outcome was a reproduced one-bin gain explicitly below the noise floor). Recorded in the
isolated subtree [novelty/novelty.md](novelty/novelty.md).

**Falsification criteria.** If a later run under the same novelty bar produced a reproducible,
significance-passing sub-frontier submission from a genuinely novel optimizer/init mechanism, the
"saturated track + novelty constraint ⇒ no promotable result" claim would be refuted. If the
"algebraic no-op" diagnoses were shown to be wrong (the signals are non-zero in practice), the
mechanism for the failures would be mischaracterized.

**Proof.** E12.

**Evidence basis.** The best robust novelty-wave result was a reproduced crossing one 25-step grid
bin below baseline, which the agent itself flags as "below the required 2x step noise floor"; the
novelty bar explicitly excluded schedule and optimizer+schedule combinations; and representative
new couplings were diagnosed as exact-polar no-ops ("for exact polar `U`, input-column norms
satisfy `‖U[:,j]‖² = 1`").

**Sources.**
- sub-noise-floor best ← `novelty/codex/scratchpad/THREAD.md:579` «`3.27960` crossing at 3475. This is only a 25-step grid improvement from 3500, below the … required 2x step noise floor» [result]
- novelty bar excludes the metric-moving surfaces ← `novelty/codex/scratchpad/THREAD.md:248-250` «optimizer+schedule and schedule-only combinations do not count as novel … Optimizer-level combinations can count only when one optimizer mechanism's output materially shapes another mechanism's behavior» [input]
- exact-polar no-op ← `novelty/codex/scratchpad/THREAD.md:1214` «the proposed signal is identically zero: for exact polar `U`, input-column norms satisfy `‖U[:,j]‖² = 1`» [result]

**Dependencies.** C05 (the same seed-fragility that makes single crossings untrustworthy here).
