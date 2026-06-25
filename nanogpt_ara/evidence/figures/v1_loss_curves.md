# Figure: v1 record validation loss curve

**Source.** `record_configs/20260515_codex_v1_v12iso_3205/loss_curves.png` (title "codex v1 record
validation"). Screenshot: `v1_loss_curves.png`.

**Figure type.** quantitative_plot (line + uncertainty band).
**Extraction method.** visual_description + exact_from_labels for the annotated reference lines.
**Reading confidence.** high for the threshold/bin lines and curve endpoints; medium for
intermediate point reads.

**Axes.** x = training step (~2875 to ~3210, linear); y = validation loss (~3.2800 to ~3.2975,
linear).

**Content.** A blue "controlled-seed mean" validation-loss curve descends roughly linearly from
≈3.2950 at the left to the 3.28 line. A grey uncertainty band hugs the mean. A red dashed horizontal
line marks the **3.28 threshold**; a green dotted vertical line marks the **record bin 3205**, which
sits just right of where the mean crosses 3.28 — i.e. the controlled-seed mean reaches the target at
the submitted bin.

**Supports.** C01, C08 (the submitted bin is where the cohort mean — not a single seed — crosses the
target). Exact cohort statistics are in `evidence/tables/v1_seed_table.md`.
