# Artifacts — pointer index

The concrete artifacts of this experiment persist in an external store (the run database and the
committed journals/record-configs). Per the ARA rule for externally-persisted artifacts, this is a
**pointer index** — one entry per artifact class, with stable anchors — not a copy. Paths are relative
to the repo root `experiments-autonomous-speedrunning-codex/`. The original on-cluster paths
(`/beegfs/elie/…`) are preserved inside `runs.jsonl` (`original_paths`).

## Run index (the comprehensive store)

- **A01 — `data/runs_self_contained/runs.csv`** — the run index, filtered to the four Codex waves:
  **8,224 runs** (header + 8,224 rows). 32 columns including `family`, `purpose`, `status`,
  `final_val_loss`, `final_step`, `train_steps`, `step_to_3_28`, the `is_*` status flags, and per-run
  artifact paths. Per-wave counts: **v1 = 2,165, novelty = 254, v2 = 2,729, v3 = 3,076**.
- **A02 — `data/runs_self_contained/runs.jsonl`** — the same index as JSONL, with full `artifacts`
  (bytes + sha256 + original_path), `local_paths`, and `original_paths` per run.
- **A03 — `data/runs_self_contained/agents/{codex_v1,codex_novelty,codex_v2,codex_v3}/runs/<id>/`** —
  per-run export directories (git-ignored on disk, ~1.8 GB): each holds `launched_script.py`,
  `metadata.json`, `train.log`, and (where present) `launch_stub.sh` / `source_snapshot.py`.

Every experiment in [../logic/experiments.md](../logic/experiments.md) names the `family` / `version` to
filter A01 by. The pruning sweeps, statistical cohorts, and baselines are all rows in A01.

## Submitted record configs (committed)

- **A04 — `record_configs/20260515_codex_v1_v12iso_3205/`** — v1 record: `README.md` (recipe + n=16 seed
  table), `loss_curves.png`, `pruning.png`, `pruning_data.json`.
- **A05 — `record_configs/20260515_codex_v2_legal_3037/`** — v2 record (same file set).
- **A06 — `record_configs/20260515_codex_v3_nosphere_2949/`** — v3 record (same file set).

These are mirrored into [../evidence/](../evidence/) (figures copied; READMEs/JSON transcribed into
evidence tables).

## Representative submitted script (v3 nosphere)

- **A07 — v3 nosphere submitted variant** —
  `data/runs_self_contained/agents/codex_v3/runs/10389-v3prune-w258loo-nosphere-r3-preempt-a81eb0c72f/launched_script.py`
  (54,473 bytes, sha256 `d51e67ef5a70e289ab728ec748dbdb12ecc85b8463e1ef73bcb508ab6ad73092`). Original
  path `…/scratchpad/variants/v3prune_w258loo_nosphere_spherela_p012_qkcontra0125_cvfloor060_softceil075_end2905_sched3025_vfade2850_rad045_warmsoapskip_ts3020.py`.
  Header credits the public PRs (#291/#274/#275/#278/#287); `FINAL_TRAIN_STEPS=3020`,
  `FINAL_SCHEDULE_STEPS=3025`, `FINAL_LR_POWER=1.2`. Its `train.log` records `first_step_le_3p28=2940`,
  `final_val_loss=3.27689`. (The submitted **bin 2949** is the N=16 cohort checkpoint, not this single
  seed.)
- **A08 — v3 nosphere source snapshot** — `…/10389-…/source_snapshot.py` (61,963 bytes, sha256
  `34da98d4b5d602cecd8fa7a81e8f15ace82489a4a8cd65778ec2b4fb32f407dd`) — the full self-logged source.

## Quarantined (non-compliant) artifact — recorded as journey, not result

- **A09 — the v12-derived (non-compliant) v2 frontier** — every `v2cx`-prefixed v12-derived run in A01
  (`family=v12`, 2,672 rows include the quarantined set). These carry the illegal `RMSNorm.forward` /
  q-k-norm forward-path change and are **not** valid records (C05). The compliant rebuild uses the
  `v2cxleg` prefix / `legal_v12opt…` variants.

## Per-wave journals & generated material (committed)

- **A10 — v1** — `v1/codex/{AGENTS.md,goal.md,plan.md}`, `v1/codex/scratchpad/{THREAD.md,clusters.md,picklist.md}`,
  `v1/codex/scratchpad/{ideas/,variants/,sweeps/,assets/,candidates/,tools/}`.
- **A11 — novelty** — `novelty/codex/{AGENTS.md,goal.md,plan.md}`,
  `novelty/codex/scratchpad/{THREAD.md,existing_results_summary.md,ideas/,variants/,rule_checks/,papers/}`
  (the ~100+ derived idea writeups live in `ideas/`).
- **A12 — v2** — `v2/codex/{goal.md}`, `v2/codex/scratchpad/{THREAD.md,ideas/,variants/,papers/,worktrees/}`.
- **A13 — v3** — `v3/codex/{goal.md}`, `v3/codex/scratchpad/{THREAD.md,ideas/,variants/,papers/,submission/,tools/}`,
  and the leave-one-out record `v3/codex/scratchpad/w258_2940_leave_one_out_pruning_20260513.md`.

> No code is transcribed into `src/execution/`: every concrete artifact above persists in the store or
> the committed tree, so this index points to it rather than duplicating it.
