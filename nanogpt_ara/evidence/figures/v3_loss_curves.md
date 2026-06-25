# Figure: v3 record validation loss curve

**Source.** `record_configs/20260515_codex_v3_nosphere_2949/loss_curves.png` (title "codex v3 record
validation"). Screenshot: `v3_loss_curves.png`.

**Figure type.** quantitative_plot (line + faint per-seed traces).
**Extraction method.** visual_description + exact_from_labels for reference lines.
**Reading confidence.** high for threshold/bin lines; medium for intermediate reads.

**Axes.** x = training step (~2875 to ~3020, linear); y = validation loss (~3.276 to ~3.288, linear).

**Content.** A bold blue "controlled-seed mean" descends from ≈3.284 at step ~2875, crossing the red
dashed **3.28 threshold** at roughly step ~2930 and continuing down to ≈3.2767 at step ~3020; faint
grey per-seed traces fan around it. A green dotted vertical line marks the **record bin 2949**, which
sits to the right of the mean's 3.28 crossing — the cohort mean is comfortably below target at the
submitted bin (consistent with the statistically-viable ~2940 note). The curve continues past 2949 to
the run's true end at 3020.

**Supports.** C06, C08. Exact statistics (step 2949 and step 3020 columns):
`evidence/tables/v3_seed_table.md`.
