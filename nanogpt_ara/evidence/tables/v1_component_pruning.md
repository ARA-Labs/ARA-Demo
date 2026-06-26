# Table — v1 component pruning (leave-one-out)

Per-component contribution from the "pruning-rerun codex_v1_v12iso" sweep **at the 3195-step screen,
n=8** (NOT the 3205 record cohort). `delta` = val_loss when the component is removed minus the baseline
(positive ⇒ the component helped). Baseline `v12iso-baseline`: mean 3.27907, n=8, score 0.0026304372.
Transcribed verbatim from `pruning_data.json`. Sorted most→least load-bearing.

| Component removed | Δ val_loss (exact) | Δ (figure) | mean | score (3.28−μ)·√n | std |
|---|---:|---:|---:|---:|---:|
| noTailEMA | 0.0025100000000000122 | +0.00251 | 3.28158 | −0.004468914857099368 | 0.00074 |
| noMuon2f | 0.0022899999999999032 | +0.00229 | 3.28136 | −0.0038466608896548975 | 0.00085 |
| noMuSched | 0.0009100000000001884 | +0.00091 | 3.27998 | 0.00005656854249403832 | 0.00067 |
| noErrorFeedback | 0.0007600000000000939 | +0.00076 | 3.27983 | 0.00048083261120623416 | 0.00075 |
| noAggMo3 | 0.00024000000000024002 | +0.00024 | 3.27931 | 0.00195161471607384 | 0.00056 |
| noTailRD | 0.00017000000000022553 | +0.00017 | 3.27924 | 0.0021496046148061143 | 0.00086 |
| noTailFeedback | 0.000140000000000029 | +0.00014 | 3.27921 | 0.0022344574285490556 | 0.00059 |
| noResRMSNorm | 0.00011000000000027654 | +0.00011 | 3.27918 | 0.0023193102422907415 | 0.00083 |
| noLateLR | 0.00002000000000013 | +0.00002 | 3.27909 | 0.00257386868351831 | 0.00072 |
| noBeta2Thaw | −0.00001000000000007 | −0.00001 | 3.27906 | 0.002658721497261252 | 0.00071 |
| noMomRefresh | −0.00003999999999982 | −0.00004 | 3.27903 | 0.0027435743110029373 | 0.00074 |
| noResPulse | −0.00007000000000001 | −0.00007 | 3.27900 | 0.0028284271247458787 | 0.00086 |

**Reading.** Tail-EMA evaluation and factorized hidden preconditioning (Muon2F) are the load-bearing
pair; the three bottom rows are at/below zero (removing them does not hurt) → droppable per the
pruning rule (C09). **Source:** `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json`.
Supports C02, C03, C09. Figure: [../figures/v1_pruning.md](../figures/v1_pruning.md).
