# Journey — turn-by-turn exploration log, ls20

Game `ls20`, Level 1. Played by Claude Code (Opus) via CcRelay. Frames in
`harness/runs/ls20-*_ccrelay.jsonl`.

| turn | action | observed effect | inference |
|------|--------|-----------------|-----------|
| 0 | (initial) | Level-1 board: block at rows45–49 c33–37; key-box top; budget bar bottom | start |
| 0→1 | A1 | block ↑ to rows40–44; budget bar −1 unit | A1 = UP; moves cost budget |
| 1→2 | A2 | block ↓ back to rows45–49 | A2 = DOWN |
| 2→3 | A3 | block ← to cols ~28–32 | A3 = LEFT |
| 3→4 | A4 | block → | A4 = RIGHT (model complete) |
| 4→9 | A1×5 | block climbed col-6 corridor to R4C6 | corridor threads to key-box |
| 9→10 | A1 | block entered R3C6 (box bottom), state NOT_FINISHED | reaching box ≠ win |
| 10→11 | A1 | **0 cells changed** — block wedged vs box border | walls no-op (C4); box not enterable (DE1) |
| 11→16 | A2,A2,A3,A3,A3 | block ↓↓ then ←←← across room R5 to R5C3 | repositioning toward speck |
| 16→17 | A2 | block onto speck R6C3; **58 cells changed**; NOT_FINISHED | speck overwritten, not a win (DE2) |
| ~10..17 | (cumulative) | **control panel @-pattern toggled** (rows57–58 flipped) | panel is dynamic → C5 (likely real lock state) |

| 16→17 | A2 onto speck | **panel changed** (only change in 18 turns; episode-log diff) | speck = toggle SWITCH; panel now matches key-box target `111/001/101` → C6 |
| 17→23 | navigate back to box mouth R4C6 | nav, no state change | reposition to deliver |
| 23→24 | A1 into box | **1479 cells changed, levels_completed 0→1** | LEVEL 1 SOLVED → C7 confirmed [[recipes]] R-L1 |
| 24 | (Level 2 begins) | new maze; block@R8C5, key-box on left, panel+budget reset(42) | mechanic REUSED → transfer test |

**Level 1 SOLVED at turn 24.** Mechanic: align lock (step switch) → deliver block into
unlocked key-box. Full recipe in [[recipes]] R-L1. Now on Level 2 (same primitives, new maze).

## Level 2 (turns 24–42) — partial; new mechanic found, not yet solved
- Target (key-box, re-read precisely): `111 / 100 / 101`. Start panel: `111 / 001 / 101`.
  They differ ONLY in the middle row (`001` vs `100`).
- Attempt 1: walked 17 moves to the only switch (R9C9) and stepped it → panel `101/001/111`
  (a **vertical flip**, [[methods]] M6). **A flip leaves the middle row unchanged**, so it
  cannot produce the target. Budget (2/move, M7) ran out → attempt lost.
- RESET (turn 42) → restarts **Level 2** (levels_completed stays 1; budget refreshes to 42;
  panel resets to `111/001/101`). So retrying a level is cheap and keeps prior levels. [[methods]]
- **OPEN PUZZLE (the L2 wall):** changing the middle row needs a control that the visible
  board doesn't obviously provide (rare-color scan finds exactly ONE switch = the flip).
  Hypotheses to test next attempt: (a) a 2nd switch/control hidden or reached via a specific
  path; (b) the key-box target itself is settable by the block; (c) L2 box is NOT lock-gated
  and direct delivery works (cheap-ish to test: 15 moves to the box mouth R6C2 then A2).
  This is the natural place for `wm-predict` over this ARA to propose the hidden control.

