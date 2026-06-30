# L4 v2 raw notes (session 2026-06-29, WM-assisted) — pattern-axis hunt

## Entry state this session
- Live game mid-L4: levels_completed=3, %%=8 (one death already from a prior session), budget started ~35.
- Did NOT re-climb fresh (game was alive and usable); operated on the live L4 with 2 lives.

## WM QUERY (did it help? — record for the project thesis)
- Invoked wm-retrieve + wm-predict over ara-ls20/ asking where the L4 PATTERN control is.
- WM RETRIEVAL surfaced the decisive precedent trace:N23 / R-L3: the L3 PATTERN switch was ITSELF
  "a faint colour-0/1 floor speck" (macro R2C9) only operable by approaching from ONE specific side
  (R2C10 going LEFT). It flagged trace:N44's "specks not steppable" as an UNDER-SAMPLED VISUAL verdict
  (C10 violation) — the specks were dismissed by eye, never actually stepped from each side.
- WM PREDICTION: pattern control is most likely one of the 8 color-1 specks, reachable from an untried
  side (branch a), else in a portal-only-reachable pocket (branch b). Confidence medium. Concrete probe:
  step the block onto each speck from its open-floor side and read the panel.
- VERDICT ON WM HELP: **YES, materially.** It redirected me from "specks are walls, give up" to actively
  TESTING the specks AND it named the portal-pocket branch — which the session's findings then partly
  vindicated (a portal-gated pocket DOES exist). It also implicitly drove the panel re-read (see below).

## CORRECTION #1 (big): the panel decoder (scratchpad/step.py) MIS-READS the L4 panel.
- step.py reports panel = 111/111/111. RAW glyph decode is DIFFERENT.
- Panel = macro (11,0), color-e ($) fill. Exact color-e cells (rows55-60): 2x2 blocks at
  (55-56,5-6),(57-58,3-4),(57-58,5-6),(59-60,5-6),(59-60,7-8).
- 3x3 of 2x2 cells, rows{55-56,57-58,59-60} x cols{3-4,5-6,7-8}:
  row0=010, row1=110, row2=011  =>  **PANEL = 010/110/011 colour e**, NOT 111/111/111.
- Wrote scratchpad/panel.py (correct reader). step.py's panel field is UNRELIABLE on L4; use panel.py.
- TARGET re-confirmed from key-box (1,1) @ (1x1 cells, rows6-8 cols10-12): row6=111,row7=001,row8=101
  => target = 111/001/101 colour @ (9). So pattern axis must drive 010/110/011 -> 111/001/101.
- NOTE: baseline 010/110/011 is OUTSIDE the H06 4-state cycle (111/001/101 etc.) — so the L4 pattern
  mechanic may NOT be the same H06 cycle. This is new and unexplained.

## CORRECTION #2 (big): L4 PORTALS ARE GENUINE (overturns the _l4_raw "all warps were budget deaths").
- Reproduced MANY warps at budget>0 with %% UNCHANGED (8 throughout) = genuine portals, not deaths.
  (Deaths drop %% and respawn at L4-start (1,10); these did neither.)
- Portal (cell + exit-direction -> destination) data points collected this session (all %%-stable):
  * (4,7)+RIGHT -> (9,8)
  * (4,7)+LEFT  -> (4,10)
  * (4,7)+DOWN  -> (1,7)        [also from N42]
  * (9,8)+UP    -> (8,6)
  * (8,7)+RIGHT -> (8,6)
  * (8,3)+UP    -> (9,3)
  * (3,6)+DOWN  -> (4,10)       [from N42; (3,6)+RIGHT pass-through is CLEAN]
- So (4,7) is a 3-way portal HUB (RIGHT/LEFT/DOWN all warp; only UP non-portal). Portals are
  DIRECTION-SPECIFIC: passing THROUGH (3,6) going RIGHT did NOT warp; only (3,6)+DOWN warps.
- CONSEQUENCE: pathfind.py / macro lattice are BLIND to portals and route straight through them, so
  long plans desync constantly. nav.py drift-flags real warps but still wastes budget re-planning into them.
