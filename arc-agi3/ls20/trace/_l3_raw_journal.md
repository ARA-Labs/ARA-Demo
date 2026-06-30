# L3 raw journal (scratch)

## Initial state (turn 152)
- levels_completed=2, budget=42, block@macro R9C1 (color-9 @@@@@ block, scr rows47-49 cols9-13).
- Panel (bottom-left, color-c N, scr rows55-60 cols3-8) = 111/001/101
- Target (key-box RIGHT, color-9 @, scr rows51-53 cols53-55) = 101/100/111
- All 3 rows differ. (recon O01 said panel 101/001/101 — row1 was misread; actual 111/001/101)
- Compound control glyph scr rows46-48 cols29-31 = `@$$ / @ %% / NN%` at macro R9C5.
- X-boxes (color-b): scr rows16-18 cols34-36 (~macro R3C6), scr rows31-33 cols19-21 (~macro R6C3). 
- Plan: sample control cycle per C10 before any toggle commitment.

## Moves log

## L3 control SAMPLED (turns 83-? after restart; new scorecard afd9abd1)
- Harness had died (SIGINT at turn 152 prior session). Restarted main.py --agent=ccrelay; game reset to L1.
- Speed-ran L1 (R-L1: switch R6C3 flips mid row -> deliver UP x2 into top-center keybox; win turn13) and L2 (R-L2: switch R9C9 3 step-ons via cycle, X-box refills R10C7/R3C2, deliver R6C2 DOWN x2; win turn58). Both recipes transferred cleanly.
- L3 reached fresh turn58, budget42.
- COMPOUND CONTROL @ macro R9C5 (glyph @$$/@ %%/NN% = colors 9/e/8/c) is a 4-COLOR SELECTOR, NOT a pattern switch.
  Sampled 6 step-ons (C10!): panel FILL COLOR cycles N(c)->@(9)->$(e)->%(8)->N(c)->... period 4. PATTERN 111/001/101 UNCHANGED by it.
  One press alone would have falsely read 'c->9 flip' -> C10 vindicated again.
- Panel pattern 111/001/101 (fixed by color-control) != target pattern 101/100/111. Target drawn in color-9 @.
  => need a SEPARATE pattern switch. Candidate: faint color-0/1 speck cluster at macro R2C9 (scr rows11-13 cols49-51).
- Plan: refill R6C3, sample R2C9 speck to learn pattern cycle, then set pattern=101/100/111 AND color=@(9), deliver into RIGHT keybox.

## L3 BOTH controls fully sampled — solution understood
- PATTERN SWITCH @ macro R2C9 (faint color-0/1 speck, scr rows11-13 cols49-51). Approached from R2C10 going LEFT.
  Cycles pattern (period 4, SAME cycle as L2 H06): 111/001/101 -> 101/001/111 -> 101/100/111 -> 111/100/101 -> (back).
  TARGET pattern 101/100/111 = state #2 => 2 step-ons from baseline.
- COLOR CONTROL @ macro R9C5: cycles fill color c->9(@)->e($)->8(%)->c, period 4.
  TARGET color = @ (9, the key-box color) => 1 step-on from baseline.
- L3 = TWO independent controls (pattern + color), unlike L1/L2 (pattern only). Both must be set, then deliver RIGHT.
- Budget note: a move at budget 0 STILL executes (and an X-box still refills) — budget 0 is not a hard stop for the next single move.
- Plan: RESET to baseline, then: 2x pattern-switch step-ons (R2C9) + 1x color step-on (R9C5) + deliver into RIGHT key-box. Use X-box refills (R3C6, R6C3) to fund.

## L3 is MULTI-STAGE (key discovery, turn 173-174)
- Aligned panel = target (pattern 101/100/111 + color @) then routed block to R8C10 (above RIGHT key-box) and pushed DOWN.
- First A2 push = 186-cell change = DELIVERY SUCCEEDED. But it did NOT win the level. Instead:
  block teleported back to START (R9C1), panel RESET to baseline (111/001/101, color N/c), budget refilled (0->40),
  and the %%-marker counter (color-8 cells, bottom-right row61-62, grouped +%%+%%+%%) dropped 12 -> 8.
- => L3 needs MULTIPLE deliveries. %%-marker = stage/delivery counter: 12 = 3 stages (4 cells each). 1 done, 2 to go.
- Target is IDENTICAL each stage (101/100/111 @). So repeat the SAME recipe per stage:
  color: 1 step-on R9C5; pattern: 2 step-ons R2C9; deliver: to R8C10 then 1x A2 DOWN (186-cell push delivers).
- Delivery here is ONE effective push (the 186-cell change), not the L2 two-push (H09 is L2-specific).
- Important nav note: pre-planned long routes desync (macro display vs pathfind have a +1 col offset, and a wall-hit strands the block). Always RE-PATHFIND from current pos and execute short verified segments.

## L3 NOT SOLVED — the 3rd-delivery wall (reproduced x3, deterministic)
- Full lock recipe WORKS: per delivery, set color=@ (1 step-on R9C5) + pattern=101/100/111 (2 step-ons R2C9), route to R8C10, push DOWN once = 186-cell DELIVERY (block consumed, teleports to start, panel resets to baseline, budget refills to 42, %% counter -4).
- %% counter (color-8 cells bottom-right, +%%+%%+%% = 3 markers x4 cells = 12): decremented ONLY by deliveries (X-box refills do NOT touch it; verified). 12 -> 8 -> 4 over deliveries #1,#2.
- THE WALL: delivery #3 (when counter would hit 0) is NOT a 186 wedge — the block SLIDES through R8C10 -> R9C10 (only 54-cell change) and the game goes GAME_OVER with levels_completed STILL 2 (a LOSS, not a win). Reproduced 3x identically. Box geometry/approach corridor look UNCHANGED after 2 deliveries; budget=0 at push is NOT the cause (deliveries #1/#2 also pushed at budget 0 and wedged fine).
- => 2 of 3 deliveries land cleanly with the SAME target, but the finale needs something different I could NOT determine within budget: candidates = (a) the 3rd slot wants a DIFFERENT panel target (pattern and/or color) than 101/100/111@, (b) a different box-entry side once 2 slots are filled, (c) a hidden precondition. Box `@` always *displayed* 101/100/111 though.
- STATUS: L3 unsolved. Game left RESET clean (counter 12, budget 42, levels_completed 2).
