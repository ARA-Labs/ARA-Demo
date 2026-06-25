# Table — v3 record, 16-seed validation at step 2949 (and 3020)

- **Source:** `record_configs/20260515_codex_v3_nosphere_2949/README.md:18-47` (transcribed exactly)
- **Type:** results table (native markdown in source)

## Significance (at step 2949)

```text
n = 16
mean val loss = 3.27886125
std            = 0.00125939
(3.28 - mu) * sqrt(n) = 0.00455500
```

Exceeds the Track-3 threshold `0.004`. With σ=0.0013, z = 3.5038, one-sided p = 0.000229
(p < 0.001). The runs continue to `train_steps=3020`; the submitted bin is the logged step-2949
checkpoint. Supports [C06](../../logic/claims.md), [C11](../../logic/claims.md). The stack is
statistically viable to ~2940 at N=16.

## Per-seed validation loss @ 2949 and @ 3020

| Seed | 2949 val | 3020 val |
| -: | -: | -: |
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

The 2949 → 3020 gap (cohort mean 3.27886 → 3.27670) shows the run keeps descending well past the
submitted bin; 2949 is the earliest checkpoint clearing the significance gate, not the run's lowest
loss.
