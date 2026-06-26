# Environment & reproducibility

## Benchmark code

- **Training script:** `records/track_3_optimization/train_gpt_simple.py` from the modded-nanogpt fork
  (KellerJordan/modded-nanogpt lineage). All submitted variants are this script with changes confined to
  the **Optimization** and **Init & Optim Hyperparams** sections; the forward/architecture/data/batch
  code is byte-identical to the workspace baseline (the v2 compliance boundary — C05).
- **Self-logging:** the script reads its own source via `sys.argv[0]` at startup and writes the full
  code into the result log, so every run's exact recipe is recoverable from its log. Submitted runs
  hardcode HPs (no CLI args).

## Model & data (fixed contract)

- **Model:** a ~124M-parameter GPT (the `train_gpt_simple.py` architecture), trained on **FineWeb10B**
  (`cached_fineweb10B`). Architecture, dataset, and batch size are frozen by the benchmark; one
  forward-backward per step.
- **Precision:** bf16 forward path. The forward-path precision is load-bearing and rule-bound — a
  near-equivalent `RMSNorm.forward` / q-k-norm rewrite is an illegal change (C05). cuDNN SDPA is
  disabled for the compiled causal-attention layout (`torch.backends.cuda.enable_cudnn_sdp(False)`);
  Flash/mem-efficient/math SDPA remain enabled.
- **Target:** validation loss ≤ 3.28; the bin is the first step crossing it.

## Hardware

- **1 node, 8 GPUs** — `8×{H100,H200}` for v1/novelty, `8×H200` for v2/v3. ~15 min per run; effectively
  unlimited wall-clock (the benchmark is wallclock-irrelevant). One run at a time on the main `cluster`
  partition (the script grabs all 8 GPUs); parallel fanout via the `preempt` partition behind an
  idle-node gate. [src: `v1/codex/goal.md:56-59`, `v3/codex/goal.md:106-110`]

## Software

- **PyTorch** with CUDA (the novelty wave pinned a repo-local venv at `torch==2.10.0+cu128`); stdlib +
  PyTorch only in submitted scripts — `AdamW` plus local Muon code, **no third-party optimizer-library
  imports** (a reproducibility check enforced this at submission). [src: `v2/codex/scratchpad/THREAD.md:810`]
- **Scheduler:** Slurm (`sbatch`/`sacct`); Codex-owned jobs use a `codex-` name prefix.

## Run command

```bash
cd /beegfs/elie/modded-nanogpt-agent
torchrun --standalone --nproc_per_node=8 \
    records/track_3_optimization/train_gpt_simple.py \
    2>&1 | tee records/track_3_optimization/ai/scratchpad/runs/<run-id>.log
```

The submitted records hardcode all HPs; the per-seed runs set the seed via the `T3OPT_SEED` /
`SLURM_JOB_ID` environment variable (`SEED = int(os.environ.get("T3OPT_SEED", os.environ.get("SLURM_JOB_ID","0"))) % 2**31`).

## Reproducibility of the submitted records

Each record validates over **n=16 non-cherry-picked seeds (0..15)** with a distinct `--seed N` per run;
the result directory contains 16 full reproducibility logfiles per record. The submission gate is the
cohort z-margin `(3.28 − μ)·√n ≥ 0.004` (σ=0.0013, one-sided p < 0.001). See
[../evidence/tables/](../evidence/tables/) for the per-seed tables and
[artifacts.md](artifacts.md) for the run-store pointers.

## Note on the raw run store

The 8,224 exported run directories (`data/runs_self_contained/agents/*/runs/`, ~1.8 GB) and the agents'
in-worktree raw logs (~1.2 GB) are kept **on disk** so pointers resolve, but are git-ignored to keep the
tracked tree light (~130 MB). The run **index** (`runs.csv` / `runs.jsonl`), the per-wave journals, and
the record configs are committed. [src: `README.md:91-100`]
