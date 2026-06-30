# Solution recipes — ls20

## R-L1 — Level 1 solved (turn 24, levels_completed 0→1) [confirmed]
**The Locksmith loop, in two phases:**
1. **Align the lock.** Read the target pattern from the key-box `@` symbol (a 3×3 grid).
   Read the current pattern from the bottom-left panel (3×3, 2×2 cells). Step the block
   onto each **switch** (a rare color-0/1 speck on the floor) to toggle the panel until it
   **matches the key-box target**. (L1: one switch at R6C3 flipped the middle row `100→001`,
   completing the match `111/001/101`.)
2. **Deliver the block.** With the lock matched, the key-box (walled-shut while unlocked —
   see [[dead_ends]] DE1) becomes **enterable**. Drive the block into the key-box → level
   clears (the move redraws the whole screen, ~1479 cells, levels_completed +1).

**Move model** ([[methods]]): A1↑ A2↓ A3← A4→, 5-cell steps; walls = no-op; each move costs
1 budget unit. Use [[harness/macro.py]] for the 12×12 maze map and [[harness/status.py]] for
block-pos + panel + budget.

Provenance: ai-executed (played live by Opus via CcRelay, turns 0–24).

## R-L2 — Level 2 solved (turn 131, levels_completed 1→2) [confirmed, live]
**Same Locksmith loop as R-L1, with a 4-state cycling switch.** L2 start: block@R8C5,
panel `111/001/101`, target (key-box `@`, on the LEFT) `111/100/101`, budget 42 @ 2/move.

1. **Learn the switch cycle (cheap, do this first).** The ONLY floor switch is at macro
   **R9C9**. Stepping ONTO it cycles the lock through 4 states:
   `111/001/101 → 101/001/111 → 101/100/111 → 111/100/101 → …`. (Do NOT assume "flip" — that
   was the falsified C8.) From the fresh start, **3 step-ons** reach the target `111/100/101`.
   Toggle by stepping off (e.g. left to R9C8) and back on (right to R9C9).
2. **Fund the route with X-box refills.** The maze is large (start→switch ≈17 moves, switch→
   box ≈18 moves) and each move costs 2. Step the block onto an `X`-box (macro **R10C7** near
   the switch, **R3C2** near the box-approach) to **refill budget to 42** ([[methods]] M8).
   These do NOT touch the lock — safe to use any time.
3. **Deliver.** With panel==target, drive the block to **R6C2** (directly ABOVE the key-box;
   floor-reachable via the top row R2 then down col-2/3) and press **DOWN twice**: the 1st
   press wedges onto the box border, the 2nd pushes fully in → full-screen redraw, +1 level
   ([[methods]] M9).

**Executed route this session** (after RESET, with mid-route refills): start→R9C9 (toggle#1,
budget→8) → R10C7 refill (→42) → back to R9C9 (toggle#2) → off/on (toggle#3) = panel matched
`111/100/101` → up the col-9 corridor and across row-2 to R3C3 → R3C2 refill (→42) →
R6C2 → DOWN, DOWN = WIN. Provenance: ai-executed (Opus, live, turns 86–131).

**L3 reached** (turn 131): bigger maze, key-box now on the RIGHT (target read `101/100/111`),
THREE X-boxes, a NEW multi-color control glyph (@/$/%/N at scr rows46-48 c29-31, macro ~R9C5)
— unexplored. Panel starts blank-ish. Budget 42. [[journey]]

## Transfer note — Level 2 reuses this mechanic [the demo thesis, live evidence]
Level 2 (entered at turn 24) presents the SAME primitives — a movable block, a key-box
(left side, rows 7–9), the lock panel, the budget bar — in a new maze. The L1 recipe (align
lock via switches → deliver block) should transfer. This is the "earlier levels teach,
later levels test/recombine" curriculum the demo is built on: the ARA accrued on L1 is the
prior that should let the agent solve L2+ faster than cold exploration. [[journey]]
