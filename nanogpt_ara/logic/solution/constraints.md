# Constraints & Limitations

The honest envelope of these results (INSIGHTS.md §20, §9, §18). Read before transferring anything.

## Boundary conditions (fixed by the benchmark)
- **Model**: GPT-124M (12 layers, dim 768, vocab 50304) — fixed.
- **Data**: FineWeb-10B — fixed.
- **Batch**: 8 x 64 x 1024 tokens — fixed.
- **Objective**: `step_to_3_28` (first val <= 3.28); wall-clock and per-step FLOPs are explicitly free.
- **Allowed changes**: optimizer, schedule, initialization, a few hyperparameters only.
- Every conclusion (which optimizer, which schedule, which per-role split) holds *only inside this box*
  (A1). These are results about optimizing a fixed target, not about optimizers in general.

## Known limitations
1. **Wall-clock / FLOP tax (graded).** The v3 recipe trades ~17% fewer steps for ~20% more compute per
   step (188 vs 157.5 ms). On a wall-clock- or FLOP-budgeted run the expensive v3 machinery (SOAP/
   Aurora) can be a net loss. The cheap v1/v2 levers (MuonEq, train-steps trim, per-role LR/WD,
   mu-sched) are *strictly favorable* (fewer steps AND cheaper per step, ~147 ms) and should transfer;
   the v3 SOAP/Aurora machinery is benchmark-specific (worth it only when per-step cost is free).
2. **Overfit to the exact 3.28 threshold.** Frontier hitters cluster `min_val_loss` ~3.2765-3.2773
   (a median only ~2.6-3.3e-3 below 3.28; ~17% clear by <0.001). The runs are tuned (via `train_steps`
   and the power-cooldown stop) to cross *3.28* as early as possible and halt — not to minimize loss.
   `step_to_3_28` does NOT generalize to "steps to reach loss X" for any other X (3.27 would need more
   steps and a different schedule; 3.29 fewer). The metric and recipe are entangled with the number
   3.28.
3. **Scale-bound to 124M.** The "Muon's orthogonalization beats heavier second-order" conclusion holds
   because NS already captures the curvature at this size; the agents explicitly flag SOAP "may win at
   >=350M" (cc_v1 `ideas.md` #8). The whole "where the gains live" map could invert at larger scale.
4. **Records are best-of-N over a noisy floor.** The headline 2880-2885 is a lucky-seed tail with a
   ~9-12% per-config miss rate; seed-verified is ~2930. Any single quoted step count overstates by
   ~30-50 steps. Use seed-verified medians (and `min_val_loss` below ~15-step resolution).
5. **The v3 frontier is one shared artifact, not two independent confirmations.** The two agents' v3
   records are byte-identical (shared public-PR pool), so the frontier has not been independently
   replicated in the scientific sense. The independent-replication evidence is the weaker v1 overlap.
6. **Validation-cadence coupling.** Part of the train-steps "gain" is a measurement artifact of the
   logging cadence; comparisons below ~15 steps are within the noise floor and should be made on a
   continuous metric.

## Assumptions carried by the recipe
- A2: per-step compute is free (the recipe spends it freely; see limitation 1).
- A3: the 3.28 threshold is exact and is the thing being crossed-and-stopped-on (see limitation 2).
- The frozen architecture/init structure (two-optimizer partition, zero-init output proj, 15*tanh
  logit softcap) is assumed; per-role splits are defined relative to it.

## What transfers vs what does not
| Transferable (mechanism) | Non-transferable (artifact) |
|---|---|
| orthogonalize then per-row normalize -> raise LR | the exact constants (0.0375, power_c, ...) |
| differentiate LR / WD / schedule per parameter role | the subset-SOAP machinery (scale/benchmark-specific) |
| trim the training horizon | the 3.28-specific stop step |
| schedule exploration->exploitation in optimizer-space | single-number best-of-N records |
| seed-verify and report medians + miss-rate | the v3 recipe as "independent replication" |
