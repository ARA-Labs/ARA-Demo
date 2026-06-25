# Figure: v3 W258 leave-one-out pruning

**Source.** `record_configs/20260515_codex_v3_nosphere_2949/pruning.png` (title "codex v3 W258 LOO
pruning"). Screenshot: `v3_pruning.png`. Data: `src/configs/v3_pruning_data.json`, transcribed in
`evidence/tables/v3_pruning_table.md`.

**Figure type.** quantitative_plot (horizontal bar chart).
**Extraction method.** exact_from_labels (bars annotated; cross-checked against JSON).
**Reading confidence.** high.

**Axes.** x = "delta val_loss when removed (positive means component helped)", linear, 0.000 to
~0.0053; y = ablation. Dashed reference at 0.001, dotted at 0.003. W258 leave-one-out sweep at step
2949.

**Content (exact deltas from the JSON).** Two red bars past 0.003 — **nosoap +0.00528** and
**noradial +0.00374** — are the indispensable mechanisms (removal collapses the tail). Two orange
bars — novsoap +0.00228, nosoft +0.00186 — and nocontra +0.00133 are clearly load-bearing. Grey
bars below: nolacv +0.00075, **nosphere-notangent +0.00070** (the combined two-removal control, which
regresses), noqkcontrascale +0.00047, notailradial +0.00019, nolacvfloor +0.00003.

**Key reading.** The submitted "nosphere" baseline already has the sphere-lookahead **pull** removed
and is the n=16 reference (score +0.006332 at step 2949); every charted ablation removes a *further*
component and is positive (helped), so all charted mechanisms are kept. The combined
`nosphere-notangent` removing both sphere terms regresses (+0.00070), proving the two removals do not
compose.

**Supports.** C06.
