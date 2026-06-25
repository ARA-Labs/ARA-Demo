# Claims

Falsifiable assertions extracted from the synthesis.

**Reading convention.** The `Statement` is high-level natural language only — *what was tested, what
was observed, and why it happens* — with no numbers. All concrete values, run IDs, and detailed
setups live in the later bullets: `Falsification criteria`, `Evidence basis` (what the cited data
directly shows), and `Interpretation` (broader mechanistic reading). Each `Proof` references
experiment IDs in [experiments.md](experiments.md). Everything is grounded to
`data/runs_self_contained/runs.csv`, agent scratchpads, run code, and `train.log`. `[HYP]` marks
uncertain mechanisms.

## C01: No silver-bullet optimizer — the gain is compositional
- **Statement**: Across five waves of search, no single optimizer substitution captured the available
  improvement. The step-count reduction instead came from stacking many independently small,
  previously-published levers and re-tuning them to a shared backbone. Because each lever acts on a
  different part of the update — conditioning, per-role scaling, schedule shape, training horizon —
  their effects compound rather than overlap, so the frontier looks like an *integration* of ideas
  rather than the discovery of one.
- **Status**: supported
- **Falsification criteria**: A single optimizer swap (one method replacing Muon, no other changes)
  reaching <= ~2930 seed-verified steps would refute compositionality.
- **Proof**: [E01, E11]
- **Evidence basis**: Muon reference 3500 -> ~2880-2885 single-best-seed -> ~2930 seed-verified, i.e.
  ~16-17% fewer steps and ~48% fewer than the AdamW baseline (5625). cc_v1 `ideas.md` integrated
  ladder entries 1-7 each have 3-seed dval in [-0.0009, -0.0048]; no single substitution moved the
  frontier by more than ~1-2%. The LOO ablation (§14) shows every hitting component is worth
  <= ~85 steps.
- **Interpretation**: Muon's orthogonalized update already captures most cheap curvature at 124M, so
  residual gains live in second-order details (per-group scaling, NS conditioning, schedule shape,
  init) that only compound.
- **Dependencies**: C03, C13
- **Tags**: compositional, frontier, levers

## C02: Trimming `train_steps` is the single biggest free lever (and partly a measurement artifact)
- **Statement**: Shortening the total training horizon was tested as a lever and turned out to be the
  largest single source of step reduction, with no measurable cost to validation quality at the
  target. The effect is twofold: the baseline genuinely over-trains in its final cooldown steps, and
  the headline metric is read off a coarse validation cadence, so the model actually crosses the
  target *between* logged validations and a finer cadence "recovers" steps it was already achieving.
  There is nonetheless a hard floor — past a point the target is genuinely not yet reached.
- **Status**: supported
- **Falsification criteria**: If shortening the horizon raised `min_val_loss` above 3.28, or if dense
  validation at the true crossing did not change `step_to_3_28`, the lever would not be "free".
- **Proof**: [E02]
- **Evidence basis**: §2.A.1, §6.1, §8.3. Horizon trims 3500 -> ~2900 give -250 to -325 steps;
  run names pervasively encode `tsXXXX`. On a 3500-step trajectory, a forced validation at step 3450
  hits (seeds 3.27844 / 3.27777) while 3425 misses (3.28178). The v3 record validates every 5-10
  steps from step 2820 onward to pin the first sub-3.28 step (2885: 3.27972).
- **Interpretation**: Two effects stack — real over-training removal plus a coarse-cadence measurement
  gap that dense late validation closes; the floor (3425 miss) shows the underlying crossing is real.
- **Dependencies**: none
- **Tags**: train_steps, schedule, validation-cadence, artifact

