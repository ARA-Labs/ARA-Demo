# Table: v1 leave-one-out component pruning

**Source.** `src/configs/v1_pruning_data.json` (copied verbatim from
`record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json`). "pruning-rerun aggregate for
codex_v1_v12iso at the original 3195-step screen", `target_step = 3195`. n=8 per row. `delta` =
mean(component removed) − baseline mean; positive ⇒ component helped. Baseline (full stack) mean
3.27907, score 0.0026304372260136043.

| Component removed | mean | delta | score | std |
| --- | -: | -: | -: | -: |
| (baseline: full v12iso) | 3.27907 | 0.0 | 0.00263044 | — |
| noResPulse | 3.27900 | −0.00007 | 0.00282843 | 0.00086 |
| noMomRefresh | 3.27903 | −0.00004 | 0.00274357 | 0.00074 |
| noBeta2Thaw | 3.27906 | −0.00001 | 0.00265872 | 0.00071 |
| noLateLR | 3.27909 | +0.00002 | 0.00257387 | 0.00072 |
| noResRMSNorm | 3.27918 | +0.00011 | 0.00231931 | 0.00083 |
| noTailFeedback | 3.27921 | +0.00014 | 0.00223446 | 0.00059 |
| noTailRD | 3.27924 | +0.00017 | 0.00214960 | 0.00086 |
| noAggMo3 | 3.27931 | +0.00024 | 0.00195161 | 0.00056 |
| noErrorFeedback | 3.27983 | +0.00076 | 0.00048083 | 0.00075 |
| noMuSched | 3.27998 | +0.00091 | 0.00005657 | 0.00067 |
| **noMuon2f** | **3.28136** | **+0.00229** | −0.00384666 | 0.00085 |
| **noTailEMA** | **3.28158** | **+0.00251** | −0.00446891 | 0.00074 |

**Reading.** Only `noTailEMA` and `noMuon2f` drive the score negative (target missed) when removed —
the two load-bearing components. The tail-residual mechanics (pulse/refresh/thaw/late-LR) are within
the ~0.001 noise band; three are marginally negative. Supports C03.
