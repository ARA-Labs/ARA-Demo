# Results — C04: architecture-compliant statistical pass (the v2 frontier; the C02/N59 gate re-run)

> **Re-export, not a fresh measurement.** Every score below already lives in this wave's `trace/`
> node N78 `result:` field (and N77 for the frontier walk) and in `logic/claims.md` C04's
> Statement / Evidence basis. Per-run final losses independently confirmed against the cited run
> logs under `v2/codex/scratchpad/runs/` (each run's `indexed_run` line carries `final_val_loss`,
> `first_step_le_3p28`, and the `variant:` source).
>
> **Speedrun claim rule** (logic/concepts.md "Noise floor / statistical-significance gate"): a
> recipe is claimable iff `(3.28 − mean_final_val_loss) · sqrt(n) ≥ 0.004`, computed by EXACT
> fixed-step cohort (anti-p-hacking: fixed-step cohorts + same-checkpoint scan, not per-run
> val-spam). This is the SAME gate that crystallized C02 at v1-007/N59, now applied on the
> architecture-COMPLIANT base (C05).

- **Claim**: C04 (supported, depends on C05).  **Wave**: v2.
- **Source trace node**: N78 (resolved) — "Submission-validity statistical pass ... crystallizes O23 → C04"; frontier walk N77.
- **Compliance premise**: C05 — byte-identical-Architecture base (baseline `RMSNorm.forward` + q/k `F.rms_norm`), enforced by `src/execution/launch_variant_gate.sh`.
- **Recipe**: `legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625` (config: `src/configs/legal_v12opt_ts3037_v2.py`; core: `src/execution/legal_v12opt_muon_contra.py`).

## PASS — the claimable C04 frontier (ts3037)

| run cohort (recipe) | stop | n | mean_final_val_loss | score (3.28−mean)·√n | verdict |
|---|---|---|---|---|---|
| legal-v12opt-rolewd-rolelr2-lookahead-…-ts3037-cm0225-attn0625-sig | 3037 | 8 | 3.2783775 | 0.004589 (z=3.53, σ≈0.0013, one-sided p≈0.000208) | PASS — the verified compliant frontier |

The 8 `ts3037` per-seed final losses (the cohort, from the `sig-r1..r8` logs): `[3.27823, 3.27882,
3.27831, 3.27862, 3.27769, 3.27845, 3.27919, 3.27771]` → mean 3.2783775. Each crosses 3.28 by step
3025 (`first_step_le_3p28: 3025`) but the run early-stops at `final_step: 3037`; **3037 is the
earliest COMMON validation checkpoint whose cohort passes** (step 3025's same-checkpoint cohort
scores only 0.002454 → FAIL).

Older long-step compliant controls also pass but are NOT the frontier (conservative, above 3037):
`legal_v12opt_ts3100` n=3 score 0.00551; `ts3150` 0.00936; `ts3200` 0.01652 (N78).

## REJECTED — the low-step legal frontier (noise-floor artifacts by the cohort gate)

| run cohort (recipe family) | stop | n | mean_final_val_loss | score | verdict |
|---|---|---|---|---|---|
| rolewd-rolelr2-lookahead-…-cm0225-attn0625 | 2962 | 38 | 3.28243 | −0.01496 | REJECTED |
| rolewd-rolelr2-lookahead-…-cm0225-attn0625 | 2963 | 22 | 3.28248 | −0.01163 | REJECTED |
| rolewd-rolelr2-lookahead-…-cm0225-attn0625 | 2970 | 21 | 3.28158 | −0.00724 | REJECTED |
| rolewd-combo-…-cm0225-attn0625             | 2982 | 17 | 3.28131 | −0.00539 | REJECTED |
| (fixed-step cohorts off the clean ts2962 stack) ts2987 | 2987 | 7–8 | 3.28165 | −0.00438 | FAIL |
| (fixed-step cohorts off the clean ts2962 stack) ts3012 | 3012 | 8 | 3.27982 | 0.00052 | FAIL |
| step 3025 (same-checkpoint anti-val-spam scan) | 3025 | — | 3.279132 | 0.002454 | FAIL |

## Reading
- The verified compliant frontier is **ts3037**, NOT the single-seed low-step crossings the N77 walk
  reached (down to step 2962: `ts2962-r41` final 3.27992 crossing @2962; `ts2963-r11` 3.27947;
  `ts2970-r12` 3.27942; `ts2982-r32` 3.2796 crossing @2975). Those single-seed crossings are
  as-committed INPUTS, not achieved bins — by the cohort gate they FAIL.
- **Identical rigor coda to C02**: just as C02's lower 3170 floor was REJECTED at n=15 and C02 settled
  on the n-verified s3195/s3220, here the low-step (`ts2962`–`ts2982`) cohorts are REJECTED and the
  verified frontier settles at the higher, compliant `ts3037`.
- This is the v2 wave's FIRST architecture-compliant AND statistically-verified frontier. It confirms
  the reading (C05/N78) that "the invalid forward-path change materially helped the sub-3000 behavior":
  removing the forward-path change (C03's cc-v12 base) AND imposing the gate moved the verified
  frontier UP from C03's claimed sub-3000 to 3037.
- Reproducibility (N78): each `ts3037` seed's indexed `source_log` exists and begins with the exact
  `legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py` source; imports stdlib + PyTorch
  only (`AdamW` + local Muon), no third-party optimizer library. Logs linked under `evidence/logs/`.
- Still ABOVE the user's <2800 stretch target (not reached — trace N16). config:
  `src/configs/legal_v12opt_ts3037_v2.py`  |  core: `src/execution/legal_v12opt_muon_contra.py`,
  `launch_variant_gate.sh`.