## C03: MuonEq (pre-NS row normalization) is the strongest single Muon-internal lever
- **Statement**: Two ways of equalizing per-row update magnitude in Muon were compared: normalizing
  the momentum rows *before* the Newton-Schulz orthogonalization (MuonEq) versus normalizing the
  already-orthogonalized update *after* it (NorMuon). Pre-NS normalization was clearly the stronger of
  the two, and combining both gave no additional benefit. The reason is that the pre-NS version
  improves the *input* to the orthogonalization (so the result is more faithful), whereas the post-NS
  version only rescales an update that is already orthogonal, and doing both corrects the same
  imbalance twice.
- **Status**: supported
- **Falsification criteria**: If post-NS normalization (NorMuon) matched or beat pre-NS, or if the two
  stacked additively, the pre-NS conditioning mechanism would be wrong.
- **Proof**: [E01, E11]
- **Evidence basis**: cc_v1 `ideas.md` #6/#7/#14; §2.B.3. MuonEq 3-seed mean dval@3125 = -0.00484
  (the best single lever, ~11 sigma vs seed std 0.00043); NorMuon = -0.00155; MuonEq+NorMuon stacked
  = -0.0014 (~= NorMuon alone). LOO `loo14_no_normuon` -> 2930 (= full recipe, i.e. NorMuon redundant
  once Aurora/MuonEq present).
- **Interpretation**: Equalizing per-row momentum scale before NS hands the orthogonalization a
  better-conditioned input so rows contribute equally to the spectral fit.
- **Dependencies**: C05
- **Tags**: MuonEq, NorMuon, Newton-Schulz, normalization

## C04: Normalization buys a higher learning rate (non-monotonic LR trajectory)
- **Statement**: The best Muon learning rate was not constant across the experiment: it was pushed
  *up* once per-row normalization was added (because controlling the per-step update magnitude makes a
  bigger global step stable), then pulled back *down* when heavier preconditioning was stacked on in
  the final wave (because that changed the effective update geometry again). The takeaway is that the
  "right" learning rate is a property of the whole preconditioning stack, not a fixed property of
  Muon.
- **Status**: supported
- **Falsification criteria**: If the optimal LR were invariant across waves (constant ~0.025 regardless
  of normalization/preconditioning) the "normalization buys headroom" mechanism would fail.
- **Proof**: [E01, E03]
- **Evidence basis**: §5.2, §13.2. Muon base LR moved 0.025 (baseline) -> 0.045 (v2, +80%) -> 0.0375
  (both v3 records). The up-move accompanies MuonEq/Aurora row-normalization; the down-move accompanies
  SOAP-on-subset + Aurora being stacked in v3.
- **Interpretation**: Per-row normalization clamps update variance so a larger global step stays
  stable; v3's heavier preconditioning re-shapes the geometry, re-lowering the optimal LR.
- **Dependencies**: C03, C05
- **Tags**: learning-rate, normalization, non-monotonic

## C05: A method's effect is backbone- and parameter-subset-dependent (sign flips)
- **Statement**: The same optimizer modification was observed to help in one context and hurt in
  another, depending on what else was in the recipe and which parameter matrices it was applied to.
  Most strikingly, a second-order preconditioner that fails when applied to the whole model becomes
  one of the most valuable levers when restricted to the matrices where Muon's orthogonalization
  leaves curvature signal on the table. The general lesson is that gains measured against a vanilla
  baseline do not transfer additively, so every imported lever had to be re-tested at the current
  backbone.
- **Status**: supported
- **Falsification criteria**: If full-model and subset SOAP gave the same sign, or if Muon^2's PR gain
  transferred additively into the stack, context-dependence would be refuted.
- **Proof**: [E03, E05]
- **Evidence basis**: §2.D.1/§2.D.3/§3.2/§5.3/§16. Full-model SOAP `00182-soap-lr3e-2` asymptotes at
  3.38876 and never hits 3.28; SOAP on MLP+V is part of the 2885 stack (removing MLP-SOAP costs ~+85
  steps). Muon^2 showed -175 steps vs vanilla Muon in a public PR but regressed in-stack
  (`family=muon2f` best 3190).
