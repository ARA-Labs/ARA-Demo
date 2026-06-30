# Methods — action → effect (forward model), ls20

All `ai-executed`, observed on Level 1 by pressing one action and diffing the frame.

## M1 — A1 moves the block UP one block-length (5 cells)
- Evidence: turn 0→1. Block (the `N`-cap / `@`-body object) at rows 45–49 → rows 40–44.
  52 cells changed. State stayed NOT_FINISHED. [[block]]
- Provenance: ai-executed.

## M2 — A2 moves the block DOWN one block-length
- Evidence: turn 1→2. Block rows 40–44 → rows 45–49.
- Provenance: ai-executed.

## M3 — A3 moves the block LEFT one block-length
- Evidence: turn 2→3. Block cols 33–37 → cols ~28–32.
- Provenance: ai-executed.

## M4 — A4 moves the block RIGHT one block-length (inferred, to verify)
- Inference from the up/down/left complement; not yet directly pressed.
- Provenance: ai-suggested (pending confirmation).

## M5 — every action consumes one unit of the bottom budget bar
- Evidence: turn 0→1 also flipped cells (61,13)/(62,13) `X→-` — the leftmost unit of the
  `X` status bar (rows 61–62) was consumed. One unit per move. [[budget-bar]]
- Provenance: ai-executed.

## M6 — Level 2: the switch CYCLES the lock through 4 states (CORRECTED — it is NOT a flip)
- **SUPERSEDES the old "vertical flip" reading.** The earlier 1-toggle observation looked
  like a top↔bottom flip, but stepping onto the switch (R9C9) REPEATEDLY reveals it is a
  4-state cycle, and the **middle row DOES change**. Mapped live (L2, this session, by
  toggling the R9C9 switch on/off many times and reading `status.py` each time):
  - cycle order (each "step onto switch" = +1):
    `111/001/101` → `101/001/111` → `101/100/111` → `111/100/101` → (back to `111/001/101`)
  - The 3rd state in the cycle, **`111/100/101`, EXACTLY equals the key-box target.**
- So from the fresh L2 start (`111/001/101`), **3 step-ons** of the switch reach the target.
  The middle row toggles `001`↔`100` every other step; top/bottom rows swap every step.
- This DISSOLVES the "L2 needs a hidden 2nd control" wall ([[claims]] C8, now refuted):
  the single R9C9 switch is sufficient — it was just under-sampled before. [[claims]] C9.
- Provenance: ai-executed (live toggling, turns ~68–85).

## M8 — the `X`-boxes (color-b hollow 3×3) are BUDGET-REFILL stations, NOT lock controls
- Two on L2: upper at macro **R3C2** (scr rows16-18 c15-17) and lower at **R10C7**
  (scr rows51-53 c39-41). Stepping the block ONTO either: budget bar instantly REFILLS to
  full (42), the X-box glyph is consumed/overwritten, and the **panel/lock is UNCHANGED**.
  - Evidence: R3C2 t53→54 budget 20→42, panel unchanged; R10C7 t71→72 budget 8→42, panel
    unchanged. The prime-lead hypothesis ("X-box = the 2nd lock control") is FALSIFIED.
- Strategic use: refill mid-route to fund long traversals. On L2 a refill is adjacent to
  both the switch (R10C7) and the box-approach path (R3C2). [[recipes]] R-L2.
- L3 has THREE X-boxes (R3C6, R6C3, and one in the lower-mid maze) — same refill role
  expected (to verify). Provenance: ai-executed.

## M9 — delivery into the key-box takes TWO pushes (wedge, then enter)
- L2 delivery from R6C2 (directly above the box): 1st A2 wedged the block onto the box's top
  border (54 cells, no win); 2nd A2 pushed it fully in → **1421-cell full-screen redraw,
  levels_completed 1→2 (WIN)**. Budget through-floor only blocks once the block clears the
  border. So plan for 2 delivery presses, not 1. Provenance: ai-executed (turns 129→131).

## M7 — Level 2 budget costs ~2 units per move (vs ~1 in L1)
- Evidence: budget 42→40→38→…→8 over the L2 path, −2 per action. So L2 ≈ 21 moves total.
- Provenance: ai-executed.

## Movement quantum
- The board is effectively a grid of 5×5 macro-cells; the block snaps one macro-cell per
  press. Walls (color-4 `=`) presumably block movement (to verify when a move is attempted
  into a wall — expect 0 cells changed = blocked).
