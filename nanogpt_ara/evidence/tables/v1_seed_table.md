# Table: v1 record (bin 3205) — 16-seed reproducibility

**Source.** `record_configs/20260515_codex_v1_v12iso_3205/README.md` (transcribed verbatim).
Stack: v12iso / MuSched. Validated over n=16 non-cherry-picked seeds (0..15), distinct `--seed N`.

## Cohort statistics at step 3205
```
n = 16
mean val loss = 3.27897187
std            = 0.00069831
(3.28 - mu) * sqrt(n) = 0.00411250
```
Exceeds the Track 3 threshold of 0.004. Equivalently, with sigma=0.0013, z = 3.1635, one-sided
p = 0.00078 (p < 0.001).

## Per-seed val_loss at step 3205
| Seed | 3205 val |
| -: | -: |
| 0 | 3.27827 |
| 1 | 3.27802 |
| 2 | 3.27853 |
| 3 | 3.28004 |
| 4 | 3.27902 |
| 5 | 3.27968 |
| 6 | 3.27834 |
| 7 | 3.27823 |
| 8 | 3.27855 |
| 9 | 3.27813 |
| 10 | 3.27903 |
| 11 | 3.27991 |
| 12 | 3.27892 |
| 13 | 3.27977 |
| 14 | 3.27969 |
| 15 | 3.27942 |
| **Mean** | **3.27897** |

**Supports.** C08 (submitted bin passes the fixed-step cohort gate).
