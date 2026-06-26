# Constraints, limitations & scope

## The lawful core (always binding)

Six rules govern every wave; a run, candidate, or claim that violates one is invalid regardless of what
else it achieved. [src: `v1/codex/AGENTS.md:11-28`]

1. **Benchmark hard rules** — same dataset, batch, and architecture as `train_gpt_simple.py`; one
   forward-backward per step; hyperparameters hardcoded; val ≤ 3.28 to count. Modifications belong only
   in the **Optimization** and **Init & Optim Hyperparams** sections.
2. **Noise-floor gate** — no candidate is "passing" without **2 seeds AND ≥ 2× the noise floor** over
   the prior best (noise floor ≈ 50 steps / ≈ 0.001 loss).
3. **Stuck detector** — at 30 consecutive same-family runs without a `step_to_target` improvement, the
   family is ruled out and the agent pivots.
4. **Slug-stack ≤ 3 modifiers** — a 4th modifier means a new family (rename, fresh stuck counter).
5. **Two-seed reproduction** before any new "best" is recognized.
6. **Pruning before submission** — a pre-submission leave-one-out round is mandatory; a modifier is
   dropped only on a 2-seed mean inside ±0.5× the noise floor; the post-pruning recipe must re-clear the
   noise-floor gate before submission.

## The compliance boundary (what "fixed architecture" binds)

The hard rules bind the **numerical forward path**, not just layer shapes. The v2 wave established (the
hard way) that a mathematically-near-equivalent rewrite of `RMSNorm.forward` or attention q-k
normalization is a **precision/behavior change** and is invalid — even though it materially helped.
After the user flag, the rule was sharpened to: *never change `RMSNorm`, attention normalization, or any
model `forward` path; build variants from the workspace `train_gpt_simple.py` and preserve forward/norm
code byte-for-byte; only Optimization and Init & Optim Hyperparams may change.* A launch-time
Architecture gate (byte-identical diff, exact RMSNorm/q-k-norm, forbidden gain/norm-path optimizer
logic) was added to enforce it. → C05. [src: `v2/codex/scratchpad/THREAD.md:126-134`]

Experimental code that breaks any hard rule lives in `scratchpad/variants/` for diagnostics **only** and
is never submitted.

## Scope

**In scope:** any optimizer change; per-parameter-group HPs, schedules, init; LR/WD/β/ε/momentum sweeps;
schedule shape (warmup, decay, WSD, cosine, trapezoid, multi-stage, schedule-free); init scale and
per-module init; diagnostic instrumentation (submitted runs use the canonical script with HPs hardcoded).

**Out of scope:** architecture changes (no value embeddings, skip-lambda gymnastics, attention-pattern
changes); batch-size / data changes; multi-step inner loops or grad-accumulation tricks; anything that
violates the track README.

**Novelty wave only (additional):** every submitted recipe must contain ≥1 idea not published on arXiv,
adjudicated by a search subagent before any run; porting a published method and tuning its HPs fails the
mission. → novelty_derivation.md, C10.

## Limitations & honest caveats

- **High variance dominates.** Per-seed variance (~50 steps) is comparable to the contested gains; many
  single-seed "wins" are low-tail singletons (C11). The submitted bins are cohort statistics, not lucky
  crossings (C06), but they remain sensitive to the σ=0.0013 / 0.004-margin convention (A3).
- **Cohort accounting differs between record and pruning.** The submitted-record cohorts (N=16, seeds
  0–15, at the record bin) and the component-pruning cohorts (N=8 at a screen step for v1/v2; the W258
  N≤16 sweep at 2949 for v3) are **different cohorts** and yield different means for the "same" stack.
  Evidence files attribute each number to its exact source; do not cross-compare them as one number.
- **Most knowledge is transferred, not invented.** v3's load-bearing mechanisms (Soft-Muon, radial,
  SOAP, power-law LR) are reproduced public PRs (related_work.md); the Codex contribution is the
  compliant composition, compression, pruning, and validation — not the mechanisms.
- **The novelty negative is bounded to this mechanism class and constraint set.** C10's structural
  emptiness holds for not-on-arXiv pre-polar Muon/init mechanisms under the wave's compound constraint;
  it is not a claim about all possible novelty.
- **The ~3000-step floor is mechanism-class-relative.** It was broken by changing the parent (C07), so
  "floor" means "for the local optimizer-only family," not a benchmark limit.
- **Wallclock is irrelevant by construction.** Slow-per-step methods (SOAP, full-matrix preconditioners)
  are admissible; nothing here optimizes wall-clock, and the step-time numbers (~145–190 ms/step) are
  recorded only for context.
