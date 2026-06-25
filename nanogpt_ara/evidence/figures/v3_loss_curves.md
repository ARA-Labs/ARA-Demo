# Figure — codex v3 record validation (loss curves)

![v3 loss curves](v3_loss_curves.png)

- **Source:** `record_configs/20260515_codex_v3_nosphere_2949/loss_curves.png`
- **Figure type:** quantitative_plot (line, with seed band)
- **Extraction method:** visual_description + exact_from_text (threshold 3.28, record bin 2949 exact
  per README; axis values estimated `≈`)
- **Reading confidence:** medium

## What it shows

Validation loss vs training step for the v3 `nosphere` record. The bold blue controlled-seed mean
descends from `≈ 3.2840` at step ≈ 2880 to `≈ 3.2766` at step ≈ 3020, inside a gray 16-seed band.
The red dashed line is the **3.28 threshold**; the green dotted line is the **record bin 2949**. The
mean crosses 3.28 at roughly step ≈ 2925–2930 and continues to decline; the curve is plotted out to
≈ 3020 (the runs continue to `train_steps=3020`, with the submitted bin the logged step-2949
checkpoint).

## Reading

Unlike v1/v2, the v3 curve clearly crosses 3.28 *before* the record marker and keeps descending —
the run is trained to 3020 but the submitted bin is the earlier 2949 checkpoint that passes the
significance gate (record margin 0.00455 at n=16; stat-viable to ~2940). The band is the widest of
the three (record std 0.00125939), reflecting the more aggressive compression. Supports
[C06](../../logic/claims.md), [C09](../../logic/claims.md), [C10](../../logic/claims.md). Cohort
numbers (both 2949 and 3020): [../tables/v3_seed_table.md](../tables/v3_seed_table.md).
