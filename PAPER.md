---
title: "Lowering the step count to val loss 3.28 on the track_3_optimization GPT benchmark (Codex speedrun)"
authors: ["Codex autonomous optimization agent"]
year: 2025
venue: "Internal autonomous-speedrunning experiment (track_3_optimization)"
doi: "Not available at t=0"
ara_version: "1.0"
domain: "neural-network optimization / LLM pretraining speedrun"
keywords:
  - Muon
  - AdamW
  - step_to_3.28
  - WSD schedule
  - noise-floor gate
  - optimizer search
  - FineWeb GPT pretraining
  - lawful core
claims_summary:
  - "No claims at t=0 — this is the time-invariant frame; every finding crystallizes later through the time-ordered replay."
abstract: >
  This is the t=0 FRAME of a single Agent-Native Research Artifact that a time-ordered replay
  accretes into. It captures only what the Codex agent knew at the very START of the
  experiment: the mission (reach 3.28 validation loss on the fixed train_gpt_simple.py
  benchmark in as few steps as possible), the two t=0 baselines (Muon at 3500 steps with
  lr=.025/wd=.0125, and AdamW at 5625 steps), the stretch target (below 2800 steps), the
  frozen architecture / batch / data / step definition transcribed from the canonical Muon
  baseline launched_script.py, the domain concepts in hand (Muon, Newton–Schulz
  orthogonalization, the step_to_3.28 "bin" metric, the noise-floor / statistical-significance
  gate, the lawful core, the fixed-benchmark constraints, the WSD schedule), and the open
  research questions seeded as root question nodes in the exploration tree. It contains NO
  results, NO claims with a supported/weakened/refuted status, NO achieved step-count below
  3500, and NO discovered recipe — by construction, to avoid hindsight.
---

# Lowering the step count to val loss 3.28 on the track_3_optimization GPT benchmark (Codex speedrun)

## Overview

