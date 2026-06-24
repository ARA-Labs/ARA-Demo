# Results — C03: cc-v12 step-count frontier (2-seed reproduced)  *** base NON-COMPLIANT / quarantined ***

> **Re-export, not a fresh measurement.** Every value below already lives in this wave's `trace/`
> node N68 `result:` / `evidence:` fields and in `logic/claims.md` C03's Evidence basis. Per-run
> values independently confirmed against the cited run logs under `v2/codex/scratchpad/runs/`.
>
> **COMPLIANCE CAVEAT (load-bearing):** these runs are on the cc-v12 base, which VIOLATES the
> no-forward/no-norm hard rule (C05) — they are QUARANTINED as non-submittable. C03 is the
> EXISTENCE + 2-seed-reproducibility of a sub-3000 crossing on that (non-compliant) parent via pure
> step-count tuning; it is NOT noise-floor-gated and its sub-3000 frontier is SUPERSEDED for the
> compliant benchmark by C04 (ts3037). See evidence/results/c04_legal_v12opt_statpass.md.
>
> **Metric**: `step_to_3.28` = first step at which val_loss ≤ 3.28; each run early-stops AT its
> `train_steps`, so on these reproduced cells final_val_loss == the crossing value. Inherited
> starting line: cc-v12 claimed step_to_3.28 = 3025 (an external number adopted as the parent, N61).

- **Claim**: C03 (supported — existence + 2-seed reproducibility; CONTRADICTION vs C04/C05 flagged at N79, status flip deferred).
- **Source trace node**: N68 (resolved) — "cc-v12 step-count boundary hill-climb"; lever-side negatives N69/N70.
- **Wave**: v2.  **Working lever**: the literal `train_steps` (NOT a new optimizer/init mechanism; NOT the schedule-denominator trick — N70 0/8).

## 2-seed reproduced anchor (the C03 headline, ts2999, plain cc-v12)

| run_id | seed | train_steps (stop) | step_to_3.28 | final_val_loss | source |
|---|---|---|---|---|---|
| v12-ts2999 | r4 | 2999 | 2999 | 3.27985 | N68; run log :indexed_run |
| v12-ts2999 | r7 | 2999 | 2999 | 3.27996 | N68; run log :indexed_run |
| v12-ts2999 | r3 (plain ts3000) | 3000 | 3000 | 3.27987 | N68; run log :indexed_run |

## Below-record reproduction at higher stops (same recipe, same-stop multi-seed)

| run_id | seed | train_steps (stop) | step_to_3.28 | final_val_loss | source |
|---|---|---|---|---|---|
| v12-ts3022 | r1 | 3022 | 3022 | 3.27969 | N68 ("FIRST confirmed below-record hit") |
| v12-ts3022 | r3 | 3022 | 3022 | 3.27987 | N68 |
| v12-ts3022 | r6 | 3022 | 3022 | 3.27971 | N68 |
| v12-ts3012 | r2 | 3012 | 3000 (crosses @ val-step 3000 on a 3012-denominator schedule) | 3.27901 | N68 |
| v12-ts3012 | r3 | 3012 | 3000 | 3.27914 | N68 |

## Reading
- C03 is anchored at the 2-seed-reproduced **ts2999** (r4 + r7 both cross @2999), the v2 analogue of
  C01's v1-002 moment (existence + seed-reproducibility, with the noise-floor/pruning rigor steps
  still outstanding). The first confirmed below-record hit was `ts3022-r1` (beats the inherited 3025).
- The absolute step count is NOT crystallized as a fixed "best": every run is `stat_verify=False` and
  WALLS at its stop (final ≈ 3.2799, ~1-2e-4 below 3.28, inside the ~0.001 noise floor — the
  O02/O06/O08 stop-knob pattern). The lower single-seed SCRATCH hits (step 2992 `legal-v12opt-ts2992-r28`
  3.27984, and the 2993–2998 cells) are EXCLUDED from C03 — they are sub-noise-floor stepping stones
  pending a statistical pass + pruning round (none ran this turn).
- The margin is a RUN-CONTROL gain, not a new-lever gain: the cheap orthogonal levers
  (PMI/SVC/QKP/AdaGrad-Muon) and Mousse-Lite / QKT / pow1.5+attn0.5 all closed negative or at parity
  (N63/N69), and the explicit schedule-denominator transfer was 0/8 (N70) — isolating the working
  lever to the literal `train_steps`.
- **Quarantine / supersession**: the base is non-compliant (C05); when the recipe is rebuilt on a
  byte-identical-Architecture base AND made to clear the cohort gate, the verified frontier is **3037
  (C04), not sub-3000** — the sub-3000 behavior was forward-path-assisted (N78/N79). config (records
  WHAT RAN, not a submittable recipe): `src/configs/ccv12_ts2999_v2_NONCOMPLIANT.py`.
