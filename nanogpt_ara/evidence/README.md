# Evidence Index

All evidence is transcribed from the tables/figures of `research_insights/INSIGHTS.md`, which is
itself grounded to `data/runs_self_contained/runs.csv` (10,428 runs), per-run `train.log` /
`metadata.json`, and the agents' scratchpads. Source labels point to the INSIGHTS.md section the table
or figure appears in. Exact cell values are preserved; approximate figure readings are marked "~".

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/frontier_progression.md](tables/frontier_progression.md) | §1, INSIGHTS.md | C01, C10, C12 | Best step_to_3_28 per wave per agent (baseline->v3) |
| [tables/baseline_recipe_anatomy.md](tables/baseline_recipe_anatomy.md) | §0, INSIGHTS.md | C01, C02, C03, C04, C06 | The §0 two-optimizer baseline (Muon ref = 3500) |
| [tables/loo_ablation.md](tables/loo_ablation.md) | §14, INSIGHTS.md | C01, C03, C06, C13 | 4-seed leave-one-out ranking of every component |
| [tables/cross_agent_v3_constants.md](tables/cross_agent_v3_constants.md) | §18, INSIGHTS.md | C15 | Byte-identical v3 constants across agents |
| [tables/v1_divergence_families.md](tables/v1_divergence_families.md) | §19, INSIGHTS.md | C12, C15 | First-120-run family split (breadth vs depth) |
| [tables/seeds_for_significance.md](tables/seeds_for_significance.md) | §21, INSIGHTS.md | C09, C16, C17 | Seeds/arm vs claimed gain (n~8sigma^2/Delta^2) |
| [tables/noise_floor_seed_groups.md](tables/noise_floor_seed_groups.md) | §9, INSIGHTS.md | C03, C09, C17 | Frontier vs safe 8-seed groups (std, miss-rate) |
| [tables/search_economy_runs.md](tables/search_economy_runs.md) | §12, INSIGHTS.md | C12 | Runs launched per wave per agent |
| [tables/temporal_curriculum_phases.md](tables/temporal_curriculum_phases.md) | §17, INSIGHTS.md | C08, C14 | Phase-active levers (explore/converge/soften) |
| [tables/seed_verified_frontier.md](tables/seed_verified_frontier.md) | §30, INSIGHTS.md | C09, C12, C16, C17 | Distinct-seed re-verify of each wave's record; honest frontier 2930/2950; +0–10 step penalty |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/crossover_val_vs_step.md](figures/crossover_val_vs_step.md) | §8, INSIGHTS.md | C08, C14 | Val_loss vs step: record loses early, crosses ~1750, wins |
| [figures/power_law_lr_trajectory.md](figures/power_law_lr_trajectory.md) | §15, INSIGHTS.md | C02, C06, C13 | Muon-group LR under the convex power-law cooldown |

## Notes on fidelity
- These are **raw transcriptions** of the synthesis's tables, not derived subsets; each preserves the
  full row set of its source section.
- Numbers are copied exactly (e.g. baseline final_val_loss 3.28027; MuonEq dval -0.00484; group A std
  0.00043; LOO soap_mlp 3010). Figure readings between stated anchors are flagged "~".
- The underlying per-run data lives at `data/runs_self_contained/` (see `src/environment.md` for the
  CSV schema and reproduction entry points).
