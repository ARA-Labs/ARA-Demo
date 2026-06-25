# Temporal curriculum: phase-active levers across the 2900-step run

**Source**: §17 table in research_insights/INSIGHTS.md (decoded from
`cc_v3/07070-v88-aurora-proj-s2/launched_script.py` ramp constants).
**Caption**: "The v3 record is a time-scheduled curriculum of >=6 levers that hand off across the run
(explore -> converge -> soften)."
**Extraction type**: raw_table

| Phase | Steps | Active levers |
|---|---|---|
| Explore | 0 - ~1625 | mu warmup 0.85->0.95 (0-300); LR flat 0.0375 (0-~599); Contra-Muon -0.2->0 (0-1920, decorrelate from raw grad); attn trust-floor 0.45 forcing SOAP-trust (0-1375, fades by 1625) |
| Converge | ~1625 - 2400 | hard Newton-Schulz; Contra ~= off; trust gate fully data-driven; convex power-law cooldown underway |
| Soften | 2400 - 2900 | soft-Muon blends in 0->0.80 (2400-2890); power cooldown steepens; mu cools 0.95->0.85 (2850-2900); stop at LR=1.8% of flat |

**Reading**: The Explore-phase ramps anneal off right at the measured crossover (~step 1750, see
figures/crossover_val_vs_step.md) — i.e. the lose-early/win-late curve is engineered, not incidental.

Maps to claims: C08, C14.
