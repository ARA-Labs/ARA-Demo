# L4 raw exploration notes (session 2026-06-29_001)

## Board map (macro 12x12, clean start after RESET)
- Block start: macro (1,10). Block = 5x5, top 2 rows color-c (N), bottom 3 rows color-9 (@).
  step.py H10 detector (9>=6 AND c>=4) locates it correctly.
- Key-box: macro (1,1) (top-left), `@` 3x3 target read from rows6-8 cols8-10:
  row6 @@@ =111, row7 +@+ =010, row8 @+@ =101  => TARGET pattern = 111/010/101, colour @ (9).
- Panel (bottom-left, macro (11,0)): step.py reads pattern=111/111/111 colour=e ($).
  (manual 2x2 decode gave an irregular $ blob; step.py 3x3 decode => 111/111/111.)
- Colour selector: macro (6,6), compound glyph rows31-33 `@$$ / @ % / NN%` (same look as L3 R9C5).
- X-boxes (budget refill, color-b): macro (3,3) and (10,6).
- Right indicator NNNNN/@@@@@ at (1,10) = THE BLOCK (not a fixture) — moves with it.
- color-1 specks (5-cell `.....` strips) at 8 macros: (3,8)(4,5)(5,9)(6,3)(6,7)(7,0)(8,5)(8,9). role TBD.

## NEW MECHANIC (L4): TELEPORTER cells (reproducible)
- From macro (4,7): pressing A2 (down) -> block warps to (1,7) [jumps UP 3 rows].
  Reproduced twice. Walking down col7: (1,7)->(2,7)->(3,7)->(4,7)->(1,7).
- From macro (4,7): pressing A3 (left) -> block warps to (4,10) [jumps RIGHT, opposite dir].
- So the destination depends on EXIT DIRECTION, not a single fixed target.
  Hypothesis: target cells (5,7) [down-of-(4,7)] and (4,6) [left-of-(4,7)] are teleporters
  that immediately warp the entering block. (5,7) & (4,6) read as plain color-3 floor, NOT specks.
- This breaks naive pathfinding: BFS routes THROUGH these cells and gets warped off-plan.
- Workaround found: BFS avoiding (5,7) yields alt route to selector (6,6): A2 A2 A2 A3 A2 A2
  via (4,6)->(5,6)->(6,6) -- BUT that uses (4,6) which ALSO warped. Need full teleporter map.

## TODO
- Map ALL teleporter cells + their per-direction destinations.
- Then route to colour selector (6,6) and pattern switch(es); sample each (C10).
- Identify what sets pattern 111/010/101 (target middle row 010 is unusual vs H06 cycle).
- Deliver into key-box (1,1) (2-push, H09).

## Budget: ~2/move on L4. Refill at X-boxes (3,3),(10,6).

## !!! UNIFYING DISCOVERY: the "teleports/portals" were BUDGET-DEATH RESPAWNS (no portals exist) !!!
- Confirmed from full log scan (turns 173..741 etc): EVERY apparent "teleport/portal jump" is the SAME
  event: when the budget bar reaches 0 and you press one more move, the block RESPAWNS at the current
  LEVEL'S START cell, budget refills to 42, and %% decrements by one step (12->8->4->reset 12).
  Level starts: L1 block respawn ~(9,6); L2 -> (8,5); L3 -> (9,1); L4 -> (1,10).
- So the L4 "(4,7) hub with direction-dependent destinations" was an ARTIFACT: each "warp" was just a
  budget-0 death respawning to L4-start (1,10) (or to wherever the next over-budget move landed it).
  THERE ARE NO PORTALS on L1-L4. The block always moves 1 macro-cell/press; walls = no-op.
- %% is the LIVES/DEATHS counter: 3 deaths drain it (12->8->4->0); resets to 12 on each new level start.
  GAME_OVER = you die (budget hits 0) when %% is already 0 -> no life left -> episode ends, harness exits.
- THEREFORE the L4 mechanic was NOT characterized this session: I never actually mapped L4's lock because
  I kept dying. The L4 controls (selector (6,6), X-boxes (3,3)/(10,6), 8 color-1 specks, pattern source)
  remain UNCHARACTERIZED. Target read cleanly though: key-box (1,1) pattern 111/001/101 (re-read: middle
  row @ is the RIGHT cell => 001, not 010), colour @ (9); panel starts 111/111/111 colour e.

