# Table — Novelty-wave mechanism outcomes (negative result)

- **Source:** `novelty/codex/scratchpad/THREAD.md` (line refs per row, via the wave journal)
- **Type:** derived outcomes summary (this is a *derived subset* of the novelty journal, not a
  source `Table N`). Baseline bar: Muon crosses `3.27673` first at step 3500; the next meaningful
  grid bin below is 3375; a real gain must clear a ~2× step noise floor and reproduce on a distinct
  seed. Supports [C12](../../logic/claims.md), [C05](../../logic/claims.md).

## Mechanisms that ran (best outcome) — none promotable

| ID | Mechanism (intended) | Best outcome | Verdict | Ref |
|---|---|---|---|---|
| RSI001 | residual-stream isometric init | final 3.27819, target only @3500 | no crossing gain | THREAD.md:255 |
| VFG001 | value/fc-only gain init | crossed 3475; reproduced 3.27960→3.27962 | **best robust** — but below noise floor | THREAD.md:577-580 |
| NGI001 | norm-gain imbalance init | single-seed 3475 (3.27986) | reproduction failed (3.28080) | THREAD.md:489,574 |
| PDS001 | polar-disagreement split Muon | target only @3500 | no promotion | THREAD.md:570 |
| WMS001 | weight-derived momentum seed | single-seed 3450 | no promotion | THREAD.md:677 |
| CMU001 | commutator-corrected Muon | single-seed 3475 (3.27912) | no promotion | THREAD.md:705 |
| GMS001 | gain-gradient → Muon shear | single-seed 3450 (3.27878) | no promotion | THREAD.md:828 |
| BIGE001 | branch input-Gram exchange | single-seed 3450 (3.27819) | no promotion | THREAD.md:1411 |
| NDF001 | finite-NS defect feedback | 3375 (3.27999) | seed-1234 failed (3.28289) | THREAD.md:1333-1342 |
| (≈ 2 dozen more) | non-additive Muon couplings | at best single-seed 3450 | none reproduce to 3375 | THREAD.md:705-1822 |

## Killed before code (the dominant mode)

| Kill category | Representative IDs | Reason |
|---|---|---|
| Reduces to known prior | RCM (Muon²/Muon²-F), TGM (OrthoGrad/Mano), GCM (Gradient Centralization), SEC (Dion/GaLore), DGB (Fixup/DeepNet), GRC (Stiefel/Cayley) | not novel | THREAD.md:326-465 |
| Exact-polar algebraic no-op | CPD, GLC, NMA, MNL | signal identically 0 for exact polar (UᵀU = I, ‖U[:,j]‖²=1) | THREAD.md:1214,1855 |
| Linearizes to a scalar blend | (multiple) | reduces to Nesterov/de-Nesterov coefficient | THREAD.md:1783 |
| Source/formula swap | WSE, SCE, RCG, BLT, BDE, SPF, DWD, WPO, PJD, JSP | not a fresh non-additive interaction | THREAD.md:1632-2027 |

## Bottom line

The best *robust* result of the entire wave is a reproduced **25-step (one grid bin)** gain — "below
the required 2x step noise floor." No mechanism reached a reproducible 3375 crossing. The negative
result is mechanism-attributed: the metric-moving surfaces (schedule, optimizer+schedule) were
ruled non-novel, and the remaining surface yielded only literature-duplicates, exact-polar no-ops,
or sub-noise-floor effects. → [C12](../../logic/claims.md).