## Level 2 — SOLVED this session (turns 53–131). The "wall" was a measurement error.
| turn | action | observed effect | inference |
|------|--------|-----------------|-----------|
| 42→54 | walk to R3C2, step on upper X-box | budget 20→**42** refilled; X-box consumed; **panel unchanged** | X-box = BUDGET REFILL, not lock control ([[methods]] M8, [[dead_ends]] DE4) |
| 54→72 | walk to R10C7, step on lower X-box | budget 8→**42**; panel unchanged | 2nd X-box also a refill |
| 69 | step on R9C9 switch (1st) | panel `111/001/101`→`101/001/111` | looked like a flip (the old M6) |
| 72→85 | **toggle R9C9 repeatedly** (off/on ×several) | panel cycles `…→101/100/111→111/100/101→111/001/101→…` middle row CHANGES | switch = **4-state CYCLE**; `111/100/101` IS in the cycle ([[methods]] M6 corrected; [[claims]] C8 refuted→C9) |
| 86 | RESET | fresh L2: block@R8C5, panel `111/001/101`, budget 42 | clean solve attempt |
| 86→102 | start→R9C9 (17 moves) = toggle#1 | panel→`101/001/111`, budget→8 | 1st toggle |
| →R10C7→R9C9 | refill (→42), return = toggle#2 | panel→`101/100/111` | refill funds the toggles |
| →off/on | toggle#3 | panel→**`111/100/101` = TARGET (matched)** | lock satisfied |
| →R2-row→R3C2 | refill (→42) en route to box | budget→42, panel stays matched | refill on the delivery leg |
| →R6C2 | drive above key-box | budget 36 | in delivery position |
| 129→130 | A2 (down) | 54 cells, block wedges on box border, no win | delivery needs a 2nd push ([[dead_ends]] DE5) |
| **130→131** | **A2 (down) again** | **1421 cells redrawn, levels_completed 1→2** | **LEVEL 2 SOLVED** ([[claims]] C9, [[recipes]] R-L2) |
| 131 | (Level 3 begins) | bigger maze; block@R9C1; key-box on RIGHT (target `101/100/111`); 3 X-boxes; a NEW multi-color control glyph (@/$/%/N ~macro R9C5); budget 42 | L3 unexplored — stopped here to record |

**Level 2 SOLVED at turn 131.** Root cause of the earlier "wall": the switch's transform was
under-sampled (1 press → looked like a flip). The single R9C9 switch, cycled 3×, reaches the
target; X-boxes refill budget; deliver with 2 DOWN presses. Now on **Level 3** (levels_completed=2).

## Level 3 — reconnaissance only (turns 131–151), NOT solved [budget exhausted this session]
- Layout (12×12 macro): block starts ~R9C1 (left); **key-box on the RIGHT** (scr rows 49-56,
  cols 53-59). Panel bottom-left as usual.
- Lock state read precisely (NOTE: L3 panel is drawn in color-c `N`, not @=9, so `status.py`'s
  @-only panel view shows it BLANK — read the panel from `look.py` glyphs instead):
  **panel = `101/001/101`**, **target (key-box `@`) = `101/100/111`**. They differ in the
  MIDDLE row (`001`↔`100`) AND the BOTTOM row (`101`↔`111`) — a 2-row gap (harder than L2).
- Controls spotted (unverified): a **NEW compound multi-color glyph** at scr rows 46-48 cols
  30-32 (`@$$ / @ %% / NN%`, colors 9/e/8/c) = macro **R9C5** — prime switch suspect; a small
  speck cluster at macro **R2C9** (scr rows 12-13 cols 50-51); THREE `X`-boxes (macro R3C6,
  R6C3, and lower-mid) presumed budget-refills (M8). 
- Probe attempt FAILED to gather data: pathfind to R9C5 (20 moves) overran; the executed move
  list left the block stranded at R1C5 (the col-5 corridor is walled at R2, so "down" pressed
  into walls). A1 from there into the wall and the final A2 were no-ops (4-cell budget-only
  diffs). Lesson for next session: **the central corridor to R9C5 is entered from R5C5 going
  DOWN through R7C5, not from the top R1C5** — re-pathfind from a fresh RESET and verify each
  step's actual landing (the block can desync from the planned path when a press hits a wall).
- Budget hit 2 (≈1 move) → stopped. Recommend: RESET L3, refill-aware route to R9C5, sample
  that compound control several times (per C10) to learn its cycle before planning toggles.
