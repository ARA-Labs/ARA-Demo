# Evidence Index — ls20

All claims and heuristics in this ARA are grounded in a single live-play episode log. The
"evidence" is the raw frame-by-frame record produced while Claude Code (Opus) played ls20
turn-by-turn via the `CcRelay` agent; each cited turn can be replayed from the log.

## Raw proof

- `harness/runs/ls20-9607627b_ccrelay.jsonl` — the CcRelay play episode (the primary evidence;
  contains the per-turn frames, actions, budget, and `levels_completed` referenced throughout
  `trace/exploration_tree.yaml`).
- `harness/runs/ls20-9607627b_arawm.jsonl` — the companion ARA-WM run for the same game id.

Paths are relative to the repo root
`/Users/chengyangshi/Library/Mobile Documents/com~apple~CloudDocs/Summer Intern/ara-wm-arc-agi3/`.

## Turn → evidence map (load-bearing observations)

| Fact | Source turns | Used by |
|------|--------------|---------|
| Move model A1↑ A2↓ A3← A4→, 5-cell steps, 1 budget/move (L1) | 0→4 | C01, C02, H01–H05 |
| Box border 0-cell no-op (walls cost budget; box lock-gated) | 10→11 | C03, C04, N04 (DE1) |
| Speck step 58 cells, no win | 16→17 | N05, N06 (DE2) |
| Panel changed exactly once = switch toggled middle row to target | panel-diff 0→18 | C05, C06, N07 |
| L1 delivery: 1479-cell redraw, levels_completed 0→1 | 23→24 | C07, N08, R-L1 |
| L2 X-boxes refill budget 20→42 / 8→42, panel unchanged | 53→54, 71→72 | H08, N10, N15 (DE4) |
| First R9C9 step looked like a flip; ~2 budget/move on L2 | 69 | C08, H07, N11 |
| Repeated toggling → 4-state cycle, middle row changes | 72→85 | C09, H06, N12, N14 |
| L2 solve: 3 toggles + 2-push delivery, 1421-cell redraw 1→2 | 86→131 | C07, C09, H09, N13, N16 (DE5), R-L2 |
| L3 recon (key-box RIGHT, 3 X-boxes, compound control); probe failed | 131→151 | O01–O03, N17–N19 |

## Encoding note

Frames are 64×64, 16 colors, rendered to glyphs:
`' '=0 .=1 :=2 -=3 ==4 +=5 *=6 #=7 %=8 @=9 O=a X=b N=c W=d $=e &=f`. The board is effectively a
12×12 grid of 5×5 macro-cells.
