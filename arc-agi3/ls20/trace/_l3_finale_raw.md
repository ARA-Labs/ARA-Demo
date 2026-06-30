# L3 finale raw notes — 2026-06-29 session 001 (continuation)

## Baseline (fresh L3 after RESET, turn ~697)
- Block real pos R9C2 (macro), moved up to R8C2 after A1. Macro col band = (c-4)//5.
- Panel baseline = 111/001/101 (colour-c/N). [confirmed]
- Key-box RIGHT target = 101/100/111 (colour @/9). [confirmed]
- Colour selector R9C5 glyph @$$/@ %/NN%; pattern switch R2C9; %%=12; budget=42.
- Align recipe (O05): 1 colour step-on (c->@) at R9C5 + 2 pattern step-ons at R2C9.
- Deliver: route to R8C10 (above right key-box via col-10 from above), press DOWN = 186-cell delivery, %% -4, block resets to start, panel resets to baseline, budget refills 42.
- WALL (O07): deliveries #1,#2 wedge clean; #3 slides 54-cell -> GAME_OVER, levels stays 2.

## Hypotheses to test for 3rd delivery
H1: lock must be RE-ALIGNED before each delivery (target pattern/colour CHANGES after #1/#2).
H2: 3rd delivery uses different slot/entry side.
H3: per-stage colour/pattern requirement (3rd state).
H4: hidden precondition / different approach side.

## Plan: deliver #1, #2 normally; BEFORE #3 diff the key-box @ symbol AND panel target vs baseline; inspect board for moved/new boxes.

## Log:

### Delivery #1 align (turn ~720)
- Navigation note: pathfind/detectors have +1 col ambiguity; reliable method = move one macro at a time, detect block by color-9>=12 macro cell, verify panel/glyph effect. The block-detector falls back to R11C0 artifact when block overlaps a UI cell (selector/keybox).
- Stepped block down col5 onto selector R9C5: panel FILL colour c->@ confirmed (panel now 111/001/101 in @). Pattern still baseline. Need 2 pattern step-ons at R2C9 to reach 101/100/111.

### MAJOR REFRAME (turn ~72, on L2 levels_completed=1)
- Harness died (SIGINT) mid-session; restarted fresh. Re-won L1 (R-L1, 2-push delivery confirmed). Now on L2.
- KEY: L2 in THIS session ALSO has the %%-multi-delivery + X-box + dual-panel mechanic (not the simple single-delivery in old R-L2). The mechanic appears UNIFORM across L2/L3.
- Built robust navigator scratchpad/step.py: single-action + re-pathfind each step + block-detector requires BOTH color-9>=6 AND color-c>=4 (uniquely IDs block vs panel). This fixed the +1 desync that plagued prior sessions. Works flawlessly.
- Pattern switch confirmed at macro R9C9 (color-0/1 floor speck), 4-state cycle (H06): 111/001/101 -> 101/001/111 -> 101/100/111 -> 111/100/101. L2 target = 111/100/101 (state4). Toggle = step OFF to adjacent floor then ON; each step-ON advances one state.
- Left key-box delivery target = 111/100/101 at macro R7-9 C1-2.
- DELIVERIES FIRED during play: %% 12->8->4 (two deliveries) as block moved while panel aligned. After each delivery: block teleports to start, panel RESETS to baseline 111/001/101, budget refills. CONFIRMS O06.
- NOW AT 3rd/FINAL delivery (%%=4). Block@R6C2 above left box. Panel=baseline 111/001/101 (NOT aligned). 
- HYPOTHESIS H1 (re-align before each delivery) is the leading candidate: panel resets after every delivery, so the FINAL push needs a FRESH re-alignment. Testing now: align to 111/100/101 then push down into box.

### BREAKTHROUGH on delivery mechanism (turn ~100, L2, fresh after RESET)
- DELIVERY FIRES AT THE SWITCH: with panel aligned to target (111/100/101) and block ON switch R9C9, the FIRST move OFF the switch (e.g. ACTION1 up) instantly triggers delivery: block consumed -> teleport to start R8C5, panel resets to baseline, %% -=4. The block NEVER travels to the left key-box; the "key-box @" is just the TARGET-PATTERN DISPLAY.
- So each delivery = (align at switch) + (step off). Deliveries #1,#2 OK. #3 (%% 4->0) = GAME_OVER (loss) despite same align+step-off.
- => H1 'must re-align each time' is NECESSARY (panel resets) but NOT SUFFICIENT. The 3rd delivery needs something else. Now checking H3: does the TARGET pattern/colour change for the final delivery? Inspecting key-box @ symbol before delivery #3.

### FINAL-DELIVERY SIGNATURE NAILED (turn ~318, L2)
- Deliveries #1/#2 (switch-delivery): align panel to 111/100/101 ON switch R9C9, step off (any dir) -> block TELEPORTS to start (8,5) [new block spawned], panel RESETS, big redraw, %% -=4. SUCCESS.
- Delivery #3 (%% 4->0): SAME align + step-off-up -> only 54-cell move, block goes R9C9->R8C9 (NO teleport, NO new block), panel stays aligned, %%=0, state=GAME_OVER. levels stays 1.
- INTERPRETATION: switch-delivery spawns a replacement block each time. At %%=0 there's no spawn and no win -> the switch is a FEEDER, not the winning deposit. The WIN must be the block entering the actual LEFT KEY-BOX (R7-9 C1-2, target 111/100/101) on the final stage.
- NEXT TEST: do 2 switch-deliveries (%%->4), then for the 3rd drive the block INTO the left key-box (approach R6C2, push down) instead of stepping off the switch. Need the panel aligned for the box too.

### COMPREHENSIVE CHARACTERIZATION (turns ~100-913)
Note: harness restarted FRESH this session (levels 0). Re-won L1. Got STUCK on L2 — which now exhibits the SAME %%-multi-stage delivery wall as L3. The old simple-box R-L2 recipe NO LONGER WORKS (game/level variant changed). So the 3rd-delivery wall is UNIFORM across L2 & L3.

DELIVERY MECHANISM (L2, fully mapped, deterministic):
- ONE switch only (R9C9, color-0/1 speck). ONE block. ONE left key-box (display only).
- 4-state pattern cycle on step-ON (H06): 111/001/101 -> 101/001/111 -> 101/100/111 -> 111/100/101 -> (back). Step-OFF never cycles.
- DELIVERY = block ON switch + panel == target (111/100/101) + step OFF (ANY direction) => block teleports to start, panel resets to baseline, budget refills, %% -=4, BIG redraw. Works for %% 12->8 and 8->4.
- FINAL (%% 4->0): identical align + step-off => NOT a teleport, just a 54-cell normal move (R9C9->R8C9), panel stays aligned, %%=0, state=GAME_OVER, levels unchanged. THE WALL.
- Step-off when panel NOT aligned (states 1/2/3) = normal move, NO delivery, %% unchanged, panel state PERSISTS.

HYPOTHESES TESTED & FALSIFIED:
- H1 (re-align each delivery): NECESSARY (panel resets after each) but NOT sufficient — #3 aligned correctly and still GAME_OVER.
- H3 (target changes for stage 3): FALSE — box @ target stays 111/100/101 at %%=12/8/4; board byte-identical between %%=12 and %%=4 except block & %% counter (full-board diff = empty).
- H2 (different slot/opening for #3): FALSE — no board change, no new opening; only one switch, one box.
- Direction of final step-off: A1/A2/A3/A4 all GAME_OVER.
- Budget: irrelevant (deliveries fire at budget 0 too).
- BOX-DELIVERY path: box is LOCKED unless panel aligned (push gives 0 cells when unaligned). But the exact target 111/100/101 is UNCARRIABLE to the box: aligning requires the block ON the switch, and ANY step-off-while-aligned triggers the switch-delivery (teleport) — so an aligned block can never travel to the box. Carried non-target states (e.g. state3 101/100/111) reach the box but the box rejects them. Maze topology funnels return routes back through R9C9, resetting carried panel state. Box does NOT remember alignment across a delivery.

NET: the switch-delivery is the only target-aligned delivery channel; it succeeds twice then GAME_OVERs on the %%->0 transition. The intended winning final action remains UNKNOWN.

REFINED HYPOTHESES FOR NEXT SESSION:
- R1: There may be a SECOND control (a colour selector like L3's R9C5, or a 2nd switch) that must be set ONLY for the final stage; re-scan the whole L2 board for any color-0/1 speck OR compound glyph beyond R9C9 at %%=4 specifically (some controls may appear only at a given %%).
- R2: The win may require the block to be physically IN the box at the %%->0 moment, achievable only if there's a way to align the box independent of the switch (un-found control) — search hardest for that.
- R3: Possibly the final delivery must be done from the OTHER cycle direction or a HALF-state (the cycle has 4 states; maybe stage-3 target is a 5th/colour variant). Sample the switch >8 presses to confirm period-4 with no hidden 5th state.
- R4: Try NOT emptying %% — e.g., win via box delivery while %%>0 (do 0 or 1 switch-deliveries then box). Need the box-align breakthrough first.
- TOOLING WIN: scratchpad/step.py (single-action + re-pathfind + 9&c block detector) fully fixes the +1 desync; reuse it. Promote O08 navigation heuristic.

ROBUST TOOLING NOTE: block detector = macro cell with BOTH color-9>=6 AND color-c>=4 (distinguishes block from panel/UI). pathfind+macro.py have a +1 col display ambiguity; single-step re-pathfind neutralizes it.
