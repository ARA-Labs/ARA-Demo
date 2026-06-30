# Claims — ls20 mechanics, win condition, transfer

Crystallized current-best claims. Numbers live in `Proof`/`Sources` (grounded against the
episode log `harness/runs/ls20-9607627b_ccrelay.jsonl`), never in `Statement`. History lives
in `trace/`.

## C01: ls20 is a block-navigation (sokoban/Locksmith) puzzle
- **Statement**: A single movable block is steered by four directional actions through a
  walled maze; the block snaps one fixed-size step per action.
- **Conditions**: Holds for ls20 Levels 1–2 (observed); presumed for L3 (same primitives seen
  at recon). Untested boundary: levels beyond L3.
- **Sources**: [block-step ← trace/exploration_tree.yaml:N02 «A1 = UP; moves cost budget» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: An action moves something other than the single block, or the block moves
  by a non-fixed amount.
- **Proof**: [evidence/README.md → frames turns 0→4 (A1–A4 each move the block one macro-cell)]
- **Dependencies**: []
- **Tags**: mechanics, movement, sokoban

## C02: Moves are budget-limited
- **Statement**: Each action consumes from a finite move budget shown in the bottom bar, so
  solutions must be short and probing must be hypothesis-driven.
- **Conditions**: L1 ~1 unit/move; L2–L4 ~2 units/move (the per-level cost rate differs); full
  bar = 42. The budget is a per-life resource coupled to a separate lives pool — exhausting it and
  acting again is an overdraft that respawns the block and spends a life (see C12). RESET does NOT
  merely refresh the budget: it restarts the WHOLE GAME to Level 1, discarding completed levels
  (corrected this session — N41); a death-respawn (not RESET) is what refills the budget mid-level.
- **Sources**: [L2-cost ← logic/solution/heuristics.md:H07 «budget 42→40→38→…→8 over the L2 path, −2 per action» [result]; reset-full-game ← trace/exploration_tree.yaml:N41 «A RESET dropped levels_completed 3->0 ... RESET restarts the ENTIRE game at Level 1» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: An action leaves the budget bar unchanged, or the budget never reaches 0.
- **Proof**: [evidence/README.md → turn 0→1 leftmost X unit consumed; L2 budget decrements by 2/move; harness.log RESET at count 214 dropped levels_completed 3→0]
- **Dependencies**: [C12]
- **Tags**: mechanics, budget
- **Last revised**: 2026-06-29 (2026-06-29_001#5)
<!-- 2026-06-29 (#10, N60): POSSIBLE CONTRADICTION flagged (NOT resolved, NOT overwriting): on L6, `play.py send
     RESET` refreshed ONLY the current level (block→L6 start, %%→12, budget→42, X-boxes restored) and KEPT
     levels_completed=5 (no drop to L1, no replay needed). This conflicts with the N41/#5 reading that RESET
     restarts the WHOLE game to L1 (levels 3→0). Either RESET behaves differently by context, or N41 was itself a
     desync. Used the per-level-refresh behaviour repeatedly + reliably this session. Needs reconciliation next
     session (re-test RESET from a clean known state and watch levels_completed). Statement left intact pending that. -->
<!-- 2026-06-29 (#14, N73): SECOND confirming instance — on L7, `play.py send RESET` likewise refreshed ONLY the
     current level (block→(3,3), %%→12, budget→42, all 6 X-boxes restored) and KEPT levels_completed=6, including a
     RESET taken from %%=4 that restored full lives. So per-level-refresh now holds on BOTH L6 (N60/N70) and L7 (N73),
     used repeatedly+reliably. The N41 whole-game-restart reading looks like a stale desync. Statement STILL left
     intact (the RESET clause is in Conditions, not the budget Statement); the two-instance evidence is recorded here
     for a researcher to fold the RESET clause into Conditions next pass. Operationally on L7 this gives UNLIMITED
     safe retries via RESET-before-%%=0. -->


## C03: Reaching/parking on the key-box is NOT the win condition
- **Statement**: Bringing the block adjacent to or onto a candidate target cell (key-box,
  speck) does not by itself complete the level; the level is gated by the lock state, not by
  position.
- **Conditions**: Established on L1. Superseded the earlier "reach a target cell to win"
  reading once the lock mechanic (C06) was found.
- **Sources**: [box-noop ← trace/exploration_tree.yaml:N06 «0 cells changed — block wedged vs box border» [result]]
- **Status**: refuted
- **Provenance**: ai-executed
- **Falsification**: A level completes the moment the block reaches a target cell with no lock
  match required.
- **Proof**: [evidence/README.md → turn 10→11 box border 0-cell no-op; turn 16→17 speck covered, still NOT_FINISHED]
- **Dependencies**: [C06]
- **Tags**: win-condition, refuted, superseded

## C04: A move into a wall is a no-op that still costs budget
- **Statement**: Driving the block into an impassable (color-4) cell changes zero cells but
  still consumes one budget unit.
- **Conditions**: L1; presumed general. Useful as a cheap wall probe but still burns a move.
- **Sources**: [zero-cells ← trace/exploration_tree.yaml:N06 «0 cells changed» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: A move into a wall changes >0 cells, or such a move leaves the budget
  unchanged.
- **Proof**: [evidence/README.md → turn 10→11, A1 into the box border, 0 cells changed]
- **Dependencies**: [C01, C02]
- **Tags**: mechanics, walls, budget

## C05: The control panel is dynamic and reflects lock state
- **Statement**: The bottom-left control panel is not decorative — stepping the block onto a
  switch changes the panel's pattern, so the panel displays a mutable lock/loop state rather
  than a static label.
- **Conditions**: First seen on L1 (the panel changed exactly once across 18 turns, caused by
  the switch step). Generalized and made precise by C06.
- **Sources**: [one-change ← trace/exploration_tree.yaml:N07 «panel changed (only change in 18 turns; episode-log diff)» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: The panel pattern never changes across an episode regardless of switch steps.
- **Proof**: [evidence/README.md → panel @-pattern toggled rows 57–58 between turn ~10 and turn 17]
- **Dependencies**: [C01]
- **Tags**: lock, panel, mechanics

## C06: Lock mechanic — switch=toggle, key-box=target pattern, panel=current pattern
- **Statement**: The level encodes a 3×3 lock: the key-box `@` symbol is the target pattern,
  the bottom-left panel is the current pattern, and stepping the block onto a switch toggles
  the current pattern. The lock is satisfied when panel == target.
- **Conditions**: L1: the switch (R6C3) flipped the panel's middle row so panel matched the
  key-box target; the switch is a toggle (not consumed). Satisfying the lock is necessary but
  not sufficient — a delivery step remains (C07).
- **Sources**: [middle-row ← trace/exploration_tree.yaml:N07 «speck = toggle SWITCH; panel now matches key-box target `111/001/101`» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: Stepping the switch leaves the panel unchanged, or the level completes
  with panel != key-box target.
- **Proof**: [evidence/README.md → panel-diff across the L1 episode: changed exactly once at turn 16→17, middle row 100→001, matching target 111/001/101]
- **Dependencies**: [C05]
- **Tags**: lock, switch, key-box, breakthrough

## C07: Win = deliver the block into the now-unlocked key-box
- **Statement**: With the lock satisfied (panel == target), the previously walled-shut key-box
  becomes enterable; driving the block into it completes the level.
- **Conditions**: Confirmed on L1 and L2. Before the lock is matched the box is a no-op wall
  (DE1).
- **Sources**: [redraw ← trace/exploration_tree.yaml:N08 «1479 cells changed, levels_completed 0→1» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: The block enters a matched key-box and the level does not complete, or a
  level completes without any key-box delivery.
- **Proof**: [evidence/README.md → L1 turn 23→24 ~1479-cell redraw, levels_completed 0→1; L2 turn 130→131 1421-cell redraw, 1→2]
- **Dependencies**: [C06]
- **Tags**: win-condition, delivery

## C08: "L2 switch = vertical flip + a hidden 2nd control needed"
- **Statement**: (REFUTED hypothesis) The L2 switch only flips the lock top↔bottom, leaving
  the middle row unchanged, so a second hidden control is required to reach the target.
- **Conditions**: Arose from a single observed step-on of the L2 switch that looked like a
  flip. Disproved by repeated sampling (C09): the apparent flip was an under-sampling artifact.
- **Sources**: [under-sample ← trace/exploration_tree.yaml:N12 «4-state cycle that DOES change the middle row» [result]]
- **Status**: refuted
- **Provenance**: ai-executed
- **Falsification**: Repeated switch steps fail to ever change the middle row (the condition
  that would have kept it alive — not observed).
- **Proof**: [evidence/README.md → turns ~72–85 repeated R9C9 toggling cycles the middle row 001↔100]
- **Dependencies**: [C09]
- **Tags**: lock, switch, refuted, under-sampling

## C09: L2 is solved by the ONE switch alone (4-state cycle) plus a 2-push delivery
<!-- CONFLICT RESOLVED 2026-06-29 (turn #4, see trace/exploration_tree.yaml:N34). The session #3
     "multi-stage %% L2" (N31) was a LEVEL-TRACKING DESYNC, not an L2 variant: from a clean
     levels_completed=0 start this claim's recipe (R-L2) re-won L2 in a SINGLE 2-push box delivery
     (N33), and the %% counter is a permanent UI fixture that never decremented on any L1/L2 delivery.
     C09 stands `supported`, unmodified. The old conflict observations O09/O10 are FALSIFIED (N35). -->
- **Statement**: A single switch whose transform is a 4-state cycle suffices to reach the L2
  target from the fresh start in a fixed number of step-ons; delivery into the matched key-box
  takes two pushes (wedge, then enter). No second lock control exists.
- **Conditions**: L2 start panel `111/001/101`, key-box target `111/100/101`; the R9C9 switch
  cycles `111/001/101 → 101/001/111 → 101/100/111 → 111/100/101 → …`, so 3 step-ons reach the
  target. Budget funded by X-box refills (H08).
- **Sources**: [three-stepons ← logic/solution/heuristics.md:H06 «3 step-ons reach the target `111/100/101`» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: From the fresh L2 start, no number of switch steps reaches the key-box
  target, or delivery succeeds in a single push.
- **Proof**: [evidence/README.md → live L2 solve turns 86–131: cycle mapped, 3 toggles → matched, 2 DOWN presses → 1421-cell redraw, levels_completed 1→2]
- **Dependencies**: [C06, C07]
- **Tags**: lock, switch, cycle, delivery, L2-solved

## C10: The per-level lock TRANSFORM differs, but the RECIPE is invariant
- **Statement**: Across levels the switch's transform changes (toggle vs multi-state cycle),
  but the solution loop is invariant: read the target from the key-box `@`, drive the block
  onto switch(es) until panel == target, then deliver the block into the unlocked key-box. The
  switch's full cycle must be sampled before planning toggles.
- **Conditions**: Supported by L1 (2-state middle-row toggle, single pattern axis), L2 (4-state
  cycle, single pattern axis), and L3 (TWO axes — pattern switch + colour selector, see C11); the
  must-sample-first lesson is the transferable correction that dissolved the false C08. The recipe
  holds across all FOUR solved levels; the per-level change is the number/kind of control axes and the
  obstacle class, not the loop. L4 is now SOLVED (this session): same loop — read target (key-box `@`
  pattern 111/001/101 + colour @), a two-axis lock (colour selector (6,6) reusing the L3 4-state cycle
  a 4th time + a pattern speck at (6,4)), then the ordinary 2-push delivery — over a NEW obstacle class,
  a portal/teleporter maze (C13). The C10 must-sample-first lesson was directly load-bearing on L4: the
  colour selector was sampled 6× (refuting a "double-duty" shortcut) and the pattern speck — initially
  mis-judged "not steppable" — was a C10 under-sampling error corrected by trying an untried side. So the
  recipe is now VERIFIED through an L4 win.
- **Sources**: [transforms ← logic/solution/recipes.md:R-L2 «L1 switch = middle-row toggle (2 states); L2 switch = 4-state cycle» [result]; L3-two-axis ← logic/solution/recipes.md:R-L3 «set colour @ at R9C5, pattern 101/100/111 at R2C9, then 2-push box delivery → 1425-cell redraw, levels 2→3» [result]; L4-win ← logic/solution/recipes.md:R-L4 «colour @ set at (6,6) [6× sampled] → pattern 111/001/101 set at (6,4) from the SOUTH → carried free aligned block to (1,3) → LEFT, LEFT = WIN, levels 3→4» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: A future level wins by a procedure other than read-target → match-panel →
  deliver, or its switch transform is fully known from a single press in a way that breaks the
  recipe.
- **Proof**: [evidence/README.md → L1, L2, L3, L4, and L5 all solved by the same loop with different control sets (1 toggle / 1 cycle / 2 axes / 2 axes + portal maze / 2 axes + portal-pocket selector + a 2-speck composed pattern lock); trace N14 the under-sampling dead_end whose lesson is this claim; N36 the L3 two-axis win; N49 the L4 win (must-sample-first refuted a double-duty shortcut and corrected a "not steppable" misread); N51 the L5 win (the same read-target→match-panel→deliver loop held over a portal-pocket colour selector + a composed PPQQ pattern word, C14)]
- **Dependencies**: [C06, C07, C09, C11, C14]
- **Tags**: transfer, recipe, meta, invariant
- **Last revised**: 2026-06-29 (2026-06-29_001#9)
<!-- 2026-06-29 (#9, N51): C10 CONFIRMED THROUGH A 5th WIN (L5). The invariant loop held even though L5
     added the two hardest wrinkles yet — a portal-ONLY-reachable colour selector pocket (entrance
     (2,6)+UP→(5,6)) and a TWO-SPECK COMPOSED pattern lock needing a searched word PPQQ (C14, not a single
     press). The per-level change was again the control SET + obstacle class, not the loop. Status stays
     supported (a 5th instance). The real L5 difficulty was budget/lives logistics, not the loop (N52). -->

## C11: L3's lock has TWO independent axes (pattern + colour); aligning is free of any catch-22
- **Statement**: A level's lock may combine more than one independent axis — here a 3×3 pattern
  and a fill colour — each driven by its own control; setting one axis does not disturb the other,
  an aligned axis PERSISTS when the block steps off its control, and the fully-aligned block remains
  free to navigate. Delivery is the ordinary push into the now-unlocked key-box (C07), not a special
  step-off event — so there is no catch-22 between aligning and delivering.
- **Conditions**: L3: pattern axis driven by the switch at macro R2C9 (same 4-state cycle as H06),
  colour axis by the selector at R9C5 (4-state fill-colour cycle N→@→$→%); target = pattern
  101/100/111 in colour @, key-box on the RIGHT (R9C10). Each control's step-off (aligned or not) is
  a normal move; the colour selector never delivers. Untested boundary: levels beyond L3, and whether
  axis count grows further.
- **Sources**: [two-axis-win ← trace/exploration_tree.yaml:N36 «set colour @ at R9C5, pattern 101/100/111 at R2C9; aligned step-off = normal move; 2-push box delivery → 1425-cell redraw, levels 2→3» [result]; no-catch22 ← trace/exploration_tree.yaml:N35 «aligned step-off off BOTH L3 controls is a normal 54-cell move, panel persists, no delivery» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: Setting one axis flips the other; an aligned axis resets on step-off; the
  aligned block is consumed/teleported on step-off (a real catch-22); or L3 completes by something
  other than pushing the aligned block into the key-box.
- **Proof**: [evidence/README.md → L3 solve this session (N36): both axes set independently, aligned step-off off R2C9 and R9C5 each a normal move, free aligned block delivered by 2 DOWN pushes into R9C10 → 1425-cell redraw, levels_completed 2→3; N35 the dead_end retiring the catch-22/multi-stage model]
- **Dependencies**: [C06, C07, C10]
- **Tags**: lock, two-axis, colour, L3-solved, catch-22-refuted
- **Last revised**: 2026-06-29 (2026-06-29_001#5)
<!-- 2026-06-29 (#5): C11's two-axis structure CONFIRMED to extend to L4 recon (key-box (1,1) target
     pattern 111/001/101 + colour @; colour selector (6,6) = same 4-state cycle as L3) — see trace N43.
     L4 NOT solved (pattern-axis control unlocated, N44), so no new claim crystallized; the L4 extension
     stays staged (O16). Status unchanged. -->
<!-- 2026-06-29 (#7, N49): C11 now CONFIRMED THROUGH AN L4 WIN, not just recon. L4's two axes are the
     colour selector (6,6) [colour-only, proven by 6 clean samples] and the pattern speck (6,4); each set
     independently, alignment PERSISTED on step-off + through navigation, and the free aligned block
     delivered into key-box (1,1) by a 2-push (no catch-22) — exactly the C11 structure. 4th confirming
     level. Status stays supported (a 4th instance, no rewrite needed). The colour-selector-double-duty
     hypothesis (a single dual-axis control) was REFUTED here, reinforcing that the axes are INDEPENDENT
     controls. -->
<!-- 2026-06-29 (#9, N51): C11 CONFIRMED THROUGH A 5th WIN (L5) — two INDEPENDENT axes again (colour selector
     (5,5) in a portal pocket + the pattern axis), each set independently, alignment PERSISTED across the
     pocket portal exit AND the long delivery navigation. NEW: the L5 PATTERN axis was itself driven by TWO
     composing controls (C14) — so an axis can be multi-control, but the colour↔pattern axes stay independent
     (setting colour never touched the pattern across all the pocket sampling). Status stays supported. -->

## C12: ls20 is twin-resource — a per-life move budget AND a finite %% lives pool; budget-0 overdraft = death-respawn that spends a life
- **Statement**: Play is governed by two coupled resources: a move-budget bar that depletes per
  action and refills to full at single-use X-boxes, and a small bottom-right marker pool that acts
  as a lives counter. Exhausting the budget bar and acting again does not merely waste the move — it
  respawns the block at the current level's start (discarding in-progress lock alignment), refills
  the budget, and consumes one unit of the lives pool. The lives pool resets at the start of each
  level and only decrements on such an overdraft death; a death taken with the pool already empty
  ends the episode. Refilling the budget while it is still positive costs no life.
- **Conditions**: Observed across ls20 L1–L4 this run. Budget ≈1/move on L1, ≈2/move on L2–L4; full
  bar = 42 (~21 moves). Lives pool = the color-8 `%%` markers, 3 groups × 4 cells = 12, stepping
  12→8→4→0 (one step = 4 cells = one death); resets to 12 per level (CONFIRMED on L5 — %% reset to 12 on
  entry). Overdraft = pressing a move while budget = 0. CRITICAL refinement (L5, N51): a death from %%=12→8
  and 8→4 each RESPAWN the block (level-start, budget refilled), but the death from %%=4→0 is TERMINAL —
  it does NOT respawn, it is immediate GAME_OVER. So %%=4 is the LAST life (zero margin); never overdraft at
  %%=4. Untested boundary: the exact budget/move rate and per-step granularity (4) at L6+.
- **Sources**: [overdraft-respawn ← trace/exploration_tree.yaml:N38 «budget 0 + another move → block respawns at level-start, budget 0->42, %% decrements one step» [result]; lives-reset ← trace/exploration_tree.yaml:N39 «%% RESETS to 12 at the start of each level ... steps down 12->8->4->0 with each death» [result]; free-refill ← trace/exploration_tree.yaml:N38 «refills at budget>0 are FREE (12->12)» [result]; game-over ← trace/exploration_tree.yaml:N39 «a death while %%=0 → state=GAME_OVER» [result]; marker-count ← logic/solution/heuristics.md:H11 «%% markers ... 3 groups × 4 cells = 12» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: The budget bar reaching 0 followed by a move leaves the block in place (no
  respawn) and the %% pool unchanged; OR a refill at budget>0 decrements %%; OR the %% pool fails to
  reset between levels; OR an episode continues normally after a death at %%=0.
- **Proof**: [evidence/README.md → episode-log runs/ls20-9607627b_ccrelay.jsonl turns 173/220/313/359 (REFILL budget 0→42 each paired with %% −4) and free refills (budget 20→42 / 4→42 with %% unchanged); two live GAME_OVERs at %%=0 this session; %%=12 observed fresh at L1/L2/L3/L4/L5 starts; L5 (N51): 12→8 and 8→4 overdrafts respawned cleanly, the 4→0 overdraft was immediate GAME_OVER (terminal last life)]
- **Dependencies**: [C02]
- **Tags**: budget, lives, death-respawn, game-over, mechanics, twin-resource
- **Last revised**: 2026-06-29 (2026-06-29_001#9)
<!-- CONTRADICTION RESOLVED 2026-06-29 (#5, trace N40): supersedes the prior "%% is a PERMANENT UI
     FIXTURE" reading (N33/N35/N36). That reading was partially right (it correctly retired the
     desync-era "per-delivery %% multi-stage" model) but wrong that %% is decorative: %% stayed 12 in
     those runs only because they never overdrafted/died. Reconciled here: %% = lives, ticks on death.
     The L1/L2/L3 win records (N08/N13/N36, C07/C09) are UNAFFECTED — those solves never died. -->

## C13: Later ls20 levels add a portal/teleporter maze as a navigation obstacle, orthogonal to the lock
- **Statement**: From Level 4 onward an ls20 level overlays a portal network on the maze: stepping a
  floor cell in a given direction warps the block to a fixed destination cell instead of the adjacent
  one. Portals are NAVIGATION obstacles only — traversing one does not change the lock panel
  (pattern or colour) — so the lock recipe (C10/C11) is untouched, but pathfinding must be portal-aware
  (treat each (cell,direction) as a possible warp edge) or it desyncs. Some cells are multi-portal
  "trap hubs" with only one non-warp exit.
- **Conditions**: First seen on L4 (solved this session) and re-seen on L5 (entered, unsolved): both
  have a 3-way trap hub at macro (4,7). The full portal map per level is partial when discovered; the
  robust countermeasure is re-pathfinding after every single leg from the re-detected block position
  (H10), which absorbs unmapped warps. Untested boundary: portal density/layout at L5-L7, and whether
  any level's portal gates a lock control (none seen so far — L4's pattern control (6,4) was on open
  floor, not portal-gated).
- **Sources**: [l4-portals ← trace/exploration_tree.yaml:N49 «portal-aware BFS ... 3 more L4 edges found live ((4,9)+A3→(9,8),(5,6)+A1→(4,10),(6,8)+A1→(5,6)); re-pathfind-each-leg absorbed the gaps» [result]; l4-hub ← staging/observations.yaml:O18 «(4,7) = a 3-way portal HUB (only UP is non-portal, so it is a TRAP cell)» [result]; no-lock-effect ← staging/observations.yaml:O18 «Portal traversal does NOT change the panel pattern (re-tested vs the CORRECT baseline 010/110/011)» [result]; l5-hub ← trace/_l4plus_raw.md «L5 ... (4,7) is AGAIN a trap hub ... (4,7)+A2->(1,7); (4,7)+A3->(4,8)» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: A portal traversal changes the lock panel; OR an L4+ level has no portals; OR a
  lock control is reachable ONLY through a portal that also alters the lock (a genuine portal-gated
  control); OR a fixed portal-aware BFS over the full edge set still mis-routes (warps are not
  deterministic per (cell,direction)).
- **Proof**: [evidence/README.md → L4 solved this session (N49) with the portal-aware navigator;
  O18 mapped 7+ direction-specific edges; L5 SOLVED (N51) with a portal-aware navigator over a portal-pocket]
- **Dependencies**: [C01, C10]
- **Tags**: portals, navigation, obstacle, L4, L5, mechanics
- **Last revised**: 2026-06-29 (2026-06-29_001#9)
<!-- 2026-06-29 (#9, N51): STRENGTHENED through the L5 WIN. L5 introduced a genuine PORTAL-GATED CONTROL —
     the colour selector (5,5) was reachable ONLY through a warp ((2,6)+UP→(5,6)), the first lock control
     that REQUIRES a portal to reach. This does NOT falsify C13's "portals don't change the lock" clause:
     traversing the entrance warp did not alter the panel; the portal only GATES ACCESS to the selector, it
     does not BE the selector. So the "portal-gated control" falsifier (a portal that also alters the lock)
     is still NOT met — access-gating ≠ lock-altering. The (4,7) trap-hub motif recurred on L5 but was NOT
     the pocket gate (its RIGHT/UP are plain floor). Status stays supported. -->


## C14: A lock axis may be driven by MULTIPLE composing controls whose transforms form a group — the alignment is a word over them, found by search, not a single press
- **Statement**: A single lock axis (here the 3×3 pattern) can be controlled by more than one switch,
  each applying its own deterministic transform to the panel; the transforms compose (do not commute in
  general), so reaching the target is a SEQUENCE (word) of step-ons over the several controls, computed by
  searching the transform group from the baseline — not a fixed number of presses on one control. At least
  one such transform can be a pure spatial permutation of the 3×3 (a grid rotation).
- **Conditions**: L5 pattern axis: two controls — (2,3) = a period-6 transform, (7,3) = a fixed 90° grid
  rotation (position-permutation); neither's own orbit reaches the target, but the word "press (2,3) twice
  then (7,3) twice" does (found by BFS over the two transforms). Generalizes the single-control pattern
  switch of L1/L2/L3 and the single-press speck of L4. Untested boundary: axis-count and transform-kind at
  L6+ (L6 recon shows a rotation-type pattern speck again, O22); whether >2 controls ever drive one axis.
- **Sources**: [ppqq ← logic/solution/recipes.md:R-L5 «word PPQQ: 010/110/011 --PP--> 110/011/101 --QQ--> 101/110/011 (= target)» [result]; rotation ← trace/exploration_tree.yaml:N51 «(7,3)=transform Q, a FIXED 90-deg grid ROTATION, perm [6,3,0,7,4,1,8,5,2]» [result]]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: A multi-control pattern axis is shown to be solvable by any single control alone (its
  orbit contains the target), OR the controls' transforms are non-deterministic (a step-on yields different
  panels from the same state), OR no word over the controls reaches a reachable-looking target.
- **Proof**: [evidence/README.md → L5 solved this session (N51): (2,3) period-6 + (7,3) 90°-rotation, offline BFS gave the forced word PPQQ, verified live to reach 101/110/011, then delivered → levels 4→5; L6 (N55): the rotation speck (8,4) re-confirmed = the SAME Q 90°-rotation perm, a 2nd independent rotation-control instance]
- **Dependencies**: [C06, C10, C11]
- **Tags**: lock, pattern, composed-controls, group, search, L5-solved
<!-- 2026-06-29 (#10, N55): C14 STRENGTHENED on L6 (level UNSOLVED, but this sub-mechanic empirically RESOLVED).
     L6's rotation pattern-speck (8,4) was live-sampled and its orbit
     110/011/101→101/011/110→101/110/011→011/110/101→(back) is reproduced EXACTLY by L5's Q perm
     [6,3,0,7,4,1,8,5,2] (90° CW rotation) — so the SAME rotation transform recurs as an independent 2nd
     instance, making "a pattern control can be a fixed grid rotation" a CROSS-LEVEL motif, not an L5 one-off.
     On L6 the UPPER key-box pattern target 101/110/011 = Q^2 (rotation speck pressed twice) — reachable by ONE
     control's orbit, no word needed; the LOWER target 101/001/111 is OUTSIDE Q's orbit and DOES need a word over
     {pure-speck (2,4), Q} (the pure speck's transform is unsampled — open thread). Status stays supported (a 2nd
     instance, no rewrite). Practical read note: the on-cell panel read LAGS the speck step-on by ~1 turn; sample
     with A1-on / A2-off / ≥3 NEUTRAL settle-moves / then read. -->
<!-- NOTE: the L6 rotation-speck and the colour selector RENDER at slightly different macro cells across frames
     (selector seen at (5,5) and (4,4); specks shifted too) — read control positions LIVE each visit, don't hardcode. -->
<!-- 2026-06-29 (#12, N63/N64): C14 FURTHER STRENGTHENED on the L6 LOWER axis (level still unsolved). The pure speck P
     (row-2 patroller) was cleanly catchable (oscillate (2,1)↔(2,2); each panel-change = one P apply) and partially
     mapped: P is a genuine period-6 NON-permutation (on-bit count varies), and — the new structural fact — P has
     MULTIPLE DISJOINT period-6 orbits (mapped two: A={…101/001/111…} containing the LOWER target, B={111/101/101,
     010/101/110,110/011/010,101/100/111,…}). The post-UPPER panel 101/110/011 sits in orbit B, so pure P-catching
     can NEVER reach the target in orbit A — the LOWER alignment GENUINELY requires a {P,Q} WORD where Q bridges
     between P's orbits, then P walks to the target within the right orbit. This is the strongest C14 instance yet:
     not just "a word over commuting-ish controls" but "Q is structurally REQUIRED to cross between a control's
     disconnected orbits." Status stays supported. OPEN: map P's orbits to closure + offline-BFS the exact word
     101/110/011→101/001/111 over {P-trans, Q-perm} before the next live run (the run was LOST mid-exploration to budget). -->
<!-- 2026-06-29 (#13, N66/N67): C14 CONFIRMED THROUGH THE L6 WIN + the P-structure CORRECTED. SINGLE-catch sampling
     (one verified before→after per catch) shows P is a SINGLE closed period-6 cycle "orbit B"
     [010/110/011→111/001/101→110/011/101→010/010/111→101/101/111→011/101/010→back], NOT the "multiple disjoint orbits"
     of the #12 comment (that was a BATCH-sampling confound — N67, multi-apply per oscillation). The Q-bridge claim STANDS
     but sharpens: Q is Q-CONJUGATE to orbit B (Q maps every orbit-B state into the LOWER orbit, and Q(111/001/101)=
     101/001/111=the LOWER target exactly) — so the LOWER word QQPPPPPQ (offline BFS over {P-cycle,Q}) is forced and ENDS in Q
     to cross out of P's orbit onto the target. This is the strongest C14 instance to date and now VERIFIED in a win (R-L6,
     levels 5→6). Status stays supported (a 2nd composed-word level, both rotation-control instances). -->



## C15: From L6, lock controls can be MOBILE (patrol one step per displacement move) and key-box delivery can be MULTI-BOX (all boxes delivered in one life)
- **Statement**: A later ls20 level may make the lock controls MOBILE — each control (pattern specks, colour
  selector) advances one step along a fixed patrol each time the player makes a displacement move (a wall-bounce
  no-op does not advance them; with no input they are frozen), turning "use a control" into a pursuit/timing
  catch rather than a stationary step-on. A control is caught by occupying its cell on the turn it is there; for a
  control patrolling a single row, a PARITY law (block_col + control_col invariant) forbids catching it from the
  adjacent row, so the catch must be made by entering the control's own row and crossing it. Additionally, a level
  may present MULTIPLE key-boxes each with its own target (pattern+colour); the level is won only when ALL boxes
  are delivered, and the deliveries must occur within a SINGLE life — a death-respawn restores every box (and the
  panel), so a partial multi-box delivery cannot be banked across a death. The lock-alignment recipe (C10/C11/C14)
  is otherwise unchanged; the per-box target is read from that box's `@`/colour glyph as usual. The DELIVERY ORDER
  is FORCED by geometry, not convention: the shared panel PERSISTS across a partial (non-completing) box delivery
  (only a level-complete redraw or a death resets it), and delivering the first box DISSOLVES its frame to floor,
  which UNBLOCKS the maze cells that were portal-isolated behind it — so the second box's approach only becomes
  reachable after the first is delivered. The two boxes generally demand DIFFERENT pattern+colour on the one shared
  panel, so the alignments cannot be held simultaneously: the loop is align-A → deliver-A → realign-B → deliver-B,
  all within one life.
- **Conditions**: L6 (UPPER box DELIVERED live, level UNSOLVED — LOWER pending): two key-boxes — UPPER (7,10) target pattern 101/110/011 colour-% reached
  by Q² (the mobile row-8 rotation speck caught twice), LOWER (10,10) target 101/001/111 colour-@ needing a word
  over {pure row-2 speck P, Q}; the colour selector roams rows 4-6 (caught by 2D pursuit, no parity trap); the box
  column is a portal-isolated pocket entered only via the warp (2,9)+A1→(5,9). The UPPER box was delivered live
  (its frame dissolved) but the level did not complete (LOWER pending); an overdraft death restored both boxes.
  EMPIRICALLY RESOLVED this turn (N62): (a) the shared panel PERSISTS at the UPPER target after the UPPER box
  dissolves (does NOT reset); (b) the dissolved UPPER box (7,10) becomes plain floor and UNBLOCKS col-10 — (8,10)/(9,10)
  [the LOWER-box approach], previously portal-isolated, become reachable, along with the pocket exit; (c) therefore the
  delivery order is FORCED UPPER-before-LOWER (the LOWER box (10,10) is reached only from (9,10)+A2, gated on (7,10)
  dissolving). Untested boundary: P's exact transform (period-6 non-permutation, partially mapped — the LOWER target
  101/001/111 IS in its orbit, N63), the full one-life double-delivery execution, and L7.
- **Sources**: [mobile ← trace/exploration_tree.yaml:N58 «controls advance one step per displacement move; row-9 parity forbids the naive catch; catch by entering the control's row and crossing» [result]; multibox ← trace/exploration_tree.yaml:N59 «UPPER box delivered (frame dissolved) but levels stayed 5; an overdraft death RESTORED both boxes → both deliveries must be in one life» [result]; panel-persists+col-unblock+forced-order ← trace/exploration_tree.yaml:N62 «shared PANEL PERSISTS after partial delivery; delivering UPPER UNBLOCKS COL-10 (BFS from (8,10) reaches 68 cells incl (9,10)); DELIVERY ORDER IS FORCED UPPER-before-LOWER» [result]; lower-word ← logic/claims.md#C14]
- **Status**: supported
- **Provenance**: ai-executed
- **Falsification**: The L6 controls are shown stationary (the "movement" was a read artifact); OR a single key-box
  delivery completes a multi-box level; OR a multi-box level's partial delivery survives a death-respawn; OR the
  controls can be caught from the adjacent row (no parity law).
- **Proof**: [evidence/README.md → L6 this session: controls tracked moving one step per displacement move (N58); UPPER box delivered live via mobile-catch + portal-pocket warp, frame dissolved, but levels stayed 5; overdraft death restored both boxes (N59); panel-persistence + col-10-unblock + forced-order all live-verified (N62)]
- **Dependencies**: [C10, C11, C13, C14]
- **Tags**: mobile-controls, multi-box, parity, pursuit, one-life, forced-order, panel-persistence, L6, mechanics, breakthrough
- **Last revised**: 2026-06-29 (2026-06-29_001#13)
<!-- 2026-06-30 (N74/N75): L7 SOLVED (levels 6→7, WIN — GAME COMPLETE 7/7, R-L7). L7 is the mobile-control family
     (C15: P'/Q patrol, caught by crossing; selector cycles colour) BUT is SINGLE-box, not multi-box — the multi-box
     reading (a first box at (10,10) dissolving a wall) was REFUTED ((10,10) is a plain X-box). Instead L7's key-box
     is LOCK-GATED IN FOG: a fog-of-war reveal maze hides the key-box in a portal-isolated pocket whose gate (9,5)→(10,5)
     opens ONLY when panel==target (C07 extended to fog), colour-alone never (N72). The target, a "lone colour-8 cell",
     is actually a READABLE 3×3 rendered 1px/cell (decoded 101/110/011 colour-%); the {P',Q} word PPPPPQQ (offline BFS,
     C14) reaches it; delivered via (9,5)+A2. So C15's mobile-controls clause held on L7; its multi-box/forced-order
     clause is L6-specific (does not generalize to L7). The WM (wm-predict) led the L7 solve — its C07-in-fog frame
     was the decisive call. -->
<!-- 2026-06-29 (#13, N66): C15 CONFIRMED THROUGH THE L6 WIN (levels 5→6, R-L6). The full two-box one-life
     double-delivery was executed end-to-end in ONE life with ZERO deaths: UPPER aligned+pocket-delivered (frame
     dissolved, panel persisted, col-10 unblocked) → LOWER realigned on the shared panel (colour @ + the {P,Q} word
     QQPPPPPQ) → LOWER delivered via the same (2,9)+A1→(5,9) pocket warp + the now-unblocked col-10 to (9,10)+A2 into
     (10,10). All C15 sub-claims (mobile-control catch via row-cross/2D-pursuit, parity law, forced UPPER-first order,
     panel-persistence, col-unblock, one-life-both-deliveries) held in the win. The remaining "untested boundary" of
     #12 (P's exact transform, the one-life execution) is now CLOSED: P = single period-6 cycle (N67), one-life run
     proven feasible by an offline budget-ledger and confirmed live. Status stays supported (now via a full win, not
     just the UPPER half). The decisive enabler was precomputing P+word OFFLINE (zero in-run exploration) + a tight
     refill schedule (1,7)/(9,1)/(1,1) with (1,1) refilled right after P⁵. -->
<!-- 2026-06-29 (#12, N62/N63): C15 STRENGTHENED — the three previously-"untested boundary" pieces of the two-box
     protocol are now EMPIRICALLY RESOLVED via a live UPPER delivery: (a) the shared panel PERSISTS across a partial
     delivery; (b) delivering UPPER dissolves (7,10) to floor and UNBLOCKS col-10 so the LOWER approach (9,10) becomes
     reachable; (c) delivery ORDER is FORCED UPPER-before-LOWER. The general clause "delivering box 1 unblocks box 2 +
     panel persists → order forced" added to the Statement. The pure speck P's clean catch method (oscillate (2,1)↔(2,2))
     was found and P partially mapped (period-6 non-permutation, LOWER target in orbit, N63). Level STILL unsolved
     (LOWER delivery + the one-life execution pending); status stays supported (UPPER half fully verified). -->
<!-- NOTE (open, do not crystallize as recipe yet): full R-L6 awaits the one-life double-delivery execution. The
     budget logistics remain the binding difficulty — L6's 3 single-use X-boxes are top-heavy ((1,1),(1,7),(9,1)) and
     the P-catch realign-for-LOWER (row 2) is far from (9,1); save (9,1) for the col-10 LOWER leg. %% mind: this turn
     burned down to the last life again on budget corners — N62/N63 deaths were forced overdrafts during exploration. -->

