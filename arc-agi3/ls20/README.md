# ARC-AGI-3 `ls20` — Agent-Native Research Artifact (ARA)

An AI agent (Claude Code / Opus) played the ARC-AGI-3 game **`ls20` (Locksmith)** with no
tutorial and **cleared all 7 levels (7/7, WIN)** — building a **world model** of the game as
it went and using that world model (`wm-predict`) to crack the levels it could not solve cold.

This ARA was produced **live, during play, by the `research-manager` skill** (event-driven,
crystallize-on-closure) — not hand-authored. It is the read substrate for the ARA World Model.

## What's here
- **`trajectory.html`** — open this first (self-contained, double-click). An interactive map of
  the agent's full 7-level process: the exploration tree (75 nodes incl. 19 dead-ends and several
  honest self-corrections), per-step plain-language narratives with verbatim evidence, a concept
  glossary, and the solution recipes.
- `logic/` — current best understanding: `claims.md` (C01–C15), `concepts.md`, `problem.md`,
  `solution/recipes.md` (R-L1..R-L7) + `solution/heuristics.md` (H01–H12).
- `trace/` — append-only journey: `exploration_tree.yaml` (the research DAG), per-day session
  records, the manager's reasoning log, and raw per-level notes.
- `staging/` — observations awaiting a closure signal. `evidence/` — proof index.
- `_handwritten_raw/` — the pre-migration hand-written notes, archived for provenance.

## Headline
The World Model directly enabled wins the agent couldn't reach from recorded routes alone
(L4, L6, L7). An ablation (full-ARA agent vs a recipes-only agent) on the unseen L7 showed the
recipes-only agent never operated a single lock control, while the world-model agent characterized
the whole lock — the ARA earns its keep as a *world model*, not a trajectory cache.
