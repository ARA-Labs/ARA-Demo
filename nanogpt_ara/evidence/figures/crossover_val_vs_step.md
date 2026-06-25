# Figure: training-curve crossover (val_loss vs step, baseline vs v3 record)

**Source**: §8 table in research_insights/INSIGHTS.md (val_loss vs step extracted from `train.log` of
baseline `00001` (3500 steps) and record `07070-v88-aurora-proj-s2` (2900 steps)).
**Caption**: "Val_loss at matched steps. Delta = record - baseline; positive = record is worse
(behind). The record loses early, crosses at ~step 1750, then wins decisively."
**Axes**: X = training step; Y = validation loss.
**Extraction type**: figure_data

| step | baseline val_loss | v3 record val_loss | Delta (record - baseline) |
|---:|---:|---:|---:|
| 125 | 4.6436 | 4.4730 | -0.171 (ahead) |
| 375 | 3.9244 | 3.9525 | +0.028 (behind, max deficit) |
| 1000 | 3.6199 | 3.6287 | +0.009 (behind) |
| 1625 | 3.4851 | 3.4938 | +0.009 (behind) |
| 1750 | 3.4642 | 3.4626 | -0.002 (crossover) |
| 2000 | 3.4277 | 3.4103 | -0.017 (ahead) |
| 2500 | 3.3677 | 3.3240 | -0.044 (ahead) |
| 2750 | 3.3409 | 3.2915 | -0.049 (far ahead) |

**Contrast (no late payoff)**: full SOAP `00182-soap-lr3e-2` is behind throughout — step 1000: 3.828
vs 3.620; step 3000: 3.399 vs 3.316 — and asymptotes at 3.38876, never reaching 3.28
(`step_to_3_28=None`). The crossover is a property of the specific (conditioned) recipe, not a general
"slow-start-is-fine" rule.

**Mechanism**: Contra-Muon (-0.2, ramping off by step 1920) + higher LR (0.0375) trade early loss for
conditioning; the crossover (~1750) sits where Contra anneals off; the compressed 2900-step convex
cooldown steepens the final drop. Record hits 3.28 at step 2885 vs baseline 3500.

Maps to claims: C08, C14.
