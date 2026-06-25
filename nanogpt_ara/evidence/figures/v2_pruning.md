# Figure — codex v2 component pruning (leave-one-out bar chart)

![v2 pruning](v2_pruning.png)

- **Source:** `record_configs/20260515_codex_v2_legal_3037/pruning.png` (data:
  `pruning_data.json`, mirrored at [../data/v2_pruning_data.json](../data/v2_pruning_data.json))
- **Figure type:** quantitative_plot (horizontal bar)
- **Extraction method:** exact_from_labels (printed Δval per bar; cross-checked against JSON)
- **Reading confidence:** high

## What it shows

`Δ val_loss when removed` for each modifier of the `legal_v12opt` stack at the 3037 step budget
(baseline mean 3.27885, n=8 unless noted). Three red bars (largest), one orange (RoleLR), two orange
(lookahead / Polar Express), then gray. X-axis 0 → ~0.0045 with guides at 0.0010 and 0.0030.

## Transcription (top → bottom, exact printed labels)

| Component removed | Δval (printed) |
|---|---:|
| noMuSched | +0.00459 |
| cf1.0 | +0.00388 |
| noMuonEq | +0.00353 |
| noRoleLR | +0.00292 |
| noLookahead | +0.00117 |
| noPolarExpress | +0.00117 |
| noEtaMin | +0.00097 |
| noEmbedInit | +0.00092 |
| noRoleWD | +0.00041 |
| noContraMuon | +0.00008 |

## Reading

The three largest bars are **inherited** levers (mu-schedule, cooldown-floor, MuonEq); the largest
**v2-specific** addition is `noRoleLR` (+0.00292), with lookahead and role-WD smaller — exactly the
record's own summary that "Lookahead and role LR/WD are the main v2-specific additions; MuonEq and
the Muon schedule remain the largest inherited contributors." Supports
[C03](../../logic/claims.md) (MuonEq) and [C04](../../logic/claims.md) (role-LR/WD). `noContraMuon`
is ≈ 0. Full numerics: [../tables/v2_pruning_table.md](../tables/v2_pruning_table.md).
