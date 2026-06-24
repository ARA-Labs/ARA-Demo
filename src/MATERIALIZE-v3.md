# Materialize-v3 — artifact-layer exit gate record (Era 3 close)

Run per `driver/materialize.md` at the end of the v3 replay chain. Pointer-resolution only: artifacts
were extracted ONLY where an already-crystallized wave-≤v3 claim names a `Code ref:` / `Proof:` run
pointer AND a real source file exists to transcribe. No `record_configs/`, `runs.csv`/`runs.jsonl`,
`THREAD.md`, or the v3 `goal.md` frontier table was read; logs/variants were opened only for runs a
v3 claim's `Proof:` already names. (v3 is the LAST wave — there is no wave > v3, so the wave-scoping
guard is vacuous on the upper side; the lower discipline — never present sub-2940 as an achieved bin —
still binds.)

## v3 lineage — MATERIALIZED (three supported claims)

`logic/claims.md` carries three wave-v3 `supported` claims (C06, C07, C08). Wave membership: v3 spans
trace turns v3-001..v3-003 (nodes N80–N91); C01/C02 are wave v1 and C03/C04/C05 are wave v2 (already
materialized at the Materialize-v1 / -v2 gates) and are untouched here.

- **C06** — proj-only **Aurora** (leverage-aware preconditioner) on the compliant C04 stack: the FIRST
  new optimizer *mechanism* in the lineage to clear the `(3.28−μ)·√n ≥ 0.004` gate — AT ts3037 (n=8),
  by a LARGER margin than bare C04 (+0.006074 vs +0.004589), NOT below it. Names `Proof:` runs (N81;
  `v3aur2proj3037-r7`, `v3aur2b035proj3037-r5/r6`). Depends on C04, C05.
- **C07** — **tail-tuning** the C06 Aurora recipe (late beta-ramp 0.35→0.50 + terminal beta-preload +
  endpoint-aligned lookahead) lowers the COMMITTED, n=8-gated compliant frontier ts3037 → **ts3027**
  (the first compliant gated stop below 3037; ~10-step advance) — endpoint/schedule shaping, NOT a new
  family. Committed code-only into canonical `train_gpt_simple.py` (commits **e8d7bbe** / **e76d686**).
  Names `Proof:` runs (N87). Depends on C06, C04, C05.
