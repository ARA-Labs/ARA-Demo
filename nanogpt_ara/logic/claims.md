# Claims

Each claim states the reusable mechanism/relationship a result reveals. Numbers live in
`Evidence basis` / `Proof` (the evidence layer), not in the Statement. `Sources` entries ground
load-bearing numbers in files opened and confirmed during compilation.

---

## C01 — Decoupling the LR-schedule horizon from the training stop step buys earlier crossings

**Statement.** On this benchmark, holding the learning-rate decay denominator ("horizon") larger
than the step at which training stops ("stop") — rather than compressing the whole cooldown into a
shorter run — lets a Muon-family run reach the target loss at a lower step than a run whose schedule
is compressed to that stop. The schedule shape near the end, not just the total step budget,
controls where the target is first crossed.

**Conditions.** Muon-family optimizer on the fixed nanoGPT, target `val_loss <= 3.28`; demonstrated
across the 3375–3450 stop region in v1's open search. Untested boundary: very aggressive
compression (e.g. `horizon == stop` at much lower steps) closes the gain; the relationship is a
local lever, not a monotone law to arbitrarily low steps.

**Status.** Supported (multi-seed, single wave).

**Falsification criteria.** If, on this setup, runs with `horizon == stop` cross `val_loss <= 3.28`
at the same or lower step as horizon>stop runs at matched compute, the lever is illusory.

**Evidence basis.** The first reproduced v1 improvement over the 3500 baseline came from
`horizon3500-stop3450` (two seeds crossing below the target), and the descent to lower stops each
required a colder horizon.

**Proof.** E01.

---

## C02 — Row-normalizing the orthogonalized Muon update (NorMuon), at colder momentum and higher LR, lowers steps-to-target

**Statement.** Dividing each row of Muon's Newton-Schulz-orthogonalized update by an EMA of its
squared norm and re-RMS-matching to Muon's canonical update scale (NorMuon), combined with a colder
preconditioner momentum (`beta2 ≈ 0.90` rather than `0.95`) and a higher Muon LR (~0.030 vs 0.025),
reaches the target at fewer steps than canonical Muon — the row-wise second-moment normalization is
the active ingredient, not the LR change alone.

**Conditions.** Fixed nanoGPT, Muon family, v1 open-search regime around the 3350–3450 bins.
Untested boundary: interaction with the later full v12iso stack is captured separately by the
leave-one-out pruning (C03), where NorMuon's marginal contribution is folded into the 2-factor /
schedule components.

**Status.** Supported (multi-seed).

**Falsification criteria.** If a matched canonical-Muon run at the same higher LR and colder beta2,
*without* the row normalization, crosses at the same step, NorMuon adds nothing beyond its HPs.

**Evidence basis.** v1 found `beta2=0.90` ahead of `0.95`, and Muon LR `0.030` a clear positive,
together enabling the 3450→3350 descent.

**Proof.** E02.

---

## C03 — In the v1 "v12iso" stack, a late tail-EMA evaluation shadow and 2-factor preconditioning are load-bearing; the tail residual mechanics are near-noise

**Statement.** When a deep optimizer stack is built by accretion, leave-one-out pruning separates
load-bearing mechanisms from decorative ones: for v12iso, removing the late full-model EMA
evaluation shadow or the 2-factor (row/column) preconditioning each costs roughly an order of
magnitude more validation loss than removing any single tail-residual mechanism (residual pulse,
momentum refresh, beta2 thaw, late-LR), several of which are individually within noise. The
reusable lesson is that endgame evaluation averaging and gradient preconditioning carry the stack,
while the late residual-shaping tricks are tuning, not structure.

**Conditions.** v12iso stack at the 3195-step pruning screen, n=8 per ablation. Untested boundary:
the tail mechanics may interact super-additively in combinations not individually ablated; the
pruning is one-at-a-time.

**Status.** Supported (n=8 leave-one-out).

**Falsification criteria.** If a re-run of the pruning sweep at matched seeds shows a tail-residual
mechanism with a removal delta comparable to `noTailEMA`/`noMuon2f`, or shows those two as
near-noise, the load-bearing/decorative split is wrong.

