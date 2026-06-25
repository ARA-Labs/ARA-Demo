# Figure: v1 component pruning (leave-one-out)

**Source.** `record_configs/20260515_codex_v1_v12iso_3205/pruning.png` (title "codex v1 component
pruning"). Screenshot: `v1_pruning.png`. Underlying data: `src/configs/v1_pruning_data.json`,
transcribed in `evidence/tables/v1_pruning_table.md`.

**Figure type.** quantitative_plot (horizontal bar chart).
**Extraction method.** exact_from_labels (each bar is annotated with its delta).
**Reading confidence.** high (values printed on bars; cross-checked against the JSON).

**Axes.** x = "delta val_loss when removed (positive means component helped)", linear, 0.0000 to
~0.0030; y = component removed (one bar each). Dashed vertical reference at 0.0010, dotted at 0.0030.

**Content (top to bottom, exact deltas from the JSON).** Two orange bars stand out past the 0.0010
line: **noTailEMA +0.00251** and **noMuon2f +0.00229** — the load-bearing components. Then grey bars
below the noise band: noMuSched +0.00091, noErrorFeedback +0.00076, noAggMo3 +0.00024,
noTailRD +0.00017, noTailFeedback +0.00014, noResRMSNorm +0.00011, noLateLR +0.00002,
noBeta2Thaw −0.00001, noMomRefresh −0.00004, noResPulse −0.00007 (the last three slightly negative,
i.e. removal marginally helped — pure tuning).

**Supports.** C03 (tail-EMA and 2-factor preconditioning are load-bearing; tail-residual mechanics
are near-noise). n=8 per ablation at the 3195-step screen.