## OPERATING RULE going forward (lets you climb reliably): ALWAYS refill at an X-box while budget is
## still POSITIVE (>=2). A refill from budget>0 is free (no %% cost) and avoids the death-respawn.
## Plan routes so an X-box is reachable within the budget bar (~21 moves) at every leg.

## !!! CRITICAL: RESET = FULL-GAME RESET to Level 1 (NOT level-retry) !!!
- harness.log: at count 214 a RESET dropped levels_completed 3 -> 0. RESET restarts the WHOLE game
  to L1 (block back at L1 start R9C6, levels_completed=0). The task brief's "RESET restarts L4" is
  WRONG for this game/harness. DO NOT press RESET to retry a level -- it costs you L1-L3.
  Recovery = re-win L1,L2,L3 via R-L1/R-L2/R-L3 (no RESET) to climb back to L4.
- CONSEQUENCE for L4 portal mapping: my earlier "same moves -> different destinations" chaos was
  because intervening RESETs had dropped me to L1/L2/L3 boards. The ONLY clean L4 portal facts are
  the ones taken BEFORE the first stray full reset (the (4,7)-hub block; see below) -- but even those
  are now suspect since I can't be 100% sure which level I was on. TREAT L4 PORTAL MAP AS UNVERIFIED.

## !!! CRITICAL #2: %% MARKERS ARE A REAL DEPLETING RESOURCE -> GAME_OVER (overturns prior ARA claim) !!!
- The bottom-right %% markers (color-8) are NOT a permanent decorative UI fixture (the ARA / prior
  session said they were -- that is now FALSIFIED for L3/L4).
- Observed this session on L3: %% counted 12 -> 8 -> 4 -> 0, decrementing by ~4 each time I hit an
  X-box refill (or over a span of moves). When budget(X bar) hit 0 AND %% hit 0 simultaneously, the
  game went state=GAME_OVER (turn frozen, actions no-op, levels stuck at 2). So the run ENDED mid-L3.
- Interpretation (provisional): %% is a SECOND global resource -- possibly "lives"/"continues" or a
  hard global move/refill cap. Each X-box refill may COST a %% unit (refill is not free!), or %% ticks
  down per N moves. So X-boxes refill the per-leg budget bar but draw down the global %% pool; when both
  are empty the episode is over. NEEDS clean measurement: count exact moves/refills per %% decrement.
- IMPLICATION: H08 ("X-boxes are free refills, never touch lock") needs an addendum: refills may cost
  the %% global resource. And H10's "budget 0 is not a hard stop" holds ONLY while %% > 0.
