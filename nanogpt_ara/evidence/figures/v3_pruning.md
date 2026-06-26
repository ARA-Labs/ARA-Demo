# Figure — v3 W258 leave-one-out pruning

![v3 W258 LOO pruning](v3_pruning.png)

- **Source:** `record_configs/20260515_codex_v3_nosphere_2949/pruning.png` (data: `pruning_data.json`;
  "W258 leave-one-out sweep at step 2949; deltas relative to the nosphere baseline from the same sweep").
- **Figure type:** quantitative_plot (horizontal bar chart).
- **Extraction method:** exact_from_labels — printed Δ labels cross-checked against `pruning_data.json`.
- **Reading confidence:** high.

**What it shows.** Title "codex v3 W258 LOO pruning". X-axis = "delta val_loss when removed (positive
means component helped)", 0.000 → ≈0.0053. Bars largest→smallest: **nosoap +0.00528**, **noradial
+0.00374** (both red, the load-bearing pair), **novsoap +0.00228**, **nosoft +0.00186**, **nocontra
+0.00133** (orange), nolacv +0.00075, nosphere-notangent +0.00070, noqkcontrascale +0.00047, notailradial
+0.00019, nolacvfloor +0.00003. Dashed/dotted vertical guides at ≈0.001 and ≈0.003.

**Reading:** SOAP (extended to MLP+V) and outward-radial dampening are the most load-bearing; V-SOAP,
Soft-Muon, and Contra follow. The bottom entries (nolacvfloor, notailradial, noqkcontrascale,
nosphere-notangent) are small — and the **sphere-lookahead pull** is the one removed for the "nosphere"
record (its own removal, not shown as a bar here because it *is* the baseline; the related
`nosphere-notangent` shows that removing the *second* sphere term too costs +0.00070 and breaks the
boundary).

**Supports:** C08 (nosoap/noradial load-bearing), C09 (the nosphere prune + non-composition). Full table:
[../tables/v3_component_pruning.md](../tables/v3_component_pruning.md).
