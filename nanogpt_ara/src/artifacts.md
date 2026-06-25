# Artifacts — pointer index

The concrete artifacts of this work persist in a linkable on-disk store (a run index + per-run
exports + submitted record configs). Per the ARA convention, they are represented here as a
**pointer index** — one entry per artifact store, with the granularity needed to resolve any single
run — not copied. Nothing is re-encoded as a prose stub; the method/recipes live in
[../logic/solution/](../logic/solution/).

## Run database (8,224 attached runs)

| Store | Path | What it is |
|---|---|---|
| Run index (CSV) | `data/runs_self_contained/runs.csv` | 8,224 rows + header; one row per run, the four Codex waves only |
| Run index (JSONL) | `data/runs_self_contained/runs.jsonl` | Same rows with nested artifact pointers (sha256, byte sizes) |
| Per-run exports | `data/runs_self_contained/agents/{codex_v1,codex_novelty,codex_v2,codex_v3}/runs/<export_id>/` | `metadata.json` + `launched_script.py` + `train.log` per run |

**Runs per wave** (from `runs.csv`): codex_v1 = 2,165; codex_novelty = 254; codex_v2 = 2,729;
codex_v3 = 3,076.

**`runs.csv` columns** (the per-run index schema):
`export_id, agent_version, agent_label, version, agent, family, purpose, status, run_id,
launched_at, final_val_loss, min_val_loss, final_step, train_steps, step_to_3_28, num_val_points,
train_time_s, step_avg_ms, is_completed, is_canceled, is_preempted, is_timeout, is_failed,
is_incomplete, is_stat_verify, config_path_source, run_dir, train_log, launched_script,
source_snapshot, console_log, launch_stub`.

**`metadata.json` per run** carries the same fields plus `artifacts.{launched_script,train_log}`
with `sha256` and `original_path`, `purpose` (`statistical_verification` / screen / ablation),
`family` (the slug prefix), and the original `repo_path`/`log_path`. Example: the Muon baseline
`00606-baseline-muon-3500-seed0-4ecc6ecfa1` records `final_val_loss 3.27658`, `step_to_3_28 3500`,
`is_stat_verify true`.

**Family distribution** (top families in `runs.csv`): `v12` (2,672), `tailresrmsstack` (651),
`normuon` (507), `muon2f` (413), `formalprune` (162), `v12iso` (120), `adammini` (66),
`v12musched` (25), plus the v3 `v3u2900-worker*` and `v3prune-w258loo-nosphere` (16) families and
the novelty `ngi`/`rsi`/`vfg` families — i.e. the run store directly indexes the screens, frontier
walks, pruning rounds, and significance cohorts referenced by [../logic/experiments.md](../logic/experiments.md).

> Note (`README.md:91-100`): the bulk raw logs under `agents/*/runs/<id>/` and
> `*/codex/scratchpad/runs/` (~3 GB) are git-ignored but kept on disk so these pointers resolve; the
> CSV/JSONL index and the metadata/script/log per run are tracked.

## Submitted record configs (the three frontiers)

| Wave | Path | Bin | Cohort |
|---|---|---|---|
| v1 | `record_configs/20260515_codex_v1_v12iso_3205/` | 3205 | n=16, seeds 0..15 |
| v2 | `record_configs/20260515_codex_v2_legal_3037/` | 3037 | n=16, seeds 0..15 |
| v3 | `record_configs/20260515_codex_v3_nosphere_2949/` | 2949 | n=16, seeds 0..15 |

Each contains `README.md` (recipe + seed table + significance), `loss_curves.png`, `pruning.png`,
and `pruning_data.json` (the raw leave-one-out contributions, mirrored under
[../evidence/data/](../evidence/data/)). The submitted v2 variant file is
`legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py` (named in
`../../v2/codex/scratchpad/THREAD.md:810`); the v3 submission tree is `v3/codex/scratchpad/submission/`.

## In-worktree scratchpad assets (per wave)

Each wave's `*/codex/scratchpad/` holds the journal and working set, all tracked:
`THREAD.md` (the append-only journal), `runs.jsonl` (in-worktree run index), `variants/` (diagnostic
script copies), `ideas/` (per-idea deep memos), `sbatch-stubs/`, `papers/` (paper subagent
writeups), and `picklist.md`/`clusters.md` (v1). The v3 wave also has
`w258_2940_leave_one_out_pruning_20260513.md` (the W258 pruning record) and `tools/`.

## Why no `src/execution/` transcription

Every concrete artifact here **persists in the linkable store above** (the run database and record
configs), and each submitted run's exact code is self-logged inside its own `train.log`. There is
no code that lives *only* inside this artifact and would otherwise be lost, so per ARA Rule 14 the
correct representation is this pointer index — not a lossy copy of selected scripts into
`src/execution/`.
