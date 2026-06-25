---
title: "Where the Gains Live: A Grounded Anatomy of Autonomous nano-GPT Optimizer Speedrunning"
authors:
  - "Autonomous agents: Claude Code (Opus 4.7)"
  - "Autonomous agents: Codex (GPT-5.5)"
  - "ARA synthesis (compiled from research_insights/INSIGHTS.md)"
year: 2026
venue: "Internal research synthesis — modded-nanogpt track_3_optimization (Prime Intellect)"
doi: "N/A (internal experiment export); ARA methodology: arXiv:2604.24658"
ara_version: "1.0"
domain: "Deep-learning optimization / autonomous ML research"
keywords:
  - "Muon optimizer"
  - "Newton-Schulz orthogonalization"
  - "nano-GPT speedrun"
  - "learning-rate schedule"
  - "SOAP / Shampoo preconditioning"
  - "second-order optimization"
  - "autonomous research agents"
  - "ablation / leave-one-out"
  - "seed noise floor"
  - "compositional optimizer levers"
claims_summary:
  - "There is no silver-bullet optimizer: the ~16-17% step reduction (3500 -> ~2880-2930) is a compositional stack of ~8-10 published levers, each worth -0 to -0.005 val loss."
  - "The strongest single Muon-internal lever is MuonEq (per-row L2-normalize momentum BEFORE Newton-Schulz, dval -0.00484, ~11 sigma); the same operator's sign flips with backbone and parameter subset."
  - "The frontier is a thin tail over a noisy seed floor (std ~0.0004-0.001, ~9-12% of seeds miss 3.28), so single-best-seed records overstate; seeds needed scale as n ~ 8*sigma^2/Delta^2."
  - "The frontier recipe is a temporal curriculum (explore early -> exploit late) whose lose-early/win-late crossover (~step 1750) is engineered, not incidental."
  - "A 4-seed leave-one-out ablation shows a long-tailed contribution distribution: power-law cooldown is critical (removing it -> all seeds miss), SOAP-on-MLP is the largest hitting lever (~+85 steps), NorMuon is redundant (~0)."
abstract: "Two autonomous coding agents (Claude Code / Opus 4.7 and Codex / GPT-5.5) competed on modded-nanogpt track_3_optimization: reach validation loss 3.28 on GPT-124M in as few training steps as possible, changing only the optimizer/schedule/init/hyperparameters (architecture, batch size, and data fixed). Across 10,428 logged runs over five waves (baseline -> v1 -> novelty -> v2 -> v3) they cut the Muon reference from 3500 to ~2880-2885 steps single-best-seed (~2930 seed-verified), ~16-17% fewer steps and ~48% fewer than the AdamW baseline. This ARA is a grounded anatomy of that result. The central finding: the baseline already sits near a sharp local optimum, so gains come not from a silver-bullet optimizer but from stacking many ~0.001-val-loss levers (MuonEq pre-NS row normalization, SOAP-on-subset, Aurora row-rescale, Contra-Muon, Polar-Express Newton-Schulz, per-role LR/WD/schedule differentiation, power-law cooldown, train-steps trimming) re-tuned to a shared backbone. A method's sign is backbone- and parameter-subset-dependent (full SOAP fails at ~3.39 but SOAP on MLP+V is the biggest hitting lever); the frontier recipe is a time-scheduled curriculum; the seed noise floor is comparable to single-lever gains; and the cross-agent v3 records are byte-identical (shared public-PR lineage, not independent rediscovery). Every claim is grounded to the run export (runs.csv, 10,428 runs), agent scratchpads, run code, and training curves."
---

# Where the Gains Live: A Grounded Anatomy of Autonomous nano-GPT Optimizer Speedrunning

## Overview

Two autonomous agents were tasked with a saturated optimization benchmark — minimize the number
of training steps GPT-124M needs to reach validation loss 3.28 on FineWeb-10B, holding the
architecture, batch size, and data fixed and changing only the optimizer, schedule, initialization,
and a handful of hyperparameters. This ARA compiles the grounded synthesis of that experiment
(`research_insights/INSIGHTS.md`, 21 sections + TL;DR, backed by `research_insights/PROGRESS.md`).

