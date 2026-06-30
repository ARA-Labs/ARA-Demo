# Problem

## Goal

Play and solve the ARC-AGI-3 game `ls20` (Locksmith) by **inferring its mechanics from
live play under a move budget**. The agent is given no rules — only directional actions
(A1–A4), a reset, and the rendered frame each turn. It must discover the forward model
(what each action does), the win condition, and a reusable solution recipe purely by
pressing actions and diffing frames, while spending as few budget units as possible.

## Setting

- Board: 64×64 grid, 16 colors, effectively a 12×12 grid of 5×5 macro-cells.
- The agent steers a single movable `block` with 4 directional actions through a walled maze.
- A bottom budget bar depletes per action; running out ends the attempt. RESET restarts the
  current level (keeps `levels_completed`, refreshes budget).
- The game is a curriculum: earlier levels teach primitives; later levels recombine them.
  The thesis is that an ARA accrued on early levels is a prior that lets the agent solve
  later levels faster than cold exploration.

## Success criterion

A move drives `levels_completed` up by 1 (observed as a full-screen redraw). Levels 1 and 2
were solved live; Level 3 is reconnoitered but unsolved (budget exhausted this session).

## Provenance

Empirically-observed-by-play = `ai-executed`; inferences not yet pressed = `ai-suggested`.