**Evidence basis.** Removal deltas (val_loss when removed, positive = component helped): `noTailEMA`
+0.00251, `noMuon2f` +0.00229 — the only two beyond the ~0.001 noise band; vs `noResPulse`
−0.00007, `noMomRefresh` −0.00004, `noBeta2Thaw` −0.00001, `noLateLR` +0.00002.

**Sources.**
- `noTailEMA` removal delta +0.00251 ← `src/configs/v1_pruning_data.json` «"delta": 0.0025100000000000122, "label": "noTailEMA"» [result]
- `noMuon2f` removal delta +0.00229 ← `src/configs/v1_pruning_data.json` «"delta": 0.0022899999999999032, "label": "noMuon2f"» [result]
- `noResPulse` removal delta −0.00007 ← `src/configs/v1_pruning_data.json` «"delta": -7.00000000000145e-05, "label": "noResPulse"» [result]

**Proof.** E03.

---

## C04 — Splitting Muon LR and weight decay by parameter role, plus a row-normalized update and a Muon lookahead, beats body-uniform optimizer HPs

**Statement.** Replacing a single body-wide Muon learning rate and weight decay with **per-role**
values (distinct multipliers for q/k, v, attn.proj, mlp.fc, mlp.proj and role-specific weight decay)
on top of a row-normalized (MuonEq) update is the dominant lever of the v2 legal stack, and a Muon
lookahead (slow-weight pull) and the row-normalized update are the next strongest; uniform-HP
ablations cost the most. Parameter role, not a single global step size, is where the headroom is.

**Conditions.** v2 "legal_v12opt" stack at the 3037-step screen, n=8 per ablation; compliant
byte-identical architecture base. Untested boundary: the per-role values were hand-tuned around a
base LR 0.045 / base WD 0.030; the claim is that *role-splitting* helps, not that these exact
multipliers are optimal.

**Status.** Supported (n=8 leave-one-out).

**Falsification criteria.** If restoring a single body-wide LR and WD (the `noRoleLR` / `noRoleWD`
conditions) matches the role-split baseline at the same step and seeds, role-splitting is inert.

**Evidence basis.** Removal deltas at step 3037 (positive = helped): `noMuonEq` +0.00353,
`noRoleLR` +0.00292, `noMuSched` +0.00459 (n=3), `noLookahead` +0.00117, `noRoleWD` +0.00041 —
the role/update/schedule mechanisms dominate; `noContraMuon` +0.00008 is near-noise.

**Sources.**
- `noRoleLR` removal delta +0.00292 ← `src/configs/v2_pruning_data.json` «"delta": 0.0029200000000000337, "label": "noRoleLR"» [result]
- `noMuonEq` removal delta +0.00353 ← `src/configs/v2_pruning_data.json` «"delta": 0.003530000000000033, "label": "noMuonEq"» [result]
- `noLookahead` removal delta +0.00117 ← `src/configs/v2_pruning_data.json` «"delta": 0.0011700000000001154, "label": "noLookahead"» [result]

**Proof.** E04.

---

## C05 — A mathematically-equivalent rewrite of a normalization forward path is an architecture change under bf16 and invalidates derived results

**Statement.** Under a no-architecture-change rule with bf16 compute, even a numerically "close"
rewrite of a forward-path normalization (here `RMSNorm.forward` as `(norm(x.float()) * gains).type_as(x)`
in place of `F.rms_norm(x, ..., weight=gains.type_as(x))`, with attention q/k routed through the
same helper) changes precision behavior and therefore counts as a forward-path / architecture
change — any speedrun result built on it is non-compliant and must be quarantined, not reported.
Compliance must be enforced by **byte-identity of the architecture block**, not by judging
mathematical equivalence, because the disallowed change can be the thing that helped.

**Conditions.** This track's rules (architecture/data/batch fixed, one forward-backward per step),
bf16 forward path; surfaced when v2 inherited a cross-agent "v12" parent. The principle generalizes
to any precision-sensitive benchmark with a fixed-architecture contract; the specific lines are
RMSNorm/q-k-norm.

**Status.** Supported (research-integrity decision; user-flagged and acted on).

