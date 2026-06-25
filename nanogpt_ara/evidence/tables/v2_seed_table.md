# Table — v2 record, 16-seed validation at step 3037

- **Source:** `record_configs/20260515_codex_v2_legal_3037/README.md:17-46` (transcribed exactly)
- **Type:** results table (native markdown in source); this is the **compliant** cohort (post-quarantine)

## Significance (at step 3037)

```text
n = 16
mean val loss = 3.27853000
std            = 0.00080602
(3.28 - mu) * sqrt(n) = 0.00588000
```

Exceeds the Track-3 threshold `0.004`. With σ=0.0013, z = 4.5231, one-sided p = 3.05e-06
(p < 0.001). Supports [C06](../../logic/claims.md), [C08](../../logic/claims.md) (this is the
byte-identical-compliant rebuild, not the quarantined v12-derived stack).

## Per-seed validation loss @ 3037

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

The submitted variant is `legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py`. The
journal's anti-val-spam scan found step 3025 does *not* pass (mean 3.279132, score 0.002454); 3037
is the earliest common checkpoint that does.
