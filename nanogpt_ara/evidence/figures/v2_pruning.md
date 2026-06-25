# Figure: v2 component pruning (leave-one-out)

**Source.** `record_configs/20260515_codex_v2_legal_3037/pruning.png` (title "codex v2 component
pruning"). Screenshot: `v2_pruning.png`. Data: `src/configs/v2_pruning_data.json`, transcribed in
`evidence/tables/v2_pruning_table.md`.

**Figure type.** quantitative_plot (horizontal bar chart).
**Extraction method.** exact_from_labels (bars annotated; cross-checked against JSON).
**Reading confidence.** high.

**Axes.** x = "delta val_loss when removed (positive means component helped)", linear; y = component
removed. Pruning-rerun at step 3037.

**Content (exact deltas from the JSON).** Largest first: **noMuonEq +0.00353**, **noRoleLR +0.00292**
(the two dominant load-bearing components), then noLookahead +0.00117 (tie with noPolarExpress
+0.00117), noEtaMin +0.00097, noEmbedInit +0.00092, noRoleWD +0.00041, noContraMuon +0.00008
(near-noise). Small n=3 schedule ablations sit further out: noMuSched +0.00459, cf1.0 +0.00388.

**Supports.** C04 (role-split LR and the row-normalized MuonEq update are the dominant levers;
Contra-Muon is decorative at this operating point). n=8 per ablation (n=3 for cf1.0 / noMuSched).
