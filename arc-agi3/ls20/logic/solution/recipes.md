# Solution recipes — ls20

Per-level solution methods. Both R-L1 and R-L2 were executed live and won. The invariant
loop they share is crystallized as claim C10.

## R-L1 — Level 1 solved (turn 24, levels_completed 0→1) [confirmed]

**The Locksmith loop, in two phases:**

1. **Align the lock.** Read the target pattern from the key-box `@` symbol (a 3×3 grid). Read
   the current pattern from the bottom-left panel (3×3, 2×2 cells each). Step the block onto
   each **switch** (a rare color-0/1 floor speck) to toggle the panel until it **matches the
   key-box target**. On L1, one switch at R6C3 flipped the middle row `100→001`, completing the
   match `111/001/101`.
2. **Deliver the block.** With the lock matched, the key-box (walled-shut while unlocked — see
   exploration_tree DE1) becomes **enterable**. Drive the block into the key-box → the level
   clears (full-screen redraw ~1479 cells, levels_completed +1).

**Move model** (heuristics H01–H05): A1↑ A2↓ A3← A4→, 5-cell steps; walls = no-op; each move
costs 1 budget unit on L1. Use `harness/macro.py` for the 12×12 maze map and `harness/status.py`
for block-pos + panel + budget.

Provenance: ai-executed (played live by Opus via CcRelay, turns 0–24).

## R-L2 — Level 2 solved (turn 131, levels_completed 1→2) [confirmed, live]

**Same Locksmith loop as R-L1, with a 4-state cycling switch.** L2 start: block@R8C5, panel
`111/001/101`, target (key-box `@`, on the LEFT) `111/100/101`, budget 42 @ 2/move.

1. **Learn the switch cycle (cheap, do this first).** The ONLY floor switch is at macro
   **R9C9**. Stepping onto it cycles the lock through 4 states:
   `111/001/101 → 101/001/111 → 101/100/111 → 111/100/101 → …`. Do NOT assume "flip" — that was
   the falsified C08. From the fresh start, **3 step-ons** reach the target `111/100/101`. Toggle
   by stepping off (left to R9C8) and back on (right to R9C9).
2. **Fund the route with X-box refills.** The maze is large (start→switch ≈17 moves,
   switch→box ≈18 moves) and each move costs 2. Step the block onto an `X`-box (macro **R10C7**
   near the switch, **R3C2** near the box-approach) to **refill budget to 42** (heuristics H08).
   These do NOT touch the lock — safe to use any time.
3. **Deliver.** With panel==target, drive the block to **R6C2** (directly ABOVE the key-box,
   floor-reachable via the top row R2 then down col-2/3) and press **DOWN twice**: the 1st press
   wedges onto the box border, the 2nd pushes fully in → full-screen redraw, +1 level
   (heuristics H09).

