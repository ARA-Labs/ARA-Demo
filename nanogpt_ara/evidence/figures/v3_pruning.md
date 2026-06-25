# Figure — codex v3 W258 leave-one-out pruning (bar chart)

![v3 pruning](v3_pruning.png)

- **Source:** `record_configs/20260515_codex_v3_nosphere_2949/pruning.png` (data:
  `pruning_data.json`, mirrored at [../data/v3_pruning_data.json](../data/v3_pruning_data.json))
- **Figure type:** quantitative_plot (horizontal bar)
- **Extraction method:** exact_from_labels (printed Δval per bar; cross-checked against JSON)
- **Reading confidence:** high

## What it shows

`Δ val_loss when removed` for each component of the W258 stack at the 2949-step boundary, relative
to the **nosphere baseline** (mean 3.278416875, n=16). Two red bars (nosoap, noradial) dominate;
then orange (novsoap, nosoft, nocontra); then gray. X-axis 0 → ~0.0055 with guides at 0.0010 and
0.0030. (The pruned component itself — the sphere-lookahead pull — is the *baseline* of this chart,
so it does not appear as a bar; its removal is the submitted simplification.)

## Transcription (top → bottom, exact printed labels)

| Component removed | Δval (printed) | n |
|---|---:|---:|
| nosoap | +0.00528 | 3 |
| noradial | +0.00374 | 3 |
| novsoap | +0.00228 | 3 |
| nosoft | +0.00186 | 3 |
| nocontra | +0.00133 | 3 |
| nolacv | +0.00075 | 3 |
| nosphere-notangent | +0.00070 | 12 |
| noqkcontrascale | +0.00047 | 3 |
| notailradial | +0.00019 | 8 |
| nolacvfloor | +0.00003 | 3 |

## Reading

The SOAP sidecar and the radial brake are the two load-bearing components ([C10](../../logic/claims.md),
[C09](../../logic/claims.md)). The `nosphere-notangent` bar (+0.00070, n=12) is the *combined* sphere
removal: it is positive (worse) and the agent's verdict is that the two sphere terms do not compose —
keep the radial gate when the lookahead pull is dropped ([C11](../../logic/claims.md)). Full
numerics: [../tables/v3_pruning_table.md](../tables/v3_pruning_table.md).
