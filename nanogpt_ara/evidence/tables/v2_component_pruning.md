# Table — v2 component pruning (leave-one-out)

Per-component contribution from the "pruning-rerun codex_v2_legal" sweep **at step 3037, n=8** (cf1.0 and
noMuSched at n=3) — NOT the 3037 record cohort (which is n=16). `delta` = val_loss when removed minus
baseline (positive ⇒ helped). Baseline `legal3037-baseline`: mean 3.27885, n=8, score 0.0032526912.
Transcribed verbatim from `pruning_data.json`. Sorted most→least load-bearing.

| Component removed | Δ val_loss (exact) | Δ (figure) | mean | n | score (3.28−μ)·√n | std |
|---|---:|---:|---:|---:|---:|---:|
| noMuSched | 0.004590000000000316 | +0.00459 | 3.28344 | 3 | −0.005958254778037512 | 0.00054 |
| cf1.0 (cooldown floor) | 0.0038800000000001056 | +0.00388 | 3.28273 | 3 | −0.004728498704663245 | 0.00127 |
| noMuonEq | 0.003530000000000033 | +0.00353 | 3.28238 | 8 | −0.006731656556896071 | 0.00096 |
| noRoleLR | 0.0029200000000000337 | +0.00292 | 3.28177 | 8 | −0.005006316010800896 | 0.00096 |
| noLookahead | 0.0011700000000001154 | +0.00117 | 3.28002 | 8 | −0.0000565685424952944 | 0.00091 |
| noPolarExpress | 0.0011700000000001154 | +0.00117 | 3.28002 | 8 | −0.0000565685424952944 | 0.00061 |
| noEtaMin | 0.0009700000000001374 | +0.00097 | 3.27982 | 8 | 0.0005091168824538813 | 0.00095 |
| noEmbedInit | 0.000920000000000254 | +0.00092 | 3.27977 | 8 | 0.0006505382386908613 | 0.00124 |
| noRoleWD | 0.00041000000000002146 | +0.00041 | 3.27926 | 8 | 0.002093036072312076 | 0.0007 |
| noContraMuon | 0.00008000000000008001 | +0.00008 | 3.27893 | 8 | 0.003026417023478153 | 0.00114 |

**Reading.** The inherited mu-schedule, cooldown floor (cf1.0), and MuonEq are the largest contributors;
**role-specific LR (noRoleLR)** is the biggest *v2-specific* addition and **lookahead** a moderate one
(C04); Contra-Muon is nearly free (droppable tier). **Source:**
`record_configs/20260515_codex_v2_legal_3037/pruning_data.json`. Supports C04, C09. Figure:
[../figures/v2_pruning.md](../figures/v2_pruning.md).
