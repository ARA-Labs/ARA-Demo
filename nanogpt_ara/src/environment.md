# Environment

## Hardware
- 1 node, 8× {H100 / H200} GPUs (v3 specifically 8×H200). ~15 min per run.
- Concurrency: one run at a time on the compute node; a Slurm `preempt` partition is available for
  parallel runs. Wall-clock is irrelevant to the metric (slow-per-step methods are allowed).

## Code
- Benchmark script: `records/track_3_optimization/train_gpt_simple.py` — a simplified
  modded-nanogpt (KellerJordan/modded-nanogpt lineage). Submitted runs use this canonical script
  with all hyperparameters hardcoded into the variant file.
- Run command: `torchrun --standalone --nproc_per_node=8 train_gpt_simple.py`.
- Dependencies: Python standard library + PyTorch only. The submitted recipes import no third-party
  optimizer library (verified during v2 submission checks).
- Distributed semantics (fixed): `assert 8 % world_size == 0`; broadcast all params from rank 0
  after init; all-reduce each gradient with SUM; Muon distributes block-matrix updates by rank and
  gathers updated params.

## Fixed benchmark surfaces
See [`../logic/solution/constraints.md`](../logic/solution/constraints.md) for the full fixed
contract (model, data, batch, forward path, init partition, validation cadence, success criterion).
These must be held byte-for-byte constant; only optimizer/schedule/init hyperparameters may change.

## Data
- Training shards `data/fineweb10B/fineweb_train_*.bin`; validation shards `fineweb_val_*.bin`
  (FineWeb-10B). `val_tokens = 20 * 524288`. Not redistributed in this artifact.

## Captured artifacts in this ARA
- `src/execution/` — the three submitted recipe scripts (v1/v2/v3), transcribed verbatim from the
  agent's `variants/` directories. See `src/execution/README.md` for provenance and grounding.
- `src/configs/` — the per-wave leave-one-out pruning data (`v{1,2,3}_pruning_data.json`), copied
  verbatim from the submitted `record_configs/`.

## Reproduction notes (from the source repo)
- Raw per-seed run logs (~3 GB across 8,224 runs) are git-ignored on disk in the source repo; this
  ARA carries the run **index** (`runs.csv` / `runs.jsonl`) and the submitted record configs, not the
  bulk logs.
- The submitted bins were each validated over 16 reproducibility logfiles (seeds 0..15).
