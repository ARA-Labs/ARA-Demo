# Figure — codex v1 record validation (loss curves)

![v1 loss curves](v1_loss_curves.png)

- **Source:** `record_configs/20260515_codex_v1_v12iso_3205/loss_curves.png`
- **Figure type:** quantitative_plot (line, with seed band)
- **Extraction method:** visual_description + exact_from_text (axis endpoints estimated `≈`; the
  record bin 3205 and threshold 3.28 are exact, stated in the README)
- **Reading confidence:** medium (axis tick values read off the plot)

## What it shows

Validation loss vs training step for the v1 `v12iso` record. The bold blue **controlled-seed mean**
descends roughly linearly from `≈ 3.2965` at step ≈ 2875 to `≈ 3.279` at step ≈ 3205, inside a
narrow gray seed band (the 16 seeds). A horizontal red dashed line marks the **3.28 threshold**; a
vertical green dotted line marks the **record bin 3205**. The mean crosses the 3.28 line just before
the 3205 marker — i.e. the cohort mean reaches target at the submitted bin.

## Reading

The crossing of the blue mean below the red 3.28 line at/just-before the green 3205 line is the
visual statement of the submitted result: a cohort whose *mean* (not a lucky seed) clears target at
3205. The tight gray band illustrates the low seed variance (record std 0.00069831) that lets the
significance margin clear 0.004 at n=16. Supports [C06](../../logic/claims.md); the exact cohort
numbers are in [../tables/v1_seed_table.md](../tables/v1_seed_table.md).
