# Constraints — NOVELTY LANE (isolated sub-namespace inside the single ara/)

> **wave: novelty | isolation: hard.** Current best understanding of the boundary conditions
> the novelty wave operates under. These are the wave's *additional* rules layered on top of
> the shared t=0 lawful core (`logic/concepts.md` "Lawful core", `logic/solution/constraints.md`
> in the lineage frame — NOT read here). Crystallized only on a closure signal; mutable.

## NVC01: The novelty bar — every submitted recipe needs >=1 non-arXiv idea
- **Statement**: Every SUBMITTED recipe must contain at least one idea NOT published on arXiv.
  Published optimizers / schedules / inits may be used as inspiration only; porting a published
  method and merely tuning its hyperparameters does NOT satisfy the mission (it fails). This is
  an always-on constraint on top of the same lawful-core / benchmark rules as v1.
- **Provenance**: user
- **Scope**: Applies to every candidate before it can be a submission/result; does not restrict
  diagnostics in `scratchpad/variants/`.
- **Crystallized via**: artifact-commitment — this turn the bar was actively enforced (ideas
  killed for reducing to arXiv priors; see NV07) and the arXiv check was retained as evidence.
- **Bound to**: NV01, NV07
- **Tags**: novelty-bar, lawful-core-extension, submission-gate

## NVC02: Pre-runtime arXiv novelty-existence check (retained as evidence)
- **Statement**: Every submitted idea must PASS an arXiv novelty-existence check (a subagent
  literature search) BEFORE the run executes, and the search is retained as evidence. The
  novelty check is a pre-runtime gate on submissions, not a post-hoc note. A `not-novel` return
  kills the idea before any code is written.
- **Provenance**: user
- **Scope**: Pre-code gate; the kill note (the reduction to the prior) is itself the recorded
  contribution for a killed idea.
- **Crystallized via**: artifact-commitment — dozens of arXiv checks were run this turn and
  retained under `scratchpad/ideas/*.md`; many ideas were killed on their return (NV07).
- **Bound to**: NV01, NV02, NV07
- **Tags**: novelty-bar, arXiv-gate, pre-runtime, evidence-retention

## NVC03: TWO-GATE pre-submission protocol (rule/architecture + arXiv) before any code
- **Statement**: Every new generated idea must pass BOTH (a) a benchmark-rule/architecture
  compliance subagent AND (b) the arXiv novelty-existence subagent (NVC02) BEFORE any optimizer
  code is written. The compliance gate must confirm the idea stays within
  optimizer/init/LR/WD-schedule surfaces and does NOT alter architecture (including
  softcap/logit-cap), data, batch, sequence length, validation, or one-forward-backward
  semantics. Either gate failing kills the idea pre-code.
- **Provenance**: user
- **Scope**: Refines NVC01/NVC02 into a two-subagent gate; triggered by the clarification that
  softcap/logit-cap changes are architecture changes and therefore out of scope.
- **Crystallized via**: verbal-declaration (first-person standing rule) + artifact-commitment
  (every subsequent idea this turn carries a rule_check and an idea/novelty evidence file;
  retrospective audit passed the first batch).
- **Bound to**: NV02
- **Tags**: two-gate, compliance, architecture-frozen, softcap-out

## NVC04: Refined novelty bar — only materially NON-ADDITIVE optimizer-level interactions count
- **Statement**: optimizer+schedule and schedule-only combinations are NOT novel even when the
  schedule is signal-driven. An optimizer-level combination counts as novel ONLY when one
  optimizer mechanism's OUTPUT materially shapes another mechanism's behavior, AND that
  interaction is materially NON-ADDITIVE. Disqualified: a coupling that (i) reduces to a scalar
  Nesterov/de-Nesterov blend `(1-c)N + cD`, (ii) is an exact-polar identity/no-op (e.g.
  `offdiag` of a diagonal = 0, or `U^T U = I` so commutator terms vanish), or (iii) merely
  re-points an existing actuator to a new source/target (source/formula swap). optimizer+schedule
  remains non-novel plumbing.
- **Provenance**: user
- **Scope**: Tightens NVC01 for the optimizer-combination case; this is the binding filter that
  killed most surviving ideas pre-code once arXiv-obvious priors were exhausted.
- **Crystallized via**: verbal-declaration (first-person, stated twice) + artifact-commitment
  (9 families — alr/stm/cdm/dsl/mhs/wdi/zpb/wdr/rzb — became promotion-ineligible and 3 active
  plumbing jobs ZPB/WDR/RZB were cancelled; subsequent kills NV06/NV08 cite this bar).
- **Refines**: NVC01 (same user, a tightening — not a contradiction)
- **Bound to**: NV05, NV06, NV08
- **Tags**: novelty-bar, non-additive, optimizer-level, schedule-is-not-novel
