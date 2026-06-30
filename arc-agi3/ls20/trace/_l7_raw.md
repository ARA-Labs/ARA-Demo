# L7 raw notes (live play, 2026-06-29/30)

L7 = fog-of-war REVEAL maze, large ROTATED (diamond, ~45°) maze. Board mostly color-5 fog;
a viewport of floor(3)/wall(4) is revealed AROUND the block and moves with it.

## Pinned facts
- Block start (3,3). Panel baseline 010/010/111 colour-c (N).
- Budget rate = **2/move** (L7; L6 was 1/move). Full bar 42 = 21 moves.
- %% lives reset 12 on entry. Overdraft respawns to (3,3), refill 42, %%-4 (12->8 confirmed).
- X-boxes seen: (1,1) [scr r6-8 c9-11], (4,5) [scr r21-23 c30-32], (1,9) [scr r6-8 c50-52]
  AND a 2nd near (1,7) [scr r6-8 c40-42] in the right region. Single-use per life.
- Confirmed portal (O26): (5,7)+A1->(8,7).
- HAZARD/CLUE: first UP from (5,10)->(4,10) CHANGED panel 010/010/111 -> 100/111/100.
  Suggests a control (pattern speck) at/near (4,10) or (5,10) in the right region. Panel then
  stayed 100/111/100 for subsequent moves up col-10. NEEDS single-catch sampling (C10).

## PINNED CONTROL #1 (single-catch, C10) — speck (8,3) [left region]
A period-6 NON-permutation cycle P' (same P-family as L6, shares states with L6 orbit-B):
  010/010/111 -> 101/101/111 -> 011/101/010 -> 010/110/011 -> 111/001/101 -> 110/011/101 -> (back)
Step on from (8,2)+A4; off via A3; settled read is stable off-cell (no lag observed here).
States 010/110/011, 111/001/101, 110/011/101 ALSO appear in L6's P orbit-B.

## Q control (right region, hint not yet single-catch-confirmed)
(5,10)->(4,10) move changed panel 010/010/111 -> 100/111/100 = EXACTLY Q-rotation
perm [6,3,0,7,4,1,8,5,2] applied to baseline. Q likely lives near (4,10)/(5,10) right region.

## X-box ledger (single-use/life): (1,1),(4,5),(9,2)[left] + (1,7),(1,9)[right]. (9,2) CONSUMED this life.

## STATE 2026: %%=8->will overdraft to 4 (last life) to refill; budget was 12 stranded in (8,2) pocket.

## ★ RESET IS LEVEL-LOCAL ON L7 (confirms N60, resolves C02 contradiction) ★
From %%=4 budget42 levels=6, `play.py send RESET` -> block back to (3,3), %%=12, budget 42,
panel baseline 010/010/111, levels_completed STAYS 6 (NO drop to L1). So L7 has UNLIMITED safe
retries via RESET-before-%%=0. The old N41 "RESET restarts whole game" reading does NOT apply
here (L6/L7 RESET is level-refresh). This removes the one-life pressure for MAPPING.
DISCIPLINE: still never let an overdraft happen at %%=4 (terminal); RESET at %%=8 to be safe.

## FOG VIEWPORT: deterministic per block-position. Re-entering (3,3) reveals the SAME start
region (cols 0-6). Reveal radius ~±4 macro cells around block. Cannot hold a global map; sense locally.

## REGION MAP (macro, accumulated via scratchpad/l7acc.py -> l7_globalmap.json)
- LEFT/START region cols 0-5: block start (3,3); X-boxes (1,1),(4,5); P' speck patrols ~row8 (caught at (8,3)).
- CENTER cols 5-7: floor pocket; PORTAL (5,7)+A1 -> (8,7) [confirmed] links center->right.
- RIGHT region cols 8-11: vertical corridor rows 1-10; X-boxes (1,7),(1,9); lower pocket (10,10)X;
  Q mobile speck patrols col 10 (caught at (6,10): panel 010/010/111->100/111/100 = Q rotation EXACTLY).
