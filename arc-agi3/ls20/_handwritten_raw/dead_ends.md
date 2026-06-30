# Dead ends — ls20 Level 1 (wasted budget / falsified hypotheses)

## DE1 — "Reach the key-box to win" is FALSE
Navigated the block up the col-6 corridor to directly under the key-box (turns 4–10).
The block **cannot enter the box** — pressing A1 against the box bottom border returned
**0 cells changed** (turn 10→11, a wasted move) and state stayed NOT_FINISHED. Being
adjacent to / wedged under the box does not complete the level. Falsifies [[claims]] C3
(key-box variant). Provenance: ai-executed.

## DE2 — "Cover the rare speck (R6C3) to win" is FALSE (or insufficient)
Navigated the block onto the color-0/1 speck at R6C3 (turns 11–17). The move changed 58
cells (52 block + ~6 speck overwritten) but state stayed NOT_FINISHED, levels 0. Covering
the speck alone does not win. Provenance: ai-executed.

## Confirmed: moving into a wall is a no-op that still appears to cost budget
A1 into the box border = 0 cells changed (DE1). Use this to test walls cheaply, but it
still burns a move. Provenance: ai-executed. Updates [[claims]] C4 → supported.

## Budget spent ~17/40 by end of these dead ends — be more hypothesis-driven from here.

## DE3 (L2) — "The L2 switch is a vertical flip, so a 2nd control is needed" is FALSE
Under-sampling: a single step-on of the R9C9 switch looked like a top↔bottom flip, spawning a
hunt for a hidden middle-row control. Re-testing by toggling the switch many times showed it
is a **4-state cycle that DOES change the middle row** ([[methods]] M6 corrected, [[claims]]
C8 refuted). Lesson: sample a switch through several presses before inferring its transform.
Provenance: ai-executed.

## DE4 (L2) — "The X-boxes are the 2nd lock control" is FALSE (the prime lead)
The color-b hollow 3×3 `X`-boxes (R3C2, R10C7) were the prime suspect for a middle-row
control. Stepping onto each left the panel UNCHANGED and instead REFILLED the budget to 42.
They are refill stations ([[methods]] M8), not lock controls. Provenance: ai-executed.

## DE5 (L2) — "One DOWN press delivers the block" is INSUFFICIENT
From R6C2 above the matched key-box, the first A2 only wedged the block onto the box's top
border (54-cell move, no win). Delivery needed a SECOND A2 ([[methods]] M9). Not wasted —
just budget for 2 pushes. Provenance: ai-executed.
