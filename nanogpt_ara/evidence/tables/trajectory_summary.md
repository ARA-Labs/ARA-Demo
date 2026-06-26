# Table — trajectory summary (the four waves)

The single-agent Codex arc on `track_3_optimization`. "Bin" = `step_to_3.28` (lower is better). Cohort
mean/score are the submitted records' N=16 reproduction; `score = (3.28 − μ)·√n` must be ≥ 0.004 to pass.

| Stage | Wave | Bin | Cohort | Mean val @ bin | Std | Score (3.28−μ)·√n | Runs | Outcome |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Muon baseline | — | 3500 | 1 | 3.27658 (final) | — | — | (baseline) | the bar to beat |
| AdamW baseline | — | 5625 | — | — | — | — | (baseline) | weak baseline |
| **v1** | v1 (v12iso / MuSched) | **3205** | 16 | 3.27897187 | 0.00069831 | **0.00411250** | 2,165 | submitted record |
| novelty | novelty (isolated) | — | — | — | — | — | 254 | **negative** — no promotable submission |
| **v2** | v2 (legal frontier) | **3037** | 16 | 3.27853000 | 0.00080602 | **0.00588000** | 2,729 | submitted record |
| **v3** | v3 (nosphere) | **2949** | 16 | 3.27886125 | 0.00125939 | **0.00455500** | 3,076 | submitted record (viable to ~2940 @ N=16) |

Total Codex runs across the four waves: **8,224** (= 2,165 + 254 + 2,729 + 3,076).

**Notes.**
- Each record passes the Track-3 threshold (≥0.004); with σ=0.0013: v1 z=3.1635 (p=0.00078), v2 z=4.5231
  (p=3.05e-06), v3 z=3.5038 (p=0.000229) — all p<0.001.
- v3 runs train to `train_steps=3020`; the submitted bin is the logged step-2949 checkpoint. The v3
  cohort mean at step 3020 is **3.27670**.
- Bins are **not** the lowest single-seed crossings: v1's `s3170`, v2's `ts2962`, and v3's deeper
  per-seed crossings were all rejected/superseded by the statistical-claimability gate (C06, C11).

**Sources:** `record_configs/20260515_codex_v1_v12iso_3205/README.md:3,21-24`;
`record_configs/20260515_codex_v2_legal_3037/README.md:3,19-24`;
`record_configs/20260515_codex_v3_nosphere_2949/README.md:3,20-27,47`; per-wave run counts from
`data/runs_self_contained/runs.csv` (`version` column); baselines from `v1/codex/goal.md:6-8`.
