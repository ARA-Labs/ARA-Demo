# World-Model ARA for ARC-AGI-3 ls20

An Agent-Native Research Artifact built **from live gameplay** by Claude Code (Opus)
playing the ARC-AGI-3 game `ls20` (Locksmith) turn-by-turn via the `CcRelay` agent.
Each mechanic is grounded in observed turns of the episode log
(`harness/runs/ls20-9607627b_ccrelay.jsonl`). This is the read target for
`wm-retrieve` / `wm-predict` in later play.

This artifact was migrated into the canonical `research-manager` structure from a
hand-authored draft (archived at `_handwritten_raw/`). Content is unchanged; only the
structure was re-cast to the skill's schemas.

## Layer Index

- `logic/` — MUTABLE current best understanding
  - `problem.md` — the problem: solve `ls20` by inferring its mechanics under a move budget
  - `concepts.md` — on-screen entities (block, key-box, panel, switch, X-box/refill, budget bar)
  - `claims.md` — crystallized claims C01–C10 (mechanics, win condition, transfer)
  - `solution/heuristics.md` — action→effect forward model & control mechanics (the "how")
  - `solution/recipes.md` — R-L1, R-L2 solution recipes
- `trace/` — APPEND-ONLY journey
  - `exploration_tree.yaml` — research DAG: probes, decisions, dead_ends (DE1–DE5 + the under-sampling error), pivots
  - `pm_reasoning_log.yaml` — manager's organizational decisions
  - `sessions/session_index.yaml` — session index
  - `sessions/2026-06-29_001.yaml` — the play-session record (turns, events, key_context, open_threads)
- `staging/observations.yaml` — items not yet closed (L3 unverified controls) — STAGED
- `evidence/README.md` — index pointing at the raw episode-log frames as proof

## Encoding note

Frames are 64×64, 16 colors. The play helper renders each color as a glyph:
`' '=0 .=1 :=2 -=3 ==4 +=5 *=6 #=7 %=8 @=9 O=a X=b N=c W=d $=e &=f`.
Color-3 (`-`) = walkable floor/corridor; color-4 (`=`) = wall; color-5 (`+`) = UI frame.