- POCKET FINDING: macro (8-9, 7-9) region (incl. speck (8,9)) appears reachable ONLY via the (4,7)+RIGHT
  portal — (9,7) is a wall so row-9 doesn't connect it; (8,7)+RIGHT and (9,8)+UP both portal back out.
  This is exactly the WM's "portal-only-reachable pocket" (branch b). NOT fully explored (didn't catalogue
  (8,8)/(8,9)/(9,9) interiors for a control — ran low on budget).

## SPECK PROBE (WM branch a) — one data point, NEGATIVE so far:
- speck (3,8): strip is color-1 on the BOTTOM edge (row19 cols44-48). Stepped block (3,7)+RIGHT INTO it:
  result = 2 cells changed (budget only), block stayed (3,7), panel unchanged => WALL NO-OP. (3,8) is
  NOT steppable from the LEFT. Did NOT get to test it from BELOW ((4,8)+UP) — the route there got
  portal-warped ((4,7)+RIGHT->(9,8)) before reaching (4,8).
- The other 7 specks were NOT probed this session (navigation/budget).

## WHOLE-BOARD GLYPH INVENTORY (definitive): the ONLY non-wall/floor/frame glyphs on L4 are:
  @(block body + key-box target), N(block cap), X(the 2 X-boxes), $(panel fill), %(lives),
  . (color-1: the 8 specks, 40 cells = 8x5), and 5 color-0 (' ') cells INSIDE the selector/(6,4) walls.
  => There is NO standalone "pattern switch" glyph on open floor. The pattern control MUST be one of:
     (a) a speck steppable from an untried side, (b) something in the (4,7)-portal pocket,
     (c) the colour selector (6,6) doing DOUBLE duty (colour+pattern) — UNTESTED with the corrected
         panel reader (could not reach (6,6): it's reachable only from (5,6)+DOWN, and (5,6)/(5,7) sit
         behind the portal hub; ran low on budget before arriving).

## CONFIRMED-UNCHANGED this session
- X-box (10,6) = pure budget refill (budget->42, panel 010/110/011 unchanged, %% unchanged). H08 holds.
- Portal traversal does NOT change the pattern (verified against the CORRECT baseline 010/110/011 now,
  not the wrong 111/111/111) — strengthens N44's "portals aren't the pattern control".

## STATUS: L4 still UNSOLVED. Pattern-axis control still UNLOCATED, but the search is now much better
## bounded: glyph inventory exhausted; 3 concrete candidate branches remain; panel baseline corrected;
## portal network partially mapped (7 edges) and the portal-pocket branch identified as live.

## NEXT-SESSION PLAN (highest EV first):
1. Reach colour selector (6,6) [via col-2 up to (4,2) -> row3 right (3,4->3,7) -> (3,7)+DOWN to (4,7)
   -> AVOID (4,7) portals: from (4,7) the only non-portal exit is UP; so (4,7) is a TRAP. Better: find a
   portal-free route to (5,6). Candidate: is (5,6) reachable from (5,7)+LEFT, and (5,7) from (5,8)+LEFT,
   and (5,8) from (6,8)+UP? Map the (5,x)/(6,8) corridor first.] Then step ON the selector and read panel
   with panel.py BEFORE/AFTER: test if it changes pattern as well as colour (branch c). CHEAPEST decisive test.
2. If selector is colour-only: ride (4,7)+RIGHT into the pocket and catalogue (8,8)(8,9)(9,9) for a control;
   probe speck (8,9) from its open side.
3. Probe remaining specks from their STRIP-facing side (each speck's strip is on a specific macro edge;
   approach from the floor cell on the open side, press toward it, read panel).
4. Build a portal-aware BFS (block portal (cell,dir) edges as discovered) so navigation stops desyncing.
5. Budget/lives discipline: %%=8 (2 lives) at session end, budget 10, block parked at (5,10). Refill at an
   X-box while budget>0; never overdraft.
