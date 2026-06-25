# Figure — codex v2 record validation (loss curves)

![v2 loss curves](v2_loss_curves.png)

- **Source:** `record_configs/20260515_codex_v2_legal_3037/loss_curves.png`
- **Figure type:** quantitative_plot (line, with seed band)
- **Extraction method:** visual_description + exact_from_text (threshold 3.28 and record bin 3037
  exact per README; axis values estimated `≈`)
- **Reading confidence:** medium

## What it shows

Validation loss vs training step for the v2 `legal_v12opt` record. The bold blue controlled-seed
mean descends from `≈ 3.2945` at step ≈ 2875 to `≈ 3.2785` at step ≈ 3037, inside a gray 16-seed
band. The red dashed line is the **3.28 threshold**; the green dotted line is the **record bin
3037**. The blue mean crosses the 3.28 line at roughly step ≈ 3017–3020 and is comfortably below it
by the 3037 marker.

## Reading

The crossing occurs a little *before* the submitted bin, and 3037 is the earliest *common*
checkpoint whose cohort mean clears the significance margin — the anti-"val-spam" rule from
[C06](../../logic/claims.md) (the journal notes step 3025 does not pass the same-checkpoint scan
while 3037 does). The seed band is slightly wider than v1's (record std 0.00080602), consistent with
the larger significance margin 0.00588 the cohort still clears. Cohort numbers:
[../tables/v2_seed_table.md](../tables/v2_seed_table.md).
