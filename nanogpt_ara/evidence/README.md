# Evidence ledger

Grounded results for the Codex speedrun ARA. This experiment is compiled from a run database + record
configs (not a paper), so the "numbered figures and tables" are the **record-config artifacts**: per
wave, a validation loss-curve figure and a component-pruning figure, plus the per-seed record table and
the pruning table. Every figure is filed with BOTH the original PNG and a markdown description; every
table is transcribed to markdown from its committed text source.

## Cohort-attribution warning (read before comparing numbers)

The **record** cohorts and the **pruning** cohorts are *different* and must not be cross-compared:
- **Record tables** (`v{1,2,3}_record_seeds.md`): the submitted N=16 reproduction, seeds 0–15, at the
  record bin (v1 step 3205, v2 step 3037, v3 step 2949). Source: the record-config READMEs.
- **Pruning tables** (`v{1,2,3}_component_pruning.md`): the leave-one-out sweeps, at a *screen* step and
  a *different* N — v1 at step **3195, n=8**; v2 at step **3037, n=8**; v3 (W258) at step **2949, N≤16**.
  Source: the record-config `pruning_data.json`.
  ⇒ The "same" stack therefore has different mean values in the two tables; each file states its exact
  cohort. (The v3 record mean at 2949 is 3.27886125 (n=16 seeds 0–15) while the v3 W258 pruning baseline
  mean at 2949 is 3.278416875 (N=16 LOO sweep) — different cohorts.)

## Figures (PNG + markdown)

| File | Type | Source object | What it shows |
|---|---|---|---|
| figures/v1_loss_curves.(png/md) | quantitative_plot | v1 record `loss_curves.png` | controlled-seed mean validation crossing 3.28 at bin 3205 |
| figures/v1_pruning.(png/md) | quantitative_plot | v1 record `pruning.png` | per-component Δval_loss when removed (n=8 @ step 3195) |
| figures/v2_loss_curves.(png/md) | quantitative_plot | v2 record `loss_curves.png` | controlled-seed mean crossing 3.28 at bin 3037 |
| figures/v2_pruning.(png/md) | quantitative_plot | v2 record `pruning.png` | per-component Δval_loss (n=8 @ step 3037) |
| figures/v3_loss_curves.(png/md) | quantitative_plot | v3 record `loss_curves.png` | controlled-seed mean crossing 3.28 at bin 2949 |
| figures/v3_pruning.(png/md) | quantitative_plot | v3 record `pruning.png` | W258 leave-one-out per-component Δ (N≤16 @ step 2949) |

## Tables (markdown; text-sourced)

| File | Source | What it holds |
|---|---|---|
| tables/trajectory_summary.md | record READMEs + repo README + run index | the 3500→3205→3037→2949 arc with means/scores/run counts |
| tables/v1_record_seeds.md | v1 record README | the 16 per-seed values at step 3205 + cohort stats |
| tables/v2_record_seeds.md | v2 record README | the 16 per-seed values at step 3037 + cohort stats |
| tables/v3_record_seeds.md | v3 record README | the 16 per-seed values at steps 2949 & 3020 + cohort stats |
| tables/v1_component_pruning.md | v1 `pruning_data.json` | leave-one-out Δ/mean/score per component (n=8 @ 3195) |
| tables/v2_component_pruning.md | v2 `pruning_data.json` | leave-one-out Δ/mean/score per component (n=8 @ 3037) |
| tables/v3_component_pruning.md | v3 `pruning_data.json` | W258 leave-one-out Δ/mean/score per component (@ 2949) |

> Note on table screenshots: these tables originate as **text** (markdown tables in the record READMEs;
> JSON in `pruning_data.json`), not as visual objects, so a markdown transcription is the faithful form
> and no screenshot exists to file. Their visual companions are the `*_pruning.png` / `*_loss_curves.png`
> figures, which ARE filed as PNGs. This accounts for every numbered object per the evidence rules.
