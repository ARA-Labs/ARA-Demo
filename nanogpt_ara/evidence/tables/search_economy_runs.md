# Search economy: runs launched per wave per agent

**Source**: §12(a) table in research_insights/INSIGHTS.md (per-`agent_version` run counts from
data/runs_self_contained/runs.csv).
**Caption**: "Experiments launched (runs that produced a log) per wave. 'Completed' is lower — e.g.
codex_v1 launched 2,165, only 1,587 completed; the remainder early-killed (§11.4)."
**Extraction type**: raw_table

| Wave | Claude Code | Codex |
|---|---:|---:|
| v1 | 605 | 2,165 |
| novelty | 81 | 254 |
| v2 | 459 | 2,729 |
| v3 | 1,059 | 3,076 |
| Total | 2,204 | 8,224 |

**Recipe-version depth** (`vNN` label agents stamp on each new recipe): Claude reached v140 by v3;
Codex reached v48. Family cardinality per agent_version: cc_v2 = 41 families / 459 runs vs codex_v2 =
23 families / 2,729 runs.

**Reading**: same frontier (~2880-2885), ~3.7x fewer runs for Claude — wide-and-shallow (many recipes,
few runs each) vs Codex narrow-and-deep (few recipes, huge sweeps). The `vNN` counter is a naming
convention, not a strict iteration index.

Maps to claims: C12.