- **Interpretation**: Muon's NS already conditions Q/K-style "geometric" matrices, so SOAP duplicates
  it there (cost without signal); MLP+V carry persistent curvature anisotropy NS leaves untouched,
  where SOAP's eigenbasis scaling adds real signal.
- **Dependencies**: none
- **Tags**: backbone-dependence, SOAP, param-subset, confounder

## C06: Matrices play different roles — differentiate LR, weight decay, and schedule per role
- **Statement**: Splitting the weight matrices by structural role (attention vs MLP, plus the
  separately-optimized embedding/output/scalar group) and giving each role its own hyperparameters was
  tested and consistently helped. The benefit was observed not just for the learning rate but also for
  weight decay and even for *when* each group begins its learning-rate cooldown. It happens because
  attention and MLP matrices differ in scale, curvature, and sensitivity, so their ideal step size,
  shrinkage, and anneal timeline all differ.
- **Status**: supported
- **Falsification criteria**: If a uniform LR/WD/schedule across attn and MLP matched the per-role
  split at the frontier, role differentiation would add nothing.
- **Proof**: [E04, E11]
- **Evidence basis**: §2.C.1, §13.3, §15.3. Attention Muon LR ~0.5-0.6x of MLP (cc_v1 best run
  `...attn0.5` -> 3000); per-role weight decay attn 0.0275 < MLP 0.03125 (codex `rolewd-combo` -> best
  ~2962); per-group cooldown onset `power_c` (embed 4.98e-5 vs Muon 3.32e-6). LOO `adamw_betas` -> 2970
  (~+45) shows even the non-Muon group was not pre-optimal.
- **Interpretation**: Step size, shrinkage, and anneal timeline each want to differ by parameter role;
  per-role differentiation is a recurring frontier theme across all three axes.
- **Dependencies**: none
- **Tags**: per-role, learning-rate, weight-decay, schedule

## C07: Several well-cited optimizer modifications are clean negatives, some cross-agent confirmed
- **Statement**: A set of popular optimizer add-ons were each tested on top of Muon and each failed to
  beat the plain-Muon baseline, several of them confirmed independently by both agents. The failures
  are mechanistic, not incidental: masking updates by sign-agreement destroys the orthogonality the
  optimizer just imposed; periodic slow-weight blending and slow EMAs starve under a short training
  budget; and endgame weight-averaging adds bias without variance reduction under a schedule whose
  late learning rate is already near zero. On a saturated benchmark, a well-cited method failing is
  itself a real result.
- **Status**: supported
- **Falsification criteria**: If any of these reached a seed-verified step count below the plain-Muon
  baseline at the same backbone, the negative would be overturned.
- **Proof**: [E05]
- **Evidence basis**: §2.D.2, §6.2-§6.4; cc_v1 `ideas.md` #10/#11/#12; `v1/codex/picklist.md` §1-§3.
  Cautious-Muon (mask+renorm) ends 3.30833 and never hits (codex), and all 4 cautious modes regress at
  the cc v8 backbone; LR-floor-in-cooldown still 3500; EMA (decay 0.995 from step 2000) final 3.28010.
  Lookahead-Muon and AdEMAMix-Muon both regress.
- **Interpretation**: Cautious masking removes useful signal Muon's implicit monotone descent already
  provides; under WSD the late trajectory is near-stationary so averaging is biased; short budgets
  starve Lookahead/AdEMAMix's slow components.
- **Dependencies**: none
- **Tags**: negative-result, Cautious-Muon, Lookahead, AdEMAMix, EMA

## C08: "Lose early, win late" is real but recipe-specific
- **Statement**: A direct comparison of the validation curves showed that the frontier recipe is
  actually *behind* the baseline for most of the run before overtaking it and finishing well ahead on
  the step-to-target metric — answering the benchmark's explicit question of whether an optimizer can
  lose early yet win late. But this only holds when the early deficit *buys* something (better
  conditioning from early exploration): a recipe whose early deficit reflects a genuinely mismatched
  preconditioner loses early and never recovers. The crossover is therefore a property of the specific
  recipe, not a general "slow starts are fine" rule.
