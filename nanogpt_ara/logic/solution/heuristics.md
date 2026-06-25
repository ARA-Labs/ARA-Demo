# Heuristics

Convergence tricks and search-discipline rules that the frontier depends on. Each `Code ref` points to
a stub in `src/execution/`. `Source` cites the INSIGHTS.md section.

## H01: Row-normalize the momentum BEFORE Newton-Schulz, not after
- **Rationale**: Equalizing per-row momentum norm before orthogonalization gives NS a better-
  conditioned input, so the orthogonalization is faithful; doing it after only rescales an
  already-orthogonal update, and doing both double-corrects the same imbalance.
- **Sensitivity**: high — pre-NS is the strongest single Muon-internal lever; post-NS is materially
  weaker; the two do not stack.
- **Bounds**: per-row L2 norm with a small eps; redundant once Aurora row-rescale is present (drop one).
- **Code ref**: [src/execution/muon_pipeline.py](../../src/execution/muon_pipeline.py)
- **Source**: §2.B.3, §14.4

## H02: Once the update magnitude is normalized, raise the global learning rate
- **Rationale**: Per-row normalization (MuonEq/Aurora) clamps the per-step update variance, so a
  bigger global step stays stable — "normalization buys a higher LR." The right LR is a property of
  the whole preconditioning stack, so re-tune it whenever the stack changes.
- **Sensitivity**: high — LR moved non-monotonically (0.025 -> 0.045 -> 0.0375) across waves.
- **Bounds**: push LR up after adding normalization; pull it back down after adding heavier
  preconditioning (SOAP/Aurora) that re-shapes the geometry.
- **Code ref**: [src/execution/muon_pipeline.py](../../src/execution/muon_pipeline.py)
- **Source**: §5.2, §13.2

## H03: Trim the training horizon and validate densely near the end
- **Rationale**: The baseline over-trains in its final cooldown, and the step metric is quantized by a
  coarse validation cadence, so shortening the horizon and validating every few steps near the
  expected crossing both reach 3.28 earlier — down to a hard floor.
- **Sensitivity**: high (biggest single "free" lever) — but partly a measurement artifact.
- **Bounds**: trim until the forced near-end validation still hits; below the true crossing the target
  genuinely misses. Decouple the schedule horizon from the stop step.
- **Code ref**: [src/execution/schedule.py](../../src/execution/schedule.py)
- **Source**: §2.A.1, §6.1, §8.3, §15.4

## H04: Differentiate LR, weight decay, and cooldown onset per parameter role
- **Rationale**: Attention and MLP matrices differ in scale/curvature/sensitivity, so each role wants
  a different step size, shrinkage, and anneal timeline; the auxiliary AdamW group is also not already
  optimal and benefits from a retune.
- **Sensitivity**: medium — each axis is a small-to-mid lever, but they accumulate.
- **Bounds**: attn LR ~0.5-0.6x MLP; attn WD < MLP (0.0275 vs 0.03125); per-group cooldown onset.
- **Code ref**: [src/execution/schedule.py](../../src/execution/schedule.py)
- **Source**: §2.C.1, §13.3, §15.3, §14.3

## H05: Apply SOAP only to MLP+V, amortize the eigenbasis, norm-preserve, and trust-gate it
- **Rationale**: Second-order preconditioning helps only where curvature is anisotropic and persistent
  (MLP, value projection) and duplicates Muon where it is not (Q/K). Refreshing the eigenbasis every
  ~10 steps makes it affordable; preserving the Frobenius norm makes it compose with Muon; a per-element
  trust gate catches the cases where the stale basis would mislead.
- **Sensitivity**: high — biggest hitting v3 lever, but only with the right subset and the gate.
- **Bounds**: subset = MLP fc/proj + attn V (not Q/K); refresh freq ~10; denom power 0.5; V blend ~0.95;
  trust cos > 0.20 with an early floor ~0.45 fading by ~1625.
