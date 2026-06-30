# Concepts — on-screen entities, ls20

Term definitions for the entities the block interacts with. Provenance: ai-executed
(observed on Level 1 unless noted).

## block
The single movable piece. 5×5 cells: a `N` (color-c) cap on rows 0–1 over a `@` (color-9)
body on rows 2–4. Starts (L1) at rows 45–49, cols 33–37. Moved by actions A1–A4, snapping
one macro-cell (5 cells) per press. See `solution/heuristics.md` H01–H04.

## floor / corridor
Color-3 (`-`) cells: walkable space the block snaps through. Forms rooms and corridors —
on L1, rooms at rows 25–29 (wide) and rows 30–39 (central pillar), plus a vertical corridor
at rows 17–24, cols 34–38.

## wall
Color-4 (`=`) cells: impassable. The central `=====` pillar (L1 rows 30–39, cols 28–32) and
the outer field are walls. A move into a wall changes 0 cells but still costs a budget unit
(C04).

## key-box (target)
A framed box (color-3 outline, color-5 fill) containing a small `@` (color-9) symbol that
encodes a 3×3 **target pattern**. On L1 at rows 8–16, cols 31–39 (top), the `@` pattern at
rows 11–13. While the lock is unmatched the box is walled-shut (not enterable, DE1); once the
panel matches the target the box becomes enterable and delivering the block into it wins the
level. Position varies per level (L1 top, L2 left, L3 right).

## control-panel (lock display)
A `+`-framed panel, bottom-left (L1 rows 53–61, cols 1–10), drawn with `@` shapes. It encodes
the **current 3×3 lock pattern** (2×2 cells each). The win loop drives this panel into the
key-box target pattern by stepping the block onto switches. (L3 note: the L3 panel is drawn in
color-c `N`, not `@`=9, so an `@`-only panel reader shows it blank — read it from glyphs.)

## switch
A rare color-0/1 floor speck the block steps **onto** to toggle/cycle the lock pattern shown
in the panel. Not consumed (still present after the block moves off). The per-level transform
differs: L1's switch (R6C3) toggles only the middle row (2 states); L2's switch (R9C9) is a
4-state cycle (C09, C10).

## X-box (budget-refill station)
A color-b hollow 3×3 box. Stepping the block ONTO it instantly **refills the budget bar to
full (42)**, consumes the X-box glyph, and leaves the panel/lock UNCHANGED. It is a refill
station, NOT a lock control (the prime-lead hypothesis falsified in DE4). See heuristics H08.

## budget-bar
A horizontal bar (L1 rows 60–63, cols 12–63): the `X` (color-b) row depletes one unit per
action (left end first) on L1, ~2 units per action on L2. A move budget. `%` (color-8)
clusters at the right end were an early guess at lock/goal markers (not confirmed as such).