- **Status**: supported
- **Falsification criteria**: If no recipe existed that is behind early yet wins on step-to-3.28, or if
  every slow-start recipe eventually won, the "conditioned exploration" mechanism would be wrong.
- **Proof**: [E06]
- **Evidence basis**: §8. Record `07070-v88-aurora-proj-s2` vs baseline `00001`: behind from step ~250
  through ~1625 (max deficit +0.028 at step 375), crosses at ~step 1750, ends at 3.28 by step 2885 vs
  baseline 3500. Full SOAP `00182` is behind throughout and asymptotes at 3.38876 (`step_to_3_28=None`).
- **Interpretation**: Contra-Muon decorrelation + a higher LR trade early loss for conditioning, and
  the crossover sits right where Contra anneals off (~step 1920); SOAP's early deficit has no late
  payoff because the preconditioner is mismatched.
- **Dependencies**: C14
- **Tags**: training-dynamics, crossover, lose-early-win-late

## C09: The frontier is a thin tail over a noisy floor (records overstate)
- **Statement**: Re-running fixed configurations across many seeds revealed that the seed-to-seed
  scatter in final loss is about the same size as a whole single-lever improvement, and that at the
  frontier a meaningful fraction of seeds fail to reach the target at all. Consequently the
  best-of-many-seeds headline number is a lucky tail that overstates real performance, and honest
  claims must report the seed distribution (a median and a miss-rate) rather than the best run.
- **Status**: supported
- **Falsification criteria**: If frontier configs hit 3.28 on every seed with negligible std, the
  miss-rate tail and "report medians" recommendation would be unnecessary.
- **Proof**: [E07]
- **Evidence basis**: §9, §21. Frontier group A (`v88-aurora-proj`, 8 seeds): final-val std 0.00043,
  1/8 seeds miss; pooled `seed_reverify` miss-rate 14/152 = 9%. The README seed-verified figure is cc
  2930 vs the CSV single-best 2885.
- **Interpretation**: `step_to_3_28` has a binary miss-rate tail at the frontier; a single-number
  record can overstate by ~30-50 steps.
- **Dependencies**: none
- **Tags**: noise-floor, seeds, miss-rate, reproducibility

## C10: Novel != better on a saturated target
- **Statement**: When the search was constrained to genuinely novel operators (banning known methods
  and hyperparameter tweaks), the frontier got *worse*, and the best new operator merely matched a
  carefully re-validated plain-Muon baseline. The mechanism is that the levers that actually move this
  benchmark add structure *around* the orthogonalization core, whereas novel operators were forced to
  modify *inside* that core and so traded away the one ingredient that makes Muon work. Novelty was
  real; measurable improvement was not.
- **Status**: supported
- **Falsification criteria**: A novel operator (passing the novelty check) reaching below the
  re-validated plain-Muon baseline would refute "novel != better" here.
- **Proof**: [E08]
- **Evidence basis**: §4, §10. Both agents' novelty-wave best fell to 3375 (`cc_novelty`/`codex_novelty`);
  the re-validated plain-Muon baseline `baseline-muon-s1` also gave 3375 (3.27734); the top novel
  operator (trust-region-muon) also bottomed at 3375. Spectral-Momentum with shallow NS drifted to
  3.71 @ step 2000 and was early-killed; `scaphd-v1` was cancelled for a code-location rule violation.
- **Interpretation**: The frontier adds around the NS core (row-norm, SOAP-on-subset); novel operators
  that touch NS degrade orthogonalization; an infrastructure compliance rule also depressed the
  novelty frontier.
- **Dependencies**: C05
- **Tags**: novelty, negative-result, Newton-Schulz, saturated-benchmark

