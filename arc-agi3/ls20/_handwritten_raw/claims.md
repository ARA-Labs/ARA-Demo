# Claims — mechanics & goal hypotheses, ls20

## C1 — This is a block-navigation (sokoban/locksmith) puzzle [supported]
The single movable `block` is steered with 4 directional actions through a walled maze.
Grounded in M1–M4. Provenance: ai-executed.

## C2 — Moves are budget-limited [supported]
The bottom `X` bar depletes one unit per action (M5), so solutions must be reasonably
short. Implication: avoid wasteful probing; plan paths. Provenance: ai-executed.

## C3 — The level is cleared by bringing the block to a target [hypothesis]
Candidate targets: the top `key-box` symbol, or aligning the block with a marked goal cell.
The block (cols 33–37) is offset by 1 from the upper corridor (cols 34–38), so an
alignment/threading step is likely required. NOT yet confirmed — no win observed.
Provenance: ai-suggested. Falsifier: reach a plausible target and see if state→WIN.

## C4 — Walls (color-4) block movement [SUPPORTED]
A move into a wall changes 0 cells (no-op) but still costs a budget unit. Evidence:
turn 10→11, A1 into the box border, 0 cells changed. [[dead_ends]] Provenance: ai-executed.

## C5 — The bottom-left control panel is DYNAMIC and is the likely win target [hypothesis, strong]
The panel's `@` pattern (cols 3–8, rows 55–60) **changed** between turn ~10 and turn 17:
rows 57–58 flipped from left `@@` (cols 3–4) to right `@@` (cols 6–7). So moving the block
**toggles lock/loop state shown in the panel** — matching the official Locksmith description
("align blocks to target positions by toggling loop controls"). Combined with the **3 `%%`
(color-8) markers** at the right of the budget bar (possibly 3 locks), the win condition is
most likely **driving the panel into a target configuration / satisfying all 3 locks**, NOT
parking the block on a cell. [[concepts]] control-panel.
Provenance: ai-executed (panel change observed). Next test: single moves while watching which
panel bits toggle vs the block's macro-cell → build a position→panel-state map.
Falsifier: panel reaches its target pattern and state → WIN.

## C6 — The lock mechanic: speck=toggle switch, key-box=target pattern, panel=current pattern [SUPPORTED, breakthrough]
Diffing the panel across all 18 turns: it changed **exactly once**, caused by stepping the
block ONTO the speck (R6C3) at turn 16→17 (the 58-cell move). The speck is a **toggle
switch**, not consumed (still present after moving off).
The panel encodes a **3×3 lock pattern** (2×2 cells each). The `@` symbol inside the top
key-box encodes a 3×3 **target pattern** `111 / 001 / 101`. Stepping the switch flipped the
panel's middle row `100 → 001`, so the panel now reads `111 / 001 / 101` — **it MATCHES the
key-box target**. (Rows 0 and 2 already matched from the start; only the middle row needed
the switch.) This is the official Locksmith mechanic: *toggle loop controls to align the
lock pattern*.
Lock is now satisfied, yet state=NOT_FINISHED → a **delivery step remains**. Leading
hypothesis [C7]: with the lock matched, the previously-walled key-box is now enterable;
deliver the block into it to win. Recall DE1: before matching, A1 into the box border was a
no-op — the box was locked. Provenance: ai-executed (panel-diff across the episode log).

## C7 — Win = deliver the block into the now-unlocked key-box [SUPPORTED]
Confirmed on L1 (turn 23→24): with the lock matched, A1 into the box drove the block in,
redrew the whole screen (~1479 cells), levels_completed 0→1. [[recipes]] R-L1.

## C8 — "L2 switch = vertical flip + a hidden 2nd control" [REFUTED]
Original hypothesis: the L2 switch only flips the lock top↔bottom, so a 2nd control is needed
to change the middle row. **FALSE.** The "flip" was an under-sampling artifact — a SINGLE
toggle happened to look like a flip. Repeated toggling ([[methods]] M6, corrected) shows the
switch is a 4-state CYCLE whose middle row DOES change. No 2nd control exists; the X-boxes
that were suspected are merely budget refills ([[methods]] M8). Superseded by C9.
Provenance: ai-executed (live re-test).

## C9 — L2 is solved by the ONE switch alone (4-state cycle) + 2-push delivery [SUPPORTED, L2 SOLVED]
The R9C9 switch cycles the lock through `111/001/101 → 101/001/111 → 101/100/111 →
111/100/101 → …`. From the fresh start `111/001/101`, **3 step-ons** land on the target
`111/100/101` (= the key-box `@`). Then deliver the block into the now-unlocked key-box from
directly above (R6C2), pressing DOWN twice ([[methods]] M9). Result: **levels_completed 1→2,
1421-cell redraw = WIN** (turn 131). Budget managed via the X-box refills ([[methods]] M8).
Full sequence in [[recipes]] R-L2. Provenance: ai-executed (live solve, this session).

## C10 — The per-level lock TRANSFORM differs, but the RECIPE is invariant [supported]
L1 switch = middle-row toggle (2 states); L2 switch = 4-state cycle; both are reached by
the SAME loop: read target from key-box `@`, drive block onto switch(es) until panel==target,
deliver into key-box. The lesson for L3+: don't assume the transform — **sample the switch
several times to learn its full cycle before planning toggles** (the mistake that created the
false C8). The refutation of C8 is itself the transferable heuristic. Provenance: ai-executed.
