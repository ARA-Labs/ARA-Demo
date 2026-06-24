# Results — C01: NorMuon + decoupled-WSD sub-3500 frontier (2-seed reproduced)

> **Re-export, not a fresh measurement.** Every value below already lives in this wave's `trace/`
> node `result:` / `evidence:` fields (N12) and in `logic/claims.md` C01's Evidence basis. It is
> re-exported here as a machine-readable table with its source trace-node id + run-id. Per-run
> values independently confirmed against the cited run logs under
> `v1/codex/scratchpad/runs/` (the launched-script-embedded logs C01's Proof: names).
>
> **Metric**: `step_to_3.28` = first step at which val_loss ≤ 3.28 (lower is better); each run is
> early-stopped AT its `train_steps`, so on these reproduced cells final_val_loss == the crossing
> value. Baseline to beat: Muon @ 3500 (final 3.27658, trace N08).

- **Claim**: C01 (supported) — a sub-3500 NorMuon + decoupled-WSD recipe exists and reproduces 2-seed.
- **Source trace node**: N12 (resolved) — "normuon WSD horizon/stop boundary hill-climb".
- **Wave**: v1.

## 2-seed reproduced frontier (the C01 headline, stop3296)

| run_id | seed | train_steps (stop) | step_to_3.28 | final_val_loss | source |
|---|---|---|---|---|---|
| normuon-b090to080-mlpprojlr124375-tailresrmsstack-aggmom3hidden-h3375-stop3296 | seed0 | 3296 | 3296 | 3.27914 | N12; run log :final |
| normuon-b090to080-mlpprojlr124375-tailresrmsstack-aggmom3hidden-h3375-stop3296 | seed1 | 3296 | 3296 | 3.27872 | N12; run log :final |
| normuon-b090to080-mlpprojlr124375-tailresrmsstack-aggmom3hidden-h3375-stop3296 | seed2 | 3296 | — (miss) | 3.28047 | N14 (seed-fragility map; seed2 misses) |

## Earlier reproduced point on the same corridor (stop3345, b090to082)

| run_id | seed | train_steps (stop) | step_to_3.28 | final_val_loss | source |
|---|---|---|---|---|---|
| normuon-b090to082-mlpprojlr125-h3375-stop3345 | seed0 | 3345 | 3345 | 3.27992 | N12; variant + run log |
| normuon-b090to082-mlpprojlr125-h3375-stop3345 | seed1 | 3345 | 3345 | 3.27928 | N12; variant + run log |

## Reading
- The frontier `stop3296` reproduces on seed0 + seed1 (both cross by 3296) but seed2 misses — so
  the formally-reproduced C01 frontier at v1-002 is **3296**, not lower (trace N14 / staging O06).
  Below ~3296 the crossing becomes seed-fragile; the lower validated frontier is carried by **C02**.
- The absolute step count is NOT crystallized as a fixed "best" (C01 asserts existence +
  seed-reproducibility only); the run walls at its stop step, so the headline reflects where the run
  is stopped, not only optimizer quality (staging O02).
- config: `src/configs/normuon_v1_stop3296.py`  |  core: `src/execution/normuon.py`, `wsd_schedule.py`.