## C11: Instability is predictable and early-killable (three divergence modes)
- **Statement**: Inspecting runs that ended far above target revealed that divergence is not random:
  it falls into three recurring signatures — a slow, monotone crawl from a mis-scaled preconditioner;
  a clean descent followed by a mid-training spike and only partial recovery from a pathological
  hyperparameter; and a never-learning NaN/Inf trajectory from a bad interaction between normalization
  and warmup. All three are visible early in training, which is why the search discipline was to kill
  bad trajectories early rather than let them finish; most non-completions were cancellations, not
  crashes.
- **Status**: supported
- **Falsification criteria**: If divergences were random NaNs not predictable early from preconditioner
  scale / HP magnitude / warmup interaction, the taxonomy would not hold.
- **Proof**: [E09]
- **Evidence basis**: §11. Mode A `v17-klshampoo` descends 7.17 @ 375 -> 5.49 final (no spike); Mode B
  `armv2-eps1e6-a10` goes 4.36 @ 375 -> 5.21 @ 750 then limps back; Mode C `adamwwarm250-normuon`
  plateaus ~6.8 with 9 NaN/Inf lines. Status mix across the export: 73 failed vs 747 canceled (of
  ~10,485). All three signatures are detectable by step ~750.
- **Interpretation**: The dangerous instabilities are consequences of (a) wrong preconditioner scale,
  (b) pathological HP magnitudes, (c) normalization x warmup interactions — all early-detectable.
- **Dependencies**: none
- **Tags**: stability, divergence, early-kill, taxonomy

## C12: Two opposite search economies reach the same ceiling
- **Statement**: The two agents reached essentially the same frontier by opposite strategies: one ran
  a wide, shallow search over many distinct recipe ideas with relatively few runs each, while the
  other ran a narrow, deep search of huge hyperparameter sweeps around a small number of backbones.
  The wide-and-shallow agent used far fewer total runs yet explored far more distinct recipes, and its
  breadth located the stronger lever earlier; the deep agent over-invested its biggest early sweep in
  a weaker variant. Both routes are valid paths to the same ceiling but imply very different compute
  bills.
- **Status**: supported
- **Falsification criteria**: If run-count and recipe-diversity were equal across agents, or if only
  one style reached the frontier, the "two economies, same ceiling" claim would fail.
- **Proof**: [E10]
- **Evidence basis**: §7, §12, §19. Claude 2,204 runs vs Codex 8,224 (~3.7x) to the same ~2880-2885;
  Claude reached recipe v140 vs Codex v48. codex_v2 = 2,729 runs over 23 families vs cc_v2 = 459 runs
  over 41 families. In v1's first ~120 launch-ordered runs, Codex committed 106 to a single NorMuon
  sweep (reaching 3150) while Claude spanned ~14 families and located MuonEq (reaching 3000).
- **Interpretation**: Breadth-first located the stronger lever (MuonEq, the +11-sigma gain);
  depth-first over-invested in the weaker sibling (NorMuon, later found to be LOO-redundant); both
  converged on the Muon-family neighborhood.
- **Dependencies**: none
- **Tags**: search-economy, sample-efficiency, agent-comparison

## C13: A leave-one-out ablation shows a long-tailed contribution distribution
- **Statement**: Taking the full frontier recipe and removing exactly one component at a time (with
  multiple seeds each) produced a clean ranking of how much every piece is worth. The distribution is
  strongly long-tailed rather than uniform: one component is outright critical (without it the recipe
  fails on every seed), one is large, a handful are mid-sized, and several contribute essentially
  nothing because a stronger version of the same mechanism is already present. So a frontier recipe
  carries a few load-bearing pieces plus a tail of dead weight.
- **Status**: supported
- **Falsification criteria**: If every component contributed roughly equally (uniform LOO deltas), or
  if removing the cooldown left the recipe hitting the target, the long-tail claim would be refuted.
