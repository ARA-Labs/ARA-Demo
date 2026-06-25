# Constraints, Limitations, and the Lawful Core

This work is governed by hard benchmark rules and a self-imposed "lawful core" of research
discipline. These constraints are load-bearing: they are *why* the submitted numbers are
trustworthy and *why* several promising results were discarded.

## Benchmark hard rules (always binding)

From `../../v1/codex/AGENTS.md:275-291` (sourced from the track README). A submitted run that
violates any is invalid regardless of its score:

1. **Fixed contract.** Same dataset, batch size, and architecture as `train_gpt_simple.py` — no
   architecture, batch-size, or data changes.
2. **One forward-backward per step.** No grad accumulation, no multi-step inner loops.
3. **Must reach 3.28 val loss to count.** A run that doesn't is a failed candidate, not a "look how
   few steps" win. Every counting submission is a starting line, never a finish line.
4. **Change only `Optimization` and `Init & Optim Hyperparams`.** Init scaling and optimizer
   schedule changes are fair game; forward/normalization code is not.
5. **Hardcoded HPs** in the script for any submitted result — no CLI args.

Diagnostic code that breaks any of these lives in `scratchpad/variants/` and is **never** submitted
(`../../v1/codex/AGENTS.md:290-291`). The v2 quarantine ([C08](../claims.md)) is rule 1/4
enforcement: an inherited `RMSNorm.forward` change is a forward-path edit, so every derived result
was disqualified even though it helped.

## The lawful core (always-binding research rules)

From `../../v1/codex/AGENTS.md:11-28`. "The rest of the doc is default, not law" — these six are law:

1. **Benchmark hard rules** (above).
2. **Noise-floor gate.** No candidate is "passing" without 2 seeds AND ≥ 2× the noise floor over
   the prior best.
3. **Stuck detector.** 30 consecutive runs in one family without a `step_to_target` improvement ⇒
   the family is ruled out and the agent pivots.
4. **Slug-stack ≤ 3 modifiers.** A 4th modifier means a new family (fresh stuck counter).
5. **Two-seed reproduction** before any new "best" is recognized.
6. **Mandatory pre-submission pruning.** A modifier is dropped only on a 2-seed mean inside ±0.5×
   the noise floor (single-seed pruning is itself overfitting); the post-pruning recipe must clear
   the noise-floor gate as if new before submission.

The submitted records reflect these: each is an n=16 cohort cleared under the significance gate
(rule 2 generalized to [C06](../claims.md)), and each wave ends in a leave-one-out pruning round
(rule 6 → [C07](../claims.md), [C11](../claims.md)).

## Scope (in / out)

**In** (`../../v1/codex/goal.md:63-72`): any optimizer change; per-parameter-group HPs, schedules,
init; LR/WD/β/ε/momentum sweeps; schedule shape (warmup, decay, WSD, cosine, trapezoid,
multi-stage, schedule-free); init scale and per-module init; diagnostic-only instrumentation
(submitted runs use the canonical script with HPs hardcoded).

**Out** (`../../v1/codex/goal.md:73-78`): architecture changes (value embeddings, skip-lambda,
attention-pattern changes); batch-size / data changes; multi-step inner loops / grad-accumulation
tricks; anything violating the track README.

## Limitations of this artifact's evidence

- **L1 — Pruning deltas are small-n leave-one-out estimates.** v1/v2 pruning cohorts are n=8; v3
  ranges n=3–16. The smallest per-component contributions (e.g. v1 `noBeta2Thaw −0.00001`,
  `noResPulse −0.00007`) sit within their own seed noise; treat the *ranking of the large bars* as
  the signal, not the exact tail values.
- **L2 — The journal trails the submission.** Each `THREAD.md` is an append-only point-in-time log
  that can end before the final pruning-rerun/submission; the canonical numbers are in
  `record_configs/`. The clearest instance: v1's journal settles provisionally at `s3220`/`s3170`
  (3170 *rejected* by the gate), while the submitted v1 record is **3205**, produced by a later
  pruning-rerun captured in `record_configs/` + `pruning_data.json` rather than in the journal.
- **L3 — Recipe constants live in configs, not journals.** Several exact submitted constants (v2
  role-LR vector, lookahead step/interval/α/pull, embed init ×0.7; v3 V-SOAP blend 0.95, LACV
  timing windows, CGI α, di-fc α) are stated in the `record_configs/*/README.md` and the launched
  scripts, **not** in the `THREAD.md` journals. They are grounded here against the record READMEs;
  where a value appears only in the launched scripts it is marked as such in
  [optimizer-stack.md](optimizer-stack.md).
- **L4 — Single benchmark, single model scale.** All claims are scoped to this 124M-GPT FineWeb
  speedrun near the 3.28 threshold; none is established at other scales, datasets, or loss targets.
- **L5 — Wall-clock excluded by design.** Per-step cost is irrelevant to the metric
  (`../../v1/codex/goal.md:33-34`); slow preconditioners (SOAP/Shampoo) are admitted purely for
  step-count, so the recipes are *not* wall-clock-competitive optimizers.
- **L6 — Cross-agent inheritance.** Parts of the lineage touch another agent's output (cc v12, v48)
  and public PRs; these are attributed (RW11, RW12, RW02–RW08) and, where non-compliant,
  quarantined ([C08](../claims.md)). The only *hard-isolated* wave is novelty.
