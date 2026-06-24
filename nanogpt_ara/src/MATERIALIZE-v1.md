# Materialize-v1 — artifact-layer exit gate record (Era 1 close)

Run per `driver/materialize.md` at the end of the v1 replay chain (after the Seal). Pointer-resolution
only: artifacts were extracted ONLY where an already-crystallized wave-≤v1 claim/heuristic names a
`Code ref:` / `Proof:` run pointer. No `record_configs/`, `runs.csv`/`runs.jsonl`, `THREAD.md`, or any
wave > v1 path was read; logs were opened only for runs a v1 claim's `Proof:` already names.

## v1 MAIN lineage — MATERIALIZED (two supported claims with run pointers)

`logic/claims.md` carries two crystallized `supported` claims, both naming `Proof:` run pointers:

- **C01** — NorMuon + decoupled-WSD sub-3500 frontier (2-seed reproduced at stop3296).
- **C02** — muon2f-hidden + endpoint-EMA + v12-mu_schedule corridor, step_to_3.28 ≈ 3195–3220,
  statistically verified (depends on C01).

No main-lineage `heuristics.md` exists (the cognitive layer crystallized these as claims, not
heuristics), so no heuristic `Code ref:` was resolved.

### Extracted this gate (kernel mode — core modules + typed I/O signatures, not full scripts)

| output | files |
|---|---|
| `src/execution/` | `normuon.py` (NS5 + normuon_update + NorMuon — C01 core), `wsd_schedule.py` (decoupled WSD + beta2 warm-down — C01), `muon2f_hidden.py` (Muon2F-hidden + AggMo-3 — C02), `adam_mini.py` (AdamMiniW opt1 — C02), `endpoint_ema_and_mu_schedule.py` (endpoint EMA + isolated v12 mu_schedule — C02) |
| `src/configs/` | `normuon_v1_stop3296.py` (C01), `muon2f_v1_stop3250.py` (C02 stepping stone), `v12iso_musched_v1_stop3220.py` (C02 claimable frontier) |
| `evidence/results/` | `c01_normuon_wsd_frontier.md`, `c02_compression_corridor.md`, `c02_statistical_pass.md` |
| `evidence/logs/` | 10 symlinks to the exact proof-run `train.log`s C01/C02 cite (+ README) |

Every `src/execution/*.py` carries `# Grounding: transcribed (path:line)`; the cited paths are the
run-log-embedded launched scripts (`…/runs/*.log`) and `…/variants/*.py` snapshots the claims' Proof:
pointers name — all under `v1/` (wave ≤ v1). HPs in `src/configs/` pin the AS-COMMITTED script
literals as primary, with claim-stated interpretation values annotated inline (divergence policy).

## novelty lane — NO NV## RECIPE BY DESIGN (genuine negative result)

`src/` carries **no `NV##` recipe by design**. The novelty wave (hard-isolated `logic/novelty/`,
`trace/novelty/`) produced **zero promotable submissions** — a real negative result, not an omission:
~40 dual-gated novel mechanisms over 254 runs, ALL closed negative under the lawful-core 2-seed /
noise-floor gate (best single-seed 3375 failed 2-seed reproduction; the only 2-seed-reproduced
crossing, VFG @3475, sat below the ~2× step noise floor). Per `logic/novelty/claims.md` CV01/CV02 and
the seal link `trace/exploration_tree.yaml:N60` (`also_depends_on: [NV08]`). There is no recipe to
extract, so nothing is materialized for the novelty lane (the one novelty heuristic, HV01, is an
init-family diagnostic whose only `Code ref:` is to `novelty/codex/scratchpad/variants/` diagnostic
edits, not a promotable recipe).

## Sanity gate — PASS
- Every `src/execution/*.py` `# Grounding:` path is under `v1/` (wave ≤ v1); no `v2/`/`v3/` path appears.
- Every `src/configs/*` recipe maps to a `supported` claim (C01 → normuon_v1_stop3296;
  C02 → muon2f_v1_stop3250 + v12iso_musched_v1_stop3220).
- Every `evidence/results/*` value cites a `trace/` node id (N08/N12/N14/N51/N53/N58/N59) + run-id
  already in `ara/` (re-export, not a fresh `runs.csv` read).
- No bin below the next wave's start was written (the next-wave frontier table was not read; the
  lowest number written, 3170, is recorded as REJECTED, not as an achieved bin).
