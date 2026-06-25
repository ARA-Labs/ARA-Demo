# Leave-one-out ablation: per-component contribution at the v3 frontier

**Source**: §14 table in research_insights/INSIGHTS.md (grounded to
`agents/cc_v3/runs/*loo{01..15}_no_*-s{0..3}-*`, 629 LOO runs; clean numbered 4-seed subset; medians
and ranges computed from CSV `step_to_3_28`).
**Caption**: "Take the full frontier recipe, remove exactly one component, run 4 seeds, measure
step_to_3_28. Higher median = that component mattered more. Full recipe ~2920-2930 seed-verified."
**Extraction type**: raw_table

| Rank | Component removed (`looNN_no_*`) | Median step w/o it | 4-seed range | ~ cost of removing |
|---:|---|---:|---|---:|
| 1 | pow_cooldown | MISS (0/4 hit) | — | critical — recipe fails |
| 2 | soap_mlp | 3010 | [2990, 3010] | ~+85 steps |
| 3 | adamw_betas | 2970 | [2950, 2990] | ~+45 steps |
| 4 | uwfloor (SOAP denom floor) | 2962 | [2960, 2970] | ~+35 |
| 5 | attn_soap (SOAP on V) | 2960 | [2950, 2960] | ~+35 |
| 6 | radial (tail-radial rescale) | 2955 | [2950, 2960] | ~+30 |
| 7 | aurora (row-rescale) | 2945 | [2940, 2950] | ~+20 |
| 7 | mu_sched | 2945 | [2940, 2950] | ~+20 |
| 9 | contra (Contra-Muon) | 2940 | [2940, 2950] | ~+15 |
| 9 | muwarmup | 2940 | [2940, 2950] | ~+15 |
| 11 | mucool / difc | 2935 | [2920, 2950] | ~+10 |
| 13 | cgi / softmuon / normuon | 2930 | [2920, 2940] | ~0 (redundant) |

**Shape**: ~2 essential (pow_cooldown, soap_mlp) + ~5 useful + ~4 dead (long-tailed, not uniform).

Maps to claims: C01, C03, C06, C13.
