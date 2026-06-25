# Environment

Reconstructed from the run export and code. Items not stated in the provided source are marked
"Not specified".

- **Python**: Not specified in INSIGHTS.md (modded-nanogpt lineage; runs are standard PyTorch scripts
  `launched_script.py`).
- **Framework**: PyTorch (the run code uses `torch` tensor ops, custom Newton-Schulz / SOAP in pure
  torch). Exact version not specified.
- **Hardware**: Not specified in INSIGHTS.md. The export logs per-step wall-clock (`step_avg_ms`,
  `train_time_s`) and `train_time_s` per run, implying a single fixed GPU configuration across runs
  (modded-nanogpt is canonically multi-GPU H100; this is NOT confirmed by the provided source — do not
  assume).
- **Benchmark**: modded-nanogpt `track_3_optimization`; GPT-124M; FineWeb-10B; batch 8x64x1024 tokens.
- **Key dependencies**: torch; numpy (for analysis); the run harness records `metadata.json`,
  `train.log`, `launched_script.py`, `source_snapshot.py`, `launch_stub.sh` per run.
- **Random seeds**: seeds are an explicit experimental axis. Run names carry `sN` (s0, s1, ...);
  reproducers used 3 seeds for v1 levers and 8-16 seeds for the `seed_reverify` wave (13 config
  groups, 152 runs). The seed noise floor is `std(final_val_loss) ~ 0.0004-0.0011` and a ~9-12%
  per-config miss rate at the frontier.
- **Data export**: `data/runs_self_contained/runs.csv` (10,428 runs; 9,235 completed), `runs.jsonl`,
  `dropped_runs.jsonl`, `manifest.json`, plus per-run directories under
  `data/runs_self_contained/agents/{cc,codex}_{v1,novelty,v2,v3}/` and `agents/seed_reverify/`.

## CSV schema (per-run fields used for grounding)
`export_id, agent_version, agent_label, version, agent, family, purpose, status, run_id, launched_at,
final_val_loss, min_val_loss, final_step, train_steps, step_to_3_28, num_val_points, train_time_s,
step_avg_ms, is_completed, is_canceled, is_preempted, is_timeout, is_failed, is_incomplete,
is_stat_verify, config_path_source, run_dir, train_log, launched_script, source_snapshot, console_log,
launch_stub`.

## Reproduction entry points
- Baseline: `agents/cc_v1/runs/00001-muon-baseline-1-*/launched_script.py`.
- v3 record (cc): `agents/cc_v3/runs/07070-v88-aurora-proj-s2/launched_script.py`.
- v3 record (codex): `agents/codex_v3/runs/08953-*worker27*/launched_script.py`.
- v12 frozen backbone: `agents/cc_v2/runs/03141-v12-baseline-s2/launched_script.py`.
- LOO ablation suite: `agents/cc_v3/runs/*loo{01..15}_no_*-s{0..3}-*` (629 runs).
- Seed reverify: `agents/seed_reverify/runs/*` (13 groups).