**Falsification criteria.** If, on this setup, the rewritten and the byte-identical forward paths
produce bitwise-equal logits across seeds (so no behavior could differ), the rewrite would not be an
architecture change. The agent's own note that the legal (byte-identical) stack was higher-variance
and slower to cross sub-3000 indicates the illegal path *did* materially affect behavior.

**Evidence basis.** The violation was caught and every v12-derived `v2cx` result quarantined; the
submittable frontier (C04) was rebuilt on a byte-identical base, costing frontier relative to the
quarantined sub-3000 single-seed crossings.

**Sources.**
- forward-path violation ← `../experiments-autonomous-speedrunning-codex/v2/codex/scratchpad/THREAD.md:126` «every v12-derived codex variant inherited `RMSNorm.forward` as `(norm(x.float()) * self.gains).type_as(x)` instead of the workspace baseline `F.rms_norm(...)` ... This is a precision/behavior change in the forward path and is invalid for this track even if mathematically close» [input]
- quarantine + byte-identical rebuild rule ← `../experiments-autonomous-speedrunning-codex/v2/codex/scratchpad/THREAD.md:128-130` «all v12-derived `v2cx` results are now quarantined ... preserve forward/norm code byte-for-byte; only Optimization and Init & Optim Hyperparams may change» [input]

**Proof.** E08.

---

## C06 — In the v3 public-PR stack, SOAP preconditioning and outward-radial dampening are load-bearing; a sphere-lookahead pull is redundant and prunable

**Statement.** When a frontier stack is assembled from reproduced public mechanisms, leave-one-out
pruning identifies both the indispensable and the redundant: for v3, removing MLP+V SOAP
preconditioning or the outward-radial update dampening collapses the tail (large positive removal
delta), whereas a sphere-lookahead **pull** can be removed with no significant loss — the simplified
"nosphere" stack holds the statistical boundary. Redundancy in an accreted public-PR stack is real
and discoverable; not every imported mechanism earns its place.

**Conditions.** v3 "nosphere" stack, W258 leave-one-out sweep at step 2949 (`train_steps=3020`,
`schedule_steps=3025`); ablation n ranges 3–16. Untested boundary: the two sphere removals do not
compose — removing the pull *and* the tangent-sphere radial term together regresses — so "prunable"
applies to the pull alone, with the tangent term retained.

**Status.** Supported (leave-one-out; nosphere confirmed at n=16).

**Falsification criteria.** If re-running the W258 sweep shows the sphere-lookahead pull removal with
a removal delta comparable to `nosoap`/`noradial`, or shows SOAP/radial as prunable, the
load-bearing/redundant split is wrong.

**Evidence basis.** Removal deltas at step 2949 (positive = helped): `nosoap` +0.00528,
`noradial` +0.00374, `novsoap` +0.00228, `nosoft` +0.00186, `nocontra` +0.00133 — all load-bearing;
the nosphere baseline (pull already removed) scores +0.006332 at n=16 and is the submitted stack,
while `nosphere-notangent` (both removed) regresses by +0.00070.

**Sources.**
- `nosoap` removal delta +0.00528 ← `src/configs/v3_pruning_data.json` «"delta": 0.005283124999999611, "label": "nosoap"» [result]
- `noradial` removal delta +0.00374 ← `src/configs/v3_pruning_data.json` «"delta": 0.0037431249999997362, "label": "noradial"» [result]
- nosphere baseline score +0.006332 at n=16 ← `src/configs/v3_pruning_data.json` «"label": "nosphere-baseline", "mean": 3.278416875, "n": 16, "score": 0.006332499999999186» [result]
- `nosphere-notangent` regression +0.00070 ← `src/configs/v3_pruning_data.json` «"delta": 0.0007014583333342372, "label": "nosphere-notangent"» [result]

**Proof.** E05.

---

## C07 — Under a hard novelty constraint, the productive directions are ruled non-novel and the novel ones collapse to algebraic no-ops

