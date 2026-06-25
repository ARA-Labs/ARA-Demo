# Evidence index

This artifact has no PDF with numbered `Figure N` / `Table N`. Its evidence objects are the
**submitted record assets** (the loss-curve and pruning figures, the seed tables, and the
significance tables) plus the raw pruning data. Every figure is filed with **both** a markdown
description and its screenshot `.png`; every table is transcribed faithfully from its source. No
object is omitted.

## Figures (markdown + screenshot)

| File | Screenshot | Type | Source |
|---|---|---|---|
| [figures/v1_loss_curves.md](figures/v1_loss_curves.md) | `figures/v1_loss_curves.png` | quantitative_plot | `record_configs/20260515_codex_v1_v12iso_3205/loss_curves.png` |
| [figures/v1_pruning.md](figures/v1_pruning.md) | `figures/v1_pruning.png` | quantitative_plot (bar) | `record_configs/20260515_codex_v1_v12iso_3205/pruning.png` |
| [figures/v2_loss_curves.md](figures/v2_loss_curves.md) | `figures/v2_loss_curves.png` | quantitative_plot | `record_configs/20260515_codex_v2_legal_3037/loss_curves.png` |
| [figures/v2_pruning.md](figures/v2_pruning.md) | `figures/v2_pruning.png` | quantitative_plot (bar) | `record_configs/20260515_codex_v2_legal_3037/pruning.png` |
| [figures/v3_loss_curves.md](figures/v3_loss_curves.md) | `figures/v3_loss_curves.png` | quantitative_plot | `record_configs/20260515_codex_v3_nosphere_2949/loss_curves.png` |
| [figures/v3_pruning.md](figures/v3_pruning.md) | `figures/v3_pruning.png` | quantitative_plot (bar) | `record_configs/20260515_codex_v3_nosphere_2949/pruning.png` |

## Tables (transcribed)

| File | What it is | Source |
|---|---|---|
| [tables/v1_seed_table.md](tables/v1_seed_table.md) | 16-seed val @ 3205 + significance | `record_configs/20260515_codex_v1_v12iso_3205/README.md:17-46` |
| [tables/v2_seed_table.md](tables/v2_seed_table.md) | 16-seed val @ 3037 + significance | `record_configs/20260515_codex_v2_legal_3037/README.md:17-46` |
| [tables/v3_seed_table.md](tables/v3_seed_table.md) | 16-seed val @ 2949 (and @ 3020) + significance | `record_configs/20260515_codex_v3_nosphere_2949/README.md:18-47` |
| [tables/v1_pruning_table.md](tables/v1_pruning_table.md) | v1 leave-one-out contributions | `…v1…/pruning_data.json` |
| [tables/v2_pruning_table.md](tables/v2_pruning_table.md) | v2 leave-one-out contributions | `…v2…/pruning_data.json` |
| [tables/v3_pruning_table.md](tables/v3_pruning_table.md) | v3 W258 leave-one-out contributions | `…v3…/pruning_data.json` |
| [tables/novelty_outcomes.md](tables/novelty_outcomes.md) | Novelty-wave mechanism outcomes (negative) | `novelty/codex/scratchpad/THREAD.md` |

## Raw data

| File | Source |
|---|---|
| [data/v1_pruning_data.json](data/v1_pruning_data.json) | `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json` (verbatim copy) |
| [data/v2_pruning_data.json](data/v2_pruning_data.json) | `record_configs/20260515_codex_v2_legal_3037/pruning_data.json` (verbatim copy) |
| [data/v3_pruning_data.json](data/v3_pruning_data.json) | `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json` (verbatim copy) |

## Objects accounted for but not separately filed

- **The per-wave loss-curve PNGs are the only plots in the source records** beyond the pruning bars;
  there are no additional numbered figures. The `THREAD.md` journals reference in-worktree sweep
  figures (`assets/<sweep-id>/figures.md`) that are not part of the submitted records and are not
  re-filed here (they are pointers into the run store, indexed in [../src/artifacts.md](../src/artifacts.md)).
- **The seed and pruning tables are native markdown/JSON in the source** (not figure images), so
  they are filed as faithful transcriptions; their only "screenshot" form is the pruning **bar
  chart** (filed) which visualizes the pruning table.
