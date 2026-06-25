# Evidence ledger

The source of this ARA is a research **trajectory** (four waves of journals, plans and submitted
record configs), not a paper with numbered Tables/Figures. The evidence objects below are the
concrete, numbered artifacts that the trajectory produced: the **submitted record loss curves and
component-pruning charts** (figures) and the **seed / pruning / baseline data tables**. Every object
is filed with both a screenshot (`.png`, for figures) and a markdown transcription.

## Figures (each: `.png` screenshot + `.md` transcription)
| File | Object | Source |
| --- | --- | --- |
| `figures/v1_loss_curves.{png,md}` | v1 record validation curve | record_configs/…_v1_v12iso_3205/loss_curves.png |
| `figures/v1_pruning.{png,md}` | v1 component pruning (LOO) | record_configs/…_v1_v12iso_3205/pruning.png |
| `figures/v2_loss_curves.{png,md}` | v2 record validation curve | record_configs/…_v2_legal_3037/loss_curves.png |
| `figures/v2_pruning.{png,md}` | v2 component pruning (LOO) | record_configs/…_v2_legal_3037/pruning.png |
| `figures/v3_loss_curves.{png,md}` | v3 record validation curve | record_configs/…_v3_nosphere_2949/loss_curves.png |
| `figures/v3_pruning.{png,md}` | v3 W258 LOO pruning | record_configs/…_v3_nosphere_2949/pruning.png |

## Tables (markdown transcriptions of source data)
| File | Object | Source |
| --- | --- | --- |
| `tables/baseline_existing_results.md` | Muon/AdamW starting-bar logs + noise floor | novelty/…/existing_results_summary.md |
| `tables/v1_seed_table.md` | v1 bin-3205 16-seed cohort | record_configs/…_v1_v12iso_3205/README.md |
| `tables/v2_seed_table.md` | v2 bin-3037 16-seed cohort | record_configs/…_v2_legal_3037/README.md |
| `tables/v3_seed_table.md` | v3 bin-2949 16-seed cohort (steps 2949 & 3020) | record_configs/…_v3_nosphere_2949/README.md |
| `tables/v1_pruning_table.md` | v1 LOO removal deltas (n=8) | src/configs/v1_pruning_data.json |
| `tables/v2_pruning_table.md` | v2 LOO removal deltas (n=8/3) | src/configs/v2_pruning_data.json |
| `tables/v3_pruning_table.md` | v3 W258 LOO removal deltas (n=16/3) | src/configs/v3_pruning_data.json |

## Raw data artifacts (carried in `src/configs/`)
The three `*_pruning_data.json` files are copied verbatim from the submitted `record_configs/`; the
pruning tables and figure transcriptions above are derived from them and are exactly consistent.

## Objects deliberately not filed
- The four waves' raw per-seed run logs (~3 GB, 8,224 runs) are git-ignored in the source repo; the
  run **index** (`runs.csv` / `runs.jsonl`, 8,224 rows) exists in the source but is a bulk index, not
  a numbered evidence object — summarized here, not transcribed row-by-row.
- The blocklisted v2/v3 `goal.md` frontier tables (which headline other agents' bins) are excluded by
  the single-agent-slice scope (L1) and the anti-peeking design of the source experiment.
