# ara-ls20 — World-Model ARA for ARC-AGI-3 game `ls20` (Locksmith)

A growing Agent-Native Research Artifact built **from live gameplay** by Claude Code
(Opus) playing ls20 turn-by-turn via the `CcRelay` agent. Each mechanic here is grounded
in observed turns (`runs/ls20-*_ccrelay.jsonl` + the live frames). Provenance tag on
every entry: `ai-executed` = directly observed by pressing an action and diffing frames.

This is the read target for `wm-retrieve` / `wm-predict` in later play.

## Layers
- [concepts.md](concepts.md) — game objects / on-screen entities
- [methods.md](methods.md) — action → effect mappings (the forward model)
- [claims.md](claims.md) — mechanics, goal hypotheses, win conditions
- [dead_ends.md](dead_ends.md) — moves that wasted budget / did nothing / reset
- [journey.md](journey.md) — turn-by-turn exploration log (the research DAG)

## Encoding note
Frames are 64×64, 16 colors. The play helper renders each color as a glyph:
`' '=0 .=1 :=2 -=3 ==4 +=5 *=6 #=7 %=8 @=9 O=a X=b N=c W=d $=e &=f`.
Color-3 (`-`) = walkable floor/corridor; color-4 (`=`) = wall; color-5 (`+`) = UI frame.
