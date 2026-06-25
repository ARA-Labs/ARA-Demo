# Methodology — the evidence discipline shared across waves

The reusable contribution of this experiment is as much the **process** as the recipes. These
protocols are applied identically across v1/v2/v3 (and the novelty wave).

## The bin metric

`parse_log.py` extracts the first validation step whose `val_loss <= 3.28`. Validation logs on the
`step % 125 == 0` grid plus an explicit final validation; an "early-stop" forces a final validation
at the chosen stop step so a non-grid bin can be measured. The bin is that first-crossing step.

## Seed control

`make_seed_variant.py` inserts `torch.manual_seed(seed)` **after** the validation batch is
materialized and **before** model construction. This fixes the validation data across seeds so only
initialization and optimizer-state randomness vary — a clean cross-seed comparison.

## Two-tier promotion

- **Mechanism promotion (intra-wave).** A candidate is promoted only on a **two-seed reproduction**
  that beats the current frontier by more than the **2× noise-floor gate** (~100 steps, since the
  noise floor is ~50 steps). Reproduced-but-within-gate hits are kept as **stepping stones**, not
  promoted.
- **Submission significance (the bin).** A submitted bin must pass a **fixed-step seed cohort**
  z-test: `(3.28 - mean) * sqrt(n) >= 0.004`, with `sigma = 0.0013` (one-sided z, `p < 0.001`), over
  n distinct non-cherry-picked seeds at the hardcoded bin. Scoring uses only validation checkpoints
  common to all runs (**anti-val-spam** / anti-p-hacking). All three submissions used n=16 (seeds
  0..15). This gate is why every submitted bin is **conservative** relative to the single-seed
  frontier (C08): v1 3170→3205, v2 2962→3037, v3 sub-2900→2949.

## Leave-one-out (LOO) pruning

After a stack is built, each component is removed singly and the cohort re-run; the **removal delta**
(val_loss with component removed, minus baseline) measures its contribution. Positive = the component
helped. Components within the noise band are candidates to drop; large positive deltas are kept. The
v1/v2/v3 pruning JSONs (`src/configs/*.json`, charted in `evidence/figures/*_pruning.md`) are the
output of this protocol. Caveat: LOO is one-at-a-time and misses super-additive interactions (L2).

## Compliance gating (E08)

Every variant passes a static check before launch: `py_compile`, a `GPT.forward` /
`RMSNorm.forward` / q-k `F.rms_norm` byte-identity check against the workspace baseline, exactly one
`.backward()` call per step, and (post-v2) a launcher gate that exits non-zero on any architecture
diff or norm-gain-path optimizer plumbing. Active worktrees are audited after each launch wave.

## Novelty-wave screening (E06)

The novelty wave adds a **two-gate rule**: before any code, each idea must pass both an arXiv/local
**novelty existence check** and a **benchmark-rule compliance check**. A failure on either gate kills
the idea with no run. The **refined novelty bar** requires an optimizer-level combination to be
materially non-additive (one mechanism's output shaping another's), ruling schedule/LR/WD tuning out
as "plumbing". Same-family target-step probes are measurement-only and never count as novelty.

## Operational hygiene

Runs go to the Slurm `preempt` partition only after an idle-node check; Codex jobs carry a `codex-`
prefix and `--no-requeue`; slow-per-step outliers (multi-second steps) are cancelled and recycled.
The `runs.jsonl` index was once corrupted by concurrent Slurm appends and repaired from backup.