**Statement.** When every submitted recipe must contain an unpublished idea, the speedrun's
remaining headroom is largely inaccessible: schedule/LR/WD tuning and additive optimizer
combinations — the things that move the bin — are ruled non-novel "plumbing," and the genuinely
novel constructions (pre-polar perturbations built from Muon's orthogonalized factor) frequently
reduce to **algebraic no-ops**, because Muon's exact polar factor satisfies `U^T U = I`, so
disagreement/commutator terms built from it vanish identically. The combination yields a documented
negative result: many derivations, no promotable submission.

**Conditions.** Hard-isolated novelty wave on the same benchmark; ~40 ideas run, ~60 killed before
code under a two-gate (arXiv-novelty + benchmark-compliance) screen; "novel" required a mechanism
whose math does not reduce to a published method and whose interaction is non-additive. Untested
boundary: a different novelty bar (e.g. allowing novel *schedules*) or targets beyond Muon's polar
geometry might leave more headroom; this is the result under *this* bar.

**Status.** Supported (negative result; wave produced no promotable submission).

**Falsification criteria.** If a single novel derivation from this wave is shown to cross
`val_loss <= 3.28` at a step beyond the 2× noise-floor gate and to reproduce on a distinct seed,
the negative result is overturned.

**Evidence basis.** The best reproduced novel result was a 25-step gain (below the noise floor); the
most "interesting" optimizer ideas (e.g. GLC001) were killed pre-code as exact-polar no-ops.

**Sources.**
- exact-polar no-op kill ← `../experiments-autonomous-speedrunning-codex/novelty/codex/scratchpad/THREAD.md:1853-1855` «exact Muon polar has `U^T U = I` ... so `C = offdiag((U^T U)D - D(U^T U)) = 0` and `Z=N`» [input]
- no promotable submission / 25-step best ← `../experiments-autonomous-speedrunning-codex/novelty/codex/plan.md:13-15` [pending: plan.md:13-15 quote not re-opened verbatim this turn — narrative confirmed by extraction]

**Proof.** E06.

---

## C08 — A fixed-step seed-cohort significance gate makes the submitted bin conservative relative to the single-seed frontier

**Statement.** Requiring a submission to pass `(3.28 - mean)*sqrt(n) >= 0.004` over a **fixed-step
cohort of distinct seeds** — rather than accepting the lowest-step single-seed crossing —
systematically pushes the reportable bin above the single-seed frontier, because single-seed
sub-step crossings do not survive cohort averaging. The gap between the agent's single-seed frontier
and its submitted bin is the cost of statistical honesty, and it is large (tens of steps per wave).

**Conditions.** All three submitted waves used n=16 non-cherry-picked seeds (0..15) with
`sigma = 0.0013`; the gate threshold 0.004 corresponds to a one-sided z and `p < 0.001`. The
significance score is evaluated only at common fixed-step checkpoints (anti-val-spam), not at a
per-run cherry-picked lowest val step.

**Status.** Supported (applied identically across v1/v2/v3 submissions).

**Falsification criteria.** If a submitted cohort that passes the gate fails to reproduce its mean
on a fresh independent set of 16 seeds, or if the single-seed frontier bins themselves pass the
cohort gate, the conservatism claim is wrong.

**Evidence basis.** v2's single-seed frontier reached ~2962 but the cohort test failed at every step
below ~3012; the earliest passing checkpoint was 3037 (submitted). v3's single-seed crossings reached
sub-2900 but the submitted nosphere bin is 2949. v1's aggressive single-seed region (~3170) was
statistically rejected and the submission settled at 3205.

**Sources.**
- v2 cohort gate at 3037: mean 3.27853, score (3.28-mu)·√16 = 0.00588 ← `evidence/tables/v2_seed_table.md` (transcribed from the v2 record README) «mean val loss = 3.27853000 ... (3.28 - mu) * sqrt(n) = 0.00588000» [result]
- v1 cohort gate at 3205: mean 3.27897, score 0.004112 ← `evidence/tables/v1_seed_table.md` «mean val loss = 3.27897187 ... (3.28 - mu) * sqrt(n) = 0.00411250» [result]
- v3 cohort gate at 2949: mean 3.27886, score 0.004555 ← `evidence/tables/v3_seed_table.md` «mean val loss = 3.27886125 ... (3.28 - mu) * sqrt(n) = 0.00455500» [result]

**Proof.** E07.
