
# ===== L6 attack session (2026-06-29, turn~373 start) =====

## Entry state (verified live)
- levels_completed=5 (on L6), %%=12 (full lives), budget=30, block@(8,6), turn=373.
- panel BASELINE = pattern 110/011/101 colour-e ($) [panel.py + drive.py agree].
- drive.py active_portals() returns {} on levels==5 (PORTAL-BLIND on L6) — no _PORTALS_L6 table yet. No portals confirmed yet.

## Macro entity map (12x12, fresh read, CORRECTS O22's quick recon coords)
- block: (8,6)
- X-boxes (color-b, single-use refills): (1,1), (1,7), (9,1)  [O22 said (1,1),(1,7),(9,1) ✓]
- COLOUR SELECTOR (compound 0/8/9/c/e glyph @$$/@ %/NN%): macro (4,4)  [O22 said (6,4) — coords shifted; it's (4,4) this read]
- PATTERN speck candidates: (2,6) [color-0, 4 cells] and (8,2) [color-0 x3 + color-1 x2 = the ROTATION-type, O22's (8,6)/L5's (7,3) Q family]
- color-1 UI/portal-marker specks: (0,9), (4,10)
- panel: (11,0) colour-e
- TWO KEY-BOXES (right column band, col~10-11):
    UPPER box center ~(7,10): TARGET pattern 101/110/011 colour-% (8)  [decoded from raw rows36-38 cols55-57]
    LOWER box center ~(10,10): TARGET pattern 101/001/111 colour-@ (9) [decoded from raw rows51-53 cols55-57]
  => CONFIRMS O22's two-target structure. Likely a 2-delivery level (deliver to each box with its own pattern+colour).

## Plan
1. Sample colour selector (4,4) several times (C10) — expect the 4-state fill cycle N(c)->@(9)->$(e)->%(8).
2. Sample each pattern speck (2,6) and (8,2) several times — get their transforms (one may be a 90-deg rotation per O22/C14).
3. Offline BFS (C14) for the pattern WORD to reach EACH target (101/110/011 and 101/001/111) from baseline 110/011/101.
4. Determine delivery order + whether panel resets between deliveries.

## Control sampling (live)
### Colour selector (4,4) — SAMPLED
- Cycle = %→N→@→$  (8→c→9→e), PERIOD 4, fill-colour only (pattern untouched at 110/011/101 throughout).
- From baseline e($): 1 step-on -> % (=UPPER box target colour); reaching @ (LOWER box colour) = 3 step-ons from e (e->%->N->@) ... actually cycle order is 8->c->9->e so from e: e->8->c->9 = % then N then @ (3 steps to @, 1 step to %).
- On-cell read LAGS by ~1; the settled colour is the off-cell read (matches R-L5). Sampled ~8 step-ons across A1/A2 and A3/A4 approaches; both work; selector NEVER changed the pattern or triggered delivery (colour-only, like L3/L4/L5).
- LESSON (H11 reminder): coasted budget to 0 two cells from X-box (1,7) — (2,7) is plain floor, X-box only at (1,7), so no life-free refill reachable. Took a clean controlled overdraft death-respawn: block->L6 start (10,4), budget 0->42, %% 8 (12->8), panel reset to baseline, X-boxes restored. CONFIRMS start=(10,4) (O22) and C12 respawn. 2 lives spare now.

### Pattern speck (8,2) — PARTIAL/AMBIGUOUS (read-lag problem)
- Approached from (9,2)+A1. It is a position-permutation (rotation-family) transform like L5's Q.
- Observed orbit (with ~1-step read lag): 110/011/101 -> 101/011/110 -> 101/110/011 -> 011/110/101 -> ... -> (back to 110/011/101 after ~? applies).
- BFS over the 4 observed transition pairs leaves 8 candidate perms — NOT uniquely pinned. The panel read LAGS the speck step-on by ~1 turn, and neutral settle-moves cost budget, so clean per-apply reads are expensive.
- HAZARD HIT: burned budget to 0 twice during sampling -> 2 overdraft deaths -> %% now 4 (LAST LIFE). Block respawned to (10,4), panel reset to baseline 110/011/101.

### Speck (2,6) — NOT YET SAMPLED.

## PIVOT / DANGER (RM checkpoint)
- At %%=4 (LAST life): ANY plain overdraft = GAME_OVER = full restart (replay L1-L5 + re-clear L5). MUST refill proactively, never coast to budget 0 unless landing exactly on an X-box.
- The live-sampling-to-BFS approach (as used on L5) is TOO budget-hungry here given read-lag; need a budget-frugal sampling protocol: refill to 42, sample a control with MINIMAL moves, refill again before any leg risks 0.
- Decision: gather speck transforms with strict discipline (one X-box refill per few samples), reading on-cell after a long settle wait rather than via neutral moves.

## ★ CONFIRMED (RM crystallize candidate): L6 rotation speck = L5's Q (90° CW rotation)
- Offline check: L5's Q perm [6,3,0,7,4,1,8,5,2] reproduces my observed L6 speck orbit EXACTLY:
  110/011/101 → 101/011/110 → 101/110/011 → 011/110/101 → (back), period 4.
- => the L6 rotation speck IS the same 90° CW grid rotation as L5's (7,3) Q. Strong C14 transfer (a SECOND rotation-control instance).
- UNLOCK: Q² (rotation speck pressed TWICE) takes baseline 110/011/101 → 101/110/011 = the UPPER box PATTERN target exactly. Upper pattern needs NO BFS, NO 2nd speck — just 2 presses of the rotation speck.
- UPPER box colour-% = 1 selector press from baseline-e (e→%). So UPPER box = 2 rot-presses + 1 selector press + deliver. The CHEAP box.
- LOWER box target 101/001/111 is NOT in Q's orbit → needs pure speck P (unsampled) composed with Q (L5-style word). Sample P, then BFS {P,Q}.

## WM consult (wm-predict, RM→trace)
- Asked: rotation-speck transform identity, two-box delivery protocol, last-life-safe plan.
- DECISIVE on (1): WM/offline confirmed the speck = L5's Q (90° CW rotation). Strong positive thesis point (like L4/O19).
- (2) two-box protocol: NO precedent (L6 is first two-box level) — WM extrapolated: each box = own pattern+colour align + own delivery; panel likely RESETS after each delivery (C07 redraw+teleport); do UPPER first (cheaper). MEDIUM confidence, flagged speculative.
- (3) plan: never overdraft at %%=4; sample P frugally; solve UPPER first (Q²+selector%), confirm panel-reset, then BFS LOWER word.

## ★★ LIVE-CONFIRMED: L6 rotation speck (8,4) = Q (90° CW rotation), period 4 — same as L5's (7,3)
- Reliable sampling protocol (defeats the on-cell read LAG): A1-onto-speck, A2-off, then >=3 NEUTRAL settle moves (A4/A3 on row 9), THEN read. Each such cycle = exactly ONE Q application.
- Verified: baseline 110/011/101 --1 clean application--> 101/011/110 (= Q^1). Q orbit (period 4): 110/011/101 → 101/011/110 → 101/110/011 → 011/110/101 → back.
- The earlier "stuck"/"2=identity" confusion was the LAG + rapid A1/A2 oscillation miscounting applications. NEUTRAL-settle-then-read fixes it.
- UPPER box pattern target 101/110/011 = Q^2 (2 clean applications). CONFIRMED reachable by the rotation speck ALONE (no BFS, no pure speck) — pattern-axis for the upper box is trivial.

## ☠ DEAD-END (RM→trace): budget/lives co-depletion corner on L6 (forced restart)
- State: block (8,1), budget=3 (rate = 1/move on L6, measured 4->3), %%=4 (LAST life).
- BOTH remaining X-boxes ((1,1),(1,7)) are 7 moves away; (9,1) already consumed (single-use, H08).
- => NO reachable refill within budget. At %%=4 an overdraft = TERMINAL GAME_OVER (C12), so a death-respawn is NOT available. UNRECOVERABLE corner.
- ROOT CAUSE: spent 2 lives early on careless overdraft deaths during speck sampling (12->8->4), then consumed the (9,1) X-box, then drifted budget down far from the 2 surviving (top-row) X-boxes. Violated H11 (never let budget approach 0 without a reachable refill) compounded by being at the last life.
- DECISION: accept GAME_OVER + full restart (replay L1->L4, re-clear L5 via R-L5, capture L5.txt, then re-attack L6). The L6 knowledge below makes the re-attack fast.

## L6 KNOWLEDGE BANKED for the re-attack (all live-verified this session)
- Start (10,4). Panel baseline 110/011/101 colour-e ($). Budget rate 1/move, full bar 42. %% resets to 12 on level entry.
- X-boxes: (1,1),(1,7),(9,1) — SINGLE-USE per life. NOTE positions are top-heavy + (9,1); plan refills BEFORE leaving the bottom.
- Colour selector (5,5) [moves to (4,4) in some frames — read live]: cycle %→N→@→$ (8→c→9→e), period 4, colour-only. From baseline-e: 1 press→% (UPPER colour), 3 presses→@ (LOWER colour).
- Rotation speck (8,4): = Q, 90° CW rotation, perm [6,3,0,7,4,1,8,5,2], period 4. Protocol: A1-on, A2-off, >=3 neutral settle, read.
- Pure speck (2,4): color-0, transform UNSAMPLED (the open thread for the LOWER box word).
- UPPER key-box (7,10): target pattern 101/110/011 colour-% — pattern = Q^2 (2 rotation presses), colour = 1 selector press. CHEAP. Deliver 2-push (H09).
- LOWER key-box (10,10): target pattern 101/001/111 colour-@ — NOT in Q's orbit; needs {P,Q} word (sample P, offline BFS). colour = 3 selector presses (or fewer by order).
- Two-box: likely deliver each separately (panel resets between, C07). Do UPPER FIRST (cheaper, banks progress).
- REATTACK BUDGET PLAN: keep %% high (never overdraft); sequence controls to pass an X-box before any long leg; the right-side delivery corridor to (7,10)/(10,10) is far from X-boxes — enter it with a FULL bar (mirror R-L5 N52 logistics lesson).

## ★★★ MAJOR NEW MECHANIC (RM crystallize): L6 lock controls are MOBILE — they patrol/oscillate every turn
- Tracked over consecutive turns (block oscillating in place): EVERY turn advances the controls' positions:
  - ROTATION speck patrols ROW 8, cols 2..5, bouncing: (8,5)→(8,4)→(8,3)→(8,2)→(8,3)→(8,4)→(8,5)→... (period ~6, a back-and-forth).
  - PURE speck patrols ROW 2, cols 3..6, bouncing: (2,3)→(2,4)→(2,5)→(2,6)→(2,5)→(2,4)→(2,3)→...
  - COLOUR SELECTOR wanders rows 4-6 / cols 3-5: (6,3)→(5,3)→(4,3)→(4,4)→(4,5)→...→(6,5)→... (a roaming path; even briefly undetected at turn 664).
- The block also moves each turn (player action), so this is a PURSUIT/timing problem: to apply a control you must be on the cell the control occupies AT THAT TURN (or step onto where it will be). NOT stationary like L1-L5.
- THIS EXPLAINS: (a) pattern got corrupted Q²→Q³ mid-navigation (the rotation speck wandered onto my row-8 path); (b) selector presses missed (it had moved off the target cell); (c) the macro-coord "drift" between my earlier reads was the controls genuinely moving, not a sampling artifact.
- IMPLICATION: pre-planned speck-free routes are unreliable. Need to either (i) navigate ONLY on rows the specks don't patrol (avoid row 2 and row 8 except to catch the speck), or (ii) time interactions — step onto the control's cell on the turn it's there. The Q-transform itself is unchanged (still 90° CW rotation, +1 per genuine step-on).
- The earlier "clean baseline→Q¹→Q²→Q³" worked because I was AT (9,4) below the speck's row-8 patrol and A1 caught it when it was at (8,4); the "stuck at Q³" run = the speck had wandered so A1 onto (8,4) hit empty floor (no application).

## L6 control patrol PERIODS (deterministic) + safe-navigation insight
- Rotation speck: ROW 8, cols bounce 2↔6 triangle wave (…6,5,4,3,2,3,4,5,6…). NEVER reaches col 7+ → (8,7) and the col-7 corridor crossing of row 8 are SAFE.
- Pure speck: ROW 2, cols bounce 2↔6 triangle. (2,7+) safe.
- Selector: roams rows 4-6, cols 3-5 (irregular ~period 11). Catch it by being on its cell the turn it's there.
- COLOUR % was successfully set (panel colour now 8/% — selector caught during oscillation). Colour persists.
- Maze: col-7 is the vertical spine (R1-R9 open). Upper box (7,10) approaches: (6,10) above / (8,10) below. (6,10) reachable from the col-7 corridor via rows 5-6 WITHOUT entering rows 2 or 8.
- PLAN for UPPER box: (1) colour % [done]; (2) set pattern Q² by catching the rotation speck from row 9 (A1 onto (8,col) when speck is there); (3) navigate row9→col7→row5/6→(6,10) (avoiding rows 2,8 except the safe (8,7) crossing), deliver A2(DOWN) ×2 into (7,10).

## ★★★ BREAKTHROUGH: L6 UPPER-box ALIGNMENT fully achieved (pattern Q² + colour %) — mobile-control catch method WORKS
- The parity insight: on row 9, block_col + rot_col is INVARIANT odd → block can NEVER share a column with the row-8 speck from row 9 (so the naive "stand below, press up" catch is IMPOSSIBLE).
- WORKING CATCH: step the block ONTO row 8 (A1 from (9,C)); then the moving speck and block, both on row 8, CROSS and the catch fires as the speck steps into/through the block's cell. Pressing A1 onto (8,4) when speck approaches catches Q. Empirically: from baseline, stepping onto row 8 and oscillating A3/A4 caught Q TWICE → panel reached 101/110/011 = Q² = UPPER target.
- COLOUR %: the selector roams rows 4-6 (2D, so catchable — no parity trap). Pursue it (step toward its cell, avoid rows 2,8); landing on it advances the colour. From e, ONE catch → % (8). Confirmed: panel 101/110/011 colour-8 = full UPPER alignment.
- Alignment PERSISTS through navigation on rows 3-7,9 (just avoid the speck rows 2,8). Verified across many moves + an X-box refill (alignment held through the (1,7) refill).

## ★★ L6 HAS PORTALS (corrects O22 "no portals confirmed") — right side is portal-trapped
- Confirmed warps: (4,8)+A4 → (4,7); (4,9)+A2 → (4,7); (3,9)+A2 → (4,7). The entire upper-right region (cols 8-10, rows 3-5) warps the block BACK to col 7. drive.py is portal-BLIND on levels==5 (needs _PORTALS_L6).
- The UPPER box (7,10) cannot be reached from the TOP (every approach to col 10 via rows 3-5 portals back to col 7). Col 10 walkable rows: 5,6 (above box) and 8,9 (below box); row 7 col 10 = the box itself.
- OPEN: how to reach (6,10) [push DOWN] or (8,10) [push UP] — the box-adjacent cells — through the portal maze. Need to map the portal edges that LAND on col 10. This is the live delivery blocker (lock is SOLVED, alignment achieved).

## ★★★ POCKET ENTRANCE FOUND: (2,9)+A1(UP) → warp → (5,9) [the box column]
- The UPPER/LOWER key-box column (cols 9-10, the pocket {(4,9),(5,9),(5,10),(6,10),(8,10),(9,10)}) is portal-isolated: walls on col 9 + portals dump every top approach to (4,7). The ONLY entrance is the warp (2,9)+A1 → (5,9).
- Reach (2,9): col-7 spine up to (3,7) → (3,8) → (3,9) → (3,9)+A1 → (2,9) [all clean]. Then (2,9)+A1 → (5,9).
- From (5,9): A4 → (5,10); (5,10)+A2 → (6,10) [box approach, above upper box (7,10)]; A2 ×2 delivers DOWN into (7,10).
- Known L6 portals so far: (4,8)+A4→(4,7); (4,9)+A2→(4,7); (3,9)+A2→(4,7); (2,9)+A1→(5,9) [the useful one].
- FULL UPPER-BOX RECIPE (paper-complete): set pattern Q² (row-8 speck catch) + colour % (selector pursuit) → route to (2,9) avoiding speck rows → (2,9)+A1 warp to (5,9) → (5,10) → (6,10) → A2,A2 deliver. Budget plan: refill so the pocket-entry leg + 2 pushes have a full bar (the pocket has no X-box).

## ☠ DELIVERY ANOMALY: aligned block passes THROUGH the upper box (7,10) — no lock, no win
- With panel EXACTLY at the upper-box target (101/110/011 colour-%), pushed the block into (7,10):
  - from (6,10) DOWN: (6,10)→(7,10)→(8,10) — slid through, NO wedge, levels stayed 5.
  - from (8,10) UP: (8,10)→(7,10)→(6,10) — slid through again, NO wedge, NO win.
- So unlike L1-L5 (H09: 1st push wedges, 2nd enters → win), here the aligned block treats (7,10) as FLOOR.
- HYPOTHESES (two-box level): (a) the LOWER box (10,10, target 101/001/111 colour-@) must be delivered FIRST, or both in a specific order; (b) the win needs BOTH panels matched simultaneously (but there is ONE shared panel — so maybe deliver to one box "banks" it and resets, then the other); (c) the box accepts only a SPECIFIC approach/side not yet tried; (d) the displayed box target is which box to AVOID, or the two boxes are an XOR. 
- The lock ALIGNMENT method is fully solved; the WIN CONDITION for a two-box level is the open question. This is the "novel two-box delivery protocol" the WM flagged as unverified (O24/N56).
- State: budget 2, %%=12, alignment still held. Need to investigate delivery semantics (try LOWER box; try order; re-read both box glyphs for any 'open/closed' state difference).

## ★★ TWO-BOX WIN CONDITION DECODED: deliver BOTH boxes in ONE LIFE (a death restores both)
- Pushing the aligned block into the upper box (7,10) DID deliver it: the box frame DISSOLVED, (7,10) became floor, color-9 marked the top — the upper box is SATISFIED. But levels stays 5 until the LOWER box (10,10) is also delivered.
- CRITICAL: a death-respawn RESTORES both boxes (upper box frame came back after an overdraft death). So BOTH deliveries must happen WITHIN ONE LIFE, no death between. (Budget refills via X-boxes are fine; a death is NOT.)
- LOWER box (10,10): target pattern 101/001/111 colour-@. This pattern is NOT in Q's orbit (from baseline OR from the upper state) → it needs the PURE speck P (row-2 patroller, transform UNSAMPLED) composed with Q (an L5-style word, C14). Must sample P, BFS {P,Q} for the lower word.
- So L6 = the hardest yet: TWO sequential two-axis deliveries in one life over a mobile-control + portal-pocket maze. Upper recipe is solved; lower needs P sampled + word + its own delivery route (the lower box (10,10) approach: col 10 rows 8,9 below it — (9,10)+A2 into (10,10)? or via the same pocket).
- Plan next: sample pure speck P (row-2 cross-catch); BFS lower word; then one-life double-delivery with budget refills (upper first via pocket, then lower).

## Pure speck P — PARTIALLY sampled (transform NOT cleanly pinned)
- P patrols ROW 2 (cols 2-6), like the rotation speck patrols row 8. Catchable via the same row-cross method (step onto row 2, cross it).
- Observed (confounded) orbit fragments including a clean appearance of the LOWER TARGET:
  ...111/100/111 → 010/101/011 → 010/111/100 → 101/001/111 → 101/011/110...
  ⇒ the LOWER box target 101/001/111 IS reachable on the panel (good — the lower lock is solvable).
- P is NOT a position-permutation (BFS over perms = 0 candidates) and matches NO single/composite geometric op (rot/flip/transpose/not) on the cleanest A→B→C triple — likely because the samples are CONFOUNDED (lag + incidental rotation-speck catches during the multi-row navigation to reach P). Need a strictly rows-1-2-only clean sampling to isolate P (expensive; ran low on budget each attempt).
- OPEN: isolate P cleanly → identify its transform → BFS {P,Q} for the word baseline→101/001/111 (and the colour @ = 3 selector catches from e, or via the cycle).

## L6 STATUS SUMMARY (end of this session — UNSOLVED but deeply characterized)
SOLVED sub-problems: all mechanics (mobile controls + catch methods + portal pocket entrance + two-box-one-life win); the UPPER box delivery end-to-end (Q²+% → (2,9)+UP warp → (5,9)→(5,10)→(6,10)→push into (7,10), box dissolves = delivered).
OPEN: (1) isolate/identify the pure speck P transform; (2) BFS the LOWER word to 101/001/111; (3) the LOWER box delivery route (box (10,10), approached from (9,10)+A2 — needs its own pocket/portal route check); (4) execute the ONE-LIFE DOUBLE delivery (upper then lower) with X-box refills, no death between (a death restores both boxes). Budget logistics + mobile-control catches make this the hardest level by far.
TOOLS built: scratchpad/l6.py (state/catch helpers), scratchpad/l6solve.py (goto/set_pattern_Q2/set_colour_pct/deliver_upper — upper-box solver, all proven).

## ===== SESSION 2026-06-29 (#11) — replay re-climb + L5.txt capture + L6 re-attack =====

### Phase 1 DONE: replay L1->L4 clean, L5 re-cleared + L5.txt CAPTURED
- replay/replay.py L1 L2 L3 L4 = all CLEARED clean (levels 0->4), turn-advancing throughout (harness alive).
- L5 had NO replay file. Re-cleared via R-L5 and captured the verbatim winning action list into replay/L5.txt (56 actions).
- L5 LOGISTICS were again the hard part (N52 confirmed AGAIN): TWO controlled overdraft deaths during the QQ phase
  (lives 12->8->4) before a clean run. Root causes, now sharpened:
  (a) Routing to X-boxes / the pocket CROSSES the row-2 P speck (2,3) and row-7 Q speck (7,3), re-applying their
      transforms in transit and corrupting the pattern. FIX: do COLOUR FIRST (pocket leg never needs row-2/7 specks),
      then set pattern PP@(2,3) then QQ@(7,3) LAST, and route speck-avoiding (plan_avoid walls the speck cells).
  (b) READ-LAG on the rotation (Q) speck makes mid-sequence panel reads overshoot the application count. FIX: count
      APPLICATIONS (one on->off cycle = exactly one Q), do NOT re-read between Q steps; verify only at the very end.
      Also: even the speck-avoiding goto to (7,4) crosses (7,3) ONCE (the approach cell is adjacent), applying a stray
      Q — so budget for "QQ" was really "1 transit-Q + 1 explicit Q". Watch the settled panel and apply Q until target.
- FINAL clean L5 run (on the LAST life, %%=4): colour % via pocket (2,6)+A1->(5,6), 3 catches, exit (5,6)+A1->(4,8);
  PP@(2,3) -> 110/011/101; then to (7,4) [1 transit-Q] + 1 explicit Q -> 101/110/011 TARGET colour %; deliver route
  (3,10) via (9,10)+A2->(2,10) portal; A1,A1 -> WIN, levels 4->5. Block teleported to L6 start (10,4), %% reset 12.

### L6 RE-ENTRY confirmed (matches banked O22 + raw): start (10,4), panel baseline 110/011/101 colour-e($), budget 42, %%=12.

### L5.txt REPLAY CAVEAT
- L5.txt was recorded from the death-respawn fresh-start (8,9) = the same cell as fresh L4-exit entry, so it is valid
  from a fresh L5 start. It includes the proactive X-box refills and portal warps used live. Future restarts should run
  replay/replay.py with the L5 leg and --verify; if the maze RNG/portal layout differs it may need a live re-solve via R-L5.

## ===== SESSION 2026-06-29 (#11 cont) — L6 one-life double-delivery: UPPER delivered + LOWER mechanics cracked =====

### ★★★ BREAKTHROUGH (live-verified): the two-box delivery is a SEQUENTIAL one-panel realign, and delivering UPPER UNBLOCKS the LOWER route
Executed live this session (from a fresh %%=8 life):
1. UPPER aligned (Q² pattern 101/110/011 + colour % via selector pursuit) — note: the selector pursuit on rows 4-6
   CROSSES the rotation-speck row and corrupts Q (Q²→Q¹); fix = re-run set_pattern_Q2 AFTER colour. Refilled at (1,7)
   preserving alignment (avoid_rows=(2,8)).
2. Entered pocket (2,9)+A1→(5,9); (5,9)→(5,10)→(6,10); pushed A2(DOWN): (6,10)→(7,10)→(8,10). UPPER box DISSOLVED
   (7,10) is now plain floor (color-3). levels stayed 5.
3. ★ PANEL PERSISTS: after the UPPER box dissolved the shared panel STAYED at 101/110/011 colour-% — it did NOT reset.
   (Confirms the WM-predict answer (a): only a win-redraw/death resets the panel; a partial delivery does not.)
4. ★ DELIVERING UPPER OPENS COL-10: with (7,10) dissolved, col 10 is now connected (6,10)↔(8,10)↔(9,10); BFS from
   (8,10) reaches 68 cells incl. (9,10) [the LOWER-box approach] AND the pocket exit back to (5,9)/(2,9) and the specks.
   BEFORE delivery (8,10)/(9,10) were portal-isolated/unreachable — so the UPPER delivery is the KEY that unlocks the
   LOWER delivery geometry. ⇒ ORDER IS FORCED: UPPER must be delivered before LOWER (LOWER box (10,10) is reached only
   from (9,10)+A2, and (9,10) is only reachable after (7,10) dissolves).
5. LOWER target = pattern 101/001/111 colour-@. Set colour @ live (selector cycle from %: %→N→@ = 2 catches; colour-only,
   pattern untouched) — DONE, panel 101/110/011 colour-@.

### Pure speck P — transform PARTIALLY MAPPED (clean catch method FOUND)
- ★ CLEAN P-CATCH METHOD (defeats mobility+lag): park block oscillating (2,1)↔(2,2) [A4 right at (2,1) / A3 left at (2,2)].
  P patrols row 2 cols 2-6 (triangle). Each time P walks INTO (2,2) while the block sits there, the catch fires = ONE P
  application; the panel changes and `pure` reads None that step. So: oscillate and watch for panel CHANGE; each change =
  exactly one P application. Refill at (1,1) (right above row 2) keeps it funded.
- Observed P transitions (a→P(a)), clean chain: 010/101/011→010/111/100→101/001/111→101/011/110→100/111/100 ; plus
  110/011/010→101/100/111. ⇒ the LOWER target 101/001/111 IS a P-orbit state (good), reachable as the P-successor of
  010/111/100. P is NOT a position-permutation (bit-count varies 5,5,6,6,5) — a genuine period-6 state map, not a geometry.
- OPEN: P's full closed 6-cycle (one transition still missing: 100/111/100→? and how 110/011/010 fits) — needed to BFS the
  exact catch-count from the post-UPPER panel 101/110/011 to 101/001/111. Practically: just oscillate-catch live and STOP
  the instant the panel reads 101/001/111 (it cycles through all 6 states incl. target).

### ☠ BUDGET corner again (forced death pending): stranded at (2,2) budget 0, only (9,1) X-box left (8 moves), %%=8.
- ROOT: consumed (1,1)+(1,7) on UPPER-align + colour-@ + P-mapping; the P-mapping oscillation + refill-traversals are
  budget-hungry, and the 3 single-use X-boxes are top-heavy ((1,1),(1,7)) + (9,1). Forced overdraft death → %% 8→4 (LAST life).
- NEXT-LIFE PLAN (the whole thing is now characterized; needs a tight budget-funded execution):
  (i) On a fresh life: set LOWER pattern 101/001/111 FIRST (oscillate-catch P at (2,1)↔(2,2), refill (1,1), stop AT target),
      then colour @ (2 selector catches from baseline... actually baseline colour is e: e→%→N→@... compute live), giving the
      LOWER panel WITHOUT having touched col 10 yet. BUT the LOWER box can't be delivered until UPPER dissolves, and UPPER
      needs a DIFFERENT panel — so LOWER-first alignment is wasted (panel is shared). ⇒ ORDER: UPPER align→deliver (opens
      col10, panel persists)→realign LOWER (P-catch + colour @)→route (8,10)→(9,10)→A2,A2 into (10,10). All ONE life.
  (ii) BUDGET: save (9,1) for the final LOWER leg (it's near row 9 / col 10). Spend (1,1),(1,7) on UPPER-align + the
       post-delivery LOWER P-catch. The realign-LOWER P-catch happens at row 2 (top), far from (9,1) — so refill (1,1)
       BEFORE the P-catch, then traverse to (9,1) area / down col-10 to (9,10) on the saved (9,1) refill. Tight but feasible.

## ★★★ KEY NEW FINDING (turn 12, end): the pure speck P has MULTIPLE period-6 ORBITS → LOWER pattern NEEDS a {P,Q} WORD (not a single P-catch)
- Mapped two DISJOINT P-cycles this session:
  - ORBIT A (contains LOWER target): 010/101/011 → 010/111/100 → 101/001/111 → 101/011/110 → 100/111/100 → (…→ back)
  - ORBIT B: 111/101/101 → 010/101/110 → 110/011/010 → 101/100/111 → (…→ back)
- The post-UPPER panel 101/110/011 sits in NEITHER (catching P from it lands in ORBIT B, NOT the target orbit A).
- ⇒ reaching the LOWER target 101/001/111 from the post-UPPER state requires a {P,Q} WORD: use Q (the rotation speck)
  to bridge into orbit A, then P-catches to the target — exactly the C14 composed-controls mechanic, NOT a single
  P-catch. This is BUDGET-HEAVIER than the single-orbit P-catch I had planned, which is WHY the one-life double-
  delivery overran the budget: align UPPER + deliver UPPER + (Q-bridge + P-word for LOWER) + deliver LOWER exceeds
  what L6's 3 single-use top-heavy X-boxes ((1,1),(1,7),(9,1)) fund in one life at 1 budget/move.
- NEXT SESSION: BEFORE playing, OFFLINE-BFS over {P (both orbits' transition tables), Q (perm [6,3,0,7,4,1,8,5,2])}
  from 101/110/011 (post-UPPER) → 101/001/111 to get the exact minimal word; map P's two orbits COMPLETELY first
  (oscillate-catch (2,1)↔(2,2), refill (1,1), record till each cycle closes). THEN execute the one-life run with the
  precomputed word so no exploratory budget is wasted mid-run. Save (9,1) for the col-10 LOWER delivery leg.

## ☠ DEAD-END (turn 12): one-life double-delivery LOST to budget on the LOWER realign (N57-class, %%=4)
- UPPER box delivered cleanly on the last life (%%=4). But the LOWER realign (Q-bridge + P-word + colour @) plus the
  return to (9,10) overran budget: burned (1,1)+(1,7) on UPPER + colour-@ + the P-catch exploration, leaving only
  (9,1) (8 moves away) unreachable at budget 6. Stranded (6,1) budget 1, %%=4 → forced GAME_OVER imminent.
- ROOT: exploratory P-mapping mid-run (didn't yet know P had multiple orbits / needed a word) consumed the budget that
  the LOWER delivery needed. FIX = precompute the LOWER word OFFLINE (above) so the live run spends zero budget exploring.
- L6 remains UNSOLVED. Everything is now characterized EXCEPT the exact LOWER {P,Q} word; the one-life execution is a
  pure logistics problem with a known recipe shape. The harness will need a restart (replay L1→L4, re-clear L5 via
  R-L5/L5.txt, re-attack L6 with the precomputed word).


## ===== SESSION 2026-06-29 (#13) — P SOLVED OFFLINE, LOWER word computed =====

### P's TRUE transform: a SINGLE period-6 cycle (orbit B), SINGLE-catch verified live
- Earlier "multiple disjoint period-6 orbits" AND "single period-7 cycle" reads were BOTH confounds
  (read-lag + multi-apply per oscillation in BATCH sampling). The clean single-catch map (one `l6_lower.py p 1`
  = exactly one verified before->after) is:
  ORBIT B (period 6, closed): 010/110/011 -> 111/001/101 -> 110/011/101 -> 010/010/111 -> 101/101/111 -> 011/101/010 -> (back)
  P is this state-map (NOT a position-perm; bit-count varies). Baseline 110/011/101 is IN B (index 2).
- DECISIVE STRUCTURE: Q (90 CW rot perm [6,3,0,7,4,1,8,5,2], period 4) maps EVERY orbit-B state into the
  LOWER orbit; in particular Q(111/001/101) = 101/001/111 = the LOWER TARGET exactly. Orbit B and the LOWER
  orbit are Q-CONJUGATE; LOWER = Q(an orbit-B state). Cleanest C14 instance: Q bridges P's orbit to the target's.

### OFFLINE WORDS (BFS over {P-cycle-B, Q}) -- zero-exploration for the live run:
- UPPER pattern: Q^2 from baseline 110/011/101 -> 101/110/011 (UPPER target). 2 Q-catches.
- LOWER pattern from POST-UPPER persisted panel 101/110/011 -> LOWER 101/001/111:
    WORD = QQPPPPPQ (3 Q + 5 P = 8 catches; minimal in length AND row-switches=2).
    trace: 101/110/011 -Q-> 011/110/101 -Q-> 110/011/101 -P-> 010/010/111 -P-> 101/101/111 -P-> 011/101/010
           -P-> 010/110/011 -P-> 111/001/101 -Q-> 101/001/111
- Colours: UPPER % = 1 selector catch from e; LOWER @ = %->N->@ = 2 selector catches from %.

### Budget ledger (one life; 3 single-use X-boxes (1,1),(1,7),(9,1); 42 @ 1/move):
- Total work ~110-114 moves vs 168 available (initial 42 + 3 refills). Fits on TOTAL; binding constraint is
  refill GEOGRAPHY: LOWER P^5 leg is row 2 (refill only (1,1)); Q legs row 8; delivery (9,10) (refill only (9,1)).
  Save (9,1) for the final col-10 LOWER delivery. Selector pursuit CORRUPTS Q (crosses row 8): set colour
  BEFORE building each pattern word, re-catch Q if needed.
- LESSON reconfirmed: do NOT batch-catch P (multi-apply confound); single-catch + verify each application.
- NOTE on RESET: on L6, `play.py send RESET` REFRESHES THE CURRENT LEVEL (block->L6 start (10,4), panel baseline,
  lives 12, budget 42, X-boxes + both key-boxes restored) and KEEPS levels_completed=5 -- it does NOT drop to L1.
  So no L1->L5 replay is needed to retry L6. (Resolves the C02 RESET-semantics conflict in favour of per-level refresh.)


## ===== SESSION 2026-06-29 (#13 cont) — L6 SOLVED (levels 5->6), ONE LIFE, ZERO DEATHS =====

### ★★★ L6 CLEARED. Both boxes delivered in one life; lives stayed 12 throughout (no deaths).
Final clean run (after the offline P solve), exact sequence:
1. UPPER: set pattern Q^2 (catch row-8 rotation speck twice) -> 101/110/011; set colour % (selector pursuit,
   corrupts Q->Q^1); RE-catch Q to restore Q^2; refill (1,7); deliver via pocket warp
   (2,9)+A1->(5,9)->(5,10)->(6,10)->A2,A2 -> UPPER box (7,10) DISSOLVES, block slides to (8,10),
   panel PERSISTS at 101/110/011 colour-%, levels still 5.
2. LOWER: colour @ FIRST (selector, %->N->@ = 2 catches; pattern untouched this time) -> panel 101/110/011 col-@.
   Pattern word from post-UPPER = QQPPPPPQ (offline-BFS over {P-cycle-B, Q}):
     - QQ (catch row-8 Q twice) -> 110/011/101 ; refill (9,1) [block lands row 9 after QQ].
     - P^5 (catch row-2 pure speck 5x, INTERCEPT method = cheap ~1-5 moves/catch) -> 111/001/101.
     - refill (1,1) immediately (block at (2,2), (1,1) 2 moves) -> FULL bar for the finale (THE KEY FIX).
     - final Q (descend to (9,4), step up onto row 8, catch once) -> 101/001/111 = LOWER TARGET.
3. DELIVER LOWER: route to (2,9) [P/Q-speck-safe: row2 col>=7], warp (2,9)+A1->(5,9)->(5,10)-> descend col-10
   (now unblocked by the UPPER dissolve) to (9,10) -> A2 push into (10,10) -> FULL REDRAW, levels 5->6.
   Block teleported to L7 start (3,3), panel reset, budget->42, lives stayed 12.

### Key tooling fixes that made one-life feasible (vs prior budget-lost runs):
- P FULLY KNOWN OFFLINE (orbit B period-6) => ZERO in-run P exploration (the prior run-killer).
- IMPROVED P-catch = intercept the speck at its CURRENT column (move toward it on row 2) instead of parking at
  (2,2) and waiting => ~1-5 moves/catch (was ~8). scratchpad/l6_lower.py catch_P_once.
- Final-Q catch done by descending to row 9 then ONE step onto row 8 (the catch fires immediately) ~1 move.
- Refill ORDER (the decisive logistics fix): (1,7)=UPPER; (9,1)=after-QQ (block on row 9); (1,1)=right after P^5
  (block on row 2) so the final-Q + 12-move pocket delivery run on a FULL 42 bar. Save NOTHING for "later" past (1,1).
- LOWER delivery MUST use the (2,9)+A1->(5,9) pocket warp; the naive BFS routes into the (4,8)/(4,9) portals that
  bounce back to col 7 (a dead-end that killed an earlier run). col-10 walkable rows 5-9 after UPPER dissolves.

### HAZARD re-confirmed: any navigation crossing row-8 cols 2-6 re-applies Q (corrupts the pattern). After the
final Q, route to (2,9) avoiding row-8 cols<=6 and row-2 cols<=6 (the P speck). Both specks patrol cols 2-6 only;
col 7+ on either row is SAFE.

### RESET semantics (re-confirmed, resolves C02 conflict): on L6 `play.py send RESET` REFRESHES THE CURRENT LEVEL
(block->L6 start, panel baseline, lives 12, budget 42, X-boxes + both key-boxes restored), KEEPS levels_completed=5.
Used RESET repeatedly to get clean L6 retries with full lives -- no L1->L5 replay needed.


## ===== L7 RECON (entered after the L6 win; UNSOLVED) =====
- Entry: block (3,3), panel BASELINE 010/010/111 colour-c, lives 12, budget 42, budget rate ~1/move.
- NEW MECHANIC: L7 is a PORTAL-and-FOG REVEAL maze. The board is mostly COLOR-5 ("fog"/unexplored). The
  block reveals floor/walls as it moves; color-5 cells are NOT uniformly walkable — most read as fog and
  resolve to floor (3) or wall (4) once approached. The playable area is fragmented into PORTAL-CONNECTED
  regions, not one contiguous maze.
- Confirmed portal: (5,7)+A1(UP) -> (8,7) [a warp to a new region, revealing rows 4-10 cols 5-10].
- X-boxes seen: (1,1),(4,5) [top-left region], (1,9) [revealed later, in a different region].
- Top-left region (rows0-6 cols0-6) maze mapped (block start (3,3)); a 2nd region (rows4-10 cols5-10) reached
  via the (5,7)+UP portal. NO key-box, lock controls, or specks located yet in either region — they are in
  still-unrevealed portal regions.
- A transient color-8 glyph flashed at ~(10,5) during reveal (could be a key-box target drawn in colour-8 / %,
  like L5) — UNCONFIRMED (re-read as fog).
- STATUS: L7 UNSOLVED — needs systematic portal-network mapping to locate the key-box + lock controls before any
  solve. Stopped at budget ~6 in the (5,10) region (X-box (1,9) is in another region, not directly reachable).
  No deaths; lives 12. This is a deep multi-region exploration level; the L1-L6 Locksmith recipe (read target ->
  align panel -> deliver) presumably still applies once the controls/box are found, but the OBSTACLE class is the
  new portal-fog reveal. Max level reached this session: 6 (L7 in progress).
- OPEN for next session: build a portal-network map (probe each region's edges for warps), find the key-box +
  controls, then apply the standard align+deliver loop. Budget logistics across portal regions will be the difficulty.