- RECOVERY from GAME_OVER: must RESET, which (per CRITICAL #1) restarts the WHOLE game at L1.
- WHY THIS BIT ME: I treated refills as free and refilled liberally (~5 times across L1-L3), draining
  %% to 0. Lesson: minimize X-box refills; budget moves to spend %% sparingly; plan the SHORTEST routes.

## !!! RESOLVED: %% decrement RULE (from log correlation, turns 173/220/313/359) !!!
- %% decrements by 4 *ONLY* when you refill at an X-box while the budget bar is EXACTLY 0 (an
  "overdraft" refill: budget 0->42 costs 4 %%). Every refill from budget > 0 (e.g. 20->42, 4->42,
  6->42, 8->42) costs ZERO %% (12->12).
- So %% is an OVERDRAFT-PENALTY counter, not a per-refill cost. RULE: **always refill while budget is
  still POSITIVE (e.g. at 4-8). NEVER let budget reach 0 before touching an X-box.** Then %% stays full
  and you can refill unlimited times.
- GAME_OVER = budget 0 AND %% 0 simultaneously (you overdrafted ~3 times then ran dry again).
- This means H08 stands as-is (refills are effectively free if you never overdraft); H10's "budget 0
  still executes / X-box still refills at 0" is TRUE but TRIGGERS the %% penalty -- so avoid relying on it.
- CORRECTION to "%% is permanent UI fixture": %% IS dynamic but only moves on overdraft refills; a
  clean run that always refills early keeps %%=12 the whole game (consistent with why L1/L2/L3 prior
  wins saw %%=12 throughout -- those runs happened to refill before 0).

## L4 CLEAN CHARACTERIZATION (after disciplined re-climb to L4, budget kept positive):
- L4 target (key-box (1,1), @ rows6-8 cols10-12): pattern 111/001/101, colour @ (9). Panel starts
  111/111/111 colour e ($). So L4 = TWO-axis lock like L3 (pattern + colour).
- COLOUR selector at macro (6,6): SAME 4-state cycle as L3: N(c)->@(9)->$(e)->%(8)->N. Each step-on
  advances one. Reached colour @ by cycling. Colour persists on step-off. (Confirmed live this session.)
- L4 ALSO HAS REAL PORTALS (this is genuinely separate from budget-death; observed at budget 29-35, %%12):
  * macro (4,7) + DOWN  -> warps block to (1,7)
  * macro (3,6) + DOWN  -> warps block to (4,10)
  These are reproducible teleporters, NOT deaths. So L4's NEW MECHANIC (vs L1-L3) = a PORTAL/TELEPORTER
  network laid over the maze; certain floor cells warp the block on entry. The 8 color-1 specks
  ((3,8)(4,5)(5,9)(6,3)(6,7)(7,0)(8,5)(8,9)) are the likely portal markers/endpoints (unconfirmed map).
  Pathfinding must AVOID portal cells (BFS with them blocked yields valid routes).
- STILL TODO on L4: find the PATTERN control (selector only does colour; need to set 111->001 middle row).
  Likely one of the color-1 specks is a pattern switch (H06 4-state cycle). Then align + deliver into
  key-box (1,1) (2-push). Budget/%% discipline + portal-avoidance required.

## L4 pattern-control hunt (UNRESOLVED):
- Selector (6,6) = colour only. Searched for a pattern switch: the 8 color-1 specks are `.....` strips
  on the EDGES of WALL macro-cells (e.g. (3,8) bottom edge, (5,9)/(8,9) left edge) -- NOT steppable
  floor switches; they look like portal markers/endpoints. A color-0 cluster at (6,4) sits INSIDE a
  wall macro (R6C4=#) -- also not steppable.
- Tested hypothesis "portal traversal toggles the pattern": stepped (4,7)+DOWN through its portal ->
  pattern UNCHANGED (still 111/111/111). So portals do NOT set the pattern.
- => L4 pattern-axis control NOT located this session. Open hypotheses: (a) a pattern switch is reachable
  ONLY by riding a specific portal to an otherwise-walled region; (b) the specks are steppable from a
  particular side I didn't try; (c) pattern is set by a mechanism tied to delivering/aligning differently.
- L4 STATUS: reached cleanly (levels_completed=3), NEW MECHANIC identified (portal network) and colour
  axis solved; pattern axis + delivery NOT solved. L4 = UNSOLVED but well-characterized.

## NAV/TOOLING notes for next session:
- harness runs ~0.1-1 fps; play.py send is async. MUST wait for the turn counter to advance before
  reading the result frame (scratchpad/nav.py does this) or the block detector misreads transition frames
  (the spurious "(2,1)->(1,6)" etc. drift flags were stale-frame reads, not real warps).
- Block detector: color-c>=5 in a macro = the block (its N-cap); robust vs key-box/selector/panel.
- scratchpad/nav.py R C [maxsteps] [minbudget]: single-action+turn-wait+re-pathfind; stops at LOWBUDGET
  (default 4) so it never dies mid-route; flags real >2-cell jumps (portals) as DRIFT.
- For L4, pre-block known portals (4,7),(3,6),(5,6) in a BFS to route around them.

## L4 portal observations (EARLIER, PARTLY = budget deaths; superseded by clean section above):
- A cell behaving as a portal HUB near macro (4,7): exiting it warped the block far
  (down->(1,7), left->(4,10), right->(9,8) in one session). Panel never changed => portals are pure
  navigation, not lock controls. Needs clean re-mapping.
