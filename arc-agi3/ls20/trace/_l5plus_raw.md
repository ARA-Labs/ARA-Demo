# L5+ raw play notes (session 2026-06-29 turn #9) — ai-executed unless tagged

## Setup / replay
- Killed the stale mid-L5 harness (1 life), restarted fresh, REPLAYED L1->L4 via harness/replay/
  (replay.py L1 L2 L3 L4). CLEAN 4/4 fast-forward: L1 cleared@action12, L2@44, L3@48, L4@59 ->
  levels_completed 0->4, arrived L5 at turn 167 with %%=12 (FULL lives), budget 42. Replay reproduced
  the climb verbatim with no desync. Confirms harness/replay/ is a reliable L1->L4 regain tool.
- Fresh L5 state: block@(8,9), panel baseline 010/110/011 colour-N (panel.py), lives 12, budget 42.

## L5 layout re-confirmed (matches O20)
- Macro 12x12 (macro.py). Key-box top-right: K cluster (0,10),(1,8?),(1,9),(1,10),(2,10). [NOTE: (1,8)
  is actually an X-BOX not key-box; the real key-box @-target is the color-8 3x3 top-right.]
- COLOUR SELECTOR at macro (5,5) (compound @$$/@ %/NN% glyph, screen rows 25-29). Target pattern
  101/110/011 colour-% (8) per O20.
- X-boxes: (1,8), (2,1), (9,2) [3 this level].
- (4,7) is AGAIN a portal trap hub.

## ★ THE POCKET IS GEOMETRICALLY SEALED — confirmed precisely (the live L5 blocker)
- Reachability map (portal-aware BFS from block): EXACTLY 4 floor cells are UNREACHABLE, and they are
  EXACTLY the selector pocket: (4,6),(5,5),(5,6),(5,7). Every other floor cell (63 total) is reachable.
  So (5,5) selector is reachable ONLY by a portal that LANDS inside {(4,6),(5,5),(5,6),(5,7)}.
- Pocket geometry (floor adjacency): (5,5)[selector] touches only (5,6) [E]; walls N/S/W ((4,5),(6,5),
  (5,4)). (5,6) touches (4,6)N,(5,5)W,(5,7)E. (5,7) touches (4,7)N,(5,6)W,(5,8)E. (4,6) touches (3,6)N,
  (5,6)S,(4,7)E. So the pocket's 4 "natural" floor entrances are: (3,6)->(4,6) via A2, (4,7)->(5,7) via
  A2, (4,7)->(4,6) via A3, (5,8)->(5,7) via A3. ALL FOUR are PORTALS (tested this turn), so no floor walk in.