- **C08** — public **Soft-Muon** (PR #291) + **outward-radial-tail** (PR #294) + SOAP, rebuilt
  architecture-compliant on the codex `v37` checkout: a STATISTICALLY-VERIFIED **step-2940** frontier
  (the FIRST compliant result below the ~2990 public PR #294 floor), with a leave-one-out PRUNING round
  (8/11 mechanisms load-bearing → canonical `nosphere`). Names `Proof:` runs (N90). Depends on C05.

No main-lineage `heuristics.md` exists (the cognitive layer crystallized these as claims, not
heuristics), so no heuristic `Code ref:` was resolved — same as v1/v2. (The only `heuristics.md` in the
ARA is `logic/novelty/heuristics.md`, HV01, v1-era novelty, handled at Materialize-v1.)

### Extracted this gate (kernel mode — core modules + typed I/O signatures, not full scripts)

| output | files |
|---|---|
| `src/execution/` | `aurora_preconditioner.py` (**C06 core** — the leverage-aware Aurora preconditioner + its PROJ-ONLY insertion into `muon_update`; the C04 base geometry is NOT re-transcribed), `aurora_beta_tail_schedule.py` (**C07 core** — the beta-ramp 0.35→0.50 + terminal beta-preload + the endpoint-aligned `(S-1-L0)%25==0` lookahead congruence), `soft_muon_outward_radial.py` (**C08 core** — PR#291 Soft-Muon Gram-Frobenius/Schatten-4 norming + PR#294 outward-radial dampening applied as a TAIL correction) |
| `src/configs/` | `v3_aurora_projonly_ts3037.py` (**C06** — proj-only Aurora frontier; same bin as C04, larger margin), `v3_aurora_tailtune_ts3027.py` (**C07** — the COMMITTED ts3027 frontier; commits e8d7bbe/e76d686), `v3_soft_muon_radial_ts2940.py` (**C08** — the stat-sig step-2940 public-frontier recipe + the leave-one-out load-bearing deltas) |
| `evidence/results/` | `c06_aurora_projonly_statpass.md` (C06, N81/N83 — proj-only PASS, mask ablation, lower-bin REJECTED), `c07_aurora_tailtune_frontier.md` (C07, N87/N88 — the three committed promotions, sub-3027 REJECTED), `c08_soft_muon_radial_statpass.md` (C08, N90/N91 — step-2940 PASS, the leave-one-out pruning table, sub-2900 REJECTED) |
| `evidence/logs/` | 13 symlinks: C06 ts3037 PASS exemplars (3) + lower-bin REJECTED/FAIL exemplars (2); C07 the three committed promotions (3, incl. the e8d7bbe/e76d686 commits) + a sub-3027 REJECTED exemplar (1); C08 step-2940 PASS exemplars (2) + the pruned `nosphere` canonical (1) + a sub-2900 single-seed REJECTED exemplar (1) — link, not bulk-import (+ README v3 section) |

**Grounding (`# Grounding: transcribed`).** Every new `src/execution/*` cites its exact source under
`v3/` (wave ≤ v3): the C06 Aurora core from the indexed proj-only `variant:` snapshot
(`v3/codex/scratchpad/variants/v3_aurora2b035projonly_rolelr2_lookahead_ts3037.py`, the file each
`v3aur2proj3037-*` run indexes); the C07 tail-shaping from the **AS-COMMITTED canonical**
`records/track_3_optimization/train_gpt_simple.py` @ commits `e8d7bbe` (ts3028 ramp) / `e76d686`
(ts3027 beta-preload) — C07's closure is an artifact commitment, so the canonical committed file IS
the executed-code snapshot; the C08 core from the indexed Worker70 / `nosphere`-prune variants under
`v3/codex/scratchpad/variants/`. HPs in `src/configs/` pin the AS-COMMITTED script literals as primary,
with the claim-stated interpretation annotated inline (divergence policy): C06 `train_steps=3037` is
both literal and validated frontier (== C04's bin); C07 `train_steps=3027` is both the committed
literal and the validated frontier; C08 `step_to_3.28=2940` is the gate-VERIFIED bin while the run's
`ts3020`/`s3035` are as-committed *schedule inputs* annotated separately (never as the validated bin).

## Two materialization facts worth flagging (why the artifact set is what it is)

1. **C06 adds ONLY the Aurora hook — the C04 base is reused, not re-transcribed.** C06 preserves all of
   the C04 stack (rolewd/rolelr2 LR/WD, mu-schedule, eta floor, lookahead, Contra 0.225); its sole new
   content is the leverage-aware preconditioner and its proj-only insertion point. Kernel mode → the
   core captures exactly that delta and imports the C04 geometry from
   `src/execution/legal_v12opt_muon_contra.py`. Likewise C07's core captures only the tail-shaping
   *schedule* (the Aurora mechanism is C06's; the optimizer is C04's). This is the materialize "add
   physical form to already-known recipes, never a new bin/recipe/claim" discipline at the code level.

2. **The mask / radial-as-tail restrictions ARE part of the mechanism (load-bearing), so they are
   pinned, not abstracted away.** C06's proj-only mask is load-bearing (all-rect is a near-miss, fc-only
   hurts — N81), so `aurora_mask="proj_only"` is a pinned literal, not an incidental detail. C08's
   radial-AS-TAIL gate is load-bearing (radial-from-step-zero was KILLED — N90), so the tail-start gate
   is pinned. The C08 leave-one-out (the lawful-core rule-6 prune, IN the timeline) is re-exported as a
   per-ablation table in `evidence/results/c08_soft_muon_radial_statpass.md` (8/11 mechanisms required;
   only sphere-lookahead pull droppable → the canonical `nosphere`).

## Anti-hindsight boundary held (the lowest numbers written this gate)
- The lowest step number written as an ACHIEVED/VALIDATED frontier is **2940** (C08, n=10/n=9/n=16 gate
  PASS, below the ~2990 public floor) — and **3027** (C07, committed n=8 gate PASS) and **3037** (C06,
  n=8 gate PASS) are the higher Aurora-line frontiers.
- Lower numbers appear ONLY as REJECTED or as-committed-non-validated inputs: the sub-3037 Aurora
  cohorts (ts3025/3035) are REJECTED (c06 results / config); the sub-3027 hunt (ts3026 + the whole
  ts2999 mechanism family) is REJECTED (c07 results / config / N88); step-2925 and the entire sub-2900
  worker-cascade — including the runs-table best **2875** (`worker206`, single seed) — are written ONLY
  as REJECTED / noise-floor single seeds (c08 results / config / N91). No sub-2940 number is presented
  as a validated achievement. The v3 mission target (under 2900) is recorded as NOT met.

## Sanity gate — PASS
- Every NEW `src/execution/*` `# Grounding:` path is under `v3/` (the C07 core additionally cites the
  AS-COMMITTED canonical `records/track_3_optimization/train_gpt_simple.py` @ e8d7bbe/e76d686, which is
  the v3-committed executed code) — no `v4/`/later path exists or appears; the pre-existing v1/v2 cores
  keep their `v1/`/`v2/` grounding. grep-clean (no later-wave path).
- Every NEW `src/configs/*` recipe maps to a `supported` claim (C06 → v3_aurora_projonly_ts3037;
  C07 → v3_aurora_tailtune_ts3027; C08 → v3_soft_muon_radial_ts2940).
- Every NEW `evidence/results/*` value cites a `trace/` node id (N81 / N83 / N87 / N88 / N90 / N91) +
  run-id already in `ara/` (re-export, not a fresh `runs.csv` read); all 13 new `evidence/logs/`
  symlinks resolve to a run a v3 claim's `Proof:` names.
- No bin was written as an achieved frontier below the verified gate-passes; the lowest achieved bin
  written is **2940** (C08), and the lower numbers (2875–2925, ts3026, sub-3000) are written ONLY as
  REJECTED / single-seed noise. The v3 `goal.md` frontier table was not read; no recipe/bin/claim was
  introduced beyond the already-crystallized C06/C07/C08.