- Both P' and Q specks are MOBILE (seen at multiple cells across frames) -> C15 mobile controls.

## CONTROLS CONFIRMED (2):
- P' = speck patrolling left ~row8 (P-family period-6, mapped above).
- Q = speck patrolling right col-10 (90deg CW rotation, perm [6,3,0,7,4,1,8,5,2]).

## STILL MISSING (key blockers): COLOUR SELECTOR (compound 9/e/8/c glyph) + KEY-BOX(es) + target(s).
Candidates to explore: (1,7) pocket top-center; bottom-of-diamond ~(10,5) [O26 saw transient color-8];
left-bottom rows 9-11 cols 0-4. Likely multi-box (C15) given two regions + two pattern controls.

## COLOUR SELECTOR LOCATED + CONFIRMED: (8,1) left region. Compound glyph inner 9ee/908/cc8.
One step-on c(N)->9(@); pattern untouched; colour persists off-cell. Same 4-state cycle N->@->$->%.

## 6 X-BOXES this level (single-use/life): (1,1),(1,7),(1,9),(4,5),(9,2),(10,10). RESET restores all.

## PORTALS found: (5,7)+A1->(8,7) [center->right]; (5,6)+A2->(2,6) [center loop, up-warp].
Center pocket (cols5-7 rows2-8) is portal-rich; col-6 is a (5,6)->(2,6) loop.

## ★★ KEY-BOX IS NOT REVEALED ANYWHERE ★★ Full-frame glyph histogram (rows0-59) = ONLY
fog(5)/floor(3)/wall(4)/specks(0,1)/one X-box(b)/block(9,c)/selector(e). NO color-8(%), NO large
color-9 @ target. So the key-box(es) + target(s) are FOG-GATED behind an un-traversed portal.
Explored the full RING (left/center/right/top/bottom); key-box likely behind a portal INTO the
central wall-mass or a far pocket. THIS IS THE BLOCKER. Next: systematic 4-dir portal probe from
ring cells adjacent to the central mass.

## PORTALS found (all originate in/near CENTER pocket): 
- (5,7)+A1 -> (8,7)  [center -> right region]
- (5,7)+A2 -> (6,5)  [center loop]
- (5,6)+A2 -> (2,6)  [center up-loop]
- (7,7)+A1 -> (6,5)  [center loop]
Right-corridor lower cells (8,8)/(8,9)/(9,9)/(9,10)/(10,9)/(10,10): NO down-warp (all normal/wall).
Left-region lower cells (7,2)/(7,3)/(8,2)/(8,3): NO portal.

## KEY-BOX HUNT STATUS: a lone color-8(%) cell at (10,5), bottom-center, fog-gated. Adjacent floor
(10,4) only; (9,4),(9,5)[dead-end],(10,3),(10,6) walls -> ISOLATED POCKET reachable ONLY via an
UN-FOUND portal. WM (grounded): target colour = % (color-8 = % on L5/L6); entrance likely a DOWN-warp
from a center col-5/7 cell. Probed center col5/7 + right corridor + left lower: entrance NOT yet found.
REMAINING untested: center (6,6)/(6,7)/(7,6) all-dirs; (4,6)/(4,7)/(2,7) down; whether a RIGHT->center
return portal opens a new half; whether key-box reveals only after lock-align.
NOTE: color-8 at (10,5) is a SINGLE cell (not the usual 3x3/plus key-box) — may be a target MARKER,
the real 3x3 key-box may be adjacent in fog at (10,4).

