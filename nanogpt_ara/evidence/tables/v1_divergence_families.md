# v1 divergence: first ~120 launch-ordered runs per agent

**Source**: §19 table in research_insights/INSIGHTS.md (per-agent family tallies over the first ~120
launch-ordered v1 runs, CSV `launched_at`).
**Caption**: "Before the shared PR pool merged the agents, v1 shows genuinely different first moves:
breadth-first (Claude) vs depth-first (Codex)."
**Extraction type**: raw_table

| | Claude Code v1 (first ~120 runs) | Codex v1 (first ~120 runs) |
|---|---|---|
| Dominant early families | `ptlr` 18, `lr` 12, `qkvp` 11, `wd` 8, `musched` 6, `lookahead` 4, `ademamix` 3, ... (~14 families) | `normuon` 106, `horizon3500` 4, `ema` 2, `cautious` 1, `soap` 1 |
| Style | breadth — many small operator/param probes | depth — one massive sweep |
| v1 best | 3000 | 3150 |

**Note**: Both agents open the same way (baseline calibration + cheap schedule probes), then split:
Claude's wide net located MuonEq (dval -0.0048, the strongest lever); Codex poured 106/120 runs into a
single NorMuon sweep (dval -0.0016, the weaker sibling — later found LOO-redundant, §14.4).

Maps to claims: C12, C15.
