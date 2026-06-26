# Table — v3 W258 leave-one-out pruning

Per-component contribution from the **W258 leave-one-out sweep at step 2949**; deltas are relative to the
`nosphere` baseline from the same sweep. Baseline `nosphere-baseline`: mean 3.278416875, **n=16**, score
0.006332499999999186. (This is the W258 LOO cohort, a *different* cohort from the n=16 record table in
[v3_record_seeds.md](v3_record_seeds.md), mean 3.27886125.) `delta` = val_loss when removed minus baseline
(positive ⇒ helped). Transcribed verbatim from `pruning_data.json`. Sorted most→least load-bearing.

| Component removed | Δ val_loss (exact) | Δ (figure) | mean | n | score (3.28−μ)·√n | std |
|---|---:|---:|---:|---:|---:|---:|
| nosoap | 0.005283124999999611 | +0.00528 | 3.2836999999999996 | 3 | −0.006408587988004524 | 0.000700642562223977 |
| noradial | 0.0037431249999997362 | +0.00374 | 3.2821599999999997 | 3 | −0.0037412297443486704 | 9.84885780179299e-05 |
| novsoap | 0.002276458333333231 | +0.00228 | 3.2806933333333332 | 3 | −0.0012008885599145969 | 0.0018352202410972624 |
| nosoft | 0.0018597916666669434 | +0.00186 | 3.280276666666667 | 3 | −0.00047920072342822113 | 0.0013838472940801195 |
| nocontra | 0.001333124999999935 | +0.00133 | 3.27975 | 3 | 0.0004330127018919793 | 0.0021679252754650147 |
| nolacv | 0.0007464583333329777 | +0.00075 | 3.279163333333333 | 3 | 0.001449149175666224 | 0.0019081491905334014 |
| nosphere-notangent | 0.0007014583333342372 | +0.00070 | 3.2791183333333342 | 12 | 0.003054182924009284 | 0.0014323841113417215 |
| noqkcontrascale | 0.0004731250000000742 | +0.00047 | 3.27889 | 3 | 0.0019225763964009727 | 0.0010213226718331012 |
| notailradial | 0.00018562500000030013 | +0.00019 | 3.2786025000000003 | 8 | 0.003952726906831377 | 0.0010059501549707036 |
| nolacvfloor | 0.000026458333333589934 | +0.00003 | 3.2784433333333336 | 3 | 0.0026962257571147554 | 0.0010013158010004988 |

**Reading.** SOAP (extended to MLP+V) and outward-radial dampening are the load-bearing pair (their
removal pushes the cohort below the threshold); V-SOAP, Soft-Muon, and Contra follow. The submitted
record removes only the **sphere-lookahead pull** (the `nosphere` baseline here). The `nosphere-notangent`
row shows that *also* removing the tangent-sphere radial gate costs +0.00070 and (at N=12) loses the 2940
boundary — the two sphere removals do not compose (C09). **Source:**
`record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json`. Supports C08, C09. Figure:
[../figures/v3_pruning.md](../figures/v3_pruning.md).
