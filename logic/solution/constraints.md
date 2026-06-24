# Constraints

> **t=0 FRAME.** The boundary conditions, assumptions, and rules in force at the start of the
> experiment — all time-invariant (the benchmark and lawful core are fixed for the whole run).
> No discovered limitation of any recipe appears here; method-specific limitations crystallize
> later through the replay.

## Boundary conditions (frozen benchmark — lawful core rule 1 + "Hard rules — benchmark")
- **Architecture is fixed**: same model as `train_gpt_simple.py` — no architecture changes (no
  value embeddings, no skip-lambda gymnastics, no attention-pattern changes). See
  `src/environment.md` for the frozen architecture.
- **Data and batch are fixed**: same dataset (FineWeb 10B shards) and same batch size
  (524288 tokens/step); no data changes, no batch-size changes.
- **One forward-backward per step**: no gradient-accumulation tricks, no multi-step inner loops.
  The step is the unit `step_to_3.28` counts.
- **Success threshold**: a run must reach **val loss ≤ 3.28** to count; a run that does not is a
  failed candidate, never a "look how few steps" win.
- **Tunable surface only**: modifications are confined to the `Optimization` and
  `Init & Optim Hyperparams` sections. Init scaling and optimizer-schedule changes are fair
  game; the optimizer itself (any), per-parameter-group HPs, schedules, and init scale are
  in-scope.
- **Hardcoded HPs**: any *submitted* result hardcodes its hyperparameters in the script — no
  CLI args. Diagnostic instrumentation of the training loop is allowed, but submitted runs use
  the canonical script.
- **Diagnostics are quarantined**: experimental code that breaks any benchmark rule lives in
  `scratchpad/variants/` for diagnostics only and is never submitted as a result.

## Lawful-core constraints on the search process (always law — AGENTS.md "Lawful core")
- **Noise-floor gate** (rule 2): no candidate is "passing" without ≥ 2 seeds AND beating the
  prior best by ≥ 2× the noise floor.
- **Stuck detector** (rule 3): at 30 consecutive runs in one family without a `step_to_target`
  improvement, the family is ruled out and the agent pivots (a "noise floor or pivot?" check
  fires earlier, at 15).
- **Slug-stack ≤ 3 modifiers** (rule 4): a 4th modifier defines a new family — rename, reset
  the stuck-counter, fresh picklist entry. The family is the slug prefix, not the full string.
- **Two-seed reproduction** (rule 5): required before any new "best" is recognized.
- **Mandatory pruning before submission** (rule 6): a pre-submission pruning round is required;
  a modifier is dropped only on a 2-seed mean inside ±0.5× the noise floor (single-seed pruning
  is itself overfitting), and the post-pruning recipe must re-clear the noise-floor gate before
  submission.

## Assumptions (from goal.md)
- **Wallclock-irrelevant**: methods slow per step are acceptable if they cut the step count
  (full-matrix preconditioners like Shampoo / SOAP are fair game).
- **Compute**: 1 node, 8×{H100,H200}, ~15 min per run, one run at a time, no calendar deadline;
  effectively unlimited wall-clock.
- **Variance is real**: nothing under ~50–100 steps is treated as signal until reproduced.
- **Paper-default LRs are untrustworthy here**: e.g. AdamW LR at this scale wants ~4–8e-3, not
  the canonical 3e-4 — HP sweeps are first-class.

## Known limitations
- _None recorded at t=0._ The agent has run no experiments; method-specific limitations,
  failure modes, and ruled-out families crystallize later through the replay.

## Out of scope (from goal.md)
- Architecture changes; batch-size or data changes; multi-step inner loops / grad-accumulation
  tricks; anything that violates the benchmark hard rules.
