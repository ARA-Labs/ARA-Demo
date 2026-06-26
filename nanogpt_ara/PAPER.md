---
title: "Codex Autonomous Speedrun — Optimizer Search on track_3_optimization (v1 · novelty · v2 · v3)"
authors:
  - "Codex (autonomous research agent)"
  - "human operator (mission framing, compliance gating, submission approval)"
year: 2026
venue: "Internal autonomous-research experiment (modded-nanogpt speedrun, track_3_optimization)"
doi: null
ara_version: 1
domain: "Machine learning — neural-network optimization / autonomous AI research"
keywords:
  - "Muon"
  - "optimizer speedrun"
  - "nanoGPT / modded-nanogpt"
  - "tail-EMA evaluation"
  - "Soft-Muon / radial dampening"
  - "SOAP preconditioning"
  - "leave-one-out pruning"
  - "statistical claimability"
  - "autonomous research agent"
claims_summary: >
  A single autonomous agent (Codex) lowered the step count to reach 3.28 validation loss on the
  fixed-architecture modded-nanogpt `track_3_optimization` benchmark from the Muon baseline of
  3500 steps to a sequence of statistically-validated records: 3205 (v1, "v12iso/MuSched"),
  3037 (v2, "legal" frontier), and 2949 (v3, "nosphere"; statistically viable to ~2940 at N=16).
  A parallel hard-isolated, novelty-constrained wave produced a documented terminal negative
  result (no promotable submission). The artifact distills the reusable mechanisms — the
  horizon≠stop lever, tail-EMA evaluation, factorized hidden-matrix preconditioning, role-specific
  LR/WD + lookahead, faithful public-PR reproduction-then-compression, leave-one-out pruning, the
  statistical-claimability gate, and the exact-polar no-op laws that bounded the novelty search —
  together with the full exploration trace (8,224 runs across four waves), the cross-agent v12
  compliance quarantine, and grounded evidence.
abstract: >
  `track_3_optimization` is a wallclock-irrelevant speedrun: with the model architecture, data,
  and batch fixed, reach 3.28 validation loss on a 124M-parameter GPT in as few optimizer steps
  ("bin") as possible. The Muon baseline is 3500 steps; AdamW is 5625. Operating under a six-rule
  "lawful core" (benchmark hard rules, a two-seed reproduction requirement, a 2× noise-floor gate,
  a stuck detector, a ≤3-modifier slug cap, and a mandatory pre-submission pruning round), the
  Codex agent ran four waves. v1 screened optimizer/schedule/init levers (NorMuon, factorized
  preconditioning, Adam-mini, tail-EMA evaluation) and a transplanted "mu-schedule" to a validated
  3205-step record. A novelty wave derived and tested dozens of not-on-arXiv optimizer mechanisms;
  all reduced to a scalar coefficient or a no-op under Muon's exact polar map, or failed seed
  reproduction — a clean negative result. v2 inherited a cross-agent "v12" stack, discovered (after
  a user flag) that it carried an illegal forward-path precision change, quarantined every
  v12-derived result, and rebuilt a byte-identical-compliant frontier with role-specific LR/WD and
  Muon lookahead to a 3037-step record. v3 pivoted to faithfully reproducing the public
  modded-nanogpt PR frontier (Contra→Soft-Muon scheduling, outward-radial dampening, MLP+V SOAP,
  power-law LR), compressed it by shifting phase endpoints rather than truncating the horizon, and
  applied a W258 leave-one-out pruning sweep that found the sphere-lookahead pull redundant —
  yielding the "nosphere" 2949-step record. Across all waves the governing lesson is that
  statistical claimability `(3.28 − μ)·√n ≥ 0.004`, not a single lucky low crossing, defines a
  record.
---

# Codex Autonomous Speedrun — `track_3_optimization`

This Agent-Native Research Artifact (ARA) was compiled directly (one-shot `compiler`) from the
**single-agent Codex slice** of the autonomous-speedrunning experiment
(`experiments-autonomous-speedrunning-codex/`). It captures only work the Codex agent executed
itself, plus faithfully-attributed cross-agent and public-PR touchpoints.

**Trajectory (submitted record bins, lower = better):**
`3500 (Muon baseline) → 3205 (v1) → 3037 (v2) → 2949 (v3)`, with the **novelty** wave a documented
negative result. The metric is `step_to_3.28` ("bin"): the first training step at which a fixed
N-seed cohort mean crosses 3.28 validation loss with statistical margin.

## Layer Index

### `logic/` — cognitive layer
- [problem.md](logic/problem.md) — observations, gaps, the key insights, assumptions
- [claims.md](logic/claims.md) — C01–C12 falsifiable claims (mechanisms/takeaways), each grounded
- [concepts.md](logic/concepts.md) — the benchmark, the optimizer family, and every load-bearing term
- [experiments.md](logic/experiments.md) — E01–E16 directional verification plans (no exact numbers)
- [related_work.md](logic/related_work.md) — typed dependency graph (public PRs, papers, cross-agent)
- `solution/`
  - [constraints.md](logic/solution/constraints.md) — the lawful core, hard rules, compliance boundary, scope
  - [search_methodology.md](logic/solution/search_methodology.md) — the autonomous search process
  - [optimizer_recipes.md](logic/solution/optimizer_recipes.md) — the four wave stacks, at mechanism level
  - [novelty_derivation.md](logic/solution/novelty_derivation.md) — the novel-idea method + the no-op laws

### `src/` — artifact layer
- [environment.md](src/environment.md) — hardware, software, model/data, run command, reproducibility
- [artifacts.md](src/artifacts.md) — comprehensive pointer index into the 8,224-run store + record configs

### `trace/` — exploration graph
- [exploration_tree.yaml](trace/exploration_tree.yaml) — the research DAG across all four waves
  (decisions, dead ends, the isolated `NV##` novelty subtree, the cross-wave lineage)

### `evidence/` — grounded results
- [README.md](evidence/README.md) — the evidence ledger
- `figures/` — the six record figures (loss curves + component-pruning bars for v1/v2/v3)
- `tables/` — the trajectory summary, the three N=16 record seed tables, the three pruning tables
