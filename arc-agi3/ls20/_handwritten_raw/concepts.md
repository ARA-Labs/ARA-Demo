# Concepts — on-screen entities, ls20 (Level 1)

## block
The movable piece. 5×5 cells: a `N` (color-c) cap on rows 0–1 over a `@` (color-9) body
on rows 2–4. Starts at rows 45–49, cols 33–37. Moved by A1–A4. [[methods]]
Provenance: ai-executed.

## floor / corridor
Color-3 (`-`) cells: walkable space the block snaps through. Forms rooms (rows 25–29 wide;
rows 30–39 with a central pillar) and a vertical corridor (rows 17–24, cols 34–38).

## wall
Color-4 (`=`) cells: presumed impassable. The central `=====` pillar (rows 30–39, cols 28–32)
and the outer field are walls.

## key-box (top)
Rows 8–16, cols 31–39: a framed box (color-3 outline, color-5 fill) containing a small
`@` (color-9) symbol — pattern at rows 11–13. Hypothesis: the TARGET the block must reach
or match. Unconfirmed. [[claims]]

## control-panel (bottom-left)
Rows 53–61, cols 1–10: a `+`-framed panel with `@` shapes. Hypothesis: the "loop/lock"
control display described for Locksmith — may show block orientation/program state.
Unconfirmed.

## budget-bar
Rows 60–63, cols 12–63: a horizontal bar; the `X` (color-b) row depletes one unit per
action (left end first). A move budget. `%` (color-8) clusters at the right end (cols 54–62)
— possibly lock/goal markers. [[methods]] M5.
