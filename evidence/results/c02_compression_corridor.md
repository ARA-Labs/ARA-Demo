# Results — C02: the compression corridor below the C01 3296 frontier (building blocks)

> **Re-export, not a fresh measurement.** Values already live in this wave's `trace/` node
> `result:`/`evidence:` fields (N51, N53, N58) and `logic/claims.md` C02 Evidence basis.
> Per-run values confirmed against the cited run logs under `v1/codex/scratchpad/runs/`.
>
> **Metric**: `step_to_3.28` (lower better); runs walled at `train_steps`, so final == crossing on
> hits. The statistically-VERIFIED claimable frontiers are in `c02_statistical_pass.md`; THIS file
> records the multi-seed building blocks (stepping stones), which the narrator held BELOW the formal
> promotion bar pending that statistical pass.

- **Claim**: C02 (supported, depends on C01).  **Wave**: v1.
- **Source trace nodes**: N51 (Muon2F-hidden stepping stone), N53 (endpoint EMA), N58 (v12iso-musched).

## Block 1 — Muon2F-hidden stepping stone (N51): 3-seed reproduced at stop3250 / stop3237

| run_id | seed | stop | step_to_3.28 | final_val_loss | source |
|---|---|---|---|---|---|
| normuon-...-adamminiopt1-muon2fhidden-b2p095-eps1e3-tailresrmsstack-aggmom3hidden-h3375-stop3250 | seed0 | 3250 | 3250 | 3.27945 | N51; run log |
| ...stop3250 | seed1 | 3250 | 3250 | 3.27965 | N51; run log |
| ...stop3250 | seed2 | 3250 | 3250 | 3.27897 | N51; run log |
| ...stop3237 | seed0 | 3237 | 3237 | 3.27990 | N51; run log |
| ...stop3237 | seed1 | 3237 | 3237 | 3.27998 | N51; run log |
| ...stop3237 | seed2 | 3237 | 3237 | 3.27965 | N51; run log |
| ...stop3200 | seed0 | 3200 | — (miss) | 3.28251 | N51 (raw Muon2F walls ~3200; not closed by any internal modifier, N52) |

Reading: the first matrix-side preconditioner that HELPED (APOLLO/OLion/DION all washed out — O15,
N38/N46). Held as a STEPPING STONE, not promoted (gain over raw 3250 under the step-noise gate).

## Block 2 — endpoint EMA narrows it to ~stop3195 (N53), 3-seed

| run_id (abbrev) | seeds → step_to_3.28 (final_val_loss) | source |
|---|---|---|
| muon2f + ema0.99 start2375 stop3200 | s0/s1/s2 = 3200 (3.27967 / 3.27953 / 3.27941) | N53 |
| muon2f + ema0.99 start2250 stop3198 | s0/s1/s2 = 3198 (3.27997 / 3.27992 / 3.27964) | N53 |

Reading: EMA is the strongest endpoint-smoothing signal; fixed uniform SWA consistently worse.
Still held below the promotion bar (gain over raw Muon2F 3237 under the step-noise gate).

## Block 3 — isolated v12 mu_schedule lever (N58): 3-seed, practical floor walked 3195→3170

| run_id | seeds → step_to_3.28 (final_val_loss) | source |
|---|---|---|
| v12iso-musched-h3375-s3195 | s0/s1/s2 = 3195 (3.27917 / 3.27794 / 3.27894) | N58 |
| v12iso-musched-h3375-s3175 | s0/s1/s2 = 3175 (3.27931 / 3.27812 / 3.27982) | N58 |
| v12iso-musched-h3375-s3170 | s0/s1/s2 = 3170 (3.27916 / 3.27881 / 3.27953) | N58 |
| v12iso-musched-h3375-s3150 | seed2 = miss (3.28108); s0/s1 hit | N58 (sub-3170 seed2-limited) |

Reading: the strongest commented multi-seed compression of the run; the practical 3-seed floor is
3170, but **3170 FAILS the n-scaled statistical gate** (see `c02_statistical_pass.md` / N59), so the
PROMOTED claimable frontiers land higher, at 3195 / 3220.

- configs: `src/configs/muon2f_v1_stop3250.py`, `src/configs/v12iso_musched_v1_stop3220.py`
- cores: `src/execution/muon2f_hidden.py`, `adam_mini.py`, `endpoint_ema_and_mu_schedule.py`
