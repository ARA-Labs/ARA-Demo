# ARA-Demo

Demos of **Agent-Native Research Artifacts (ARAs)** — research knowledge packages whose
primary reader is an AI agent, not a human. Instead of a single paper, an ARA stores the
research as structured, machine-readable layers: the current best understanding
(`logic/` — claims, concepts, problem framing, solution recipes), the full journey that
produced it (`trace/` — an append-only exploration tree including dead ends), and grounded
proof (`evidence/` — verbatim numbers, figures, tables). Each demo also ships a human-facing
`PAPER.md` and a self-contained interactive `trajectory.html`.

This repository contains two complete ARAs produced by AI agents doing real work.

## The demos

### 1. `arc-agi3/` — an agent plays Locksmith and writes its own manual

An AI agent (Claude Code / Opus) played the ARC-AGI-3 game **`ls20` (Locksmith)** with no
tutorial and cleared **all 7 levels**. The ARA in [`arc-agi3/ls20/`](arc-agi3/ls20/) was built
**live, during play** — and the agent then used it as a *world model* to crack the levels it
could not solve cold (L4, L6, L7). An ablation on the unseen L7 showed a recipes-only agent
never operated a single lock control, while the world-model agent characterized the whole
lock: the ARA earns its keep as a world model, not a trajectory cache.

- [`arc-agi3/index.html`](arc-agi3/index.html) — narrative showcase, *"The Locksmith That
  Wrote Its Own Manual"* (English / 中文)
- [`arc-agi3/ls20/trajectory.html`](arc-agi3/ls20/trajectory.html) — interactive process map:
  the 75-node exploration tree (19 dead ends included), per-step narratives with verbatim
  evidence, concept glossary, and solution recipes
- [`arc-agi3/l7_showcase.html`](arc-agi3/l7_showcase.html) — the L7 world-model-vs-recipes
  ablation
- [`arc-agi3/ls20/PAPER.md`](arc-agi3/ls20/PAPER.md) — the write-up

### 2. `nanogpt_ara/` — an autonomous optimizer-search speedrun

An ARA compiled from an autonomous agent's optimizer search on the fixed-architecture
**modded-nanogpt `track_3_optimization`** benchmark. Starting from the Muon baseline
(3500 steps to 3.28 validation loss), the agent produced statistically-validated records at
**3205 → 3037 → 2949 steps** (v1/v2/v3), plus a documented terminal negative result from a
hard-isolated novelty-constrained wave.

- [`nanogpt_ara/trajectory.html`](nanogpt_ara/trajectory.html) — interactive process map of
  the search
- [`nanogpt_ara/PAPER.md`](nanogpt_ara/PAPER.md) — the write-up
- [`nanogpt_ara/evidence/`](nanogpt_ara/evidence/) — loss curves, pruning figures, and
  record-seed tables backing every claim

## How to explore

Everything is static — no build step, no server.

```bash
git clone https://github.com/ARA-Labs/ARA-Demo.git
cd ARA-Demo
open arc-agi3/index.html               # macOS; or just double-click in a file browser
open arc-agi3/ls20/trajectory.html
open nanogpt_ara/trajectory.html
```

The HTML files are fully self-contained. Alternatively, browse the ARAs as plain Markdown:
start with a demo's `PAPER.md`, then dig into `logic/` (what is known), `trace/` (how it was
learned, dead ends and all), and `evidence/` (the proof).

## Anatomy of an ARA

| Layer | What it holds |
|---|---|
| `PAPER.md` | Human-facing summary of the artifact |
| `logic/` | Current best understanding: claims, concepts, problem, solution recipes |
| `trace/` | Append-only research journey: exploration tree, session records, raw notes |
| `evidence/` | Grounded proof: verbatim numbers, figures, tables |
| `trajectory.html` | Self-contained interactive visualization of the whole process |

## Related ARA-Labs resources

- [Agent-Native-Research-Artifact](https://github.com/ARA-Labs/Agent-Native-Research-Artifact)
  — the main repository: ARA specification and the agent skills that produce, query, and
  visualize ARAs
- [*The Last Human-Written Paper: Agent-Native Research Artifacts*](https://arxiv.org/abs/2604.24658)
  — the paper introducing ARAs
- [ara-ls20](https://github.com/ARA-Labs/ara-ls20) — standalone repository of the `ls20`
  world-model ARA
- [aracommons.com](https://aracommons.com) — ARA Commons
