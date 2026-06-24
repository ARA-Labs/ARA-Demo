# Results — C06: proj-only Aurora statistical pass (the FIRST new-optimizer-mechanism gate pass; ts3037)

> **Re-export, not a fresh measurement.** Every score below already lives in this wave's `trace/`
> node N81 `result:` field (and N83 for the rejected lower bins) and in `logic/claims.md` C06's
> Statement / Evidence basis. No `runs.csv` read; each value is the cohort statistic the N81 Aurora
> campaign computed from the per-run trainer logs.
>
> **Speedrun claim rule** (logic/concepts.md "Noise floor / statistical-significance gate"): a
> recipe is claimable iff `(3.28 − mean_final_val_loss) · sqrt(n) ≥ 0.004`, by EXACT fixed-step
> cohort. This is the SAME gate that crystallized C02 (v1-007/N59) and C04 (v2-005/N78), now applied
> to the FIRST genuinely NEW optimizer MECHANISM (Aurora) on the architecture-compliant C04 base (C05).

- **Claim**: C06 (supported, depends on C04, C05).  **Wave**: v3.
- **Source trace node**: N81 (resolved) — "Aurora transplant on the compliant C04 stack ... the FIRST new optimizer mechanism to clear the gate"; lower-bin closure N83.
- **Compliance premise**: C05 — byte-identical-Architecture base, enforced by `src/execution/launch_variant_gate.sh`.
- **Recipe**: proj-only Aurora on the C04 stack (config: `src/configs/v3_aurora_projonly_ts3037.py`; core: `src/execution/aurora_preconditioner.py`; base: `src/execution/legal_v12opt_muon_contra.py`).

## PASS — the claimable C06 frontier (ts3037, proj-only Aurora)

| run cohort (recipe) | mask | beta | stop | n | mean_final_val_loss | score (3.28−mean)·√n | verdict |
|---|---|---|---|---|---|---|---|
| v3_aurora2_projonly | proj-only | 0.50 | 3037 | 8 | 3.277852 | **+0.006074** | PASS — the verified frontier (all 8 cross by 3025, one by 3000) |
| v3_aurora2b035_projonly | proj-only | 0.35 | 3037 | 8 | 3.278044 | **+0.005533** | PASS — secondary committed cohort |

C06 clears the **SAME bin as C04 (3037)** by a **larger margin** (+0.006074 vs C04's +0.004589) — it
does NOT lower the step bin; it is the FIRST new optimizer *mechanism* to gate at all (every prior
new-optimizer family washed out: O07/O11/O15/O20/O22/O24, N15/N22/N38/N52/N54/N77).

## REJECTED / NEAR-MISS — the mask ablation and the lower-bin attempts (N81 / N83)

| run cohort (recipe family) | mask | beta | stop | n | mean | score | verdict |
|---|---|---|---|---|---|---|---|
| v3_aurora2 (all-rect mask at the frontier bin) | all-rectangular | 0.25 | 3037 | 8 | 3.278588 | +0.003995 | NEAR-MISS (mask not load-bearing here → fails) |
| v3_aurora2b025 (direct lower bin) | all-rectangular | 0.25 | 3025 | 8 | 3.280365 | −0.001032 | REJECTED |
| v3_aurora2proj (direct lower bin) | proj-only | 0.50 | 3035 | 8 | 3.278666 | +0.003772 | FAIL (~0.00008 short) |
| proj-only beta0.5 ts3037 schedule, **checkpoint 3025** | proj-only | 0.50 | (3025 ckpt) | — | 3.278607 | +0.003939 | near-miss (not the verified bin) |
| proj-only beta0.35 ts3037 schedule, **checkpoint 3025** | proj-only | 0.35 | (3025 ckpt) | — | — | +0.003408 | near-miss (not the verified bin) |

## Reading
- The verified compliant frontier is **ts3037**, NOT lower. The mask ablation is informative:
  **proj/wide helps, fc/tall hurts, all-rect is intermediate** (the all-rect mask at ts3037 is a
  near-miss at +0.003995) — so the proj-only restriction is **part of the mechanism** (config
  `aurora_mask = "proj_only"`), not an incidental detail (O26).
- **Identical rigor coda to C02/C04**: just as C02's 3170 floor was REJECTED (n=15) and C04's
  ts2962–ts2982 cohorts were REJECTED, here the sub-3037 Aurora cohorts FAIL the gate and the verified
  frontier settles at the higher ts3037. The proj-tail eta-min screen's best single seed (2975,
  `v3aur2projtail-etamin001-3034` 3.27558) is a noise-floor artifact that walls at the stop, not a
  gated cohort (N83 / O28).
- **Distinctive significance**: the FIRST time a NEW optimizer mechanism (Aurora, leverage-aware
  preconditioning) clears the gate after the entire lineage's broad optimizer washout — answering
  N01/N03 in a new direction. But it does NOT advance the step-count frontier (same bin as C04); the
  bin is lowered later by C07 (ts3027, by tail-shaping the SAME Aurora mechanism).
- **The OTHER v3 branch failed structurally**: KLSOAP-H (a scale-invariant update tied to ‖W‖) FROZE
  the zero-init projection matrices (val ~5.73 vs ~3.70) — a mechanism failure, the dead_end N82 (O27).
- Logs linked under `evidence/logs/` (C06 section). config: `src/configs/v3_aurora_projonly_ts3037.py`
  | core: `src/execution/aurora_preconditioner.py`, `legal_v12opt_muon_contra.py`.