## ★ KEY-BOX POCKET IS UNREACHABLE FROM {left,center,right} — likely LOCK-GATED ★
EXHAUSTIVE portal probe (l7try.py/l7portal.py) of center (5,6/5,7/6,5/7,5/7,7/4,6/6,6 dirs),
right-corridor lower, left-lower, right-top: NO warp lands in (10,4)/(10,5). All center portals
loop within {center, (2,6), right via (8,7)}. The right region's only distinct exit is (8,7);
its bottom (10,10) is sealed.
TESTED: setting colour-% alone does NOT open the (9,5)->(10,5) wall (still wall/no-op all dirs).
HYPOTHESIS (next session): the key-box pocket opens only when the LOCK IS ALIGNED (C07 "walled-shut
key-box becomes enterable", extended to fog) — but the PATTERN target can't be read until the box
reveals (chicken-and-egg). To break it: try aligning a GUESSED pattern target. Candidate targets to
try (from the controls' reachable states + colour-%): the color-8 marker at (10,5) suggests target
COLOUR=%; PATTERN unknown. Possibly the pocket is gated by a DIFFERENT cell's portal that activates
post-align, OR there is an un-probed portal in the upper region (rows 0-2 / (1,7) pocket / top `?` cells)
NOT yet tested. Also untested: P'/Q pattern-set effect on pocket wall; the (1,7) X-box pocket interior.

## 2026-06-29/30 SESSION 2: re-climbed L1->L5 via replay (verbatim, clean) then SOLVED L6 live
via the R-L6 recipe (l6solve.py UPPER + l6_lower.py LOWER), ONE life, zero deaths:
UPPER pattern Q2 (5 mv) -> colour % (corrupted Q->re-catch Q -> 101/110/011 col-%) -> refill (1,7)
-> deliver (2,9)+A1->(5,9)->(5,10)->(6,10)->A2,A2 box (7,10) DISSOLVED, block->(8,10), panel persists,
col-10 unblocks. LOWER colour @ FIRST -> QQ (110/011/101) -> refill (9,1) [manual 2 steps; goto minb
floor blocks at low budget, drive X-box approach by hand] -> P^5 (111/001/101) -> refill (1,1) -> final
Q (101/001/111 = LOWER target) -> deliver (2,9)+A1->(5,9)->(5,10)-> col-10 descend (9,10) -> A2 into
(10,10) = FULL REDRAW, levels 5->6. Now on L7 (block (3,3), panel baseline 010/010/111 col-c, budget 42,
lives 12). Harness self-managed: setsid absent on macOS -> use nohup+disown; spawned clean once, no respawns.

## ★ WM-PREDICT consult (LEAD) on the L7 chicken-and-egg pocket — hypothesis to test live ★
Question: how does the portal-isolated (10,5) key-box pocket open? WM answer (coverage in-artifact, grounded
in C15 L6-win + N72 + N62/N66): **L7 is a MULTI-BOX level (C15); the (10,5) marker is the SECOND/final box;
the pocket opens when a FIRST, already-reachable box is DELIVERED (its frame dissolves -> unblocks the wall
guarding (10,5)) — NOT by colour-% alone (ruled out N72).** Ranked tests:
 (1) Treat (10,10) [recon glyph-classified "X" but identical macro-coord to L6's LOWER key-box; right region
     replicates L6's (2,9)+A1->(5,9)->col-10 portal template] as the FIRST key-box: read its target adjacent,
     align {P',Q}+colour to it (offline-BFS word, C14), deliver via col-10 -> watch (9,5)/(10,6)->(10,5) walls
     dissolve. Confirmer: delivery dissolves (10,10) AND a (10,5)-adjacent wall becomes floor.
 (2) If (10,10) is a true X-box (step = refill, no dissolve): align a GUESSED full target = colour-% + each
     of P''s 6 pattern states, re-test (10,5) walls after EACH (C07-in-fog; colour-only is dead).
 (3) Derivable-target shortcut: target = the P'-state at which the wall dissolved; confirm via revealed (10,5) @.
 Speculative leap: (10,10)=first-box (vs X-box) — recon read color-b as X; resolvable in ONE free RESET test.
 Confidence med-high on mechanism (C15), medium on (10,10)-specifically. Falsifier: deliver a reachable box ->
 (10,5) walls all stay no-op AND levels stays 6 -> C15-opener wrong, fall to (2).

## ★★ BREAKTHROUGH 2026-06-30: L7 KEY-BOX TARGET READ + pocket is LOCK-GATED (C07-in-fog), NOT multi-box ★★
WM-led recon resolved the chicken-and-egg:
 - (10,10) is a plain X-box (hist {3:17,b:8}, step=refill, no dissolve) — NOT the first key-box. WM path-1
   (multi-box, (10,10)=first-box) REFUTED. Full-frame scan: only ONE color-8 marker exists (fog-gated (10,5)).
 - The (10,5) "lone color-8 cell" is actually a READABLE 3x3 TARGET rendered 1px/cell, partly fog-masked.
   Decoded from raw pixels (rows 51-53 cols 30-32, '8'=on): 8.8/88./.88 = **TARGET PATTERN 101/110/011 colour-% (8)**.
   (Same state as L5 target / L6 UPPER target; in the {P',Q} reachable space.)
 - The pocket gate is (9,5)->(10,5) [block reachable to (9,5), 12-mv route from (3,3)]. At baseline-pattern+colour-%
   AND at 101/101/111+colour-%, A2 into (10,5) = NO-OP (gate closed). Confirms C07-in-fog: gate opens only when
   panel==target (pattern 101/110/011 + colour %), NOT colour-alone (N72 re-confirmed).
 - P' patrols a TINY 2-cell row-8 corridor cols 2-3 (walled col4, selector col1) -> deterministic catch by
   crossing (8,2)<->(8,3). Colour selector (8,1): cycle N->@->$->%, colour PERSISTS off-cell & across pattern.
 - OFFLINE BFS over {P'(period-6 cycle), Q(rot perm [6,3,0,7,4,1,8,5,2])} from baseline to 101/110/011:
   shortest word = **PPPPPQQ** (24 reachable states; minimal). Trace:
   010/010/111 -P->101/101/111 -P->011/101/010 -P->010/110/011 -P->111/001/101 -P->110/011/101 -Q->101/011/110 -Q->101/110/011.
 - PLAN: colour-% + word PPPPPQQ -> panel 101/110/011 col-% -> goto (9,5) -> A2 into (10,5) = DELIVER -> L7 WIN.
   WM role: its C07-in-fog "align a guessed/derivable target dissolves the pocket" hypothesis was CORRECT; the
   refinement (target is READABLE not guessed) came from decoding the marker as a 1px 3x3. Tooling: scratchpad/
   l7nav.py (map+portal-aware nav), l7pocket.py/l7p2.py (colour-% + deterministic P'-catch + gate test).

## ★★★ L7 SOLVED — levels_completed 6→7, state=WIN. GAME COMPLETE 7/7. (turn 742, one life, zero deaths) ★★★
Executed the plan: colour-% (selector 8,1) → P⁵ at (8,2)↔(8,3) corridor → panel 110/011/101 → travel right
(refill (4,5), warp (5,7)+A1→(8,7), refill (1,9)) → QQ on col-10 ((1,9)→A4→(1,10) Q#1 → A2→(2,10) Q#2) →
panel 101/110/011 col-% = TARGET → Q&P-safe 12-mv route (2,10)→(9,5) → A2 push into (10,5) = 284-cell redraw,
WIN. WM's C07-in-fog hypothesis CONFIRMED (gate opens iff panel==target; colour-alone dead). Budget was the only
constraint (single-use X-boxes; RESET-level-local gave free retries during the catcher debugging). Tooling:
scratchpad/l7solve.py (colour/p/q/deliver phases), l7nav.py (fog+portal-aware nav), l7pocket.py/l7p2.py (test).

## L7 RECON (historical) — completed; pocket entrance was the lone blocker, now resolved (lock-gated, target read).

## Open threads
- Locate key-box(es) + targets; locate all controls; map portal network; is it multi-box (C15)?
- The right region (cols 7-11) and left/start region (cols 0-5) connect via fog/portals — map.
