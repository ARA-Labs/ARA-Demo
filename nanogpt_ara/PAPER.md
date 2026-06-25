---
title: "Codex autonomous speedrun on track_3_optimization: a single-agent trajectory from Muon 3500 to bin 2949"
authors: ["Codex (autonomous agent)"]
year: 2026
venue: "Autonomous-speedrunning experiment (single-agent Codex slice)"
doi: null
ara_version: "1.0"
domain: "neural-network optimization / LLM pretraining speedrun"
keywords:
  - Muon
  - NorMuon
  - Soft-Muon
  - SOAP preconditioning
  - learning-rate schedule
  - leave-one-out pruning
  - nanoGPT speedrun
  - statistical significance (seed cohort)
  - research-integrity / compliance
  - negative result (novelty constraint)
claims_summary: >
  Across four waves (v1, novelty, v2, v3) the Codex agent lowered the step count to reach
  val_loss <= 3.28 on a fixed nanoGPT (train_gpt_simple.py) from the Muon baseline of 3500 steps
  to submitted record bins 3205 (v1), 3037 (v2) and 2949 (v3); the hard-isolated novelty wave
  produced no promotable submission (a documented negative result). The reusable knowledge is
  about which optimizer/schedule/init mechanisms are load-bearing vs prunable (via leave-one-out
  pruning), how a forward-path precision change silently violates the no-architecture rule, why
  novelty-constrained pre-polar perturbations collapse to algebraic no-ops, and how a fixed-step
  seed-cohort significance test makes the submitted bin conservative relative to the single-seed
  frontier.
abstract: >
  This artifact records the Codex agent's autonomous attack on the track_3_optimization speedrun:
  reach validation loss 3.28 on a fixed-architecture, fixed-data nanoGPT in as few optimizer steps
  ("bins") as possible. The benchmark fixes architecture, batch size and data, allowing only
  optimizer, schedule and initialization changes, one forward-backward per step. Starting from the
  Muon SOTA (3500 steps) the agent ran four waves. v1 (open search) built the "v12iso/MuSched"
  stack — NorMuon with Polar-Express Newton-Schulz, 2-factor preconditioning, split hidden
  optimizers, Adam-mini, a late tail-EMA evaluation shadow, and a tuned Muon-momentum schedule —
  submitting bin 3205. A hard-isolated novelty wave required every recipe to contain an unpublished
  idea; ~40 derivations ran and ~60 were killed before code, but nothing beat the noise floor — a
  clean negative result. v2 inherited a cross-agent "v12" parent, discovered (via the user) that its
  rewritten RMSNorm forward path was a bf16-precision architecture violation, quarantined all
  derived results, and rebuilt a byte-identical-compliant "legal" frontier with role-specific
  LR/WD and a Muon lookahead, submitting bin 3037. v3 reproduced public modded-nanogpt PRs
  (Soft-Muon, outward-radial dampening, MLP+V SOAP, power-law cooldown), then compressed and
  leave-one-out pruned them; the only redundant mechanism was a sphere-lookahead pull, yielding the
  "nosphere" bin 2949. Every submission was validated over n=16 non-cherry-picked seeds against a
  fixed-step cohort significance gate (3.28 - mean)*sqrt(n) >= 0.004.
---

# Codex autonomous speedrun on track_3_optimization

This ARA is the **single-agent Codex slice** of the autonomous-speedrunning experiment: only work
the Codex agent completed on its own, compiled from its four research waves' journals
(`THREAD.md`), plans, submitted record configs and run index. Arc on the bin metric (steps to
reach `val_loss <= 3.28`; lower = better):

**3500 (Muon baseline) → 3205 (v1) → 3037 (v2) → 2949 (v3).**
The hard-isolated **novelty** wave is recorded as an isolated subtree and produced **no promotable
submission** — a real negative result.

## Layer Index

- **Cognitive layer — `logic/`**
  - [`problem.md`](logic/problem.md) — observations, gaps, key insight, assumptions
  - [`claims.md`](logic/claims.md) — C01–C08 falsifiable claims with proof pointers
  - [`concepts.md`](logic/concepts.md) — the technical vocabulary (bin, NorMuon, Soft-Muon, SOAP, LACV, exact-polar no-op, …)
  - [`experiments.md`](logic/experiments.md) — E01–E08 verification plans (directional, no exact numbers)
  - [`related_work.md`](logic/related_work.md) — typed dependency graph (Muon, public PRs, cross-agent stacks)
  - [`solution/constraints.md`](logic/solution/constraints.md) — binding benchmark rules, assumptions, limitations
  - [`solution/v1_v12iso_stack.md`](logic/solution/v1_v12iso_stack.md) — the v1 method
  - [`solution/v2_legal_frontier.md`](logic/solution/v2_legal_frontier.md) — the v2 method + compliance event
  - [`solution/v3_nosphere_stack.md`](logic/solution/v3_nosphere_stack.md) — the v3 method
  - [`solution/methodology.md`](logic/solution/methodology.md) — bin metric, seed control, significance, noise floor, gating
  - [`novelty/negative_result.md`](logic/novelty/negative_result.md) — isolated NV subtree: the novelty-wave negative result
- **Artifact layer — `src/`**
  - [`environment.md`](src/environment.md) — hardware, fixed benchmark surfaces, run command
  - `execution/` — the three submitted recipe scripts (v1/v2/v3), captured verbatim
  - `configs/` — the per-wave leave-one-out pruning data (JSON)
- **Exploration graph — `trace/`**
  - [`exploration_tree.yaml`](trace/exploration_tree.yaml) — the research DAG (v1/v2/v3 lineage + isolated NV subtree)
- **Evidence — `evidence/`**
  - [`README.md`](evidence/README.md) — evidence ledger
  - `tables/` — seed tables, pruning tables, baseline existing-results table
  - `figures/` — record loss curves + component-pruning bar charts (screenshots + transcriptions)
