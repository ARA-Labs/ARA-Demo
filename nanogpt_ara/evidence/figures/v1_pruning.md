# Figure — codex v1 component pruning (leave-one-out bar chart)

![v1 pruning](v1_pruning.png)

- **Source:** `record_configs/20260515_codex_v1_v12iso_3205/pruning.png` (data:
  `pruning_data.json`, mirrored at [../data/v1_pruning_data.json](../data/v1_pruning_data.json))
- **Figure type:** quantitative_plot (horizontal bar)
- **Extraction method:** exact_from_labels (each bar carries its printed Δval; cross-checked
  against `pruning_data.json`)
- **Reading confidence:** high (data labels printed on every bar)

## What it shows

Horizontal bars of **`Δ val_loss when removed`** (positive ⇒ the component *helped*) for each
modifier in the v12iso stack, from the pruning-rerun at the 3195-step screen (baseline mean
3.27907, n=8). Two orange bars (the largest) sit far right; the rest are gray and small. The x-axis
runs 0 → ~0.0030 with dashed/ dotted guides at 0.0010 and 0.0030.

## Transcription (top → bottom, exact printed labels)

| Component removed | Δval (printed) |
|---|---:|
| noTailEMA | +0.00251 |
| noMuon2f | +0.00229 |
| noMuSched | +0.00091 |
| noErrorFeedback | +0.00076 |
| noAggMo3 | +0.00024 |
| noTailRD | +0.00017 |
| noTailFeedback | +0.00014 |
| noResRMSNorm | +0.00011 |
| noLateLR | +0.00002 |
| noBeta2Thaw | −0.00001 |
| noMomRefresh | −0.00004 |
| noResPulse | −0.00007 |

## Reading

Tail-EMA and Muon2F together account for an order of magnitude more than every other component —
the two dominant levers ([C02](../../logic/claims.md), [C03](../../logic/claims.md)). The bottom
three bars are ≤ 0, i.e. removing them does not hurt (net-removable), the empirical basis for
[C07](../../logic/claims.md) (add levers, then prune). Full numerics:
[../tables/v1_pruning_table.md](../tables/v1_pruning_table.md).
