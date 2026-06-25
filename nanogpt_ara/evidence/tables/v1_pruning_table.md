# Table — v1 leave-one-out pruning (full)

- **Source:** `record_configs/20260515_codex_v1_v12iso_3205/pruning_data.json` (verbatim copy at
  [../data/v1_pruning_data.json](../data/v1_pruning_data.json))
- **Source note (from JSON):** "pruning-rerun aggregate for codex_v1_v12iso at the original
  3195-step screen"; `target_step = 3195`; baseline `v12iso-baseline` mean 3.27907, n=8.
- `Δval when removed` positive ⇒ the component helped (its removal raised val loss). Visualized in
  [../figures/v1_pruning.md](../figures/v1_pruning.md).

| Component removed | mean | Δval | score | std | n |
|---|---:|---:|---:|---:|---:|
| v12iso-baseline | 3.27907 | 0.00000 | 0.0026304 | — | 8 |
| noTailEMA | 3.28158 | +0.00251 | −0.0044689 | 0.00074 | 8 |
| noMuon2f | 3.28136 | +0.00229 | −0.0038467 | 0.00085 | 8 |
| noMuSched | 3.27998 | +0.00091 | 0.0000566 | 0.00067 | 8 |
| noErrorFeedback | 3.27983 | +0.00076 | 0.0004808 | 0.00075 | 8 |
| noAggMo3 | 3.27931 | +0.00024 | 0.0019516 | 0.00056 | 8 |
| noTailRD | 3.27924 | +0.00017 | 0.0021496 | 0.00086 | 8 |
| noTailFeedback | 3.27921 | +0.00014 | 0.0022345 | 0.00059 | 8 |
| noResRMSNorm | 3.27918 | +0.00011 | 0.0023193 | 0.00083 | 8 |
| noLateLR | 3.27909 | +0.00002 | 0.0025739 | 0.00072 | 8 |
| noBeta2Thaw | 3.27906 | −0.00001 | 0.0026587 | 0.00071 | 8 |
| noMomRefresh | 3.27903 | −0.00004 | 0.0027436 | 0.00074 | 8 |
| noResPulse | 3.27900 | −0.00007 | 0.0028284 | 0.00086 | 8 |

The two largest (noTailEMA, noMuon2f) ground [C02](../../logic/claims.md), [C03](../../logic/claims.md);
the ≤0 tail (noBeta2Thaw, noMomRefresh, noResPulse) grounds the net-removable components of
[C07](../../logic/claims.md). Per **L1** in [constraints.md](../../logic/solution/constraints.md),
the small/near-zero values sit within their own n=8 seed noise.
