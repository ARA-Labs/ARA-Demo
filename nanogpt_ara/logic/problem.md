# Problem

## Setting

`track_3_optimization` is an optimizer benchmark built on a fixed nanoGPT
(`train_gpt_simple.py`, a simplified modded-nanogpt). The benchmark **fixes the architecture,
batch size, sequence length and data**, and allows only optimizer, schedule and initialization
changes, with exactly one forward-backward per step. The objective is to reach
**validation loss `<= 3.28`** in **as few steps as possible**; the submitted step count is the
**"bin"** (lower is better). Wall-clock is irrelevant — slow-per-step methods are fine if they cut
steps.

## Observations (with numbers)

- **O1 — Muon is the standing SOTA at 3500 steps.** The canonical Muon recipe (`lr=0.025`,
  `wd=0.0125`) first crosses `val_loss <= 3.28` at step 3500; the agent's own baseline run finishes
  at `val_loss = 3.27658`. (`evidence/tables/baseline_existing_results.md`)
- **O2 — AdamW is a much weaker family**, crossing only at ~5625 steps on the same setup.
- **O3 — The crossing region is noise-sensitive.** Near the 3375–3500 grid the per-seed crossing
  margin below the target is only a few thousandths of val_loss; sub-125-step claims are within
  run-to-run noise. The empirically estimated noise floor is ~50 steps in `step_to_target` and
  ~0.001 in final val_loss.
- **O4 — Prior iterations hit an empirical ~3000-step floor with optimizer-only mechanisms**;
  many post-Muon optimizers came in at parity or worse, so breaking that floor was the real prize.
- **O5 — The optimization literature is a "sea of unverified SOTA claims"**: hundreds of optimizer
  papers, mostly never compared head-to-head on the same setup, often confounded by undertuned
  baselines.

## Gaps

- **G1 — Which mechanisms actually move the bin, and which are decorative?** A deep stack of
  optimizer/schedule/init tricks can accrete; without per-component ablation it is unknown which
  layers are load-bearing.
- **G2 — Where is the boundary between a real improvement and seed noise?** A single-seed crossing
  at a lower step is not evidence; a principled significance gate is needed.
- **G3 — Can a strictly-novel (unpublished) derivation beat Muon, or do the gains live only in
  combinations of already-published ideas?**
- **G4 — Is a result built on a numerically-rewritten forward path admissible** under a
  no-architecture-change rule, given bf16 precision sensitivity?
- **G5 — When public-frontier PRs are reproduced, can the stack be compressed/pruned** without
  losing the statistical guarantee?

## Key insight

Treat the speedrun as **evidence-gated mechanism search, not leaderboard chasing**: (1) decouple
the LR-schedule horizon from the training stop step so the cooldown is not compressed; (2) accept a
mechanism only on a **two-seed reproduction past a noise-floor gate**, and a **submission** only on
a **fixed-step seed cohort** passing `(3.28 - mean)*sqrt(n) >= 0.004`; (3) after a stack is built,
run **leave-one-out pruning** to keep only load-bearing components; (4) enforce **byte-identical
compliance** of the architecture/forward path so "improvements" cannot come from a disguised
architecture change. These disciplines make the submitted bin conservative and the knowledge
reusable.

## Assumptions

- **A1** — The fixed benchmark surfaces (architecture, data, batch, forward path, validation cadence)
  are held byte-for-byte constant across every submitted run (see `solution/constraints.md`).
- **A2** — `val_loss <= 3.28` at a step, observed on the `step % 125 == 0` grid plus the explicit
  final validation, is the sole success criterion; the per-seed validation batch is fixed by seed
  control so only init/optimizer state varies across seeds.
- **A3** — The estimated noise floor (~50 steps / ~0.001 val_loss) is stationary enough across the
  3000–3500 region to gate promotions.
- **A4** — `sigma = 0.0013` is the per-seed val_loss standard deviation used in the one-sided
  z-test for the submission significance score.
