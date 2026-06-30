# L3 v2 — raw play notes (2026-06-29 session, Opus via CcRelay)

Goal: verify the level chain after the "%% L2" desync scare, then play the REAL Level 3.
Tooling: clean harness restart; robust navigator scratchpad/step.py re-created (O11 detector:
block = macro cell with BOTH color-9>=6 AND color-c>=4; single-action-then-re-pathfind).

## Setup
- Killed stale harness (was turn 982, levels=1). Clean restart: nohup uv run main.py --agent=ccrelay --game=ls20.
- Fresh frame: turn=0, state=NOT_FINISHED, levels_completed=0. CONFIRMED clean L1 start.
- NOTE the %% counter (color-8 cells rows 61-62 cols 53+, `+%%+%%+%%` = 12 cells) is present
  even on a FRESH L1 at turn 0 and stays 12 — it is a PERMANENT UI FIXTURE, not per-level.
- status.py block detector (`color-c>=5`) is UNRELIABLE on L3 (the L3 panel is colour-c N, so it
  latches the panel). step.py (BOTH color-9>=6 AND color-c>=4) located the block correctly on
  L1/L2/L3. Used step.py exclusively for block position. status.py @-panel view reads BLANK on L3
  (panel is colour-N) — read panel via raw glyphs rows 55-60 cols 3-8.

## DIAGNOSTIC — level chain verification

### L1 re-win (R-L1) — CLEAN
- Block start R9C6, panel 111/100/101 (colour @), target (key-box `@` rows 11-13) 111/001/101.
  Single switch speck at macro R6C3.
- Route: left x3 to R9C3, up x3 to R6C3 switch (step-on flips middle row 100->001, panel=111/001/101
  = target). Then up,right x3,up to R4C6 (below box), DOWN x2 (wedge + enter).
- Push 2 = 1459-cell redraw, levels_completed 0->1. ~13 moves. Budget 1/move on L1.

### L2 characterization + re-win (R-L2) — CLEAN, SIMPLE (NOT %%-multistage)
- After L1 win: block R8C5, panel 111/001/101 (@), key-box on LEFT (target `@` rows 41-43 = 111/100/101).
  ONE pattern switch speck at macro R9C9. X-boxes at R10C7 and R3C2. %% counter = 12 (fixture).
- Switch cycle confirmed (H06): 111/001/101 -> 101/001/111 -> 101/100/111 -> 111/100/101 (back).
  3 step-ons from fresh start reach target 111/100/101. Toggle = step off (left) / on (right).
- DECISIVE DIAGNOSTIC: with panel aligned (111/100/101) and block ON the switch, the ALIGNED
  step-OFF (A1 up) was a NORMAL 54-cell move — NO delivery, panel PERSISTED at target, %%=12 unchanged,
  no teleport. ==> O09's "any aligned step-off triggers switch-delivery / catch-22" is FALSE on this L2.
- Carried the free aligned block to R6C2 (above LEFT key-box), DOWN x2 (wedge R7C2, then enter).
  Push 2 = 1421-cell redraw, levels_completed 1->2. SINGLE delivery wins. X-box refills (R10C7, R3C2)
  worked: budget->42, panel persisted, %% untouched (H08 confirmed).

### DIAGNOSTIC CONCLUSION
- R-L1 and R-L2 BOTH cleanly re-won to reach Level 3. The real L2 is the SIMPLE single-delivery level.
- The prior session's "L2 became a %% multi-stage wall" (O10/N31) was a LEVEL-TRACKING DESYNC, NOT a
  changed level / variant. The %% counter is a permanent UI fixture (12 throughout L1+L2), never
  decremented by L1 or L2 deliveries. ==> N31 contradiction RESOLVED in favour of the trace's prior
  L2-solved record. O09's catch-22 framing is falsified (at least on L1/L2).

## REAL LEVEL 3 — characterization + SOLVE

### Layout (levels_completed=2)
- Block start macro R9C1 (LEFT). Key-box on the RIGHT: display K at macro R9C10 (+ R10C9-C11).
  Target `@` (colour-9) rows 51-53 cols 54-56 = pattern 101/100/111.
- Panel (bottom-left rows 55-60 cols 3-8) baseline = pattern 111/001/101 drawn in colour-c (N).
  ==> L3 lock has BOTH a PATTERN axis (111/001/101 vs target 101/100/111) AND a COLOUR axis
  (panel N=c vs target @=9). Two-axis lock (O04/O05 confirmed).
