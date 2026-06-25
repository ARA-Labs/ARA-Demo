# Seeds needed to declare a step-count gain significant

**Source**: §21.1 table in research_insights/INSIGHTS.md (derived from the `seed_reverify` wave: 152
runs across 13 config groups; frontier step-std sigma ~15 from dense-validation groups).
**Caption**: "Seeds/arm to confirm a claimed gain, from n ~ 8*sigma^2/Delta^2 (2-sample, ~2 sigma),
with frontier step-std sigma ~15 steps."
**Extraction type**: raw_table

| Claimed gain | ~ sigma-multiple (sigma~15 steps) | Seeds/arm to confirm | Maps to |
|---:|---|---:|---|
| 200 steps | ~13 sigma | 1 | a new optimizer class |
| 100 steps | ~7 sigma | 1-2 | a major lever |
| 50 steps | ~3.3 sigma | 2-3 | a strong single lever (e.g. MuonEq) |
| 25 steps | ~1.7 sigma | ~3-4 | a mid-pack component |
| 10 steps | ~0.7 sigma | ~16 | frontier tie-breaks |
| <5 steps | <0.3 sigma | impractical | below the floor |

**Measured noise floor (pooled)**: `final_val_loss` std ~0.0009-0.0011 within a config (e.g.
`v2cc_v15_ts3040` 0.00095, `v1cc_v12_ts3100` 0.00100, `v3opus_v114_ts2930` 0.00099); frontier
`step_to_3_28` std ~14-21 steps under dense validation (`v3opus_v114` 14.1, `v3cdx_nosphere_ts2940`
21.4); coarse-cadence configs read step-std ~0; pooled miss rate 14/152 = 9%.

**Protocol match**: v1 levers used 3-seed reproducers (each >=~1.7 sigma); the marginal embed-init
(-0.00091 ~ 0.9 sigma) needed all 3 and barely cleared; `seed_reverify` used 8-16 seeds for frontier
ties (~10-25 step differences). Below ~15 steps, rank on `min_val_loss` (continuous), not step count.

Maps to claims: C09, C16, C17.
