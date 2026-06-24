# Materialize-v2 — artifact-layer exit gate record (Era 2 close)

Run per `driver/materialize.md` at the end of the v2 replay chain. Pointer-resolution only: artifacts
were extracted ONLY where an already-crystallized wave-≤v2 claim names a `Code ref:` / `Proof:` run
pointer AND a real source file exists to transcribe. No `record_configs/`, `runs.csv`/`runs.jsonl`,
`THREAD.md`, or any wave > v2 (`v3/...`) path was read; the v2 `goal.md` frontier table was NOT read;
logs/variants were opened only for runs a v2 claim's `Proof:` already names.

## v2 lineage — MATERIALIZED (three supported claims)

`logic/claims.md` carries three wave-v2 `supported` claims (C03, C04, C05). Wave membership: v2 spans
trace turns v2-001..v2-005 (nodes N61–N79); C01/C02 are wave v1 (already materialized at the
Materialize-v1 gate) and are untouched here.

- **C03** — cc-v12 step-count frontier (existence + 2-seed reproduced at ts2999). Names `Proof:` run
  pointers (N68; `v12-ts2999-r4/r7`, …). **Base NON-COMPLIANT / quarantined** (see C05).
- **C04** — architecture-COMPLIANT, statistically-verified frontier at step_to_3.28 = 3037
  (`legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625`, n=8 cohort gate). Depends on C05.
- **C05** — compliance hard-rule: the cc-v12 base VIOLATES the no-forward/no-norm rule
  (`RMSNorm.forward` / q-k-norm precision change); only byte-identical-Architecture variants are
  submittable. A rule-surface constraint (not a performance recipe); its enforcement artifact is the
  launch-time gate.

No main-lineage `heuristics.md` exists (the cognitive layer crystallized these as claims, not
heuristics), so no heuristic `Code ref:` was resolved. (The only `logic/novelty/heuristics.md` entry,
HV01, is v1-era novelty and was handled — as a non-promotable diagnostic — at the Materialize-v1 gate.)

### Extracted this gate (kernel mode — core modules + typed I/O signatures, not full scripts)

| output | files |
|---|---|
| `src/execution/` | `legal_v12opt_muon_contra.py` (C04 core: Polar-Express NS5 + `muon_update` with the cm0225 contra-direction + role-split LR/WD builder + lookahead + mu-schedule), `launch_variant_gate.sh` (C05 enforcement artifact: the byte-identical-Architecture / baseline-RMSNorm / baseline-q-k-norm / no-gain-path launch gate) |
| `src/configs/` | `legal_v12opt_ts3037_v2.py` (C04 — the SUBMITTABLE verified frontier), `ccv12_ts2999_v2_NONCOMPLIANT.py` (C03 — records WHAT RAN on the quarantined non-compliant base; marked `submittable=False`) |
| `evidence/results/` | `c04_legal_v12opt_statpass.md` (C04, N77/N78 — cohort z-test: ts3037 PASS, low-step REJECTED), `c03_ccv12_stepcount_frontier.md` (C03, N68 — existence/2-seed, quarantine caveat) |
| `evidence/logs/` | 15 symlinks: C03 cc-v12 proof runs (5), the C04 ts3037 sig cohort (8), C04 rejected/control exemplars (2) — link, not bulk-import (+ README v2 section) |

**Grounding (`# Grounding: transcribed`).** Every new `src/execution/*` cites its exact source under
`v2/` (wave ≤ v2): the C04 core from the indexed `variant:` snapshot
`v2/codex/scratchpad/variants/legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py` (the
file each `sig-r*` run's `indexed_run` line names; N78 verified each run's `source_log` begins with it),
and the gate from `v2/codex/scratchpad/launch_variant.sh`. HPs in `src/configs/` pin the AS-COMMITTED
script literals as primary, with the claim-stated interpretation annotated inline (divergence policy):
for C04, `train_steps=3037` is BOTH the script literal AND the claim-validated frontier (they agree),
and the single-seed sub-3037 crossings are annotated as as-committed inputs that FAIL the cohort gate
(never pinned as achieved bins); for C03, `train_steps=2999` is the as-committed 2-seed anchor on the
non-compliant base, explicitly NOT a noise-floor-validated bin.

## Two claim-shaped special cases (why the artifact set is what it is)

1. **C03 has NO new `src/execution` core module — by design.** C03's discovered-recipe content is the
   STEP COUNT (`train_steps`), not an optimizer mechanism: it added no new optimizer/init lever (the
   cheap levers all closed — N63/N69; the schedule-denominator trick was 0/8 — N70). Its only
   distinctive code is the cc-v12 FORWARD PATH, which is a FORBIDDEN architecture change (C05), not an
   optimizer contribution — transcribing it as a "recipe core" would mis-state it (compiler Rule 14 /
   materialize Guard 5: capture what concretely exists as a recipe, no more). So C03 materializes as a
   config that records the as-committed `train_steps` on the explicitly-quarantined base, and nothing more.

2. **C05 is a rule-surface constraint, not a performance recipe** — so it has no `configs/` entry. But
   its enforcement is a CONCRETE artifact (the real `launch_variant.sh` gate), so that IS captured into
   `src/execution/launch_variant_gate.sh` (a genuine artifact in native form, not re-encoded prose).

## Anti-hindsight boundary held (the lowest numbers written this gate)
- The lowest step number written as an ACHIEVED/VALIDATED frontier is **3037** (C04, n=8 gate PASS).
- Lower numbers appear ONLY as REJECTED or as-committed-non-validated inputs: the single-seed legal
  crossings down to **2962** are recorded as REJECTED by the cohort gate (c04 results / config
  annotation), and C03's **2999** is recorded as a quarantined, non-noise-floor-gated existence anchor.
  No sub-3037 number is presented as a validated achievement. The v3 frontier table was not read; no
  v3 recipe/bin/claim was introduced.

## Sanity gate — PASS
- Every NEW `src/execution/*` `# Grounding:` path is under `v2/` (wave ≤ v2); no `v3/`/later path appears
  (the pre-existing v1 cores keep their `v1/` grounding). grep-clean.
- Every NEW `src/configs/*` recipe maps to a `supported` claim (C04 → legal_v12opt_ts3037_v2;
  C03 → ccv12_ts2999_v2_NONCOMPLIANT). C05 (rule-surface) maps to the gate in `src/execution/`, not a config.
- Every NEW `evidence/results/*` value cites a `trace/` node id (N68 / N77 / N78) + run-id already in
  `ara/` (re-export, not a fresh `runs.csv` read); all 15 new `evidence/logs/` symlinks resolve to a
  run a v2 claim's `Proof:` names.
- No bin below the next wave's (v3) start was written as achieved; the lowest achieved bin written is
  3037, and the lower numbers (2962–2999) are written ONLY as REJECTED / quarantined-non-validated.
