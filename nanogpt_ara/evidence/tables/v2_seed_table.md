# Table: v2 legal record (bin 3037) — 16-seed reproducibility

**Source.** `record_configs/20260515_codex_v2_legal_3037/README.md` (transcribed verbatim).
Stack: legal_v12opt (byte-identical-compliant rebuild). n=16 non-cherry-picked seeds (0..15).

## Cohort statistics at step 3037
```
n = 16
mean val loss = 3.27853000
std            = 0.00080602
(3.28 - mu) * sqrt(n) = 0.00588000
```
Exceeds the threshold 0.004. With sigma=0.0013, z = 4.5231, one-sided p = 3.05e-06 (p < 0.001).

## Per-seed val_loss at step 3037
| Seed | 3037 val |
| -: | -: |
| 0 | 3.27825 |
| 1 | 3.27850 |
| 2 | 3.27921 |
| 3 | 3.27833 |
| 4 | 3.27836 |
| 5 | 3.27708 |
| 6 | 3.28031 |
| 7 | 3.27841 |
| 8 | 3.27860 |
| 9 | 3.27786 |
| 10 | 3.27959 |
| 11 | 3.27801 |
| 12 | 3.27791 |
| 13 | 3.27793 |
| 14 | 3.27965 |
| 15 | 3.27848 |
| **Mean** | **3.27853** |

**Note.** The single-seed legal frontier reached step ~2962, but the fixed-step cohort failed below
~3012; 3037 is the earliest passing checkpoint (the +75-step conservative submission). Supports C04,
C05, C08.