- TWO independent controls:
  (1) COLOUR SELECTOR at macro R9C5 (compound glyph @$$/@ %/NN%, colours 9/e/8/c). Step-on cycles
      panel FILL COLOUR through period-4: N(c) -> @(9) -> $(e) -> %(8) -> N. Colour persists on
      step-off. Pattern untouched. Sampled cleanly >6x.
  (2) PATTERN SWITCH at macro R2C9 (faint color-0/1 speck rows 11-13 cols 50-52; approach from
      R2C10 going LEFT). Cycles panel PATTERN through the SAME 4-state H06 cycle as L2:
      111/001/101 -> 101/001/111 -> 101/100/111(target) -> 111/100/101. 2 step-ons from baseline
      reach target. Pattern persists on non-aligned step-off. Colour untouched.
- THREE X-boxes (refills, H08): macro R3C6, R6C3, and one upper-right. %% counter = 12 (fixture).

### Two-axis break — KEY TEST (the task's hypothesis), CONFIRMED
- Set COLOUR to @ at R9C5 (1 step-on c->@; persists on step-off — verified the full N->@->$->%->N cycle).
- Carried block to R2C9, set PATTERN to target 101/100/111 (2 step-ons). Now FULLY ALIGNED
  (pattern 101/100/111 + colour @ = key-box target), block ON the pattern switch, %%=12.
- KEY TEST: ALIGNED step-OFF the pattern switch (A4 right) = NORMAL 54-cell move. NO delivery,
  pattern+colour PERSISTED at full target, %%=12 unchanged, no teleport. ==> the catch-22 is BROKEN:
  a fully-aligned block is FREE to navigate. (Same result earlier for the colour-selector step-off.)
- Carried the free fully-aligned block down col-10 to R8C10 (above RIGHT key-box), DOWN x2:
  push1 = 54-cell wedge into R9C10; push2 = 1425-cell full-screen redraw, levels_completed 2->3. WIN.

### IMPORTANT corrections vs prior staged L3 notes
- %% counter is NOT a multi-stage delivery gate. It stayed 12 for the ENTIRE L3 solve. The prior
  "%% decrements 4 per delivery, 3 deliveries needed, 3rd = GAME_OVER" (O06/O07) was a desync-era
  misreading. ONE genuine box-delivery wins L3.
- The earlier accidental "delivery" (%% 12->8, teleport) during rapid colour-selector cycling was a
  spurious/misattributed event in the chaotic cycling, NOT the intended mechanic — clean single-step
  sampling showed NO selector step-off ever delivered at any colour state.
- L3 delivery = the SAME 2-push box-delivery as L1/L2 (H09), into the RIGHT key-box at R9C10. The
  O06 "186-cell delivery, teleport, panel reset" framing is superseded.

## R-L3 recipe (crystallizable)
1. COLOUR: go to selector R9C5, 1 step-on (c->@). Colour persists on step-off.
2. PATTERN: go to switch R2C9 (approach R2C10 left), 2 step-ons -> 101/100/111. Persists on step-off.
   (Order independent; the two axes are independent.)
3. Fund with X-box refills (R3C6/R6C3/upper-right) as needed; refills don't touch lock or %%.
4. DELIVER: carry the FREE fully-aligned block to R8C10 (above RIGHT key-box R9C10), DOWN x2
   (wedge + enter) = 1425-cell redraw, levels 2->3. SINGLE delivery wins.
Provenance: ai-executed (Opus, live, this session, turns 0->141).

## Heuristic corrections
- H06 stands (pattern switch 4-state cycle; reproduced again on L3 switch R2C9).
- H09 stands (2-push box delivery; reproduced on L1, L2, L3).
- O09 (catch-22 / aligned-step-off-delivers) is FALSIFIED on L1/L2/L3 — aligned step-off is a normal
  move and the block stays aligned. The two-axis "break" is really just "there is no catch-22".
- O10 (%% governs L2 / L2 no longer wins) is FALSIFIED — desync. R-L2 cleanly re-won.
- O06/O07 (%% multi-stage L3, 3 deliveries, GAME_OVER wall) FALSIFIED — single delivery wins L3,
  %% is a fixture.

## Final state
levels_completed=3 (now on Level 4), budget 42, %%=12. Level 3 SOLVED.