**Executed route this session** (after RESET, with mid-route refills): start→R9C9 (toggle#1,
budget→8) → R10C7 refill (→42) → back to R9C9 (toggle#2) → off/on (toggle#3) = panel matched
`111/100/101` → up the col-9 corridor and across row-2 to R3C3 → R3C2 refill (→42) → R6C2 →
DOWN, DOWN = WIN. Provenance: ai-executed (Opus, live, turns 86–131).

## R-L3 — Level 3 solved (levels_completed 2→3) [confirmed, live]

**Same Locksmith loop (C10) with a TWO-AXIS lock (C11) — pattern + colour — and a single delivery.**
The desync-era "multi-stage %% / catch-22 finale" model was FALSIFIED (trace N35): the %% counter is
a permanent UI fixture (stays 12 throughout), aligned step-off is a normal move, and L3 wins on ONE
genuine box-delivery. L3 start: block@R9C1 (LEFT), key-box on the RIGHT (display at macro R9C10), panel
baseline pattern `111/001/101` in colour-c (N), target = pattern `101/100/111` in colour **@** (9).
Read the panel from `look.py`/raw glyphs (status.py's @-only view reads blank because the panel is
colour-N); locate the block with the H10 detector (status.py latches the colour-N panel on L3).

1. **Set the COLOUR axis.** Drive the block onto the COLOUR SELECTOR at macro **R9C5** (the compound
   glyph `@$$/@ %/NN%`). Each step-on advances the panel FILL COLOUR through a 4-state cycle
   N(c)→@(9)→$(e)→%(8)→N. **1 step-on** (c→@) sets the target colour @. Colour persists on step-off;
   the selector NEVER triggers a delivery (sampled clean at every state). Pattern untouched.
2. **Set the PATTERN axis.** Drive to the PATTERN SWITCH at macro **R2C9** (approach from R2C10 going
   LEFT). It cycles the panel PATTERN through the same 4-state H06 cycle
   `111/001/101 → 101/001/111 → 101/100/111 → 111/100/101`. **2 step-ons** reach the target
   `101/100/111` (toggle by stepping off to R2C10 and back). Pattern persists on step-off; colour
   untouched. The two axes are INDEPENDENT (order doesn't matter).
3. **No catch-22.** The fully-aligned block (pattern 101/100/111 + colour @) steps OFF either control
   as a NORMAL move and stays aligned — carry it freely to the key-box.
4. **Fund + deliver.** Refill at the X-boxes (macro R3C6, R6C3) as needed (H08; they don't touch the
   lock or %%). Route the aligned block down col-10 to **R8C10** (above the RIGHT key-box R9C10) and
   press **DOWN twice** (1st wedges into R9C10, 2nd enters) → ~1425-cell full-screen redraw,
   levels_completed 2→3 (H09).

**Executed this session** (turns 58–141, after a clean L1+L2 re-win): colour @ set at R9C5 → pattern
101/100/111 set at R2C9 → carried free aligned block to R8C10 → DOWN, DOWN = WIN. Provenance:
ai-executed (Opus, live).

## R-L4 — Level 4 solved (levels_completed 3→4) [confirmed, live]

**Same Locksmith loop (C10) + TWO-AXIS lock (C11), now over a PORTAL maze (C13) — solved on the FIRST
clean attempt with a portal-aware navigator.** L4 start: block@macro (1,10); key-box = a plus-shape
around macro **(1,1)**; panel BASELINE = pattern `010/110/011` colour **e** ($) [read with
`scratchpad/panel.py` — `step.py`'s panel field mis-reads L4 as `111/111/111`, a decoder bug]; target
(key-box) = pattern `111/001/101` colour **@** (9).

1. **Set the COLOUR axis.** Drive (portal-aware) onto the COLOUR SELECTOR at macro **(6,6)** (the
   compound `9/e/8/c` glyph; reachable only from (5,6) going DOWN — walled left/right/down otherwise).
   Each step-on advances the panel FILL COLOUR through the SAME 4-state cycle as L3 (a 4th occurrence):
   `$→%→N→@` (e→8→c→9). Re-toggle by stepping off UP to (5,6) and back DOWN. Stop on **@**. Colour
   persists on step-off; the selector is COLOUR-ONLY — it does NOT touch the pattern (verified by 6
   clean C10 samples; the "selector double-duty" hypothesis was REFUTED).
2. **Set the PATTERN axis** — the L4-specific find. The pattern control is the **color-0 floor speck at
   macro (6,4)**, steppable from the **SOUTH** ((7,4)+UP→(6,4)); it is NOT steppable from other sides
   (the earlier "(6,4) is inside a wall" was an under-sampled visual verdict — a C10 violation). **ONE
   step-on** drives the panel pattern `010/110/011 → 111/001/101` = exactly the target. (Baseline
   `010/110/011` is OUTSIDE the H06 4-state cycle, so this speck is its own pattern mechanism, not the
   H06 cycle; its full transform was not over-sampled because one press hit the target — re-sample if
   re-solving.) Pattern persists on step-off; the two axes are INDEPENDENT (C11), no catch-22.
3. **Navigate portal-aware.** L4 has a portal/teleporter network (C13): stepping certain floor cells
   warps the block to a fixed destination (e.g. (4,7) is a 3-way trap hub). Use a PORTAL-AWARE BFS
   (`scratchpad/pathfind_portal.py`) whose graph includes the (cell,direction)→destination warp edges,
   AND re-pathfind after EVERY leg (`scratchpad/drive.py`, H10) — the portal map is partial, so the
   re-plan absorbs any unmapped warp. Refill at the 2 single-use X-boxes (macro (3,3), (10,6)) while
   budget>0 (H08/H11); stepping onto an X-box even at budget 0 refills life-free (the budget-0 X-box
   refill takes precedence over the overdraft death — see H08 addendum).
4. **Deliver.** Carry the fully-aligned free block (pattern `111/001/101` + colour @) to macro **(1,3)**
   (immediately RIGHT of the key-box) and press **LEFT (A3) twice**: 1st wedges into (1,2), 2nd enters
   (1,1) → full-screen redraw, levels_completed 3→4 (H09).

**Executed this turn** (after a clean L1+L2+L3 re-win, no RESET): colour @ set at (6,6) [6× sampled] →
pattern `111/001/101` set at (6,4) from the SOUTH → carried free aligned block to (1,3) → LEFT, LEFT =
WIN, no death (%% stayed 12). The WM (O19/N45) predicted the winning branch ("a speck steppable from an
UNTRIED side"). Provenance: ai-executed (Opus, live); the winning hypothesis was ai-suggested (WM).

## Transfer note — Levels 2, 3 & 4 reuse this mechanic [the demo thesis, live evidence]

Level 2 (entered at turn 24) and Level 3 present the SAME primitives — a movable block, a key-box, the
lock panel, the budget bar — in new mazes. The L1 recipe (align lock via switches → deliver block)
transferred to L2 (single pattern axis) and to L3 (TWO axes: a pattern switch + a colour selector). This
is the "earlier levels teach, later levels test/recombine" curriculum the demo is built on: the ARA
accrued on L1/L2 is the prior that let the agent solve L3 directly once the desync was cleared. The
per-level lock differs (1 toggle / 1 cycle / 2 axes / 2 axes + portal maze) but the recipe is invariant
(C10). L4 added a PORTAL maze (C13) as its new obstacle class and was solved on the first clean attempt
once a portal-aware navigator + the (6,4)-speck pattern control were found. L5 (entered this session)
presents the SAME two-axis-lock-plus-portals family (target pattern `101/110/011` colour-%, selector
(5,5), pattern-speck candidates (2,3)/(7,2), portal-heavy with a (4,7) trap-hub AGAIN) and is in
progress (UNSOLVED). L6/L7 unexplored.

A from-scratch replay of the L1→L4 winning action sequences lives at `harness/replay/` (`L{n}.txt` +
`replay.py`), extracted verbatim from this session's episode log, so a future restart can re-climb to
L4 without re-reasoning.

## R-L5 — Level 5 solved (levels_completed 4→5) [confirmed, live]

**Same Locksmith loop (C10) + TWO-AXIS lock (C11) over a PORTAL maze (C13), with TWO new wrinkles: a
portal-only-reachable colour-selector POCKET, and a TWO-SPECK COMPOSED pattern lock (C14).** L5 start:
block@(8,9); panel BASELINE = pattern `010/110/011` colour-N [panel.py]; target (key-box) = pattern
`101/110/011` colour-**%** (8). X-boxes (1,8),(2,1),(9,2) (single-use per life; reset on respawn).

1. **Set the PATTERN axis — TWO composing specks (the L5-specific find, C14).** Two pattern controls:
   the color-0 speck at **(2,3)** (transform **P**, a period-6 cycle — approach from (2,4)+A3 or (2,2)+A4)
   and the speck at **(7,3)** (transform **Q**, a FIXED 90° grid ROTATION, position-perm
   `[6,3,0,7,4,1,8,5,2]` — approach from (7,2)+A4). Neither speck's own orbit contains the target; an
   offline BFS over {P,Q} gives the FORCED word **PPQQ**:
   `010/110/011 --P--> 111/001/101 --P--> 110/011/101 --Q--> 101/011/110 --Q--> 101/110/011` (= target).
   Order is forced (P before Q). Press P twice at (2,3), then Q twice at (7,3). **Read the SETTLED panel
   with the block stepped OFF the speck** (the on-cell read lags by one). **Hazard:** stepping a speck IN
   PASSING re-applies its transform — route speck-free once the pattern is set.
2. **Set the COLOUR axis — the portal-pocket selector.** The selector (5,5) sits in a portal-only POCKET
   (the only 4 unreachable floor cells {(4,6),(5,5),(5,6),(5,7)}; all 4 natural entrances are portals).
   **ENTRANCE = (2,6)+A1(UP) → (5,6)** (a warp landing inside). Inside, oscillate **(5,6)↔(5,5)** (A3 on /
   A4 off) — each step-ON advances the panel FILL COLOUR through the SAME 4-state cycle N→@→$→% (a 5th
   occurrence); 3 ON-steps reach **%**. **Do NOT press A1 inside the pocket** ((5,6)+A1 warps back OUT to
   (4,8)). **EXIT** the pocket via (5,6)+A1→(4,8); colour persists. (The (4,7) trap hub is NOT the pocket
   gate on L5 — its RIGHT/UP are plain floor; only LEFT/DOWN portal.)
3. **Deliver — the SOUTH arm.** Key-box = a PLUS at (0,10),(1,9),(1,10),(1,11),(2,10), center/target
   (1,10). The WEST arm (1,9) is a WALL (a push from (1,8) is a no-op). The enterable arm is the **SOUTH
   (2,10)**: route (speck-free) to **(3,10)** and press **A1(UP) twice** — 1st wedges into (2,10), 2nd
   enters (1,10) → full redraw, levels_completed 4→5 (H09).
4. **Budget/lives (the real difficulty — see N52).** Both axes + the long portal corridors make L5 a
   logistics problem: refill at the (9,2) X-box AFTER QQ (not before) so a FULL bar covers the ~14-step
   delivery corridor + 2 pushes (~32 budget). Use the budget-0-onto-X-box life-free refill (H08/O21). At
   **%%=4 NEVER plain-overdraft** — that life is the LAST (4→0 = GAME_OVER, not a respawn).

**Executed this session** (after a clean replay re-climb to L5): PP at (2,3) → colour % at the pocket →
QQ at (7,3) [panel = target 101/110/011 colour %] → (3,10) → A1, A1 = WIN, levels 4→5. Tooling:
`scratchpad/l5_pocket.py` (pocket colour helper), `scratchpad/portal_hunt.py` (pocket-entrance finder),
`scratchpad/drive.py` (portal-aware driver, `_PORTALS_L5` table). Provenance: ai-executed (Opus, live);
the offline PPQQ BFS was ai-executed; WM consults were directionally helpful (N53), not decisive.

## R-L6 — Level 6 solved (levels_completed 5→6) [confirmed, live, ONE life, zero deaths]

**The Locksmith loop (C10) + two-axis lock (C11) + composed-control word (C14) + MOBILE controls and a
TWO-BOX one-life double-delivery over a portal-pocket maze (C15).** L6 start: block (10,4); panel BASELINE
pattern `110/011/101` colour-e ($) [panel.py]. TWO key-boxes: UPPER (7,10) target pattern `101/110/011`
colour-**%** (8); LOWER (10,10) target pattern `101/001/111` colour-**@** (9). X-boxes (single-use/life):
(1,7),(9,1),(1,1). Budget 42 @ **1/move**. %% resets to 12 on entry. RESET refreshes L6 (full lives/budget,
boxes restored, levels stays 5) — no replay needed to retry.

**The two transforms (offline-solved, zero in-run exploration):**
- **Q** = the row-8 rotation speck = 90° CW grid rotation, perm `[6,3,0,7,4,1,8,5,2]`, period 4.
- **P** = the row-2 pure speck = a SINGLE closed period-6 cycle ("orbit B"):
  `010/110/011 → 111/001/101 → 110/011/101 → 010/010/111 → 101/101/111 → 011/101/010 → (back)`.
  Map P by SINGLE-catch (one verified before→after per catch) — batch-catching confounds it (N67).
- **Q is Q-conjugate to orbit B**: Q maps every orbit-B state into the LOWER orbit, and
  `Q(111/001/101) = 101/001/111 = LOWER target` exactly. This is why the LOWER word ends in Q.
- UPPER pattern = **Q²** (baseline → `101/110/011`). LOWER pattern word from the POST-UPPER persisted panel
  `101/110/011` = **QQPPPPPQ** (offline BFS over {P-cycle, Q}; minimal, 8 catches; via `scratchpad/l6_bfsword.py`).

**Mobile-control catch methods (C15):** controls advance one step per displacement move. Row-9 PARITY forbids
catching a single-row patroller from the adjacent row — catch a speck by ENTERING its row and CROSSING it; catch
the roaming selector by 2D pursuit. P-catch cheaply by INTERCEPTING the speck at its CURRENT column (move toward
it on row 2) — ~1-5 moves/catch vs ~8 for park-and-wait. Both specks patrol cols 2-6 only; col 7+ on rows 2/8 is SAFE.

**Execution (forced UPPER-first — delivering UPPER dissolves (7,10) and unblocks col-10 for LOWER, C15):**
1. **UPPER align.** Set pattern Q² (catch row-8 Q twice). Set colour % (pursue the selector; this CROSSES row 8
   and corrupts Q→Q¹) — so **re-catch Q** afterward to restore Q². Refill at **(1,7)** (preserves alignment, avoid_rows=(2,8)).
2. **UPPER deliver.** Route to (2,9) (speck-safe), warp **(2,9)+A1→(5,9)**, then (5,9)→A4→(5,10)→A2→(6,10)→**A2,A2**
   into (7,10): the box DISSOLVES (becomes floor), block slides to (8,10), levels stays 5. The shared **panel PERSISTS**
   at `101/110/011` colour-%; **col-10 unblocks** ((8,10)↔(9,10) now reachable).
3. **LOWER align.** Set **colour @ FIRST** (selector, %→N→@ = 2 catches; do colour before pattern so selector
   pursuit can't corrupt the pattern word). Then the word **QQPPPPPQ**: **QQ** (catch row-8 Q twice) → `110/011/101`;
   refill **(9,1)** (block lands on row 9 after QQ); **P⁵** (intercept-catch row-2 P five times) → `111/001/101`;
   refill **(1,1) RIGHT AFTER P⁵** (block at (2,2), (1,1) is 2 moves — the decisive logistics fix, N69); **final Q**
   (descend to (9,4), one step up onto row 8 catches it) → `101/001/111` = LOWER target.
4. **LOWER deliver.** Route to (2,9) avoiding row-8/row-2 cols≤6 (don't re-apply Q/P), warp **(2,9)+A1→(5,9)**→A4→(5,10),
   descend col-10 (now unblocked) to (9,10), **A2** push into (10,10) → FULL REDRAW, levels 5→6. Block → L7 start (3,3).

**Refill schedule (the binding logistics):** (1,7)=UPPER, (9,1)=after-QQ, (1,1)=after-P⁵. The offline budget-ledger
proved one-life feasibility (~110 moves / 168 available); the live run confirmed it with lives staying 12 (zero deaths).

**Executed this session** (after a clean RESET-to-L6; full P-orbit precomputed offline so the run spent zero
exploratory budget): the route above, ending A2 from (9,10) into (10,10) = WIN, levels 5→6. Tooling:
`scratchpad/l6solve.py` (UPPER solver), `scratchpad/l6_lower.py` (LOWER solver: colour/q/p/deliver), `scratchpad/l6_bfsword.py`
(offline {P,Q} word BFS). Provenance: ai-executed (Opus, live); the offline P-solve + word BFS were ai-executed; the
colour-before-pattern + save-(9,1) ordering was ai-suggested (wm-predict, directionally correct). The prior "P has multiple
disjoint orbits" reading was FALSIFIED here (single-catch shows one period-6 cycle — N67).

## R-L7 — Level 7 SOLVED (levels_completed 6→7) [confirmed, live] → GAME COMPLETE 7/7

**The Locksmith loop (C10) + two-axis lock (C11) + composed {P′,Q} word (C14) + MOBILE controls (C15) over a
FOG-OF-WAR REVEAL maze, with the key-box LOCK-GATED in a portal-isolated pocket (C07 extended to fog — the WM's
decisive call).** L7 start: block (3,3); panel BASELINE pattern `010/010/111` colour-c (N); budget 42 @ **2/move**
(L7 is 2/move, not 1); %% resets 12 on entry; **RESET is LEVEL-LOCAL** (block→(3,3), full lives/budget, all 6
X-boxes restored, levels stays 6) → UNLIMITED free retries; budget — not lives — is the binding constraint.
**6 single-use-per-life X-boxes**: (1,1),(1,7),(1,9),(4,5),(9,2),(10,10). Two MOBILE pattern controls + a colour
selector + a portal network; the board is mostly fog(5) with a ~±4-cell viewport that moves with the block.

**Controls (all left/right-region, mobile per C15):**
- **Colour selector (8,1)** [left]: step-on cycles fill colour N→@→$→% (the same 4-state cycle as L3–L6); colour
  PERSISTS off-cell AND across pattern changes (axes independent, C11). Approach from (8,2)+A3, oscillate (8,2)↔(8,1).
- **P′ speck** = a period-6 NON-permutation cycle, patrols a TINY 2-cell row-8 corridor cols 2–3 (walled at col 4,
  selector at col 1): `010/010/111→101/101/111→011/101/010→010/110/011→111/001/101→110/011/101→(back)`. CATCH
  deterministically by entering the corridor and CROSSING: park at (8,2), press A4 to cross to (8,3) (and A3 back) —
  each cross = one P′ apply. Single-catch (one verified before→after) per the C10 must-sample-first rule.
- **Q speck** = 90° CW rotation, perm `[6,3,0,7,4,1,8,5,2]`, patrols **col-10** (rows 1–8) in the RIGHT region. CATCH
  by entering col-10 and crossing Q VERTICALLY: from (1,9)→A4→(1,10) (cross #1) →A2→(2,10) (cross #2) when Q sits at
  (2,10) — two col-10 crossings = QQ.

**The KEY-BOX target (the chicken-and-egg break, WM-led):** the key-box sits in a bottom-center pocket
{(10,4),(10,5),(10,6)} reachable from OUTSIDE only via the gate **(9,5)→(10,5)** (12-move route from start). The
target was thought unreadable (a "lone colour-8 cell") — but it is a READABLE 3×3 rendered 1px/cell, partly fog-masked:
decoded from raw pixels (board rows 51–53, cols 30–32, on='8') = **`101/110/011` colour-% (8)** (same state as the
L5 target / L6 UPPER target). The pocket is **LOCK-GATED** (C07-in-fog): at baseline-pattern+% and at
`101/101/111`+% the (9,5)+A2 push is a no-op; it OPENS only when panel == the exact target. Colour-% ALONE never
opens it (re-confirmed). (10,10) is a plain X-box, NOT a key-box — L7 is SINGLE-box, not multi-box.

**The word (offline {P′,Q} BFS, baseline→target):** **PPPPPQQ** (minimal over 24 reachable states):
`010/010/111 -P→101/101/111 -P→011/101/010 -P→010/110/011 -P→111/001/101 -P→110/011/101 -Q→101/011/110 -Q→101/110/011`.

**Execution (one life, zero deaths, via `scratchpad/l7solve.py` + `l7nav.py`):**
1. **Colour %** at the (8,1) selector (cycle to %); colour persists. 2. **P⁵** at the (8,2)↔(8,3) corridor (5 clean
   single-catches) → panel `110/011/101` colour-%. 3. Travel to the RIGHT region: refill (4,5) → (5,7) →
   **warp (5,7)+A1→(8,7)** → up col-9 → refill **(1,9)**. 4. **QQ** on col-10: (1,9)→A4→(1,10) [Q#1] →A2→(2,10)
   [Q#2] → panel **`101/110/011` colour-%** = TARGET. 5. **Deliver Q&P-safe**: route (2,10)→(9,5) avoiding col-10
   (Q) and the row-8 cols 2–3 corridor (P′) [a 12-move BFS], then **A2 at (9,5)** → the gate opens, block enters
   (10,5) → 284-cell redraw, **levels_completed 6→7, state=WIN**.

**Budget logistics (the binding difficulty):** 6 single-use X-boxes / life; ration them — the costly leg is
left→right (start→(5,7)→portal). Refill schedule that worked: (4,5) before the portal, (1,9) on entry to the right
region; (9,2)/(1,7)/(1,1)/(10,10) held in reserve. RESET-level-local makes mis-rations free to retry.

Provenance: ai-executed (Opus, live). **The WM (wm-predict) was decisive**: its grounded C07-in-fog hypothesis
("the portal-isolated pocket opens only when the lock is aligned to a derivable target; colour-alone is dead") was
the correct frame; the live refinement was that the target is READABLE (decode the marker as a 1px 3×3), not merely
guessable, and that (10,10) is an X-box (refuting the WM's secondary multi-box guess). The offline PPPPPQQ BFS was
ai-executed.

## ★ GAME COMPLETE — ls20 7/7 (levels_completed=7, state=WIN) ★
All seven levels cleared in one session: L1–L5 via verbatim replay (`harness/replay/`), L6 via R-L6 (one-life
two-box double-delivery), L7 via R-L7 (WM-led fog-pocket lock-gate). The World Model led the L7 solve — its
read-only grounded reasoning over the ARA cracked the chicken-and-egg pocket that had blocked the prior session.
