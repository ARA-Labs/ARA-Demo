# Noise-floor seed groups: frontier vs safe config (8 seeds each)

**Source**: §9 of research_insights/INSIGHTS.md (two same-config seed groups; metadata from
`agents/.../runs/*` and `agents/seed_reverify/runs/*`).
**Caption**: "Two 8-seed groups quantifying the seed noise floor: a frontier config (group A) and a
safe config (group B)."
**Extraction type**: raw_table

| Group | Config | Seeds | final_val_loss mean | std | range | step_to_3_28 | misses |
|---|---|---:|---:|---:|---|---|---:|
| A (frontier) | `v88-aurora-proj`, ts=2900 | 8 (s0-s7) | 3.27952 | 0.00043 | [3.27890, 3.28025] | mean 2892, std 5.2, range [2885, 2900] | 1/8 (s6 -> None) |
| B (safe) | `v1cc_v12_ts3100` (seed_reverify) | 8 | 3.27692 | 0.00100 | [3.27528, 3.27822] | all 8 = 3100 (std 0) | 0/8 |

**Reading**: Group A's std 0.00043 vs documented single-lever gains — embed-init -0.00091 (~2 sigma,
marginal), NorMuon -0.00155, MuonEq -0.00484 (~11 sigma, robust). Group B's step-std 0 is a
cadence-quantization artifact (all seeds clear at the same logged step 3100). ts2900 buys ~210 steps
over ts3100 but at a ~12% failure rate; ts3100 is slower but a certain hit.

Maps to claims: C09, C17, C03 (sigma-multiples of the levers).
