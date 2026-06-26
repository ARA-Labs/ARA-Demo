# Table — v3 record per-seed validation (n=16, steps 2949 & 3020)

The submitted v3 "nosphere" record: validation loss at the submitted bin (step 2949) and at the training
endpoint (step 3020) over 16 non-cherry-picked seeds. Transcribed verbatim from the record README.

Cohort stats @ step 2949: **n = 16, mean = 3.27886125, std = 0.00125939, (3.28 − μ)·√n = 0.00455500**
(≥ 0.004 ⇒ passes; z = 3.5038, one-sided p = 0.000229). Statistically viable to ~2940 at N=16.

| Seed | val @ 2949 | val @ 3020 |
|---:|---:|---:|
| 0 | 3.27809 | 3.27591 |
| 1 | 3.27936 | 3.27718 |
| 2 | 3.27863 | 3.27648 |
| 3 | 3.27889 | 3.27677 |
| 4 | 3.28034 | 3.27817 |
| 5 | 3.27808 | 3.27592 |
| 6 | 3.27846 | 3.27629 |
| 7 | 3.27681 | 3.27461 |
| 8 | 3.28060 | 3.27848 |
| 9 | 3.27930 | 3.27713 |
| 10 | 3.27798 | 3.27584 |
| 11 | 3.28048 | 3.27832 |
| 12 | 3.28003 | 3.27786 |
| 13 | 3.27682 | 3.27468 |
| 14 | 3.27762 | 3.27546 |
| 15 | 3.28029 | 3.27812 |
| **Mean** | **3.27886** | **3.27670** |

**Source:** `record_configs/20260515_codex_v3_nosphere_2949/README.md:29-47`. Supports C06, C07, C08;
figure [../figures/v3_loss_curves.md](../figures/v3_loss_curves.md). Note: this N=16 record cohort
(mean 3.27886125 @ 2949) is a *different* cohort from the W258 leave-one-out baseline
(mean 3.278416875 @ 2949 in [v3_component_pruning.md](v3_component_pruning.md)).
