# Table: v2 leave-one-out component pruning

**Source.** `src/configs/v2_pruning_data.json` (copied verbatim from
`record_configs/20260515_codex_v2_legal_3037/pruning_data.json`). "pruning-rerun aggregate for
codex_v2_legal_3037 at 3037 steps", `target_step = 3037`. n=8 per row (n=3 for cf1.0 and noMuSched).
`delta` positive ⇒ component helped. Baseline (legal3037, full stack) mean 3.27885, score
0.0032526911934580745.

| Component removed | mean | delta | score | std | n |
| --- | -: | -: | -: | -: | -: |
| (baseline: legal_v12opt) | 3.27885 | 0.0 | 0.00325269 | — | 8 |
| noContraMuon | 3.27893 | +0.00008 | 0.00302642 | 0.00114 | 8 |
| noRoleWD | 3.27926 | +0.00041 | 0.00209304 | 0.00070 | 8 |
| noEmbedInit | 3.27977 | +0.00092 | 0.00065054 | 0.00124 | 8 |
| noEtaMin | 3.27982 | +0.00097 | 0.00050912 | 0.00095 | 8 |
| noPolarExpress | 3.28002 | +0.00117 | −0.00005657 | 0.00061 | 8 |
| noLookahead | 3.28002 | +0.00117 | −0.00005657 | 0.00091 | 8 |
| **noRoleLR** | **3.28177** | **+0.00292** | −0.00500632 | 0.00096 | 8 |
| **noMuonEq** | **3.28238** | **+0.00353** | −0.00673166 | 0.00096 | 8 |
| cf1.0 | 3.28273 | +0.00388 | −0.00472850 | 0.00127 | 3 |
| noMuSched | 3.28344 | +0.00459 | −0.00595825 | 0.00054 | 3 |

**Reading.** `noMuonEq` and `noRoleLR` dominate the removal deltas (the row-normalized update and the
per-role LR split are the load-bearing levers); `noLookahead` and the schedule/init terms are
positive; `noContraMuon` is near-noise. Supports C04.