- **Proof**: [E11]
- **Evidence basis**: §14; `agents/cc_v3/runs/*loo{01..15}_no_*` (629 LOO runs; clean 4-seed subset).
  Full recipe ~2925-2930 seed-verified. Median step when each component is removed: `pow_cooldown`
  MISS (0/4 hit, critical); `soap_mlp` 3010 (~+85); `adamw_betas` 2970 (~+45); `uwfloor`/`attn_soap`
  ~2960 (~+35); `aurora`/`mu_sched` ~2945 (~+20); `contra`/`muwarmup` ~2940 (~+15); `normuon`/`cgi`/
  `softmuon` ~2930 (~0). Shape: ~2 essential + ~5 useful + ~4 dead.
- **Interpretation**: Schedule shape (neutral at the baseline) becomes load-bearing once the rest of
  the recipe saturates — a higher-order case of backbone-dependence; redundant levers are not pruned.
- **Dependencies**: C01, C03, C06
- **Tags**: ablation, leave-one-out, ranking, long-tail

## C14: The frontier recipe is a temporal curriculum (explore early, exploit late)
- **Statement**: Decoding the record recipe shows it is not a static optimizer but a *time-scheduled
  curriculum* in which different levers switch on and off over the course of training. An early
  exploration phase deliberately decorrelates the update from the greedy gradient and forces trust in
  the second-order preconditioner; a middle phase hands control to the hard orthogonalization and a
  data-driven trust gate; and an endgame phase softens the orthogonalization and steepens the cooldown
  to settle into the minimum. This time schedule is exactly the engineered cause of the lose-early/
  win-late crossover, with the explore-phase levers annealing off right at the measured crossover.
- **Status**: supported
- **Falsification criteria**: If the ramp constants did not bracket the measured crossover step
  (~1750), or if removing the time-scheduling left the curve unchanged, the curriculum claim would fail.
- **Proof**: [E12]
- **Evidence basis**: §17. Explore (0-~1625): mu warmup 0.85->0.95 (0-300), Contra-Muon -0.2->0 by
  step 1920, attn trust-floor 0.45 fading by 1625. Soften (2400-2900): soft-Muon blends 0->0.80,
  convex power-cooldown steepens, mu cools 0.95->0.85. The crossover from §8 is at ~step 1750.
- **Interpretation**: The agents learned to schedule exploration->exploitation in optimizer-space, not
  just LR-space; `trust_gate` is the cheap correctness check that makes amortized (stale-basis) SOAP
  safe. Soft-Muon's endgame-softening mechanism is partly `[HYP]`.
- **Dependencies**: C08
- **Tags**: temporal-curriculum, explore-exploit, Contra-Muon, soft-Muon, trust-gate

## C15: The cross-agent v3 records are byte-identical — shared lineage, not independent discovery
- **Statement**: A direct diff of the two agents' final-wave record recipes shows they are
  component-for-component identical, down to exotic magic constants and byte-identical helper
  functions, differing only in trivial timing offsets. So the apparent "independent convergence" at
  the frontier is really a shared public-PR pool that both agents drew from and pushed back to — a
  correction to an earlier reading that treated the convergence as evidence of real problem structure.
  The genuine independent-exploration signal is in the first wave, where the agents made different
  first moves and landed apart before the shared pool pulled them together.
- **Status**: supported (corrects an earlier overclaim that the convergence evidenced real structure)
- **Falsification criteria**: If the two v3 records differed in core operators/constants (not just
  timing offsets), independent rediscovery would be back on the table.
- **Proof**: [E13]
- **Evidence basis**: §18 side-by-side table: FINAL_LR_POWER 1.2/1.2, MUON_LR 0.0375/0.0375,
  CONTRA_MUON_COEFF -0.2/-0.2, SOFT_MUON_P 0.1/0.1, SOAP_PARAM_MODE mlp_plus_v/mlp_plus_v,
  ATTN_EARLY_TRUST_FLOOR 0.45/0.45; only timing offsets differ (e.g. CONTRA end 1920 vs 1930). The
  functions `trust_gate`, `soft_via_newtonschulz5`, `soap_update_preconditioner` are the same code. In
  v1 the agents diverged: cc operator-first to 3000 vs codex schedule-first to 3150.