The contribution is **negative-and-anatomical** rather than a new method: it maps *where the
step-count gains actually live* on this benchmark. The headline is that the ~16-17% reduction
(3500 -> ~2880-2930 steps) is **compositional** — a stack of ~8-10 published levers each worth a
fraction of a 0.001 val-loss unit, re-tuned to a shared backbone — and that a lever's effect is
**backbone- and parameter-subset-dependent** (the same operator helps or hurts depending on *where*
in the recipe it sits). Supporting findings cover the seed noise floor (records are a lucky tail
with a ~9-12% miss rate), the engineered "lose-early/win-late" temporal curriculum, a leave-one-out
ablation ranking every component, two opposite agent search economies that reach the same ceiling,
and a correction showing the cross-agent v3 records are byte-identical (shared lineage, not
independent discovery).

This artifact follows the ARA structure (arXiv:2604.24658): a cognitive layer (claims/concepts/
heuristics), a physical layer (configs + executable stubs of the novel levers), an exploration graph
(the research DAG across five waves, including dead ends), and grounded evidence (the exact tables
from the synthesis, themselves grounded to `data/runs_self_contained/runs.csv` and run logs).

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Benchmark + baseline observations -> gaps -> key insight -> assumptions |
| [claims.md](logic/claims.md) | 17 falsifiable claims (C01-C17) with proof pointers to experiments |
| [concepts.md](logic/concepts.md) | 16 formal definitions (Muon, MuonEq, NorMuon, SOAP-on-subset, Contra-Muon, trust_gate, WSD/power-law cooldown, step_to_3_28, noise floor, ...) |
| [experiments.md](logic/experiments.md) | 14 declarative verification plans (E01-E14) |
| [solution/architecture.md](logic/solution/architecture.md) | The frontier recipe as a component graph (two-optimizer partition + Muon pipeline + schedule controller) |
| [solution/algorithm.md](logic/solution/algorithm.md) | Math + pseudocode of the Muon update pipeline, SOAP preconditioner, Contra ramp, power-law LR |
| [solution/constraints.md](logic/solution/constraints.md) | Generalization limits (scale-bound 124M, 3.28-overfit, wallclock tax, best-of-N, fixed arch/data) |
| [solution/heuristics.md](logic/solution/heuristics.md) | 10 convergence/search heuristics (H01-H10) with code refs |
| [related_work.md](logic/related_work.md) | Typed dependency graph (Muon, MuonEq, NorMuon, SOAP, Cautious, Polar-Express, Contra/PRs, ...) |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [configs/training.md](src/configs/training.md) | Exact optimizer/schedule hyperparameters with rationale + sensitivity | C01-C04, C06, C13 |
| [configs/model.md](src/configs/model.md) | Fixed GPT-124M architecture, batch, data, logit softcap | (context) |
| [execution/muon_pipeline.py](src/execution/muon_pipeline.py) | MuonEq row-norm, Newton-Schulz, soft-Muon, Aurora rescale, Contra ramp | C03, C04, C14 |
| [execution/soap_subset.py](src/execution/soap_subset.py) | SOAP-on-subset preconditioner + trust_gate (MLP+V only) | C05, C13 |
| [execution/schedule.py](src/execution/schedule.py) | Per-role power-law cooldown, mu-schedule, horizon decoupling | C02, C06, C13 |
| [execution/diagnostics.py](src/execution/diagnostics.py) | Seed-significance formula, miss-rate, early-kill divergence test | C09, C11, C17 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 22-node research DAG across baseline->v1->novelty->v2->v3 (incl. dead ends + decisions) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 9 tables + 2 figures, each mapped to claims |
| tables/*.md | Frontier progression, LOO ablation, cross-agent constants, seeds-for-significance, search economy, noise-floor seed groups, temporal curriculum, baseline recipe |
| figures/*.md | Training-curve crossover (val_loss vs step); power-law LR trajectory |
