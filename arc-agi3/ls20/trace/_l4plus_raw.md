# L4+ raw play notes (this session, 2026-06-29) — ai-executed unless tagged

## Session context
- Restarted harness fresh (previous game had EXITED/SIGINT). Re-climbed L1->L2->L3 via recipes,
  then SOLVED L4. Now on L5.
- Tooling built this session: scratchpad/pathfind_portal.py (portal-aware BFS) and
  scratchpad/drive.py (consolidated robust driver: O11 block detector, single-action-then-
  re-pathfind H10, turn-wait, low-budget stop, portal-aware BFS gated per level).
- Portal table must be gated PER LEVEL (levels_completed): L4 portals != L5 portals. A bug where
  the L4 PORTALS table applied on L1/L2/L3 caused phantom-warp BFS loops; fixed by active_portals()
  returning {} unless on the matching level (L4=levels==3, L5=levels==4).

## L4 SOLVED (levels_completed 3->4, turn 167)
- Layout: block start (1,10). key-box = plus-shape around macro (1,1) (K cluster R0C1,R1C0-2,R2C1).
- Panel BASELINE = 010/110/011 colour-e ($)  [panel.py canonical; step.py's 111/111/111 is the bug].
- Target (key-box) = pattern 111/001/101 colour-@ (9). Re-confirmed.
- TWO-AXIS lock (pattern + colour), same family as L3.

### DECISIVE TEST (the brief's cheapest-first hypothesis): does the COLOUR selector double as the
### pattern control?  ANSWER: NO.
- Colour selector at macro (6,6) (compound 9/e/8/c glyph). Sampled 6x clean (C10): stepping it
  cycled COLOUR through the 4-state cycle %->N->@->$ (8->c->9->e) while the PATTERN stayed ROCK-SOLID
  at 010/110/011 every single sample. The selector is COLOUR-ONLY. The double-duty hypothesis is REFUTED.
- (6,6) selector geometry: walled left/right/down; only entry/exit is UP to (5,6). Re-toggle by
  stepping off UP to (5,6) and back DOWN to (6,6).

### PATTERN AXIS CONTROL = the color-0 floor speck at macro (6,4), steppable from the SOUTH.
- O16 had said "(6,4) is a color-0 cluster inside a wall / not steppable" — that was an UNDER-SAMPLED
  VISUAL verdict (a C10 violation), exactly as the WM flagged (O19, candidate (a): "a speck steppable
  from an UNTRIED side"). Approaching (6,4) from the SOUTH ((7,4)+UP->(6,4)) STEPPED onto it.
- Stepping onto (6,4) changed the panel pattern 010/110/011 -> 111/001/101 in ONE step = EXACTLY the
  target pattern. (Did not over-step it; one step-on landed the target. Transform-kind, e.g. toggle vs
  cycle, NOT fully sampled because it hit target immediately — flagged for re-sampling if re-solving.)
- Alignment PERSISTS on step-off and through navigation (like L3). Colour was already @ from the
  selector sampling, so after the speck step BOTH axes were aligned.

### Delivery
- Routed (portal-aware) to (1,3) (immediately RIGHT of the key-box). Panel persisted 111/001/101 @.
- 2-push delivery (H09): A3 (LEFT) wedged to (1,2) [key-box border, no win], A3 again ENTERED (1,1)
  -> WIN, levels_completed 3->4. Budget/lives fine throughout (lives stayed 12, never died on L4).

### L4 portal map (O18 + corrections this session)
- O18's mapped edges were used by pathfind_portal.py and got the block across. BUT several MORE
  portal edges were discovered live that are NOT in O18: (4,9)+A3->(9,8); (5,6)+A1->(4,10);
  (6,8)+A1->(5,6). So the L4 portal map is still PARTIAL. (4,7) is a trap hub (O18) confirmed.
- drive.py's re-pathfind-each-leg handled the unmapped warps (re-plans from actual landing), which is
  why the solve succeeded despite an incomplete portal table.

### N48 resolution (panel baseline contradiction O16 vs O17)
- SETTLED in favour of O17/panel.py: live panel reads 010/110/011 colour-e. O16's 111/111/111 came
  from the buggy step.py decoder. The L4 pattern axis drives 010/110/011 -> 111/001/101 via the (6,4)
  speck (a single-press control, NOT obviously the H06 4-state cycle — baseline 010/110/011 is outside
  the H06 cycle, consistent with a different/independent pattern mechanic).

### WM utility (thesis evidence)
- The WM's prior guidance (O19) DIRECTLY led to the L4 solve: it named "speck steppable from an
  untried side" as candidate (a) and flagged the "specks not steppable" verdict as under-sampled.
  Testing the (6,4) speck from the SOUTH (untried side) was exactly that branch, and it WAS the
  pattern control. Strong positive data point for "ARA-as-world-model directs play."

## Mechanic corrections found this session (stage; affect H08/C12)
- BUDGET-0 X-BOX REFILL IS SAFE (no death): stepping onto an X-box cell while budget==0 REFILLS to 42
  and does NOT decrement %% (verified repeatedly on L3 and L5). The overdraft death-respawn happens
  only on a NON-refill move pressed at budget 0. So the X-box refill takes precedence over the
  budget-0 overdraft. This REFINES H08/C12 (which implied refill-at-0 = overdraft). Operationally:
  you CAN coast to budget 0 and land on an X-box to refill life-free; only a plain/wall move at 0 kills.
- DELIVERY 2-push confirmed on L4 too (wedge then enter), and the WINNING (2nd) push pressed at
  budget>0 (even budget 2) is a normal win, not an overdraft — only matters that budget>0 when pressed.

## L5 (in progress, NOT solved) — levels_completed 4
- Start (8,9), right corridor. key-box top-right (macro ~R0-2 C9-10).
- Panel baseline 010/110/011 colour-c (N). Target = pattern 101/110/011 colour-% (8) [decoded from the
  color-8 3x3 at scr rows6-8 cols55-57: 8.8/88./.88]. Two-axis lock again.
- Colour selector at (5,5). Pattern-speck candidates: (2,3) [4x color-0], (7,2) [3x color-0 + 2x color-1].
- L5 is PORTAL-HEAVY in the right corridor; (4,7) is AGAIN a trap hub. L5 portals discovered so far:
  (7,9)+A1->(8,9); (9,10)+A2->(2,10); (4,7)+A2->(1,7); (4,7)+A3->(4,8). Portal-blind BFS loops at
  (4,7); added these to drive.py _PORTALS_L5 so BFS avoids the trap.
- One death taken on L5 (overdraft at budget 0 in the portal corridor): lives 12->8.
- Status at pause: lives 8, budget ~6, block stuck upper-right; about to retry with portal-aware BFS.

## L5 deeper probing (turn 8, still UNSOLVED) — ai-executed; WM-consulted (ai-suggested)
- Consulted wm-predict over ara-ls20/ for an L5 plan (1 life left). WM answer (key points):
  (a) bet pattern speck = (2,3) [pure 4x color-0, byte-match to L4's (6,4)] over (7,2) [mixed 0/1, looks
      like an L3-style switch]; step from its open-floor side; (b) avoid (4,7) by working LEFT/BOTTOM,
      colour-first then speck, refill on a full bar before the top-right delivery corridor; (c) EXPECT a
      SINGLE-PRESS speck (not H06 cycle) because L5 baseline 010/110/011 == L4 baseline, OUTSIDE the H06
      cycle (target 101/110/011 differs only in the TOP row 010->101 = a one-press-sized change).
  WM confidence: medium on lock, LOW on navigation survivability (left-half portal density unmapped).
- Acted on it: the LOWER-LEFT route (8,9)->(9,2) is PORTAL-FREE and clean — reached the left X-box (9,2),
  refilled to 42 life-free. GOOD: the left/bottom is navigable.
- BUT the COLOUR SELECTOR (5,5) sits in a PORTAL-ONLY POCKET: with the L5 portal edge (5,8)+LEFT->(1,7)
  added, there is NO floor path to (5,5) (drive.plan returns NO PATH). The pocket (floor C5-8 on row5) is
  guarded — its left exit (5,8)->(5,7) is a portal, and (5,4)/(4,5)/(6,5) are walls. So (5,5) is reachable
  ONLY by a warp that LANDS inside the pocket — entrance NOT yet found (the L5 analog of L4's (4,7)+RIGHT
  pocket). This is the live L5 blocker.
- L5 portal edges known so far (added to drive.py _PORTALS_L5): (7,9)+UP->(8,9), (9,10)+DOWN->(2,10),
  (4,7)+DOWN->(1,7), (4,7)+LEFT->(4,8), (3,6)+DOWN->(4,8), (5,8)+LEFT->(1,7).
- STOPPED active play at budget 6, lives %%=4 (ONE death left). Did NOT gamble the last life on the
  unmapped pocket entrance (H11 discipline + the WM's low navigation-confidence). L5 UNSOLVED.
- NEXT-SESSION L5 PLAN: restart fresh (replay L1->L4 via harness/replay/ to regain L5 with %%=12), then
  HUNT THE POCKET ENTRANCE: systematically probe right-corridor cells for a warp that lands in the C5-8/row5
  pocket (try the cells adjacent to the pocket walls; L4's pocket was entered by (4,7)+RIGHT, so test the
  hub-region exits). Once inside, set colour %, then test the (2,3) speck from its open side (expect single
  press 010/110/011->101/110/011), carry aligned block to the top-right key-box, 2-push deliver. Keep a full
  bar before the delivery corridor; never overdraft except onto an X-box.
- WM UTILITY (thesis): the WM correctly predicted (a) the left/bottom is the safe zone and (b) the selector
  being pocket-guarded is consistent with its "portal-pocket" framing; its (2,3)-speck and single-press
  predictions remain UNTESTED (couldn't reach the controls). Net: directionally helpful again, not decisive
  this turn (the pocket-entrance navigation, not the lock, is the wall).
