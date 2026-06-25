# Table — v2 leave-one-out pruning (full)

- **Source:** `record_configs/20260515_codex_v2_legal_3037/pruning_data.json` (verbatim copy at
  [../data/v2_pruning_data.json](../data/v2_pruning_data.json))
- **Source note (from JSON):** "pruning-rerun aggregate for codex_v2_legal_3037 at 3037 steps";
  `target_step = 3037`; baseline `legal3037-baseline` mean 3.27885, n=8.
- `Δval when removed` positive ⇒ the component helped. Visualized in
  [../figures/v2_pruning.md](../figures/v2_pruning.md).

| Component removed | mean | Δval | score | std | n |
|---|---:|---:|---:|---:|---:|
| legal3037-baseline | 3.27885 | 0.00000 | 0.0032527 | — | 8 |
| noMuSched | 3.28344 | +0.00459 | −0.0059583 | 0.00054 | 3 |
| cf1.0 | 3.28273 | +0.00388 | −0.0047285 | 0.00127 | 3 |
| noMuonEq | 3.28238 | +0.00353 | −0.0067317 | 0.00096 | 8 |
| noRoleLR | 3.28177 | +0.00292 | −0.0050063 | 0.00096 | 8 |
| noLookahead | 3.28002 | +0.00117 | −0.0000566 | 0.00091 | 8 |
| noPolarExpress | 3.28002 | +0.00117 | −0.0000566 | 0.00061 | 8 |
| noEtaMin | 3.27982 | +0.00097 | 0.0005091 | 0.00095 | 8 |
| noEmbedInit | 3.27977 | +0.00092 | 0.0006505 | 0.00124 | 8 |
| noRoleWD | 3.27926 | +0.00041 | 0.0020930 | 0.00070 | 8 |
| noContraMuon | 3.27893 | +0.00008 | 0.0030264 | 0.00114 | 8 |

The three largest are inherited levers (mu-schedule, cooldown-floor, MuonEq → [C03](../../logic/claims.md));
`noRoleLR` is the largest v2-specific addition and `noRoleWD` a smaller one
([C04](../../logic/claims.md)); `noLookahead` is the v2-specific lookahead lever; `noContraMuon` ≈ 0.
The `cf1.0` and `noMuSched` rows are n=3 (smaller cohorts).
