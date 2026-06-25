# Claims

Falsifiable takeaways from the Codex speedrun trajectory. Each `Statement` is the **mechanism or
relationship** a result reveals — the reusable WHY — with the named recipes, run IDs, and numbers
demoted to `Evidence basis` / `Proof` and the evidence layer. Numbers in `**Sources**` are quoted
verbatim from the cited file and were opened during compilation. Provenance: all claims are
`ai-executed` (produced by the Codex agent's own runs) unless noted.

---

## C01 — Decoupling the LR-decay horizon from the training-stop step is the foundational step-compression lever

**Statement.** On this benchmark, running the canonical learning-rate cooldown *schedule* to a
nominal horizon while *stopping* training at a smaller step count crosses the loss target in fewer
steps than recomputing a shorter cooldown — because the canonical trajectory sits only marginally
above target at intermediate checkpoints, so the gain comes from *reading the crossing earlier on
the same curve* rather than from a faster-decaying curve. Every submitted record is built on this
schedule/stop decoupling.

**Conditions.** nanoGPT track_3, Muon-family optimizers, 3.28 target, cosine/linear/power-law
cooldowns. Untested: whether the decoupling helps under schedules with no long shallow tail, or once
the stop step is pushed far below the schedule horizon (where the cooldown is too steep to have
flattened).
**Status.** Supported (foundational across v1/v2/v3).
**Falsification criteria.** A matched run with `schedule_steps = train_steps` (a genuinely shorter
cooldown) reaching the same or lower bin would refute the mechanism; so would the decoupled run
crossing *later* than the shorter-cooldown run at equal stop step.
**Proof.** E01.
**Evidence basis.** v1 record uses `schedule_steps=3375` with submitted bin 3205; v3 record uses
`train_steps=3020`, `schedule_steps=3025` with submitted bin 2949 (the run continues past the logged
crossing). The wave's first reproduced improvement was a `stop3450` horizon run.
**Dependencies.** —
**Sources.**
- "Muon `mu` schedule … **linear LR cooldown on `schedule_steps=3375`**" ← `record_configs/20260515_codex_v1_v12iso_3205/README.md:11` [input]
- "PR #287 power-law cooldown constants with `train_steps=3020`, `schedule_steps=3025`" ← `record_configs/20260515_codex_v3_nosphere_2949/README.md:11` [input]
- "The runs continue to `train_steps=3020`, but the submitted bin is the logged step-2949 checkpoint" ← `record_configs/20260515_codex_v3_nosphere_2949/README.md:16` [input]

---

## C02 — Second-moment normalization of the orthogonalized Muon update (NorMuon → Muon2F) is a top-tier optimizer contributor to step compression

**Statement.** Normalizing Muon's Newton–Schulz output by per-row / factorized second moments
(NorMuon's row normalization, Muon2F's two-factor preconditioning) materially lowers the bin: it
stabilizes the compressed-cooldown tail by equalizing per-row update magnitudes, buying mid/late-curve
margin that a single global Muon step does not. In the final v1 stack, removing the factorized
preconditioner is the second-largest degradation of any single component.

**Conditions.** Muon matrix optimizer on a 124M GPT at a compressed horizon; hidden matrices only
(the v1 stack applies Muon2F hidden-only). Untested at full horizon or on the auxiliary groups.
**Status.** Supported.
**Falsification criteria.** A leave-one-out removal of the factorized preconditioner that changes
validation loss within ±1× the noise floor would refute its load-bearing status.
**Proof.** E02.
**Evidence basis.** v1 component-pruning sweep at step 3195: `noMuon2f` is the 2nd-largest positive
delta; the NorMuon `beta=0.90` family carried the wave from 3450 down to 3350.
**Dependencies.** C01.
**Sources.**
- `noMuon2f` removal worsens validation by `+0.00229` (`mean 3.28136` vs baseline `3.27907`) ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:104-106` «"delta": 0.0022899999999999032, "label": "noMuon2f", "mean": 3.28136» [result]
- "NorMuon with Polar-Express-style Newton-Schulz projection and row/column preconditioning on hidden matrices." ← `record_configs/20260515_codex_v1_v12iso_3205/README.md:6` [input]

---

## C03 — Eval-only tail weight-averaging (tail-EMA) compresses the bin but is seed-fragile near the floor

**Statement.** Maintaining an exponential moving average of the weights during the late phase and
swapping it in *only for validation* lets the loss cross the target a few steps earlier, because it
averages away late-training weight noise rather than changing the optimization trajectory. It is the
single most load-bearing component of the v1 stack — but its margin is small relative to seed
variance, so below ~3195 steps the crossing becomes seed-fragile (some seeds miss).

**Conditions.** Eval-only averaging (weights restored under `torch.no_grad()` after eval), decay
~0.99, start ~step 2000, on the v1 Muon2F/Adam-mini stack. The fragility boundary (~3195) is
specific to this stack and noise floor.
**Status.** Supported; bounded by seed fragility.
**Falsification criteria.** Removing tail-EMA changing validation within ±1× noise floor would
refute its load-bearing status; conversely, a reproduced multi-seed crossing well below 3195 with
the same EMA settings would refute the fragility bound.
**Proof.** E03.
**Evidence basis.** v1 pruning at step 3195: `noTailEMA` is the largest single positive delta.
**Dependencies.** C02.
**Sources.**
- `noTailEMA` removal worsens validation by `+0.00251` (`mean 3.28158`), the largest single delta ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:112-114` «"delta": 0.0025100000000000122, "label": "noTailEMA", "mean": 3.28158» [result]
- "Tail EMA evaluation starting at step 2000 (`beta=0.99`)." ← `record_configs/20260515_codex_v1_v12iso_3205/README.md:10` [input]

---

## C04 — Scheduling the matrix momentum (mu-schedule) is a transferable, load-bearing schedule lever across waves

**Statement.** Warming the Muon momentum coefficient up early and cooling it down over the final
steps (the "mu-schedule") improves the bin in more than one independently-built stack, indicating
the gain attaches to the *training-dynamics regime* (early exploration vs late settling) rather than
to any one optimizer recipe. It is a meaningful contributor in the v1 stack and the **single
largest** contributor in the v2 stack.

**Conditions.** Muon-family matrix optimizer; `0.85 → 0.95` warmup with a short `0.95 → 0.85` final
cooldown. Demonstrated in v1 and v2; not isolated as a standalone universal law.
**Status.** Supported (corroborated across two waves).
**Falsification criteria.** A leave-one-out removal of the mu-schedule changing validation within
±1× noise floor in *both* waves would refute its load-bearing status.
**Proof.** E04.
**Evidence basis.** v1 pruning (`noMuSched` mid-table positive delta) and v2 pruning (`noMuSched`
the largest delta) both keep it.
**Dependencies.** C01.
**Sources.**
- v2: `noMuSched` removal worsens validation by `+0.00459` (`mean 3.28344`), the largest v2 delta ← `record_configs/20260515_codex_v2_legal_3037/pruning_data.json:96-98` «"delta": 0.004590000000000316, "label": "noMuSched", "mean": 3.28344» [result]
- v1: `noMuSched` removal worsens validation by `+0.00091` (`mean 3.27998`) ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:96-98` «"delta": 0.0009100000000001884, "label": "noMuSched", "mean": 3.27998» [result]

---

## C05 — Role-specific LR/WD splitting of the Muon matrix groups improves the tail at fixed average budget

**Statement.** Splitting the Muon learning rate and weight decay by tensor *role* (q, k, v,
attn.proj, mlp.fc, mlp.proj) — while holding the parameter-weighted averages at the body-wide
values — lowers the bin, because different roles want different effective step/shrinkage scales that
a single body-wide value cannot give. The role-LR split is a top-tier contributor in the v2 stack;
the role-WD split is real but smaller.

**Conditions.** v2 legal stack, base Muon LR `0.045` / base WD `0.030`, the six-role split. The
averages are held fixed, so the gain is from *reallocation*, not a net LR/WD change.
**Status.** Supported.
**Falsification criteria.** A role-split whose multipliers are reset to the body-wide value (recovering
the average) matching the split's bin would refute the reallocation mechanism.
**Proof.** E05.
**Evidence basis.** v2 pruning: `noRoleLR` is the 4th-largest delta; `noRoleWD` is small but kept.
**Dependencies.** C04.
**Sources.**
- `noRoleLR` removal worsens validation by `+0.00292` (`mean 3.28177`) ← `record_configs/20260515_codex_v2_legal_3037/pruning_data.json:72-74` «"delta": 0.0029200000000000337, "label": "noRoleLR", "mean": 3.28177» [result]
- "Role-specific Muon LR multipliers: q/k `0.61875`, v `0.625`, attn.proj `0.6375`, mlp.fc `1.0125`, mlp.proj `0.9875` of base LR `0.045`." ← `record_configs/20260515_codex_v2_legal_3037/README.md:8` [input]
- role LR multipliers in the recipe ← `src/execution/v2_legal_v12opt_recipe_ts3037.py:320-323` «_ATTN_Q_LR_MULT = 0.61875 … _ATTN_PROJ_LR_MULT = 0.63750» [input]

---

## C06 — A softened Lookahead slow-pull on the matrix weights damps late jitter and contributes a real but modest gain

**Statement.** A Lookahead variant that interpolates the live matrix weights toward a slow copy
*without resetting the fast weights to the slow copy* damps late-training matrix-weight jitter and
lowers the bin. Removing it costs a contribution comparable to the Polar-Express NS coefficients —
real, but an order of magnitude below the schedule/preconditioner levers — so it is a refinement,
not a primary driver.

**Conditions.** v2 legal stack; pull ramped in via a smoothstep from step 2450
(`ALPHA=0.35, PULL=0.15, INTERVAL=25, RAMP=150`). The "no fast-weight reset" detail distinguishes it
from standard Lookahead.
**Status.** Supported (modest effect).
**Falsification criteria.** Removing the lookahead changing validation within ±1× noise floor, or a
standard reset-Lookahead matching it, would weaken the claim.
**Proof.** E06.
**Evidence basis.** v2 pruning: `noLookahead` ties `noPolarExpress` at `+0.00117`.
**Dependencies.** C05.
**Sources.**
- `noLookahead` removal worsens validation by `+0.00117` (`mean 3.28002`) ← `record_configs/20260515_codex_v2_legal_3037/pruning_data.json:64-66` «"delta": 0.0011700000000001154, "label": "noLookahead", "mean": 3.28002» [result]
- lookahead params ← `src/execution/v2_legal_v12opt_recipe_ts3037.py:393-397` «_LOOKAHEAD_START_STEP = 2450 … _LOOKAHEAD_ALPHA = 0.35 … _LOOKAHEAD_PULL = 0.15 … _LOOKAHEAD_RAMP_STEPS = 150» [input]

---

## C07 — In the public-frontier (v3) stack, SOAP preconditioning and outward-radial dampening are the load-bearing components

**Statement.** When a deep multi-lever public-PR stack (Soft-Muon + Contra + radial + SOAP + LACV +
power-law cooldown) is compressed, the dominant contributions come from *preconditioning* (SOAP,
extended to MLP+V) and from *outward-radial update dampening* — removing SOAP is the single largest
degradation, and removing the radial control is the second. The many late micro-levers around them
contribute far less. The benefit of preconditioning + radial control therefore concentrates the
stack's value, mirroring the v1 pattern (preconditioning + averaging dominate).

**Conditions.** v3 nosphere stack at step 2949; SOAP in `mlp_plus_v` mode with V-blend 0.95; radial
outward scale 0.45 with a tail guard. Demonstrated on the public-PR lineage, not isolated from it.
**Status.** Supported.
**Falsification criteria.** A leave-one-out removal of SOAP or radial control changing validation
within ±1× noise floor would refute their load-bearing status.
**Proof.** E07.
**Evidence basis.** v3 W258 leave-one-out at step 2949: `nosoap` and `noradial` are the two largest
positive deltas; `novsoap` (V-SOAP only) is third.
**Dependencies.** C01, C08.
**Sources.**
- `nosoap` removal worsens validation by `+0.00528` (`mean 3.28370`), the largest v3 delta ← `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json:64-66` «"delta": 0.005283124999999611, "label": "nosoap", "mean": 3.2836999999999996» [result]
- `noradial` removal worsens validation by `+0.00374` (`mean 3.28216`), the 2nd-largest delta ← `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json:56-58` «"delta": 0.0037431249999997362, "label": "noradial", "mean": 3.2821599999999997» [result]

---

## C08 — Leave-one-out pruning reveals that late stacked micro-levers contribute within noise and are removable, and that co-located mechanisms need not compose

**Statement.** A mandatory leave-one-out pruning round repeatedly finds that, once a deep stack is
built, several late-added micro-levers contribute within ±noise (or slightly *negative*) and can be
dropped at no cost — the "nosphere" result drops the sphere-lookahead pull to zero while preserving
the step-2940 boundary. Moreover two mechanisms that target the same locus need not compose: removing
the sphere *pull* helps, and a separate variant removing the tangent *gate* is independently valid,
but removing *both* loses the boundary. Pruning is thus a load-bearing epistemic step, not bookkeeping.

**Conditions.** Applied to the v1 (step 3195) and v3 (step 2949) stacks; "co-located non-composition"
shown for the v3 sphere pull vs tangent gate. The specific droppable set is stack-specific.
**Status.** Supported.
**Falsification criteria.** If every leave-one-out removal worsened validation by ≥ 1× noise floor
(no droppable micro-levers), or if the two sphere removals composed without losing the boundary, the
claim would be refuted.
**Proof.** E08.
**Evidence basis.** v1 pruning: `noResPulse`, `noMomRefresh`, `noBeta2Thaw` have ≤ 0 deltas (removal
does not hurt). v3 pruning: the `nosphere` baseline already *is* the pruned stack; the combined
`nosphere-notangent` removal carries a positive (degrading) delta.
**Dependencies.** —
**Sources.**
- v1 `noResPulse` delta `-0.00007` (removal does not worsen) ← `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json:24-26` «"delta": -7.00000000000145e-05, "label": "noResPulse"» [result]
- v3 `nosphere-notangent` (combined removal) degrades by `+0.00070` ← `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json:80-82` «"delta": 0.0007014583333342372, "label": "nosphere-notangent", "mean": 3.2791183333333342» [result]
- "the sphere-lookahead pull is disabled (`SPHERE_LOOKAHEAD_PULL=0.0`), hence the submitted `nosphere` stack." ← `record_configs/20260515_codex_v3_nosphere_2949/README.md:12` [input]
- the prune in code (pull 0.0, tangent gate retained) ← `src/execution/v3_nosphere_recipe_ts3020.py:144,156` «SPHERE_LOOKAHEAD_RADIAL_PARAM = "q,k" … SPHERE_LOOKAHEAD_PULL = 0.0» [input]

---

## C09 — Individually-helpful levers do not stack additively near the noise floor; a package can wash out while one isolated lever carries the gain

**Statement.** Combining several levers that each help in isolation can *fail* as a package: in the
v1 wave the full "v12" multi-lever package missed every stop it was tried at, while the **isolated**
mu-schedule lever — the same wave, one lever — reproduced the frontier. Near the noise floor, lever
effects are not additive; interactions can cancel, so isolating a single lever can beat stacking
many. This is a direct counter-instance to the orthogonal-and-additive assumption (gap G2).

**Conditions.** v1 wave, the "v12" lever set (attention-LR, pre-NS row-L2, embed-init, Contra)
packaged vs the mu-schedule isolated. Shown at the compressed horizon near the seed-noise floor.
**Status.** Supported (single decisive instance + corroborated by the cross-wave pruning pattern in C08).
**Falsification criteria.** If the full v12 package had reproduced a bin at or below the isolated
mu-schedule's bin, the non-additivity claim would be refuted.
**Proof.** E09.
**Evidence basis.** v1 `THREAD.md`: full/simplified `v12pack` variants missed all stops; isolated
`v12iso-musched` hit and reproduced. The submitted v1 record is named the "v12iso/MuSched" stack.
**Dependencies.** C04, C08.
**Sources.**
- "This is the **v12iso/MuSched** codex stack." ← `record_configs/20260515_codex_v1_v12iso_3205/README.md:5` [input]
- v1 package-vs-isolate finding (full v12 package missed all stops; isolated mu-schedule hit) ← `v1/codex/scratchpad/THREAD.md:2202,2208` [pending: THREAD line read by extraction subagent, not re-opened this compile]

---

## C10 — An un-audited forward-path precision change can masquerade as an optimizer gain; only provenance + byte-identical compliance lets a speedrun gain be attributed correctly

**Statement.** A numerical change inside the model's forward path (here, a `RMSNorm.forward` that
upcasts via `norm(x.float())` and routes q/k through the same helper, inherited from a *different
agent's* "v12" stack) materially produced the apparent sub-3000-step advantage — not the optimizer.
Once flagged as a benchmark-rule (architecture) violation, all v12-derived results had to be
quarantined and the frontier rebuilt on a byte-identical-compliant base, which regressed the
submittable bin from a single-seed crossing at 2963 to 3037. The lesson: a speedrun gain is only
attributable to the optimizer when the forward path is provably unchanged; provenance + a
compliance gate are prerequisites for any cross-stack comparison.

**Conditions.** v2 wave; the inherited parent is the cc/Claude agent's "v12" stack (cross-agent
provenance). The violation is a bf16 forward-path precision change, not an optimizer change.
**Status.** Supported (a decisive epistemic event, recorded with attribution).
**Falsification criteria.** If the compliant rebuild (baseline `RMSNorm.forward`) had reached the
same sub-3000 bins as the tainted base, the forward-path change would not have been the source of the
advantage and the claim would be refuted.
**Proof.** E10.
**Evidence basis.** The compliant `legal_v12opt` recipe uses the baseline RMSNorm form; the v2 record
is the legal frontier at 3037; the single-seed crossing reached 2963 only on the search path.
**Dependencies.** C04, C05.
**Sources.**
- "the user then flagged its `RMSNorm.forward` / q-k-norm as a forward-path precision change that violates the no-architecture-change rule, and Codex **quarantined** every v12-derived result" ← `README.md:67-69` [input]
- "The *submittable* v2 frontier (**C04**, `legal_v12opt` @ 3037) is rebuilt on a byte-identical-compliant base." ← `README.md:70-71` [input]
- "legal frontier bin 3037 (single-seed crossing at 2963)" ← `README.md:18` [input]
- compliant baseline RMSNorm.forward in the recipe ← `src/execution/v2_legal_v12opt_recipe_ts3037.py:65` «return F.rms_norm(x, (x.size(-1),), weight=self.gains.type_as(x))» [input]
- the handed parent's provenance ← `v2/codex/goal.md:8` «**Best: 3025 steps** — cc-agent's v12 stack» [input]

---

## C11 — Under a hard novelty constraint plus isolation, the noise-dominated regime yields a negative result: no derived novel mechanism survived both reproduction and the 2× noise-floor gate

**Statement.** Requiring every submission to contain a non-published mechanism, while forbidding the
search from porting-and-tuning published methods, produced no promotable result on this benchmark.
The best *reproduced* novel crossing was a 25-step gain — below the 2× (≈100-step) noise-floor gate —
and the two best *apparent* crossings failed exact-seed reproduction. The combination of a
noise-dominated regime and a constraint that pushes the search off the methods most likely to work
makes a clean negative result the honest outcome. A clean negative on a hard constraint is itself a
contribution.

**Conditions.** The hard-isolated novelty wave (no access to other worktrees); novelty enforced by a
pre-run arXiv existence-check subagent and a refined "materially non-additive interaction" bar.
**Status.** Supported (faithful negative result).
**Falsification criteria.** A novel mechanism reaching a ≥ 2×-noise-floor bin improvement reproduced
over ≥ 2 seeds would refute the negative result.
**Proof.** E11.
**Evidence basis.** Novelty `plan.md` "Current state": the single reproducible sub-3500 crossing is
25 steps (below the gate); the two best 3375 crossings failed reproduction. No promotable submission.
**Dependencies.** C12.
**Sources.**
- "Reproducible but not promotable: `vfg001_gain080_lr026_t3475` reached `3.27960` at 3475 … and `3.27962` on seed 1234. This is only a 25-step grid improvement, below the 2x noise-floor gate" ← `novelty/codex/plan.md:13-15` [result]
- "Failed reproduction: `ngi001_n0875_m1125_t3450` reached the target at observed step 3375 on one seed, but exact repeat `9003` missed 3375 (`3.28149`)" ← `novelty/codex/plan.md:18-19` [result]
- "every submitted recipe must contain at least one idea that has not been published on arXiv" ← `novelty/codex/goal.md:11-12` [input]
- "a **negative result** (no promotable submission)" ← `README.md:17` [input]

---

## C12 — Single-seed sub-frontier crossings systematically fail cohort significance; the submittable bin sits well above the single-seed frontier

**Statement.** On this benchmark a single-seed crossing is a hypothesis, not a result: seed variance
is comparable to the entire sub-threshold margin, so a fixed-step cohort z-test
`(3.28 − μ)·√n ≥ 0.004` repeatedly demotes the lowest single-seed crossings and the submittable bin
lands tens of steps higher. v2's single-seed crossing at 2963 became a submittable 3037; v3's viable
bin (~2940) sits above its lowest observed crossings. The discipline that converts a seed-lottery win
into a defensible record is the cohort gate, not the lucky seed.

**Conditions.** All four waves; `σ ≈ 0.0013`, n=16 seed cohorts for the submitted records, the
`(3.28 − μ)·√n ≥ 0.004` bar (p < 0.001).
**Status.** Supported (governs every submission).
**Falsification criteria.** A single-seed sub-frontier crossing that, re-run as an n≥8 cohort at the
same step, cleared the `0.004` bar would refute the systematic gap.
**Proof.** E12.
**Evidence basis.** All three records report n=16 cohorts with explicit scores; the v2 single-seed
2963 vs submittable 3037 gap; the noise floor ≈ 50 steps vs the ~0.0011 sub-threshold margin.
**Dependencies.** —
**Sources.**
- v2 cohort: "n = 16 / mean val loss = 3.27853000 / (3.28 - mu) * sqrt(n) = 0.00588000 … `p < 0.001`" ← `record_configs/20260515_codex_v2_legal_3037/README.md:21-26` [result]
- "legal frontier bin 3037 (single-seed crossing at 2963)" ← `README.md:18` [input]
- noise floor "`step_to_target` ≈ 50 steps … `final_val_loss` mean ≈ 0.001" ← `v1/codex/AGENTS.md:161-162` [input]
- v3 cohort score `0.00455500` at the submitted bin 2949 ← `record_configs/20260515_codex_v3_nosphere_2949/README.md:24` [result]
