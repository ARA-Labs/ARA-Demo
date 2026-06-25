# Frontier progression by wave (best step_to_3_28 per agent)

**Source**: §1 table in research_insights/INSIGHTS.md (grounded to data/runs_self_contained/runs.csv,
best `step_to_3_28` among completed target-hitting runs, single-best-seed).
**Caption**: "Best step_to_3_28 among completed target-hitting runs, per wave (CSV; single-best-seed)."
**Extraction type**: raw_table

| Wave | Claude Code | Codex | Notes |
|---|---|---|---|
| baseline | 3500 | 3500 | Muon reference |
| v1 | 3000 | 3150 | first wave, all levers allowed |
| novelty | 3375 | 3375 | ideas must pass a novelty check -> frontier regresses (§4) |
| v2 | 3000 | 2962 | start from v1 frontier, push toward 3000 |
| v3 | 2885 | 2880 | start from v2 + public PRs; under-2900 search |

**Seed-verified headline (README, more conservative than single-best-seed):** by v2 both pass 3035;
by v3 Claude reaches 2930, Codex 2950.

**Reference points**: AdamW baseline 5625 steps; Muon reference 3500 (`00001-muon-baseline`,
final_val_loss 3.28027); best public record at start 3225. Net improvement: 3500 -> ~2900-2930
(~16-17% fewer steps; ~48% fewer than AdamW).

Maps to claims: C01, C10, C12.
