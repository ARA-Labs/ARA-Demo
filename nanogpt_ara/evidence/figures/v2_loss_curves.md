# Figure: v2 record validation loss curve

**Source.** `record_configs/20260515_codex_v2_legal_3037/loss_curves.png` (title "codex v2 record
validation"). Screenshot: `v2_loss_curves.png`.

**Figure type.** quantitative_plot (line + faint per-seed traces).
**Extraction method.** visual_description + exact_from_labels for reference lines.
**Reading confidence.** high for the threshold/bin lines and endpoints; medium for intermediate reads.

**Axes.** x = training step (~2875 to ~3045, linear); y = validation loss (~3.280 to ~3.295, linear).

**Content.** A bold blue "controlled-seed mean" descends from ≈3.295 at step ~2875 to ≈3.2785 at the
right edge; faint grey individual-seed traces fan around it (visibly more spread than v1 — consistent
with the agent's note that the legal stack is higher-variance). A red dashed line marks the **3.28
threshold**; a green dotted vertical line marks the **record bin 3037**. The mean crosses 3.28 at
roughly step ~3018 and is below it at the 3037 bin, where the cohort score clears the gate.

**Supports.** C04, C05 (higher-variance legal stack), C08. Exact statistics:
`evidence/tables/v2_seed_table.md`.
