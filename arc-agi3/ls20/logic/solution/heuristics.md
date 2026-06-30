# Heuristics — ls20 forward model & control mechanics

The action→effect mappings and the switch-cycle / refill / 2-push delivery mechanics — the
"how" of playing ls20. All observed live by pressing one action and diffing the frame.
Code refs point at the harness helper scripts used to read state.

## H01: A1 moves the block UP one macro-cell (5 cells)
- **Rationale**: Pressing A1 translates the block up by one 5-cell macro-cell; the rest of the
  board is unchanged. Establishes A1 = UP.
- **Sources**: [52-cells ← trace/exploration_tree.yaml:N02 «Block ... rows 45–49 → rows 40–44. 52 cells changed» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: low
- **Code ref**: [harness/look.py, harness/status.py]

## H02: A2 moves the block DOWN one macro-cell
- **Rationale**: A2 is the inverse of A1 — it translates the block down one macro-cell.
- **Sources**: [down ← trace/exploration_tree.yaml:N02 «block rows 40–44 → rows 45–49» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: low
- **Code ref**: [harness/look.py, harness/status.py]

## H03: A3 moves the block LEFT one macro-cell
- **Rationale**: A3 translates the block left one macro-cell.
- **Sources**: [left ← trace/exploration_tree.yaml:N02 «block cols 33–37 → cols ~28–32» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: low
- **Code ref**: [harness/look.py, harness/status.py]

## H04: A4 moves the block RIGHT one macro-cell
- **Rationale**: A4 completes the directional set as the right-move complement of A1–A3.
  Inferred from the up/down/left complement, then confirmed in play.
- **Sources**: [right ← trace/exploration_tree.yaml:N02 «A4 = RIGHT (model complete)» [result]]
- **Status**: active
- **Provenance**: ai-suggested
- **Sensitivity**: low
- **Code ref**: [harness/look.py, harness/status.py]

## H05: Every action consumes one unit of the budget bar (L1)
- **Rationale**: Each press depletes the leftmost remaining unit of the bottom `X` status bar
  (one unit per move on L1), making the bar a move budget.
- **Sources**: [unit ← trace/exploration_tree.yaml:N02 «cells (61,13)/(62,13) X→- ... One unit per move» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: low
- **Code ref**: [harness/status.py]

## H06: An ls20 PATTERN switch cycles the lock through 4 states (NOT a flip) — a recurring motif
- **Rationale**: Stepping the block onto an ls20 pattern switch repeatedly reveals a 4-state
  cycle whose middle row DOES change — superseding the earlier "vertical flip" reading, which
  was an under-sampling artifact (a single press happened to look like a top↔bottom flip). The
  cycle observed is `111/001/101 → 101/001/111 → 101/100/111 → 111/100/101 → (back)`. First seen
  on the L2 switch (R9C9): its 3rd state `111/100/101` equals the L2 key-box target, so from the
  fresh start 3 step-ons reach it. The SAME 4-state cycle was then reproduced byte-for-byte on a
  SECOND, independent switch — the L3 pattern switch at macro R2C9 (where the target 101/100/111
  is the 2nd state, so 2 step-ons reach it) — so this is a recurring ls20 switch motif, not a
  one-off L2 quirk. The old flip reading is RETIRED/corrected; toggle by stepping off and back on.
  (Note: the L3 *colour* control at R9C5 is a SEPARATE 4-state mechanism over fill colour, not a
  pattern switch — see staging O05; do not conflate the two.)
- **Sources**: [3-stepons ← trace/exploration_tree.yaml:N12 «From the fresh start, 3 step-ons reach the target `111/100/101`» [result]; L3-recur ← trace/exploration_tree.yaml:N23 «cycles the panel PATTERN through the SAME 4-state cycle as the L2 switch (H06): 111/001/101 → 101/001/111 → 101/100/111 → 111/100/101 → (back)» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: high
- **Code ref**: [harness/status.py, harness/look.py]
- **Last revised**: 2026-06-29 (2026-06-29_001#2)

## H07: Level 2 budget costs ~2 units per move
- **Rationale**: On L2 the budget bar decrements by ~2 per action (vs ~1 on L1), so a full
  42-unit bar funds roughly 21 moves; route planning must account for the higher rate.
- **Sources**: [two-per-move ← trace/exploration_tree.yaml:N11 «budget 42→40→38→…→8 over the L2 path, −2 per action» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: medium
- **Code ref**: [harness/status.py]

## H08: The X-boxes are BUDGET-REFILL stations, not lock controls — SINGLE-USE, and free only while budget>0
- **Rationale**: Stepping the block onto a color-b hollow 3×3 X-box instantly refills the
  budget bar to full (42), consumes the X-box glyph, and leaves the panel/lock UNCHANGED — so
  they fund long traversals but never touch the lock. The "X-box = 2nd lock control" lead was
  falsified (DE4). Two refinements found on L3/L4: (1) each X-box is **single-use** — it is
  consumed on the first step-on (color-b count 8→0) and does not regenerate within a level-life,
  and each level provides exactly **2** X-boxes, so plan around at most 2 free refills per life
  (a death/respawn restores them). (2) A refill is **free of any %% cost only while the budget
  bar is still positive**; refilling at budget exactly 0 is an OVERDRAFT that costs a %% life
  (see C12) — so always refill BEFORE budget reaches 0 and place the 2 refills so no leg can run
  the bar to 0. CORRECTION (2026-06-29 #7, found on L3/L4/L5): stepping the block ONTO an X-box cell
  while the budget bar is exactly 0 REFILLS to 42 life-free — it does NOT cost a %% life. The budget-0
  overdraft death (C12) is triggered only by a NON-refill move pressed at budget 0 (a plain move into
  floor/wall). So the X-box refill takes PRECEDENCE over the overdraft death: you may coast to budget 0
  and land on an X-box to refill without dying. (This refines the earlier "refilling at budget exactly 0
  is an overdraft" wording: the overdraft penalty attaches to the move's outcome being a move, not a
  refill; an X-box step at 0 is a free refill, a non-X-box step at 0 is the death-respawn.) Verified
  repeatedly this turn ((6,4)/(6,3)/(1,8) refills at budget 0 with %% unchanged).
- **Sources**: [refill ← trace/exploration_tree.yaml:N10 «R3C2 t53→54 budget 20→42, panel unchanged; R10C7 t71→72 budget 8→42, panel unchanged» [result]; single-use ← trace/exploration_tree.yaml:N41 «X-boxes are CONSUMED on first step-on (color-b count 8->0); each level has exactly 2» [result]; free-iff-positive ← trace/exploration_tree.yaml:N38 «%% decrement ONLY on an OVERDRAFT refill (budget exactly 0); refills at budget>0 are FREE (12->12)» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: medium
- **Code ref**: [harness/status.py, harness/pathfind.py, harness/scratchpad/nav.py, harness/scratchpad/drive.py]
- **Last revised**: 2026-06-29 (2026-06-29_001#7)

## H09: Delivery into the key-box takes TWO pushes (wedge, then enter)
- **Rationale**: With the lock matched, the first delivery press only wedges the block onto the
  box's top border (no win); a second press in the same direction pushes it fully in and
  triggers the win redraw. Plan for 2 delivery presses, not 1.
- **Sources**: [two-push ← trace/exploration_tree.yaml:N13 «1st A2 wedged ... 2nd A2 pushed it fully in → 1421-cell full-screen redraw, levels_completed 1→2» [result]; L3-two-push ← trace/exploration_tree.yaml:N36 «push1 = 54-cell wedge into R9C10; push2 = 1425-cell redraw, levels 2→3» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: medium
- **Code ref**: [harness/play.py, harness/status.py]
- **Last revised**: 2026-06-29 (2026-06-29_001#4)

## H10: Robust ls20 navigation — block = (color-9≥6 AND color-c≥4) macro-cell, single-action then re-pathfind
- **Rationale**: Two failure modes break naive ls20 navigation, and both are fixed by this method.
  (1) Block detection: the naive `color-c≥5` detector latches onto the bottom-left panel when the
  panel is drawn in colour-c (as on L3), mislocating the block; the reliable detector is the macro
  cell containing BOTH color-9 (≥6 cells, body) AND color-c (≥4 cells, cap), excluding color-9-only
  or color-c-only UI cells. (2) Routing: the macro display and pathfind disagree by ~+1 in the column
  index, and a press into a wall is a budget-only no-op that strands the block off-plan — so do NOT
  execute a long pre-planned action list in one shot; after each leg re-run pathfind from the CURRENT
  (re-detected) position and execute the next short segment, verifying the actual landing. Together
  these eliminated the +1 col desync across every L1/L2/L3 leg of the L3-winning session. Sub-fact: a
  move pressed at budget 0 STILL executes (and an X-box still refills) — but doing so is an OVERDRAFT
  that costs a %% life and may death-respawn the block to level-start (see C12), so budget 0 is a
  "soft" stop to be AVOIDED, not relied on. Further sub-fact found on L4: the harness runs slowly
  (~0.1–1 fps) and `play.py send` is async, so the result frame must be read only AFTER the turn
  counter advances, else the block detector misreads transition frames (the cause of spurious
  "drift"/"warp" mis-reads); `harness/scratchpad/nav.py` implements this turn-wait + low-budget stop.
- **Sources**: [detector+loop ← trace/exploration_tree.yaml:N36 «every leg landed as pathfind predicted across L1/L2/L3 → L3 win» [result]; budget-0 ← staging/observations.yaml:O08 «a move pressed at budget 0 STILL executes» [result]; turn-wait ← trace/exploration_tree.yaml:N38 «must wait for the turn counter to advance before reading the result frame» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: medium
- **Code ref**: [harness/scratchpad/step.py, harness/scratchpad/nav.py, harness/scratchpad/drive.py, harness/scratchpad/pathfind_portal.py, harness/pathfind.py]
- **Last revised**: 2026-06-29 (2026-06-29_001#7)
<!-- 2026-06-29 (#7): the single-action-then-re-pathfind loop became LOAD-BEARING on L4: the portal map
     is partial, so re-planning after every leg is what absorbed the unmapped warps and let the portal-aware
     BFS reach every control + the delivery. scratchpad/drive.py is the consolidated driver (O11 detector +
     this loop + low-budget stop + a per-level portal table); scratchpad/pathfind_portal.py is the
     standalone portal-aware BFS. step.py's PANEL field stays unreliable on L4/L5 — use scratchpad/panel.py
     for panel reads (the block-detector part of step.py/H10 is unaffected). -->


## H11: Never overdraft — refill while budget>0; %% is finite lives, GAME_OVER at %%=0
- **Rationale**: The move-budget bar and the bottom-right %% markers are TWO coupled resources
  (see C12). Letting the budget bar hit 0 and pressing one more move is an OVERDRAFT: the block
  death-respawns to the level-start (losing all in-progress alignment), the budget refills, and a
  %% life is spent (12→8→4→0). A death taken while %%=0 ends the episode (GAME_OVER → harness exits).
  So the operating rule is: keep the budget bar POSITIVE at all times — refill at an X-box (free
  while budget>0, H08) BEFORE the bar reaches 0, and plan routes so every leg can reach the next
  refill or the delivery within one budget bar (~21 moves at ~2 budget/move). Place the level's 2
  single-use X-boxes so a long isolated corridor (e.g. an L3 delivery corridor far from any X-box)
  is entered with a FULL bar. This rule is what lets a multi-leg level (L2/L3) be solved without
  ever dying; ignoring it cost two GAME_OVERs on L4 this session before it was understood.
- **Sources**: [overdraft ← trace/exploration_tree.yaml:N38 «budget 0 + another move → respawn to start, budget 0->42, %% -4» [result]; game-over ← trace/exploration_tree.yaml:N39 «a death while %%=0 → state=GAME_OVER, harness exits» [result]]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: high
- **Code ref**: [harness/scratchpad/nav.py, harness/status.py]

## H12: Plan refills around the X-box LAYOUT before descending into a far corridor — single-use boxes can strand you at the last life
- **Rationale**: The 2–3 X-boxes per level are single-use per life (H08) and are often spatially
  CLUSTERED, so a naive "refill when low" rule can leave the block in a corner with budget→0 and
  no UNCONSUMED X-box within reach. At %%=4 (the last life, C12) this is fatal: an overdraft is a
  TERMINAL GAME_OVER, not a respawn, so there is NO recovery — the run is lost to a full restart.
  Operating rule: before committing to any leg, BFS the shortest path to the nearest UNCONSUMED
  X-box and never let the bar reach a value below that distance × the per-move budget rate. Spend
  the level's X-boxes so that the LAST refill is positioned to cover the longest isolated corridor
  (the delivery corridor) with margin, and do not consume a near X-box early if a later leg will be
  far from any other. Equivalently: keep a guaranteed refill path at ALL times, and treat %%=4 as a
  zero-margin state where every move must preserve that path. This is the N57 dead-end lesson
  (sharpens H11 with the spatial/single-use dimension).
- **Sources**: [corner ← trace/exploration_tree.yaml:N57 «budget 3, %%=4, both surviving X-boxes 7 moves away, (9,1) consumed → unrecoverable GAME_OVER»; budget-rate ← trace/exploration_tree.yaml:N55 «L6 budget rate = 1/move»; single-use ← logic/solution/heuristics.md:H08]
- **Status**: active
- **Provenance**: ai-executed
- **Sensitivity**: high
- **Code ref**: [harness/scratchpad/drive.py, harness/status.py]

## Movement quantum (note)
The board is effectively a 12×12 grid of 5×5 macro-cells; the block snaps one macro-cell per
press, and walls (color-4 `=`) block movement (a move into a wall = 0 cells changed; see C04).
Use `harness/macro.py` for the 12×12 maze map, `harness/pathfind.py` for routing, and
`harness/status.py` for block-pos + panel + budget.
