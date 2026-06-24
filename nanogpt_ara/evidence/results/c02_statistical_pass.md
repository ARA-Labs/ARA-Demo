# Results — C02: statistical-relevance pass (the speedrun claim rule)

> **Re-export, not a fresh measurement.** Every score below already lives in this wave's `trace/`
> node N59 `result:` field and in `logic/claims.md` C02's Statement/Evidence basis. It is the
> turn-v1-007 statistical pass that produced the FIRST claimable lower frontiers since C01.
>
> **Speedrun claim rule** (logic/concepts.md "Noise floor / statistical-significance gate"):
> a recipe is claimable iff `(3.28 − mean_final_val_loss) · sqrt(n) ≥ 0.004`, where `mean` is the
> mean final_val_loss over `n` seeds at the recipe's stop. This certifies REPRODUCIBILITY OF THE
> MEAN (largely via n-scaling), not a large per-seed margin.

- **Claim**: C02 (supported, depends on C01).  **Wave**: v1.
- **Source trace node**: N59 (resolved) — "Statistical-relevance pass ... CRYSTALLIZES O16 → C02".
- Computed from the per-run trainer logs (runs.jsonl had one corrupt line from concurrent Slurm
  appends, repaired by removing the single invalid line; backup runs.jsonl.bak-20260504T0155Z — per N59).

## PASS — claimable C02 frontiers

| run_id (recipe) | stop | n | mean_final_val_loss | score (3.28−mean)·√n | verdict |
|---|---|---|---|---|---|
| v12iso-musched-h3375-s3220 | 3220 | 12 | 3.278060 | 0.006720 | PASS — the "cleaner v12 claim" |
| v12iso-musched-h3375-s3195 | 3195 | 39 | 3.279185 | 0.005089 | PASS |
| formalprune-norespulse-from-tailresrmsstack-aggmom3hidden-h3375-stop3296 | 3296 | 72 | 3.279470 | 0.004494 | PASS — pruned formal stack |

Also passing (older, more conservative — above the C01 frontier): normuon-lr030-h3450-stop3400 and
normuon-lr025-h3500-stop3450 (N59; conservative controls, not the C02 lower frontier).

## REJECTED — below the noise floor at scale

| run_id (recipe) | stop | n | mean_final_val_loss | score | verdict |
|---|---|---|---|---|---|
| v12iso-musched-h3375-s3170 | 3170 | 15 | 3.280266 | negative | REJECTED (its 3-seed N58 hit did NOT survive n=15) |

## Reading
- The promoted C02 frontier is the n-verified **s3195 / s3220**, NOT the raw best (3170) nor the
  rejected sub-3195 stops. The rigor lesson (N59): the 3-seed 3170 floor failed the n-scaled gate,
  vindicating the prior turns' discipline of holding sub-3296 few-seed hits as stepping stones.
- The corridor is far below C01's 3296 but still ≈400 steps ABOVE the user's <2800 stretch target
  (not reached — trace N16). No NEW optimizer family delivered this; the gains are schedule/state-level
  (Muon2F-direction on hidden, endpoint EMA, the v12 mu_schedule) — staging O16, claims C02 Interpretation.
- Individual seed members of these means (independently confirmed against the cited logs):
  s3220 seed0=3.27791, seed9=3.27663; s3195 seed20=3.27727; norespulse-3296 seed5=3.27903;
  s3170 seed23=3.27980. Logs linked under `evidence/logs/`.
- config: `src/configs/v12iso_musched_v1_stop3220.py`  |  cores: `src/execution/*` (C02 stack).
