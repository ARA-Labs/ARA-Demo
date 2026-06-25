# Table — v3 W258 leave-one-out pruning (full)

- **Source:** `record_configs/20260515_codex_v3_nosphere_2949/pruning_data.json` (verbatim copy at
  [../data/v3_pruning_data.json](../data/v3_pruning_data.json))
- **Source note (from JSON):** "W258 leave-one-out sweep at step 2949; deltas are relative to the
  nosphere baseline from the same sweep"; `target_step = 2949`; baseline `nosphere-baseline` mean
  3.278416875, n=16.
- `Δval when removed` positive ⇒ the component helped. Visualized in
  [../figures/v3_pruning.md](../figures/v3_pruning.md).

| Component removed | mean | Δval | score | std | n |
|---|---:|---:|---:|---:|---:|
| nosphere-baseline (the submitted stack) | 3.27841688 | 0.00000 | 0.0063325 | — | 16 |
| nosoap | 3.28370000 | +0.00528 | −0.0064086 | 0.00070 | 3 |
| noradial | 3.28216000 | +0.00374 | −0.0037412 | 0.00010 | 3 |
| novsoap | 3.28069333 | +0.00228 | −0.0012009 | 0.00184 | 3 |
| nosoft | 3.28027667 | +0.00186 | −0.0004792 | 0.00138 | 3 |
| nocontra | 3.27975000 | +0.00133 | 0.0004330 | 0.00217 | 3 |
| nolacv | 3.27916333 | +0.00075 | 0.0014491 | 0.00191 | 3 |
| nosphere-notangent | 3.27911833 | +0.00070 | 0.0030542 | 0.00143 | 12 |
| noqkcontrascale | 3.27889000 | +0.00047 | 0.0019226 | 0.00102 | 3 |
| notailradial | 3.27860250 | +0.00019 | 0.0039527 | 0.00101 | 8 |
| nolacvfloor | 3.27844333 | +0.00003 | 0.0026962 | 0.00100 | 3 |

The two largest keeps are the SOAP sidecar ([C10](../../logic/claims.md)) and the radial brake
([C09](../../logic/claims.md)). The `nosphere-notangent` row is the *combined* sphere removal
(positive Δ, i.e. worse) — the basis for [C11](../../logic/claims.md): the sphere terms are
substitutes, so only one is dropped (`nosphere`, the baseline here), never both. Most rows are n=3
(see **L1**).
