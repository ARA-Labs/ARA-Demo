# Claims

Each claim is a **takeaway** — the mechanism or relationship a result reveals — bound by an explicit
`Conditions` regime and a substantive `Falsification criteria`. Run IDs, bins, and scores live in
`Evidence basis` / `Proof` / `Sources`, never in the `Statement`. `Proof` references experiment IDs
in [experiments.md](experiments.md); numbers are grounded in [evidence/](../evidence/) and in the
source files cited under `**Sources**`.

Provenance tags: `ai-executed` (the agent ran it), `user-revised` (a human flag/decision changed it).

---

## C01 — Decoupling the training horizon from the LR-schedule horizon crosses the target without compressing the cooldown

**Statement:** On this benchmark, forcing the *final validation step* earlier than the
*LR-decay horizon* (running with `train_steps < schedule_steps`) reaches the loss target at a lower
step than a schedule whose decay is itself compressed to that step — because the late cooldown, not
the nominal endpoint, is where the target-crossing margin is bought. "Horizon ≠ stop" is therefore a
free step-count lever rather than a curve-shortening trade-off, and it underlies every promoted v1/v2
recipe.

**Conditions:** Muon-family optimizers on `track_3_optimization` (fixed 124M GPT, FineWeb). Holds in
the regime where the uncompressed schedule already approaches the target near its end; untested as a
universal property of arbitrary optimizers or far-from-target schedules. A too-early forced stop
(compressing past the cooldown's useful tail) misses — the lever has a lower bound per seed.

**Status:** Supported (foundational; reused across v1 and v2). Provenance: ai-executed.

**Falsification criteria:** Find a setting where, holding the optimizer fixed, a matched-`schedule_steps`
run validated at step *s* fails to beat a run whose schedule is compressed to *s* — i.e. the decoupling
gives no advantage — or where decoupling never produces a crossing the compressed schedule misses.

**Proof:** E01.

**Evidence basis:** The first improvement over the 3500 baseline was a horizon-3500 / stop-3450 run;
the lever recurred in every later promoted recipe (`schedule_steps > train_steps`). Canonical Muon was
3.28106 at step 3375 yet 3.27658 at 3500 under the 3500-step schedule, so a forced early validation can
cross without recompiling the decay.

**Sources:**
- mechanism rationale ← `v1/codex/scratchpad/THREAD.md:140-143` «It sets `train_steps=3450` but keeps a separate `schedule_steps=3500` for LR decay progress. Rationale: canonical Muon with the 3500-step schedule was `3.28106` at step 3375 and `3.27658` at 3500, so a forced final validation at 3450 may already beat the target without compressing cooldown.» [input]
- baseline 3.27658 @ 3500 ← `data/runs_self_contained/runs.csv:2` (baseline-muon-3500-seed0 row, `final_val_loss=3.27658`, `step_to_3_28=3500`) [result]

---

## C02 — Tail-EMA evaluation is the single strongest endpoint-smoothing lever in the v1 stack

**Statement:** Validating on an exponential moving average of the late-training weights (swapping in
the averaged weights for evaluation only, then restoring the online weights) lowers the achieved
validation loss enough to convert near-misses into target crossings, and contributes more to the v1
record than any other stack component. A slower average (β=0.99) beats a faster one (β=0.995); naive
fixed-window SWA and EMA-extrapolated evaluation are worse. The benefit is an evaluation-time variance
reduction, not a training-dynamics change.

**Conditions:** Late-training regime (EMA start ≈ steps 2000–2500) on the v1 Muon/NorMuon stack. The
gain is real but seed-fragile below the practical stop floor; it does not by itself make aggressive low
stops seed-stable.

**Status:** Supported. Provenance: ai-executed.

**Falsification criteria:** A leave-one-out that removes tail-EMA evaluation but holds the rest of the
v1 stack fixed should *not* be the largest single degrader at the pruning step, or β=0.995 should match
β=0.99 — either refutes the claim.

**Proof:** E04, E06.

**Evidence basis:** In the v1 component-pruning sweep, removing tail-EMA evaluation is the single worst
ablation (largest positive delta on val loss). See [evidence/figures/v1_pruning.png](../evidence/figures/v1_pruning.png)
and [evidence/tables/v1_component_pruning.md](../evidence/tables/v1_component_pruning.md).

**Sources:**
- noTailEMA is the top contributor, delta +0.00251 ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:111-117` «"delta": 0.0025100000000000122, "label": "noTailEMA", "mean": 3.28158, "n": 8» [result]
- next-largest noMuon2f +0.00229 (for ordering) ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:103-109` «"delta": 0.0022899999999999032, "label": "noMuon2f"» [result]
- β=0.99 beats β=0.995 ← `v1/codex/scratchpad/THREAD.md:1894` «`ema099s2500-h3375-stop3200` seed0 completed stronger than the `.995` seed0 cell (`3200 / 3.27953`, with `3125=3.28270`). Because this is a real hit and the best seed0 EMA beta so far» [result]

---

## C03 — Factorized (2-factor) preconditioning helps the hidden weight matrices specifically, not attention or mlp.proj

**Statement:** A factorized / two-factor preconditioner on the Muon update ("Muon2F") improves the
target step when applied to the **hidden** (non-`mlp.proj`) weight matrices, but is neutral-to-negative
when applied to attention-only, mlp-only, or all partitions (APOLLO-style). The benefit is specific to
the geometry of the hidden 2D weights; preconditioning is not a uniform good across parameter roles.

**Conditions:** v1 stack with split hidden optimizers; `pre_eps≈1e-3`. The hidden/attention/mlp.proj
role split is the relevant partition; untested outside this parameterization.

**Status:** Supported (it is the #2 contributor to the v1 record). Provenance: ai-executed.

**Falsification criteria:** An attention-only or all-partition factorized preconditioner that matches
the hidden-only variant's contribution at the pruning step would refute the role-specificity.

**Proof:** E03, E06.

**Evidence basis:** Hidden-only Muon2F reproduced a 3-seed target hit where attention-only/MLP-only
variants were neutral or negative; removing it (`noMuon2f`) is the second-largest v1 pruning delta.

**Sources:**
- noMuon2f delta +0.00229 ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:103-109` «"delta": 0.0022899999999999032, "label": "noMuon2f", "mean": 3.28136» [result]
- hidden-only is the live positive signal ← `v1/codex/scratchpad/THREAD.md:1456` «Stack-level Muon2F hidden-only on the actual Adam-mini + tailresrmsstack + hidden-AggMo parent is now the only live positive signal.» [result]

---

## C04 — Role-specific Muon LR/WD plus Muon lookahead move the *crossing step* earlier where horizon-shortening alone stalls

**Statement:** Once a stack saturates on train-step shortening, the levers that continue to pull the
target-crossing step earlier are (a) splitting the Muon learning rate and weight decay by parameter
role (q/k vs v vs attn.proj vs mlp.fc vs mlp.proj) and (b) a late-training Muon lookahead (interpolating
toward a slow weight copy). These act on the *trajectory's crossing point*, not merely the endpoint loss,
so they compound with horizon≠stop rather than substituting for it.

**Conditions:** v2 "legal" stack at the ~2960–3037 frontier; role partition and lookahead start ≈ step
2450. The single-seed crossings these enable are not themselves records (see C06/C11).

**Status:** Supported. Provenance: ai-executed.

**Falsification criteria:** A v2 leave-one-out where removing role-LR (`noRoleLR`) or lookahead
(`noLookahead`) does *not* worsen the target-step margin would refute their role.

**Proof:** E10, E12.

**Evidence basis:** In the v2 pruning sweep, role-specific LR is a large contributor and lookahead a
moderate one; the role-WD + role-LR2 + lookahead stack is what carried the frontier from a ~2982 to a
~2962 single-seed crossing before the statistical gate fixed the submitted bin at 3037.

**Sources:**
- noRoleLR delta +0.00292 ← `record_configs/20260515_codex_v2_legal_3037/pruning_data.json:71-77` «"delta": 0.0029200000000000337, "label": "noRoleLR", "mean": 3.28177» [result]
- noLookahead delta +0.00117 ← `record_configs/20260515_codex_v2_legal_3037/pruning_data.json:63-69` «"delta": 0.0011700000000001154, "label": "noLookahead", "mean": 3.28002» [result]
- role-LR/WD/lookahead recipe ← `record_configs/20260515_codex_v2_legal_3037/README.md:7-11` «Role-specific Muon LR multipliers: q/k `0.61875`, v `0.625` … Muon lookahead from step 2450, interval 25, alpha 0.35, pull 0.15» [input]

---

## C05 — The fixed-architecture rule binds the forward path; an inherited "v12" precision change was illegal and materially helped, so it was quarantined

**Statement:** "Fixed architecture" binds not only layer shapes but the *numerical forward path*: a
mathematically-near-equivalent rewrite of `RMSNorm.forward` / attention q-k normalization is a
precision/behavior change and is invalid for this track. Such a change is not cosmetic — it materially
improved sub-3000 behavior — so a frontier built on it is not a valid record and must be rebuilt on a
byte-identical-compliant base. Compliance has a real, measurable step cost; honest records pay it.

**Conditions:** v2, where the inherited cross-agent "v12" parent carried
`RMSNorm.forward = (norm(x.float()) * self.gains).type_as(x)` and routed q/k through the same helper,
instead of the baseline `F.rms_norm(x, (x.size(-1),), weight=self.gains.type_as(x))`. The user flagged
it; every v12-derived result was quarantined.

**Status:** Refuted-as-submittable / quarantined (the v12-derived sub-3000 frontier is **non-compliant**
and is recorded only as journey, not as a record). Provenance: user-revised.

**Falsification criteria:** Show the flagged forward-path rewrite is bit-identical to the baseline (no
precision change), or that a byte-identical-compliant rebuild matches the v12-derived sub-3000 frontier
step-for-step — either would mean compliance had no cost and the quarantine was unnecessary.

**Proof:** E09.

**Evidence basis:** The legal rebuild (`legal_v12opt`, byte-identical Architecture diff) reached the
target but the agent recorded that "the invalid forward-path change materially helped the sub-3000
behavior"; the submittable frontier (C04, bin 3037) is rebuilt on the compliant base. The
non-compliant config is preserved as a quarantined artifact, not a result.

**Sources:**
- the flagged violation ← `v2/codex/scratchpad/THREAD.md:126` «every v12-derived codex variant inherited `RMSNorm.forward` as `(norm(x.float()) * self.gains).type_as(x)` instead of the workspace baseline `F.rms_norm(x, (x.size(-1),), weight=self.gains.type_as(x))` … This is a precision/behavior change in the forward path and is invalid for this track even if mathematically close.» [input]
- quarantine action ← `v2/codex/scratchpad/THREAD.md:128` «all v12-derived `v2cx` results are now quarantined and must not be reported as valid frontier improvements.» [input]
- legal rebuild byte-identical ← `v2/codex/scratchpad/THREAD.md:132` «Verified the entire Architecture section diff against baseline is empty and the norm lines are identical … The diff is limited to Optimizer plus Init & Optim Hyperparams.» [input]

---

## C06 — A record is a statistic: `(3.28 − μ)·√n ≥ 0.004` over a fixed-step cohort, not a single low crossing

**Statement:** The operative definition of a passing record is a fixed-step N-seed cohort whose mean
clears the z-margin `(3.28 − μ)·√n ≥ 0.004`, not the lowest step at which any single seed crosses 3.28.
Consequently a *lower* single-seed bin is rejected when its cohort mean fails the test, and trading a
small number of extra steps for a tighter, higher-confidence mean is the correct submission. The bin
that gets submitted is the earliest common validation checkpoint whose cohort passes — chosen to avoid
validation-spam p-hacking.

**Conditions:** Track-3 threshold with σ=0.0013; cohorts of distinct `--seed N` runs. Holds wherever
per-seed variance (~50 steps) is comparable to the contested step gain.

**Status:** Supported (it determined every submitted bin: v1=3205, v2=3037, v3=2949). Provenance:
user-revised (the gate is a user-imposed rule) + ai-executed.

**Falsification criteria:** A submitted record that passed on a single-seed crossing without a
cohort-mean z-margin, or a case where a lower-mean cohort was rejected in favor of a luckier single
seed, would refute the claim that the statistic governs.

**Proof:** E07, E11.

**Evidence basis:** In v1, a 3-seed `s3170` crossing was **rejected** (negative cohort score) while a
+25-step `s3220` / the submitted 3205 cohort passed. In v2, every low-step single-seed frontier
(ts2962…ts2982) failed the z-test, and only the +75-step `ts3037` fixed cohort passed, with step 3025
explicitly failing the same-checkpoint scan.

**Sources:**
- v1 s3170 rejected, s3220 chosen ← `v1/codex/scratchpad/THREAD.md:2232` «Rejected: `v12iso-musched-h3375-s3170` `n=15`, `mu=3.280266`, negative score. User suggested +25 steps; `s3220` worked and is the cleaner v12 claim.» [result]
- v2 low-step families fail; only ts3037 passes ← `v2/codex/scratchpad/THREAD.md:810` «mean 3.2783775; score `(3.28 - mu) * sqrt(8) = 0.004589`, equivalent z = 3.53 … final step 3037 is the earliest common validation checkpoint that passes.» [result]
- the gate definition ← `record_configs/20260515_codex_v2_legal_3037/README.md:19-26` «(3.28 - mu) * sqrt(n) = 0.00588000 … with `sigma=0.0013`, this is `z = 4.5231`, one-sided `p = 3.05e-06`, satisfying `p < 0.001`.» [result]

---

## C07 — Breaking the optimizer-only ~3000-step floor requires a stronger *parent*, then compressing by shifting phase endpoints, not truncating the horizon

**Statement:** The empirical ~3000-step floor is a property of the *local optimizer-only mechanism
class*, not of the benchmark. It is broken not by another optimizer knob but by reproducing a stronger
**parent** (the public Soft-Muon + outward-radial + SOAP frontier) faithfully and then compressing it by
moving the schedule/Soft/radial *phase endpoints* earlier while *keeping the long cooldown horizon*.
Hard-truncating the whole schedule to the target step is consistently cold; preserving the back-loaded
cooldown and re-phasing is what yields a viable sub-2950 crossing.

**Conditions:** v3, building on a faithfully-reproduced public PR #294/#291 parent (horizon ≈3020–3025).
The compression target was a statistically-viable 2940–2950 bin.

**Status:** Supported. Provenance: ai-executed + user-revised (the public-frontier pivot was a user
hand-off).

**Falsification criteria:** Reaching a statistically-viable sub-2950 bin by *hard-truncating* the
schedule horizon (without a stronger parent), or showing the local optimizer-only family can be pushed
below ~3000 with a clean cohort, would refute the floor-is-parent-bound claim.

**Proof:** E13, E14, E15.

**Evidence basis:** The Aurora local sub-line repeatedly recentered near 3.280 at 2999 and never passed;
after the public-frontier pivot, faithful v48/PR#294 reproduction plus phase-endpoint compression
reached the viable 2940-boundary parents (Worker70→W211→W258), whereas every hard-horizon-2900 attempt
(W198–W200) was cold.

**Sources:**
- the ~3000 floor (prior-iteration) ← `v2/codex/goal.md:17-19` «The prior iteration hit an empirical ts=3000 floor with optimizer-only mechanisms — Newton-Muon, Tail-EMA, AdamMini, Skylight, cubic Contra, and many others all came in at parity or worse.» [input]
- the public-frontier pivot + reproduce-then-compress ← `v3/codex/goal.md:57-61` «reproduce the proven PR #294/v48 parent faithfully under the codex architecture guard, then compress that parent below 2950 rather than spending more capacity on mechanisms that have repeatedly centered around 3.282 at 2949» [input]
- keep horizon, move endpoints (not truncate) ← `v3/codex/scratchpad/THREAD.md:1087` «do not hard-compress the whole schedule to 2900; W198-W200 were cold, while W211 improved the boundary by keeping a 3025 LR horizon and aligning the Soft/radial tail.» [result]

---

## C08 — Outward-radial dampening and SOAP preconditioning are the load-bearing components of the v3 stack

**Statement:** Within the v3 "nosphere" stack, the two components whose removal most degrades the
target-step margin are the SOAP preconditioner (extended to MLP+V) and the outward-radial update
dampening; Soft-Muon scheduling and Contra are the next tier. The radial brake works specifically as a
*tail* correction (radial-from-step-0 is harmful), and SOAP is the single most load-bearing block. These
are reproduced public-PR mechanisms, not Codex inventions (see related_work).

**Conditions:** v3 W258 leave-one-out sweep at step 2949, N up to 16. "Radial dampening" = PR #294
outward-component scaling + post-step radius correction; "SOAP" = PR #278 machinery extended to MLP+V.

**Status:** Supported. Provenance: ai-executed (reproduction), external sources for the mechanisms.

**Falsification criteria:** A leave-one-out in which removing SOAP or radial dampening does *not* rank
among the largest degraders — or in which radial-from-step-0 is not harmful — would refute the
load-bearing/tail-specific claims.

**Proof:** E14, E16.

**Evidence basis:** In the W258 leave-one-out, `nosoap` is the worst ablation and `noradial` the
second-worst; see [evidence/figures/v3_pruning.png](../evidence/figures/v3_pruning.png) and
[evidence/tables/v3_component_pruning.md](../evidence/tables/v3_component_pruning.md).

**Sources:**
- nosoap is worst, delta +0.00528 ← `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json:64-69` «"delta": 0.005283124999999611, "label": "nosoap", "mean": 3.2836999999999996» [result]
- noradial second, delta +0.00374 ← `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json:56-62` «"delta": 0.0037431249999997362, "label": "noradial", "mean": 3.2821599999999997» [result]
- components are reproduced public PRs ← `data/.../10389-…-nosphere-…/launched_script.py:13-31` «This submission incorporates features from the following previous submissions @nilin PR291 … @samacqua: PR278 / MLP SOAP preconditioning … @yash-oai: PR287 / power law LR schedule» [input]

---

## C09 — Leave-one-out pruning before submission reveals redundant modifiers, but removals do not always compose

**Statement:** A converged stack accumulates modifiers that helped when added but stop pulling weight as
the stack changes; a mandatory pre-submission leave-one-out sweep is the removal mechanism. In v3 it
found the **sphere-lookahead pull** redundant once LACV and the tangent-sphere gate were present (the
"nosphere" simplification), tying/slightly simplifying the boundary. Crucially, individually-removable
modifiers are not jointly removable: dropping both sphere terms together loses the boundary — pruning
must check interactions, not just single deletions.

**Conditions:** v3 W258 sweep at step 2949; the redundancy is conditional on LACV + LACV-floor +
tangent-sphere already being in the stack. A modifier is dropped only on a 2-seed mean inside ±0.5× the
noise floor (the lawful-core pruning rule).

**Status:** Supported. Provenance: ai-executed.

**Falsification criteria:** Show that removing the sphere-lookahead pull worsens the cohort margin
beyond the pruning tolerance, or that removing both sphere terms together preserves the 2940 boundary —
either refutes the redundancy / non-composition finding.

**Proof:** E16 (and the analogous v1/v2 pruning rounds E06/E12).

**Evidence basis:** `nosphere` confirmed statistically viable at N=16; the combined `nosphere_notangent`
removal was demoted at N=12 (clearly worse), so the canonical prune is `nosphere` only.

**Sources:**
- nosphere viable at N=16 ← `v3/codex/scratchpad/THREAD.md:1202` «Nosphere confirmed at N=16: step2940 mean=3.278848 score=+0.004608 … step2949 score=+0.006332.» [result]
- removals don't compose ← `v3/codex/scratchpad/THREAD.md:1206` «Combined `nosphere_notangent` closed at N=12 and is clearly worse … the canonical prune from this round is `nosphere` only … the two sphere removals do not compose.» [result]
- the pruning rule ← `v1/codex/AGENTS.md:26-28` «A modifier is dropped only on a 2-seed mean inside ±0.5× the noise floor (single-seed pruning is itself overfitting).» [input]

---

## C10 — Under Muon's exact polar map, most genuinely-novel pre-polar mechanisms are inert or collapse to a scalar blend

**Statement:** The novelty-constrained search space is structurally near-empty: a pre-polar perturbation
built from the polar factor U that preserves singular vectors satisfies `polar(Z)=polar(M)`, and for the
square q/k/v and tall mlp.fc targets `UᵀU = I` makes off-diagonal commutator/metric tensors identically
zero — so the mechanism is a no-op. Mechanisms that finite-difference or blend the polar update instead
collapse to a scalar Nesterov/de-Nesterov coefficient (non-novel plumbing). The genuinely-novel survivors
are exactly the mechanisms that cannot matter; the mechanisms that would matter are already published.

**Conditions:** Muon polar-update optimizers on this benchmark, under the wave's compound constraint
(init/optimizer-only, materially non-additive, not-on-arXiv). The "no-op" algebra is exact for
square/tall targets under the exact polar; approximate Newton-Schulz inherits it to first order.

**Status:** Supported — terminal negative result (no promotable novelty submission). Provenance:
ai-executed.

**Falsification criteria:** Exhibit a not-on-arXiv pre-polar Muon mechanism that (a) is not algebraically
a no-op or a scalar Nesterov blend and (b) produces a reproducible, above-noise-floor step improvement —
that would refute the structural-emptiness claim.

**Proof:** E08.

**Evidence basis:** Dozens of novel derivations were implemented and run; the best (VFG) reproduced only
a 25-step grid crossing (below the 2× noise floor), three genuine 3375-crossings failed seed
reproduction, and the search tail collapsed into successive algebraic no-op proofs (CPD, GLC, NMA, DPF,
MNL, JSP, …).

**Sources:**
- the exact-polar no-op law ← `novelty/codex/scratchpad/THREAD.md:1212-1216` «for exact polar `U`, input-column norms satisfy `||U[:,j]||^2 = 1`, so the q/k/v-vs-fc column-energy imbalance collapses to ordinary Muon plus decoupled WD. No run.» [result]
- best survivor below noise floor ← `novelty/codex/scratchpad/THREAD.md:577-580` «`vfg001_gain080_lr026_t3475_seed1234` completed at `3.27962`, matching the default-seed `3.27960` crossing at 3475. This is only a 25-step grid improvement from 3500, below the required 2x step noise floor.» [result]
- the novelty constraint itself ← `novelty/codex/goal.md:9-14` «every submitted recipe must contain at least one idea that has not been published on arXiv … Porting a published method and tuning its HPs is a normal speedrun and fails this mission.» [input]

---

## C11 — Single-seed low-step crossings are predominantly low-tail singletons, not robust families

**Statement:** On this high-variance benchmark, a single-seed crossing at a low step is overwhelmingly a
favorable-noise singleton rather than evidence of a robust family: the same recipe's cohort mean sits well
above the threshold, and the limiting seed (frequently "seed 2") fails brackets the lucky seed clears.
The correct response to a single-seed win is a second seed of the *same* recipe, never a new modifier
stacked on top of it.

**Conditions:** `track_3_optimization` with ~50-step / ~0.001-loss seed variance; pervasive across all
four waves.

**Status:** Supported. Provenance: ai-executed + user-revised (codified in the lawful core).

**Falsification criteria:** A regime where single-seed low-step crossings reliably reproduce at the same
step on independent seeds (cohort mean tracks the lucky seed) would refute the singleton claim.

**Proof:** E07, E11, E16.

**Evidence basis:** v2's entire low-step frontier (ts2962…ts2982) collapsed under the cohort z-test;
v1's `s3170` 3-seed crossing was rejected; v3 brackets repeatedly hit at one seed and missed the limiting
seed. The lawful core encodes this as the noise-floor gate and two-seed reproduction.

**Sources:**
- low-step cohorts collapse ← `v2/codex/scratchpad/THREAD.md:802` «`ts2962` n=38 mean 3.28243 score -0.01496, `ts2963` n=22 mean 3.28248 score -0.01163, `ts2970` n=21 mean 3.28158 score -0.00724, and `ts2982` n=17 mean 3.28131 score -0.00539» [result]
- the gate / noise floor ← `v1/codex/AGENTS.md:160-167` «Noise-floor estimates … `step_to_target` ≈ 50 steps … Single-seed wins are ideas worth reproducing — the next launch is a 2nd seed of the same recipe, not a new modifier.» [input]

---

## C12 — Compliance, reproduction, and noise-floor discipline are what make an autonomous result survive review

**Statement:** Across the experiment, the difference between a *reported* win and a *defensible* record is
process, not cleverness: a two-seed reproduction requirement, a 2× noise-floor gate, a stuck detector, a
≤3-modifier slug cap, a mandatory pruning round, and a forward-path compliance audit each *removed*
candidate "wins" that would otherwise have been submitted (the v12 quarantine, the s3170 rejection, the
v2 low-step collapse, the nosphere/anti-composition pruning). The lawful core is therefore load-bearing on
the *output*, not merely hygiene.

**Conditions:** Autonomous multi-wave optimizer search under the AGENTS.md lawful core. The specific
thresholds (2 seeds, 2× floor, 30-run stuck, ≤3 modifiers) are this experiment's settings.

**Status:** Supported (meta-claim; corroborated by every wave's terminal decision). Provenance:
user-revised (rules) + ai-executed (application).

**Falsification criteria:** Show that dropping the gates would not have changed any submitted record —
i.e. the quarantined / rejected / collapsed candidates would all have passed a rigorous external review
anyway — and the process is merely cosmetic.

**Proof:** E07, E09, E11, E16.

**Evidence basis:** Each gate has at least one decisive intervention on the record: the compliance audit
(C05), the statistical gate (C06), the seed-singleton discipline (C11), and the pruning round (C09).

**Sources:**
- the lawful core ← `v1/codex/AGENTS.md:11-28` «These six rules are always law. A run, candidate, or claim that violates one is invalid regardless of what else it achieved … Pruning before submission — a pre-submission pruning round is mandatory.» [input]
