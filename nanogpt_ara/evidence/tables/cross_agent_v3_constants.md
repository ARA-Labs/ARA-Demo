# Cross-agent v3 recipe: byte-identical constants

**Source**: §18 table in research_insights/INSIGHTS.md (side-by-side of
`cc_v3/07070-v88-aurora-proj` vs `codex_v3/08953-...worker27...` launched_script.py).
**Caption**: "The two v3 records are component-for-component identical, including exotic magic
constants and byte-identical helper functions; only tiny timing offsets differ."
**Extraction type**: raw_table

| Constant | cc_v3 | codex_v3 |
|---|---|---|
| FINAL_LR_POWER | 1.2 | 1.2 |
| MUON_LR | 0.0375 | 0.0375 |
| CONTRA_MUON_COEFF | -0.2 | -0.2 |
| CONTRA_TO_NORMAL_END_STEP | 1920 | 1930 |
| SOFT_MUON_P | 0.1 | 0.1 |
| NORMAL_TO_SOFT_END_STEP | 2890 | 2925 |
| SOAP_PRECONDITION_FREQUENCY | 10 | 10 |
| SOAP_PARAM_MODE | mlp_plus_v | mlp_plus_v |
| ATTN_EARLY_TRUST_FLOOR | 0.45 | 0.45 |
| ATTN_TRUST_FLOOR_FADE_END_STEP | 1625 | 1625 |

**Identical functions**: `trust_gate`, `soft_via_newtonschulz5`, `soap_update_preconditioner`,
`bounded_trust_gate` are the same code in both. Only tiny timing offsets differ (e.g. CONTRA end
1920 vs 1930; soft end 2890 vs 2925).

**Implication**: v3 "convergence" is shared public-PR lineage, not independent rediscovery; the genuine
independent-exploration signal is the v1 divergence (see v1_divergence_families.md).

Maps to claims: C15 (and corrects the earlier §5.5 overclaim).
