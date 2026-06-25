---
title: "Codex Autonomous Speedrun of track_3_optimization (modded-nanogpt): the v1 → novelty → v2 → v3 single-agent trajectory"
authors:
  - "Codex (autonomous optimization-research agent)"
  - "human operator (not named in inputs)"
year: 2026
venue: "Internal benchmark speedrun — modded-nanogpt track_3_optimization (KellerJordan fork)"
doi: "Not specified in inputs"
ara_version: "1.0"
domain: "neural-network optimization / LLM-pretraining speedrunning"
keywords:
  - Muon
  - NorMuon
  - MuonEq
  - Soft-Muon
  - SOAP preconditioning
  - optimizer speedrun
  - modded-nanogpt
  - step-count compression
  - leave-one-out pruning
  - fixed-cohort significance gate
  - autonomous research agent
  - negative result (novelty wave)
claims_summary: >
  An autonomous agent (Codex) lowered the number of training steps needed to reach 3.28
  validation loss on a fixed 124M-param GPT speedrun from the Muon baseline of 3500 steps to
  3205 (v1), 3037 (v2, after a compliance rebuild), and 2949 (v3), each validated over n=16
  non-cherry-picked seeds under a fixed-cohort significance gate (3.28−μ)·√n ≥ 0.004. The work
  also produced one hard-isolated negative result (the novelty wave: no promotable submission).
  The reusable findings are mechanism-level: tail-only weight EMA and factorized second-moment
  preconditioning are the largest single levers; schedule-horizon/train-step decoupling buys
  free compression; the sub-frontier region is a seed-fragility map governed by a significance
  gate rather than a monotone frontier; redundant stack components are found by leave-one-out
  pruning; and cross-agent results that violate the no-architecture-change rule must be
  quarantined regardless of how much they helped.
abstract: >
  This artifact records the single-agent slice of an autonomous-speedrunning experiment in which
  the Codex agent attacked track_3_optimization of the modded-nanogpt benchmark — reach 3.28
  validation loss in as few one-forward-backward training steps as possible on a fixed
  architecture, data, and batch contract. Over four waves (v1 optimizer/schedule/init screening;
  a hard-isolated novelty wave; v2 role-specific LR/WD + lookahead on a compliant rebuild; v3
  reproduction-and-compression of public radial/Soft-Muon PRs) the agent drove the submitted bin
  from 3500 to 2949. The artifact is compiled directly (one-shot) from the agent's own journals
  (THREAD.md per wave), the run index (8,224 attached runs), the submitted record configs, and
  per-component leave-one-out pruning data. It separates the agent's reusable mechanism-level
  takeaways (the cognitive layer) from the exact submitted numbers and figures (the evidence
  layer), records the full exploration DAG including dead ends and the novelty-wave negative
  result, and faithfully attributes the cross-agent touchpoints (a v12 parent inherited from the
  Claude/cc agent that was tested, flagged non-compliant, and quarantined).
---

# Codex Autonomous Speedrun of `track_3_optimization` — Agent-Native Research Artifact

## What this is

A direct (one-shot) ARA compiled from `experiments-autonomous-speedrunning-codex/`: the
single-agent record of the Codex optimization-research agent lowering the step count to reach
**3.28 validation loss** on a fixed 124M-parameter GPT speedrun (modded-nanogpt
`train_gpt_simple.py`, `track_3_optimization`). "Bin" = the step at which val ≤ 3.28 is first
crossed; lower is better.

**Submitted trajectory:** `3500 (Muon baseline) → 3205 (v1) → 3037 (v2) → 2949 (v3)`, each
validated over n=16 seeds. The `novelty` wave is a hard-isolated **negative result** (no
promotable submission).

> **Compile note.** This ARA is the *direct-compiler* artifact requested by the user, distinct
> from the time-ordered replay artifact the source repo's top-level `README.md` describes at
> `ara-pipeline/ara/` (that directory is not present in this copy). A one-shot compile sees the
> whole trajectory at once; where the agent's running journal and the final submitted record
> disagree (e.g. v1's journal trails off at a provisional `s3220`/`s3170` while the submitted
> record is `3205`), the **submitted `record_configs/` READMEs are treated as authoritative**
> and the journal as the path taken. Such reconciliations are flagged in the relevant claim's
> `Conditions`/`Sources`.

## Layer Index

| Layer | File | Contents |
|---|---|---|
| Cognitive | [logic/problem.md](logic/problem.md) | Observations, gaps, key insight, assumptions |
| Cognitive | [logic/claims.md](logic/claims.md) | C01–C12 falsifiable mechanism-level claims with grounded sources |
| Cognitive | [logic/concepts.md](logic/concepts.md) | The benchmark's and the agent's technical vocabulary |
| Cognitive | [logic/experiments.md](logic/experiments.md) | E01–E12 directional verification/analysis plans |
| Cognitive | [logic/related_work.md](logic/related_work.md) | Typed dependency graph (PRs, papers, prior optimizers) |
| Method | [logic/solution/constraints.md](logic/solution/constraints.md) | The lawful core, benchmark hard rules, limitations |
| Method | [logic/solution/method.md](logic/solution/method.md) | The search methodology (gates, pruning, significance) |
| Method | [logic/solution/optimizer-stack.md](logic/solution/optimizer-stack.md) | The three submitted recipes, component by component |
| Method (isolated) | [logic/novelty/novelty.md](logic/novelty/novelty.md) | The NV## hard-isolated novelty-wave negative-result subtree |
| Artifact | [src/environment.md](src/environment.md) | Hardware, code, run protocol, reproducibility |
| Artifact | [src/artifacts.md](src/artifacts.md) | Pointer index into the 8,224 run exports + record configs |
| Trace | [trace/exploration_tree.yaml](trace/exploration_tree.yaml) | The research DAG: waves, experiments, decisions, dead ends |
| Evidence | [evidence/README.md](evidence/README.md) | Index of every filed figure and table |
| Evidence | [evidence/figures/](evidence/figures/) | 6 record figures (loss curves + pruning bars) + descriptions |
| Evidence | [evidence/tables/](evidence/tables/) | Seed tables, significance tables, pruning-contribution tables |
| Evidence | [evidence/data/](evidence/data/) | Raw `pruning_data.json` for the three submitted records |

## Reading order

Start with [logic/problem.md](logic/problem.md) for the gap and the key insight, then
[logic/claims.md](logic/claims.md) for the reusable findings. [logic/solution/method.md](logic/solution/method.md)
explains the search discipline that makes the numbers trustworthy;
[logic/solution/optimizer-stack.md](logic/solution/optimizer-stack.md) explains *what* was built.
The negative result lives in its own isolated subtree, [logic/novelty/novelty.md](logic/novelty/novelty.md).