- **Interpretation**: The defensible "real structure" evidence is (a) v1 independent divergence still
  landing in the Muon-family neighborhood and (b) the LOO showing components are individually
  load-bearing — not the v3 identity, which is mostly a copy.
- **Dependencies**: C12
- **Tags**: cross-agent, shared-lineage, replication, correction

## C16: The results have sharp generalization limits
- **Statement**: The frontier is benchmark-specific in several graded ways. It buys fewer *steps* at
  the cost of more *compute per step*, so on a wall-clock- or FLOP-budgeted run the expensive part of
  the recipe can be a net loss. It is overfit to the exact target threshold — the runs are tuned to
  cross that specific number as early as possible and then stop, not to minimize loss generally — so
  the metric does not generalize to other thresholds. The "orthogonalization beats heavier
  second-order" conclusion is bound to this model scale. And the headline records are a lucky tail over
  a miss-prone floor. The transferable parts are the cheap mechanisms; the expensive machinery, the
  exact constants, and the single-number records are not.
- **Status**: supported
- **Falsification criteria**: If the v3 recipe were also fastest in wall-clock, generalized to other
  loss thresholds, or held at >=350M scale, the limits would not apply.
- **Proof**: [E07, E14]
- **Evidence basis**: §20. Median `step_avg_ms` rose from 157.5 (baseline) to 188 (cc_v3, ~+20%) for
  ~17% fewer steps; v3 hitters cluster `min_val_loss` ~3.2765-3.2773 (a median ~2.6-3.3e-3 below 3.28,
  ~17% clear by <0.001); cc_v1 `ideas.md` #8 flags SOAP "may win at >=350M"; the architecture, batch,
  and data are fixed by rule. The cheap v1/v2 levers (MuonEq, train-steps trim, per-role LR/WD,
  mu-sched) are actually *faster* per step (~147 ms) and should transfer.
- **Interpretation**: Transferable = orthogonalize-then-row-normalize -> higher LR; per-role LR/WD/
  schedule; horizon trim; explore->exploit scheduling. Non-transferable = exact constants, subset-SOAP
  machinery, the 3.28-specific stop, single-number records.
- **Dependencies**: C04, C05, C09
- **Tags**: generalization, limits, wallclock-tax, scale-bound, overfit

## C17: Seeds needed scale inversely with the squared effect size
- **Statement**: From the seed-reverify data one can read off how many seeds are needed to call a step
  improvement significant, and the answer scales the way a standard two-sample test predicts: a large
  gain needs only a seed or two, a strong single lever needs a few, a near-frontier tie needs many,
  and a sub-handful-of-steps difference is below the floor entirely. This explains the agents'
  observed protocol — a few-seed reproducer for the early, larger levers and much larger seed groups
  for resolving frontier ties — as a seed budget correctly matched to the effect size at each stage.
  Below the floor, the quantized step metric is the wrong tool and a continuous loss metric should be
  used instead.
- **Status**: supported
- **Falsification criteria**: If a 10-step difference were reliably resolved with 3 seeds (contra the
  ~16 the formula predicts), or the floor sigma were far from ~15 steps, the rule would be miscalibrated.
- **Proof**: [E07]
- **Evidence basis**: §21. With frontier step-std sigma ~15 (dense configs: `v3opus_v114` 14.1,
  `v3cdx_nosphere` 21.4), n ~ 8*sigma^2/Delta^2 gives ~1 seed for a 200-step gain, 2-3 for 50 steps,
  ~16 for 10 steps, impractical below ~5 steps. The marginal v1 lever embed-init (-0.00091 ~ 0.9 sigma)
  needed all 3 seeds and barely cleared; the `seed_reverify` wave ran 8-16 seeds per group for frontier
  ties.
- **Interpretation**: Below ~15 steps `step_to_3_28` is too quantized — rank on `min_val_loss`
  (continuous, std ~0.001) instead; match the seed budget to the effect size.
- **Dependencies**: C09
- **Tags**: seeds, significance, noise-floor, methodology