- **Code ref**: [src/execution/soap_subset.py](../../src/execution/soap_subset.py)
- **Source**: §5.3, §16

## H06: Schedule exploration->exploitation in optimizer-space, not just LR-space
- **Rationale**: Early decorrelation from the greedy gradient (Contra-Muon) buys conditioning at the
  cost of slightly slower early loss; annealing it off and softening the orthogonalization late settles
  cleanly into the minimum. This engineered curriculum *is* the lose-early/win-late crossover.
- **Sensitivity**: medium — the ramp windows must bracket the crossover (~step 1750).
- **Bounds**: Contra coeff -0.2 -> 0 by ~1920; soft-Muon blend 0 -> 0.80 over 2400-2890; mu warmup/cool.
- **Code ref**: [src/execution/muon_pipeline.py](../../src/execution/muon_pipeline.py)
- **Source**: §8.1, §16.4, §17

## H07: Use a convex (power>1) per-role cooldown and decouple the horizon from the stop step
- **Rationale**: A convex cooldown holds LR higher through mid-training (preserving the win-late
  descent) then drops steeply to settle the minimum; computing the schedule for a longer horizon than
  the stop step harvests the trajectory while LR is still nonzero. At a sub-0.001 target margin this
  shape is the last thing standing between the recipe and the threshold.
- **Sensitivity**: high — removing it makes all frontier seeds miss (the single most critical lever).
- **Bounds**: power ~1.2; t_end > stop (e.g. 2985 vs 2900, LR at stop ~1.8% of flat); per-role `power_c`.
- **Code ref**: [src/execution/schedule.py](../../src/execution/schedule.py)
- **Source**: §14.1, §15

## H08: Match the seed budget to the effect size; rank tiny gains on a continuous metric
- **Rationale**: The seed noise floor is the same size as a single-lever gain, so the number of seeds
  needed scales inversely with the squared effect size; below the step-quantization floor the integer
  step metric cannot resolve the difference and a continuous loss metric should be used.
- **Sensitivity**: high (governs whether a claim is real).
- **Bounds**: ~1 seed for a 200-step gain, 2-3 for ~50 steps, ~16 for ~10 steps, impractical below ~5;
  below ~15 steps rank on `min_val_loss` (std ~0.001), not `step_to_3_28`.
- **Code ref**: [src/execution/diagnostics.py](../../src/execution/diagnostics.py)
- **Source**: §9, §21

## H09: Kill diverging runs early instead of letting them complete
- **Rationale**: The dangerous instabilities are not random NaNs but predictable consequences of a
  mis-scaled preconditioner (slow crawl), a pathological HP magnitude (spike-and-recover), or a
  normalization x warmup interaction (NaN/no-learn) — all detectable early — so a bad trajectory can
  be cancelled rather than wasting the full budget.
- **Sensitivity**: medium — saves compute; the cutoff threshold is a judgment call.
- **Bounds**: all three signatures are visible by step ~750; e.g. early-kill once val exceeds the
  baseline by a clear margin (~+0.29 at step 2000 for SPM).
- **Code ref**: [src/execution/diagnostics.py](../../src/execution/diagnostics.py)
- **Source**: §11

## H10: Re-test every imported lever at the current backbone (sign is context-dependent)
- **Rationale**: A method's effect flips with what else is in the recipe and which parameter subset it
  touches; gains measured against vanilla Muon do not transfer additively, so never assume a public-PR
  delta carries over — re-measure it in the live stack.
- **Sensitivity**: high — the experiment's dominant confounder.
- **Bounds**: applies to every borrowed component (SOAP full vs subset, Muon^2 in vs out of stack,
  NorMuon redundancy); decide inclusion by an in-stack ablation, not the source's headline.
- **Code ref**: [src/execution/soap_subset.py](../../src/execution/soap_subset.py)
- **Source**: §3.2, §5.3, §2.D.3
