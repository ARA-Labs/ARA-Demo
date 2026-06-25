# Environment & Reproducibility

## Benchmark code

- **Script:** `records/track_3_optimization/train_gpt_simple.py` — "descends from the
  [NanoGPT speedrun](https://github.com/KellerJordan/modded-nanogpt) … a simplified version of the
  speedrun for use in neural net optimization research" (run-export `launched_script.py:1-6`). It
  self-logs its own source into each result log (`with open(sys.argv[0]) as f: code = f.read()`),
  so every run's exact code is recoverable from its `train.log`.
- **Model:** ~124M-parameter GPT; sequence length 1024; data is the FineWeb-10B token cache
  (`cached_fineweb10B`, materialized per wave). Architecture, batch size, and data are **fixed** by
  the track contract; only `Optimization` and `Init & Optim Hyperparams` may change
  (`../logic/solution/constraints.md`).
- **Origin repo (per run metadata):** `/beegfs/elie/modded-nanogpt-agent-codex` (Codex's worktree);
  the master checkout is `/beegfs/elie/modded-nanogpt`
  (`data/runs_self_contained/agents/codex_v1/runs/00606-…/metadata.json:52,56`).

## Hardware & run protocol

- **Hardware:** 1 node × 8 GPUs (`{H100, H200}`); ~15 min per run; effectively unlimited wall-clock
  (this is a step-count, not wall-clock, benchmark) (`../../v1/codex/goal.md:56-59`,
  `AGENTS.md:209`).
- **Launch:**
  `torchrun --standalone --nproc_per_node=8 records/track_3_optimization/train_gpt_simple.py`
  (`../../v1/codex/AGENTS.md:211-213`). One run at a time on `cluster` (the script grabs all 8
  GPUs); additional runs fan out into the `preempt` Slurm partition behind an idle-node gate
  (`AGENTS.md:230-273`).
- **Determinism:** each submitted cohort uses distinct `--seed N` per run; submitted HPs are
  hardcoded in the script (no CLI args) (`record_configs/*/README.md`, `AGENTS.md:288`).

## Software (observed from run exports)

- Python 3 with PyTorch (`import torch`, `torch.distributed`, `torch.optim.AdamW`); the novelty wave
  notes a `.venv` with torch 2.10. Imports are "stdlib plus PyTorch only … no third-party optimizer
  library imports" for the submitted v2 cohort (`../../v2/codex/scratchpad/THREAD.md:810`).
- Custom Muon-family optimizers live inside the training script itself (logged with the run), not as
  external packages.

## What "counts" — verification protocol

- A run counts only if `step_to_3.28` actually fired (a run can dip past 3.28 and back — read the
  log, not just the final loss) (`AGENTS.md:224-226`).
- A submission is an n=16 cohort (seeds 0..15) clearing `(3.28 − μ)·√n ≥ 0.004` at the earliest
  common checkpoint, per [C06](../logic/claims.md). The three submitted records each ship 16 full
  reproducibility logfiles (`record_configs/*/README.md`).

## Reproducing this artifact's inputs

- **Run index:** `data/runs_self_contained/runs.csv` (8,224 rows + header) and `runs.jsonl` (same,
  with nested artifact pointers). See [artifacts.md](artifacts.md) for the schema.
- **Per-run exports:** `data/runs_self_contained/agents/{codex_v1,codex_novelty,codex_v2,codex_v3}/runs/<export_id>/`
  each containing `metadata.json`, `launched_script.py`, and `train.log`. (The bulk raw logs under
  `agents/*/runs/` and `*/codex/scratchpad/runs/` are git-ignored but kept on disk — ~3 GB total;
  re-clone from the source experiment if absent — `README.md:91-100`.)
- **Records:** `record_configs/20260515_codex_v{1,2,3}_*/` (READMEs, loss-curve and pruning PNGs,
  `pruning_data.json`).
