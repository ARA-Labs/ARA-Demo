# Results — C07: Aurora tail-tune committed frontier (ts3037 → ts3027; the FIRST compliant gated stop below 3037)

> **Re-export, not a fresh measurement.** Every score below already lives in this wave's `trace/`
> node N87 `result:` field (and N88 for the rejected lower bins) and in `logic/claims.md` C07's
> Statement / Evidence basis. No `runs.csv` read; the values are the committed-cohort statistics the
> N87 walk computed from the per-run trainer logs.
>
> **Speedrun claim rule**: claimable iff `(3.28 − mean) · sqrt(n) ≥ 0.004` by EXACT fixed-step
> cohort (the SAME C02/C04/C06 gate). C07's closure is an **artifact commitment**: the recipes are
> committed code-only into canonical `records/track_3_optimization/train_gpt_simple.py`.

- **Claim**: C07 (supported, depends on C06, C04, C05).  **Wave**: v3.
- **Source trace node**: N87 (resolved) — "Aurora proj-only beta-ramp TAIL-TUNE walks ... from ts3037 DOWN to ts3027 — THREE committed N=8 promotions"; lower-bin closure N88.
- **Compliance premise**: C05 — byte-identical-Architecture base, enforced by `src/execution/launch_variant_gate.sh`.
- **Recipe**: tail-tuned proj-only Aurora (config: `src/configs/v3_aurora_tailtune_ts3027.py`; tail schedule: `src/execution/aurora_beta_tail_schedule.py`; Aurora: `src/execution/aurora_preconditioner.py`).

## PASS — the three COMMITTED promotions (the frontier walks ts3037 → ts3027)

| promotion (recipe) | stop | n | mean_final_val_loss | score (3.28−mean)·√n | commit | verdict |
|---|---|---|---|---|---|---|
| direct beta0.35 proj-only | 3029 | 8 | 3.277816 | +0.006177 | (promoted .py) | PASS (ckpt3025 +0.005360; n=10 +0.006002) |
| late beta-ramp 0.35→0.50 (t2450 r350) | 3028 | 8 | 3.278039 | +0.005547 | **e8d7bbe** | PASS (ckpt3025 +0.004890; n=12 +0.006914) |
| beta-preload + endpoint-lookahead (p012, finalhi) | **3027** | 8 | 3.278506 | **+0.004225** | **e76d686** (docs 737b8b9) | PASS — the lowest committed gated stop (n=12 +0.005595) |

The ts3027 N=8 per-seed losses (the committed first-eight):
`[3.28031, 3.27759, 3.27725, 3.27872, 3.27974, 3.27806, 3.27816, 3.27822]` → mean 3.278506. The pass
is **max-limited by the single 3.28031 seed** (the seed-fragility the gate is designed to police);
N=12 (reserve r9–r12) → mean 3.278385, +0.005595 confirms robustness.

## REJECTED — the 3026 barrier + the entire sub-3000 (ts2999) mechanism hunt (N88)

| run cohort (recipe family) | stop | n | mean | score / note | verdict |
|---|---|---|---|---|---|
| direct ts3026 beta-preload analog | 3026 | 4 | 3.279435 | "does not port one step lower" | REJECTED |
| rank8-subbrake (best conditional mechanism) | 3026 | 8 | 3.278641 | +0.003843 (N=4 was 3.278548) | FAIL on expansion |
| dinertia-switch-b997-l012 | 3026/3000 | 4 / 5 | 3.27830 / 3.280306 | barely clears N=4 but step-3000 5-seed 3.280306 | NOT sub-3000 |
| tailfresh-dualmom (ts2999 cascade best) | 2999 | 5 | ~3.27974 | strongest multi-seed near-miss | FAIL |
| earlyfactor-delay / cautious-wd-gate / depth-wave (ts2999 single-seed hits) | 2999 | 1→4 | 3.27824 / 3.27798 / 3.27849 → ~3.2805–3.2810 on N=4 | high-variance single seeds | FAIL |
| SOAP-Aurora-Contra (user's KellerJordan suggestion) | 2999 | 5 | 3.28006 (proj-only s003); 3.28027 (fc+proj s006) | "not the sub-3000 answer as configured" | FAIL |

## Reading
- The compliant gated frontier on the Aurora/C04 backbone bottoms out at **ts3027** (an ~10-step
  advance over C04/C06's ts3037), reached by ENDPOINT TAIL-SHAPING — a beta-ramp + a terminal
  beta-preload with endpoint-aligned lookahead — **NOT a new optimizer mechanism** (the Aurora
  mechanism is identical to C06). This RESOLVES the standing C04/C06 lower-bin question (O28 / N83,
  which at v3-001 closed it NEGATIVELY at ts3025/3035) POSITIVELY.
- **Identical rigor coda**: the 3026 barrier does not yield to outlier-control or mean-shift
  mechanisms, and the entire sub-3000 family clusters at ~3.280 (N=8 viability needs mean ≤ ~3.27859),
  never gating below ts3027 — the SAME stop-knob/seed-fragility discipline as C02-3170 / C04-2962 /
  C06-sub3037. The runs-table sub-3000 single seeds are noise-floor artifacts.
- C07 is the **first lineage claim whose closure is an ARTIFACT COMMITMENT** (code committed to
  canonical), not only a commented stat-pass. The exhaustion of sub-3000 on this backbone triggered
  the public-frontier pivot (N89 → C08).
- Stays ~37 steps ABOVE the ~2990 public PR #294 floor and ~87–127 above the v3 sub-2950/sub-2900
  goal (NOT reached). Logs linked under `evidence/logs/` (C07 section). config:
  `src/configs/v3_aurora_tailtune_ts3027.py` | core: `src/execution/aurora_beta_tail_schedule.py`.