## Portal edges TESTED live this turn (each (cell,dir)->dest, all at budget>0 %% unchanged = genuine)
- (4,7)+A3(LEFT)  -> (4,8)   [portal; matches table]
- (4,7)+A2(DOWN)  -> (1,7)   [portal; matches table]
- (4,7)+A4(RIGHT) -> (4,8)   [PLAIN FLOOR step — NOT a portal]   <-- refutes the WM "hub RIGHT = pocket gate" L4 analogy
- (4,7)+A1(UP)    -> (3,7)   [PLAIN FLOOR step — NOT a portal]
- (3,6)+A2(DOWN)  -> (4,8)   [portal; matches table]
- (5,8)+A3(LEFT)  -> (1,7)   [portal; matches table]
- (5,8)+A1->(4,8) FLOOR; (5,8)+A2->(6,8) FLOOR; (5,8)+A4->(5,8) NOOP(wall)
- (4,8)+A1->(3,8) FLOOR; (4,8)+A2->(5,8) FLOOR; (4,8)+A4->(4,8) NOOP(wall)
=> The (4,7) hub has ONLY 2 portals (LEFT, DOWN), both leaving the pocket region. The hub is NOT the
   pocket entrance on L5 (unlike L4, where the hub's RIGHT exit was the pocket gate). WM L4-analogy REFUTED here.

## color-1 (.) strip cells = portal endpoint markers (per O15), and they BORDER the pocket
- Strips at: (0,6),(4,5),(5,4),(5,9),(6,7),(6,11),(8,7),(11,10) [on wall cells, color-4 dominant] + the
  (7,4) color-0/1 speck. CRUCIAL: (4,5) and (5,4) are the pocket's OWN N/W walls; (5,9),(6,7) border the
  pocket's E/SE. So a portal whose DESTINATION is the pocket likely terminates at one of these endpoints,
  i.e. lands in (4,6) [next to (4,5)], (5,5) [next to (5,4)], (5,7) [next to (6,7)]. The pocket-entrance
  portal SOURCE is still unfound — sweeping reachable cells for a warp landing in the pocket.

## Portal-destination sweep so far (portal_hunt.py): probed (5,8),(4,8) untested dirs = all FLOOR/NOOP,
   NO pocket landing yet. Hunt incomplete (budget management ate the run; (1,8) X-box now CONSUMED).
- Tooling: scratchpad/portal_hunt.py drives to candidate source cells, presses untested dirs, logs
  (cell,dir)->dest, halts on a pocket landing. Budget/life-safe (refills, never plain-overdrafts).

## ★★ POCKET ENTRANCE FOUND: (2,6)+A1(UP) -> (5,6)  [the L5 pocket gate]
- Discovered live (turn ~253): pressing A1(UP) at macro (2,6) WARPS the block to (5,6) — INSIDE the
  selector pocket! (5,6) is one of the 4 sealed pocket cells. From (5,6), step A3(LEFT) -> (5,5) selector.
- This is the L5 analog of L4's pocket entry (L4 used (6,8)+UP->(5,6); L5 uses (2,6)+UP->(5,6)) — same
  "warp from outside lands on a pocket-adjacent floor cell" mechanism (C13). The WM's "warp-into-pocket
  via an endpoint-strip-adjacent source" framing pointed at the north side; (2,6) is two rows above the
  pocket and warps DOWN into it.
- WARNING: (5,6)+A1(UP) warps BACK OUT to (4,8) (a return portal). So once in the pocket, do NOT press UP;
  go A3 to (5,5) [selector], sample colour, then exit deliberately.
- Confirmed (2,6)+A1 dest mid-sweep; need to RE-CONFIRM cleanly and map the pocket interior moves
  ((5,6)<->(5,5), (5,6)<->(5,7)) and how to EXIT the pocket carrying alignment to the key-box.
- Added (2,6,"A1"):(5,6) to drive.py _PORTALS_L5 so BFS can route INTO the pocket.

## Lives status: down to 4 (=last group; one more overdraft -> lives 0 -> respawn, then next death=GAME_OVER).
   STRICT discipline now: no plain-overdrafts; refill only by stepping onto an X-box; (2,1)+(9,2) X-boxes remain.
   L5 still UNSOLVED but the BLOCKER (pocket entrance) is CRACKED — selector now reachable.

## ✗ DISCIPLINE ERROR -> GAME_OVER (corrects a lives-counter reading)
- At lives 4 budget 0 (stuck at (4,8)), I overdrafted (forced — no adjacent X-box) expecting a respawn
  (8→4 had respawned fine earlier). Instead lives 4->0 == GAME_OVER IMMEDIATELY (turn 255, levels stuck 4).
- LESSON / mechanic refinement (sharpens C12): lives display "4" is the LAST life. The death that takes
  4->0 is the TERMINAL death (no respawn) — GAME_OVER. So 12->8->4 each respawn; 4->0 ends the game.
  (Earlier 12->8 and 8->4 overdrafts respawned cleanly; only 4->0 is fatal.) OPERATIONAL RULE going
  forward: treat lives==4 as ZERO margin — refill at an X-box BEFORE budget hits 0; never let budget reach
  0 anywhere except ON an X-box when lives==4. The real error was letting the block strand at (4,8) b=0
  with no adjacent X-box during the sweep; the portal_hunt refill logic mis-handled consumed/unreachable
  X-boxes and stranded it.
- This is the SECOND time discipline (not the lock) lost a run on L5 — the pocket-entrance HUNT itself
  burned the budget/lives. With the entrance now KNOWN ((2,6)+UP->(5,6)), the next attempt skips the hunt
  and goes straight in, so it should be far cheaper.

## ★ ATTEMPT 2 (after replay regain, %%=12): COLOUR AXIS SOLVED + pocket fully mapped
- POCKET INTERIOR MAPPED: entrance (2,6)+A1->(5,6) [clean, re-confirmed]. Inside, (5,6) exits:
  A3->(5,5)[selector, FLOOR], A1->(4,8)[portal OUT], A4->(1,7)[portal OUT], A2->(6,6)[wall].
  (5,5) exits: A4->(5,6)[FLOOR only]. So the pocket is a 2-cell oscillator (5,6)<->(5,5) for the
  colour axis; (4,6)/(5,7) are NOT reachable even from inside. Exit the pocket via (5,6)+A1->(4,8).
- COLOUR CYCLE (selector (5,5), step-ON advances): N(c)->@(9)->$(e)->%(8)->N — SAME 4-state cycle as L3/L4
  (5th occurrence). From baseline N, 3 ON-steps reach % (the target). Pattern stayed 010/110/011 every
  sample (selector COLOUR-ONLY, C11). COLOUR % SET successfully; colour PERSISTED through the portal exit
  to (4,8) (confirms C11 alignment-persists-through-portals).
- DISCIPLINE: had to overdraft once (12->8) when stranded at budget 0 next to consumed X-box — colour reset
  on respawn (C12). Re-set is cheap (~8-move pocket round trip). Lives now 8.

## ★ PATTERN AXIS = the (2,3) speck, BUT its cycle does NOT contain the target (open problem)
- (2,3) [4x color-0] IS the pattern control (steppable from (2,4)+A3). Sampled its FULL cycle (C10) — it is
  a PERIOD-6 cycle, NOT the H06 4-state cycle and NOT a single-press (the WM's single-press bet REFUTED):
    baseline 010/110/011 -> 111/001/101 -> 110/011/101 -> 010/010/111 -> 101/101/111 -> 011/101/010 -> (back)
- The TARGET pattern (re-decoded carefully from the key-box color-8 3x3 at scr rows6-8 cols54-56 =
  101/110/011) is NOT any of the 6 states in the (2,3) cycle. So (2,3) ALONE cannot set the target.
- OPEN: either (a) a SECOND pattern control exists (the (7,3) speck [3x color-0 + 2x color-1] untested) and
  the two compose, or (b) the target needs (2,3) + something else, or (c) re-examine the target decode /
  whether colour-% changes which pattern is 'target'. NEXT: sample the (7,3) speck's cycle; check if (7,3)
  or (2,3)+(7,3) reaches 101/110/011. (Both specks may be independent pattern sub-controls, OR (7,3) is the
  real single control. This is the live L5 lock puzzle now that navigation is solved.)
- WM SCORE so far: predicted (2,3) as the pattern control = CORRECT (it is a pattern switch). Predicted
  single-press / target-in-one = WRONG (period-6 cycle, target not in it). Pocket-entrance framing = helped.

## ★★ L5 PATTERN AXIS = TWO COMPOSING SPECKS (2,3)=P and (7,3)=Q — a composed-permutation puzzle
- BOTH specks are pattern controls; NEITHER's own cycle contains the target 101/110/011. They must COMPOSE.
- P = (2,3) transform (period-6 on baseline orbit):
    010/110/011 -> 111/001/101 -> 110/011/101 -> 010/010/111 -> 101/101/111 -> 011/101/010 -> (back)
- Q = (7,3) transform (period-4 on baseline orbit):
    010/110/011 -> 010/111/100 -> 110/011/010 -> 001/111/010 -> (back)
- BFS over {P,Q} using ONLY same-orbit data reaches 9 states, NOT the target. Need the CROSS transitions
  (apply Q to a P-orbit state, etc.) to open the rest of the state space. Target 101/110/011 = baseline with
  ONLY the TOP row changed 010->101 (mid 110 + bottom 011 unchanged). So I need a P/Q word that nets a
  top-row 010->101 flip leaving mid/bottom — requires mapping cross-transitions.
- (7,3) approached from WEST: (7,2)+A4 steps onto it; toggle by (7,3)<->(7,2) via A3/A4.
- (2,3) approached from EAST: (2,4)+A3 steps onto it; toggle (2,3)<->(2,4) via A4/A3.
- The two specks are ~9-12 moves apart (refill at (9,2)/(2,1) between). Composed-puzzle solving is the
  remaining L5 work; colour axis + navigation are DONE.

## ★★★ L5 LOCK FULLY ALIGNED (both axes at target simultaneously) — only DELIVERY/budget blocked
- SOLVED the composed pattern puzzle: Q=(7,3) is a FIXED 90-deg ROTATION of the 3x3 (perm [6,3,0,7,4,1,8,5,2]);
  P=(2,3) is a period-6 transform (not a pure permutation). BFS over {P (known orbit), Q (rotation, total)}:
  word **PPQQ** maps baseline 010/110/011 -> target 101/110/011. VERIFIED LIVE:
    010/110/011 --P--> 111/001/101 --P--> 110/011/101 --Q--> 101/011/110 --Q--> 101/110/011 (TARGET). ✓
  (Q applied to the off-its-orbit P-state behaved EXACTLY as the pure rotation — the extrapolation held.)
- EXECUTED end-to-end this life: set pattern 110/011/101 at (2,3) [PP], set colour % at the pocket selector,
  then QQ at (7,3) -> panel reached **101/110/011 colour % = TARGET on BOTH axes**, and the alignment
  PERSISTED through all navigation + the pocket portal exit (strong C11 confirmation across portals+specks).
- ★ SPECK AUTO-TOGGLE HAZARD: stepping the block ONTO a speck cell IN PASSING (during a walk) applies its
  transform too — so routes must AVOID (2,3)/(7,3) once the pattern is set (drive.plan + a 'crosses speck?'
  check). This caused one accidental extra P-press mid-run. Plan speck-free routes after aligning.

## ✗ DELIVERY BLOCKED BY BUDGET (the only thing between here and the L5 WIN)
- Key-box = a PLUS at macro (0,10),(1,9),(1,10),(1,11),(2,10); center+target = (1,10) (color-8 target inside
  color-5 frame). The WEST arm (1,9) is a WALL (color-4) — pushing A4 from (1,8) is a NO-OP (tested 2x, no
  win). So delivery must come from the SOUTH arm (2,10): approach (3,10) and push A1(UP) (3,10)->(2,10)->(1,10).
  [N arm (0,10) has no row above; E arm (1,11) push-cell (1,12) is off-board.] -> DELIVER FROM (3,10) GOING UP.
- BUT: stranded at (1,8) budget 6, lives 4, ALL 3 X-boxes CONSUMED this life; (3,10) is 12 steps (24 budget)
  away through portals. Cannot reach it without overdrafting, and overdraft at lives 4 == GAME_OVER. So this
  life CANNOT deliver despite the lock being fully aligned.
- ROOT CAUSE: the pocket-entrance HUNT + the (8,2)+A2 mis-step (a stale-route overdraft, 8->4) burned 2 of 3
  lives and all X-boxes before the lock was aligned. With the FULL recipe now known, a clean next attempt
  (no hunt) should align + deliver comfortably within the lives/X-box budget.

## ★ COMPLETE L5 RECIPE (for R-L5 once delivered) — everything below is verified except the final 2-push:
1. Replay L1->L4 (regain L5 %%=12 budget 42). Block start (8,9). Panel baseline 010/110/011 colour-N.
   Target = pattern 101/110/011 colour-% (8) (key-box center (1,10)). X-boxes (1,8),(2,1),(9,2) (each single-use).
2. PATTERN: at (2,3) [approach (2,4)+A3 or (2,2)+A4; period-6 transform P] press 2x -> 110/011/101;
   then at (7,3) [approach (7,2)+A4; Q = 90-deg rotation] press 2x -> 101/110/011. (Word PPQQ from baseline.)
   AVOID re-crossing either speck afterward (passing over re-applies the transform).
3. COLOUR: enter pocket via (2,6)+A1->(5,6); oscillate (5,6)<->(5,5) [A3 on / A4 off], 3 on-steps N->@->$->%;
   exit (5,6)+A1->(4,8). Colour % persists. (Do steps 2 and 3 in either order; both axes persist.)
4. DELIVER: route (speck-free) to (3,10), press A1(UP) twice -> (2,10) wedge, (1,10) ENTER -> WIN (levels 4->5).
5. BUDGET/LIVES: refill at X-boxes keeping budget>0; the budget-0-onto-X-box life-free refill (O21) is the key
   lifeline (used 3x this life). NEVER plain-overdraft at lives<=4 (== GAME_OVER). Keep a full bar before the
   delivery corridor. The whole solve is ~60-70 moves -> needs ~2-3 X-box refills; do not waste X-boxes early.

## ★★★★ L5 SOLVED — levels_completed 4->5 (turn 361, this session) ★★★★
- EXECUTED THE FULL RECIPE on the LAST life (%%=4) cleanly, no overdraft on the final pass:
  PP at (2,3) -> 110/011/101 ; colour % at the pocket selector ; QQ at (7,3) -> pattern 101/110/011
  (TARGET on BOTH axes) ; refill at (9,2) ; navigate (speck-free) to (3,10) ; **A1(UP) twice**:
  push1 (3,10)->(2,10) [south arm, MOVED — enterable since lock satisfied], push2 (2,10)->(1,10) center
  -> FULL REDRAW, levels_completed 4->5, advanced to L6 (block (10,4), %% reset to 12, budget 42).
- DELIVERY CONFIRMED: key-box = PLUS at (0,10)/(1,9)/(1,10)/(1,11)/(2,10); center (1,10) is the target;
  WEST arm (1,9) is a WALL (push from (1,8) is a no-op); the enterable arm is the SOUTH (2,10), so deliver
  by pushing UP from (3,10) (2-push H09: wedge into (2,10), enter (1,10)). This is L5's delivery geometry.
- The win came after 3 failed deliveries earlier this session (all on budget/lives discipline, NOT the lock):
  the lock was fully aligned 3 prior times but the block stranded at budget 0 away from an X-box. The fix was
  (a) PPQQ order is FORCED (P before Q), (b) refill at (9,2) AFTER QQ (not before) so the full bar covers the
  ~14-step delivery corridor + 2 pushes (32 budget), (c) avoid re-crossing specks (auto-toggle hazard), and
  (d) at %%=4 NEVER plain-overdraft (it's GAME_OVER, not a respawn).

## WM (world-model) SCORECARD on L5 (thesis evidence)
- HELPED: the pocket-entrance framing ("selector in a portal-only pocket; find the warp that lands inside",
  L4-analogy) directed the entrance hunt; the north-side endpoint-strip reasoning was in the right region;
  predicted (2,3) IS a pattern control (correct). Mixed: its "single-press speck / hub-RIGHT = gate" specifics
  were REFUTED (the entrance was (2,6)+UP, not the hub; the pattern needed a 2-speck composed PPQQ word, not a
  single press). NET: directionally useful for navigation framing; the decisive mechanics (entrance cell, the
  Q=90-deg-rotation insight, PPQQ) came from live probing + offline BFS, not the WM. A modest-positive data point.

## NEXT-ATTEMPT L5 PLAN (entrance known)
1. Restart harness + replay L1->L4 (regain L5, %%=12, budget 42).
2. Colour axis: route to (2,6) [reachable, upper area], press A1 -> warp to (5,6); A3 -> (5,5) selector.
   Sample the selector (C10): each step-on cycles panel FILL colour (L3/L4 cycle); stop on % (8) = target.
   Re-toggle by stepping (5,5)<->(5,6) (A4 off, A3 on). DO NOT press A1 in the pocket (warps out to (4,8)).
3. Exit pocket carrying colour: from (5,6) the only non-portal exits to map — (5,6)+A4->(5,7)->(5,8)+? 
   or use the return portal (5,6)+A1->(4,8) deliberately to leave (colour persists, C11). Then set PATTERN.
4. Pattern axis: speck candidates (2,3)[4x color-0, WM's bet, byte-match to L4 (6,4)] and (7,2). Expect a
   SINGLE-PRESS speck (baseline 010/110/011 -> target 101/110/011, differs only in TOP row, outside H06).
   Step it from its open side (try untried sides per C10/L4 lesson).
5. Deliver: carry aligned block to the top-right key-box, 2-push (H09).
6. DISCIPLINE: refill at X-boxes ((1,8),(2,1),(9,2)) keeping budget>8 and NEVER overdraft once lives<=8;
   at lives==4 keep a full bar before any committed corridor. The pocket round-trip is short (~few moves)
   so colour-setting is cheap now.

## L6 RECON (entered after L5 win; UNSOLVED) — levels_completed 5, %%=12, budget 42
- Block start (10,4). SAME two-axis-lock family (colour selector + pattern speck(s), rotation transforms).
- Panel BASELINE = 110/011/101 colour-e ($).
- ★ TWO key-boxes / TWO targets (NEW — L6's wrinkle):
  - UPPER box (right side, color-8): target pattern 101/110/011 colour-% (8).
  - LOWER box (right side, color-9): target pattern 101/001/111 colour-@ (9).
  - Likely a 2-delivery level (deliver to each with its own target?) OR pick one. UNTESTED.
- COLOUR SELECTOR (compound 9/e/8/c glyph) at macro (6,4).
- PATTERN speck candidates: (2,2) [4x color-0], (8,6) [3x color-0 + color-1].
  (8,6) SAMPLED: it IS a pattern control; its transform looks ROTATION-like (cycles 110/011/101 ->
  101/011/110 -> 101/110/011 -> 011/110/101 ...), same family as the L5 Q=90deg-rotation speck. Panel-read
  lag makes per-press reads noisy; read the SETTLED value with block OFF the speck.
- X-boxes: (1,1),(1,7),(9,1). color-1 strips: (0,9),(4,10),(8,6).
- ★ TOOLING NOTE for L6: drive.py _PORTALS gating is levels==4 (L5); on L6 (levels==5) active_portals()
  returns {} so the BFS is PORTAL-BLIND. If L6 has portals, add a _PORTALS_L6 table gated on levels==5
  (and map edges live like L5). No portals confirmed yet on L6.
- APPROACH for next session: same recipe as L5 — decode BOTH targets, sample selector (6,4) colour cycle +
  each speck's rotation, BFS the pattern word(s) offline, set colour+pattern, deliver (2-push per box). Watch
  the speck auto-toggle-on-pass hazard and the %%=4 no-overdraft rule. Two targets may mean two full align+deliver
  cycles (panel resets between? unknown) — characterize delivery #1's effect on the panel first.