The mission is to find an optimizer / hyperparameter / schedule / init combination that
reaches **3.28 validation loss** on the fixed benchmark `train_gpt_simple.py` in **as few
steps as possible**. At t=0 the SOTA is **Muon (lr=.025, wd=.0125) at 3500 steps**; the
**AdamW baseline is 5625 steps**; the user's stretch target is **below 2800 steps**. The
architecture, batch size, and data are frozen by rule, and each step is a single
forward-backward — so the entire search lives on the optimizer / schedule / init surface, and
every candidate is gated by a measured noise floor and reproduced across seeds (the "lawful
core").

This artifact is the **t=0 frame only**: a single ARA that a time-ordered replay will accrete
findings into, turn by turn. It deliberately holds **no results, no claims, no discovered
recipe, and no achieved step-count below 3500**. The cognitive layer states the problem, the
domain concepts, and the constraints in force at the start; the exploration tree seeds the
open research questions as root `question` nodes; `src/environment.md` transcribes the frozen
benchmark from the canonical baseline run. `logic/claims.md` and `evidence/` are intentionally
empty — every finding crystallizes later through the replay (written by `research-manager`),
and concrete recipes/configs/metrics are extracted by the `compiler` only at each main wave's
artifact exit gate. The novelty wave enters as an isolated `NV##` subtree during the replay;
there is nothing for it in the frame.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (O1–O3: fixed benchmark, Muon@3500 / AdamW@5625, the literature's confound problem) → gaps (G1–G6, the open levers) → key insight → assumptions |
| [concepts.md](logic/concepts.md) | t=0 domain concepts: Muon, Newton–Schulz (NS5), AdamW baseline / per-group split, the step_to_3.28 "bin" metric, the noise-floor / stat-sig gate, two-seed reproduction, the lawful core, fixed-benchmark constraints, recipe family / slug-stack, stuck detector, pruning rounds, the WSD schedule |
| [claims.md](logic/claims.md) | **Empty at t=0** — header only; no supported/weakened/refuted claims (every finding crystallizes later through replay) |
| [solution/constraints.md](logic/solution/constraints.md) | Frozen-benchmark boundary conditions + lawful-core process rules + assumptions + out-of-scope (no method-specific limitations yet) |

### Physical Layer (`/src`)
| File | Description |
|------|-------------|
| [environment.md](src/environment.md) | The FROZEN benchmark transcribed from the canonical baseline `launched_script.py`: architecture (12-layer GPT, model_dim 768, vocab 50304, head_dim 128, MLP 3072, seq_len 1024, RoPE, logit softcap 15, attn scale 0.12), batch (524288 tokens/step, mbs 64), data (FineWeb 10B shards), step definition, validation cadence, and the t=0 Muon SOTA recipe (the starting line) |
| [MATERIALIZE-v1.md](src/MATERIALIZE-v1.md) | **Materialize-v1 exit-gate record (Era 1 close).** Pointer-resolution log: the v1 main lineage materialized C01+C02 core modules/configs/metrics (below); the novelty lane carries **no `NV##` recipe by design** (genuine negative result, 0 promotable submissions; per `CV01`/`CV02` + seal `N60`). Sanity gate: PASS. |
| [MATERIALIZE-v2.md](src/MATERIALIZE-v2.md) | **Materialize-v2 exit-gate record (Era 2 close).** Pointer-resolution log: the v2 lineage materialized C04 (compliant stat-verified ts3037 frontier) + C05 (the launch-time compliance gate) core artifacts/config/metrics (below); C03's cc-v12 step-count anchor is materialized only as a **quarantined, non-submittable** config (its base violates the no-forward/no-norm rule, C05), with **no `src/execution` core** (its recipe content is the step count, not an optimizer — the forward-path change is forbidden, not a contribution). Lowest ACHIEVED bin written: 3037; sub-3037 (2962–2999) written only as REJECTED/quarantined. Sanity gate: PASS. |
| [MATERIALIZE-v3.md](src/MATERIALIZE-v3.md) | **Materialize-v3 exit-gate record (Era 3 close).** Pointer-resolution log: the v3 lineage materialized C06 (proj-only **Aurora** — the FIRST new-optimizer-mechanism gate pass, at ts3037), C07 (the Aurora **tail-tune** committed frontier ts3037→**ts3027**; commits e8d7bbe/e76d686), and C08 (the public **Soft-Muon + outward-radial-tail + SOAP** stat-verified **step-2940** — the FIRST compliant result below the ~2990 public PR #294 floor, leave-one-out pruned) core artifacts/configs/metrics (below). Lowest ACHIEVED bin written: **2940** (C08); the higher Aurora-line frontiers 3027 (C07) and 3037 (C06); sub-2940 (2875–2925), sub-3027 (ts3026 + the ts2999 hunt), and sub-3037 (ts3025/3035) written ONLY as REJECTED/single-seed noise. v3 mission target (under 2900) recorded NOT met. Sanity gate: PASS. |
| **`src/execution/` (materialized @ v1)** | Core optimizer/schedule modules (kernel mode — typed I/O signatures, each `# Grounding: transcribed (path:line)` from the wave-≤v1 run snapshots C01/C02 cite): [normuon.py](src/execution/normuon.py) (NS5 + NorMuon update — C01 core), [wsd_schedule.py](src/execution/wsd_schedule.py) (decoupled-WSD + beta2 warm-down — C01), [muon2f_hidden.py](src/execution/muon2f_hidden.py) (Muon2F-hidden + AggMo-3 — C02), [adam_mini.py](src/execution/adam_mini.py) (AdamMiniW optimizer1 — C02), [endpoint_ema_and_mu_schedule.py](src/execution/endpoint_ema_and_mu_schedule.py) (endpoint EMA + isolated v12 mu_schedule — C02) |
| **`src/execution/` (materialized @ v2)** | [legal_v12opt_muon_contra.py](src/execution/legal_v12opt_muon_contra.py) (**C04 core** — Polar-Express NS5 + `muon_update` with the `cm0225` contra-direction + role-split LR/WD builder `rolewd`/`rolelr2` + `lookahead` + mu-schedule; `# Grounding: transcribed` from the v2 ts3037 `variant:` snapshot), [launch_variant_gate.sh](src/execution/launch_variant_gate.sh) (**C05 enforcement artifact** — the byte-identical-Architecture / baseline-RMSNorm / baseline-q-k-norm / no-gain-path launch gate; transcribed from `v2/…/launch_variant.sh`) |
| **`src/configs/` (materialized @ v1)** | One commented config per committed recipe (as-committed script literals primary; claim values annotated): [normuon_v1_stop3296.py](src/configs/normuon_v1_stop3296.py) (C01 frontier), [muon2f_v1_stop3250.py](src/configs/muon2f_v1_stop3250.py) (C02 Muon2F stepping stone), [v12iso_musched_v1_stop3220.py](src/configs/v12iso_musched_v1_stop3220.py) (C02 statistically-verified claimable frontier) |
| **`src/configs/` (materialized @ v2)** | [legal_v12opt_ts3037_v2.py](src/configs/legal_v12opt_ts3037_v2.py) (**C04** — the SUBMITTABLE, n=8-verified compliant frontier; `train_steps=3037` is both script literal and validated frontier; sub-3037 single-seed crossings annotated as gate-FAILing inputs), [ccv12_ts2999_v2_NONCOMPLIANT.py](src/configs/ccv12_ts2999_v2_NONCOMPLIANT.py) (**C03** — records what ran on the quarantined cc-v12 base; `submittable=False`, superseded by C04) |
| **`src/execution/` (materialized @ v3)** | Core mechanisms for the three v3 claims (kernel mode; each `# Grounding: transcribed` from the wave-≤v3 variant/committed snapshots C06/C07/C08 cite): [aurora_preconditioner.py](src/execution/aurora_preconditioner.py) (**C06 core** — the leverage-aware Aurora preconditioner + its PROJ-ONLY insertion into `muon_update`; the FIRST new-mechanism gate pass), [aurora_beta_tail_schedule.py](src/execution/aurora_beta_tail_schedule.py) (**C07 core** — beta-ramp 0.35→0.50 + terminal beta-preload + the endpoint-aligned `(S-1-L0)%25==0` lookahead congruence), [soft_muon_outward_radial.py](src/execution/soft_muon_outward_radial.py) (**C08 core** — PR#291 Soft-Muon Gram-Frobenius/Schatten-4 norming + PR#294 outward-radial dampening as a TAIL correction) |
| **`src/configs/` (materialized @ v3)** | [v3_aurora_projonly_ts3037.py](src/configs/v3_aurora_projonly_ts3037.py) (**C06** — proj-only Aurora frontier; same bin as C04, larger margin +0.006074; `aurora_mask="proj_only"` is load-bearing), [v3_aurora_tailtune_ts3027.py](src/configs/v3_aurora_tailtune_ts3027.py) (**C07** — the COMMITTED ts3027 frontier; `train_steps=3027` both literal and validated; commits e8d7bbe/e76d686; sub-3027 annotated as gate-FAILing), [v3_soft_muon_radial_ts2940.py](src/configs/v3_soft_muon_radial_ts2940.py) (**C08** — the stat-verified step-2940 public-frontier recipe; `step_to_3.28=2940` is the validated bin while `ts3020`/`s3035` are as-committed schedule inputs; the leave-one-out load-bearing deltas annotated) |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 6-node research DAG — root `question` nodes ONLY (N01–N06), the open research questions from goal.md; no experiments, decisions, dead_ends, or answers yet |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Evidence index — the t=0 frame had no tables/figures; metric results + proof-run logs were filed at the Materialize-v1 exit gate (below) |
| **`evidence/results/` (materialized @ v1)** | Machine-readable metric tables re-exporting numbers already in this wave's `trace/` node `result:`/`evidence:` fields (each value cites its trace-node + run-id): [c01_normuon_wsd_frontier.md](evidence/results/c01_normuon_wsd_frontier.md) (C01, N12), [c02_compression_corridor.md](evidence/results/c02_compression_corridor.md) (C02 building blocks, N51/N53/N58), [c02_statistical_pass.md](evidence/results/c02_statistical_pass.md) (C02 speedrun-rule scores, N59) |
| **`evidence/results/` (materialized @ v2)** | [c04_legal_v12opt_statpass.md](evidence/results/c04_legal_v12opt_statpass.md) (C04, N77/N78 — the cohort z-test: ts3037 n=8 PASS score 0.004589, low-step ts2962–ts2982 REJECTED), [c03_ccv12_stepcount_frontier.md](evidence/results/c03_ccv12_stepcount_frontier.md) (C03, N68 — existence/2-seed ts2999, quarantine + supersession caveat) |
| **`evidence/logs/` (materialized @ v2)** | +15 symlinks (README v2 section): C03 cc-v12 proof runs (5), the C04 ts3037 verified cohort (8), C04 rejected/control exemplars (2) — the exact proof-run `train.log`s C03/C04's `Proof:` pointers name (link, not bulk-import) |
| **`evidence/results/` (materialized @ v3)** | [c06_aurora_projonly_statpass.md](evidence/results/c06_aurora_projonly_statpass.md) (C06, N81/N83 — proj-only Aurora PASS at ts3037, the mask ablation, the lower-bin REJECTED), [c07_aurora_tailtune_frontier.md](evidence/results/c07_aurora_tailtune_frontier.md) (C07, N87/N88 — the three committed promotions ts3029/3028/3027, sub-3027 REJECTED), [c08_soft_muon_radial_statpass.md](evidence/results/c08_soft_muon_radial_statpass.md) (C08, N90/N91 — step-2940 PASS, the leave-one-out pruning table (8/11 load-bearing → `nosphere`), sub-2900 REJECTED) |
| **`evidence/logs/` (materialized @ v3)** | +13 symlinks (README v3 section): the C06 ts3037 verified cohort exemplars (3) + lower-bin REJECTED/FAIL exemplars (2); the C07 three committed promotions (3, incl. commits e8d7bbe/e76d686) + a sub-3027 REJECTED exemplar (1); the C08 step-2940 verified cohort exemplars (2) + the pruned `nosphere` canonical (1) + a sub-2900 single-seed REJECTED exemplar (1) — the exact proof-run `train.log`s C06/C07/C08's `Proof:` pointers name (link, not bulk-import) |

## Frame status (anti-hindsight)
- **t=0 baselines recorded** (as observations, not claims): Muon @ 3500 steps; AdamW @ 5625 steps.
- **No claims**; **no achieved step-count below 3500**; **no named discovered recipe**.
- **Open questions seeded** as root `question` nodes (N01–N06).
- Anything absent from the three allowed inputs is marked **"Not available at t=0."**
