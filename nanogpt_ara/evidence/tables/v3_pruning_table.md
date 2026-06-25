# Table: v3 W258 leave-one-out pruning

**Source.** `src/configs/v3_pruning_data.json` (copied verbatim from
`record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json`). "W258 leave-one-out sweep at
step 2949; deltas are relative to the nosphere baseline from the same sweep", `target_step = 2949`.
`delta` positive ⇒ component helped. Baseline (nosphere, the submitted stack) mean 3.278416875,
score 0.006332499999999186, n=16.

| Ablation (further removal from nosphere) | mean | delta | score | std | n |
| --- | -: | -: | -: | -: | -: |
| (baseline: nosphere) | 3.27841688 | 0.0 | 0.00633250 | — | 16 |
| nolacvfloor | 3.27844333 | +0.00003 | 0.00269623 | 0.00100132 | 3 |
| notailradial | 3.27860250 | +0.00019 | 0.00395273 | 0.00100595 | 8 |
| noqkcontrascale | 3.27889000 | +0.00047 | 0.00192258 | 0.00102132 | 3 |
| nosphere-notangent | 3.27911833 | +0.00070 | 0.00305418 | 0.00143238 | 12 |
| nolacv | 3.27916333 | +0.00075 | 0.00144915 | 0.00190815 | 3 |
| nocontra | 3.27975000 | +0.00133 | 0.00043301 | 0.00216793 | 3 |
| nosoft | 3.28027667 | +0.00186 | −0.00047920 | 0.00138385 | 3 |
| novsoap | 3.28069333 | +0.00228 | −0.00120089 | 0.00183522 | 3 |
| **noradial** | **3.28216000** | **+0.00374** | −0.00374123 | 0.00009849 | 3 |
| **nosoap** | **3.28370000** | **+0.00528** | −0.00640859 | 0.00070064 | 3 |

**Reading.** Every listed ablation removes a *further* component from the already-pruned nosphere
stack, and all deltas are positive ⇒ all listed mechanisms are kept. `nosoap` and `noradial` drive
the score most negative (the tail collapses without SOAP or radial dampening). The combined
`nosphere-notangent` (removing both sphere terms) regresses by +0.00070 vs nosphere — the two sphere
removals do not compose, so only the pull is dropped. Supports C06.
