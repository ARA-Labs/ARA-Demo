# Method — the search methodology

The reusable *process* by which the agent turned an enormous, noisy optimizer search space into
three significance-validated submissions and one honest negative result. The recipes themselves are
in [optimizer-stack.md](optimizer-stack.md); the discipline that makes them trustworthy is here.

## The autonomous loop

The agent runs without human turns: it re-reads `goal.md`, mutates `plan.md` as a living workspace,
and appends every significant moment to `scratchpad/THREAD.md` (`../../v1/codex/AGENTS.md:8-9`,
`297-302`). It is told to **pick a direction and log *why*, never wait** for confirmation
(`../../v1/codex/AGENTS.md:42-49`). Context is protected by spawning subagents "ULTRA frequently"
— one paper = one subagent, one sweep = one subagent — so raw logs never flood the orchestrator
(`../../v1/codex/AGENTS.md:51-66`). Throughput is multiplied by fanning parallel runs into a
`preempt` Slurm partition behind an idle-node gate (`../../v1/codex/AGENTS.md:230-273`).

## The four-step credibility pipeline

Every candidate passes the same gauntlet; this is what separates signal from seed noise.

1. **Screen at a fixed budget.** A new optimizer/lever is first tested at a fixed step budget
   against the **3500-step Muon bar** (`../../v1/codex/AGENTS.md:334`), with a pre-declared kill
   criterion. HP sweeps are first-class: coarse log-spaced LR, refine around a peak, then WD, then
   schedule shape (`../../v1/codex/AGENTS.md:338-355`).
2. **Reproduce before believing.** Variance is real; nothing under 50–100 steps is signal until
   re-run on a different seed (rule 5, [C05](../claims.md)). Single-seed wins seed a *second seed of
   the same recipe*, never a new modifier (`../../v1/codex/AGENTS.md:165-167`).
3. **Walk the frontier by `train_steps` only.** Once a recipe is verified, the step frontier is
   descended by copying that exact parent and changing *only* `train_steps` — never re-tuning knobs
   on a working low-step file — so each lower bin is attributable to the budget, not a confound
   (`../../v2/codex/scratchpad/THREAD.md` `rolewd`/`lookahead` walks).
4. **Prune, then certify.** Before submission: a mandatory leave-one-out pruning round (rule 6)
   quantifies each component's `Δval when removed` and drops the redundant ones; then the
   post-pruning recipe must clear the **fixed-cohort significance gate** `(3.28−μ)·√n ≥ 0.004` over
   n=16 seeds, with an anti-"val-spam" same-checkpoint scan choosing the earliest common passing
   checkpoint as the bin ([C06](../claims.md), [C07](../claims.md)).

## Why each discipline exists (the failure it prevents)

| Discipline | Failure it prevents | Claim |
|---|---|---|
| Schedule-horizon decoupling | Wasting the schedule's warm-LR headroom by matching cooldown to a shorter run | [C01](../claims.md) |
| Two-seed reproduction | Promoting a favorable-seed crossing as a "win" | [C05](../claims.md) |
| Fixed-cohort significance gate | P-hacking a single low-tail crossing into a submission | [C06](../claims.md) |
| Leave-one-out pruning | Carrying dead modifiers until the recipe is unattributable; submitting an unnecessarily complex stack | [C07](../claims.md), [C11](../claims.md) |
| Compliance audit + quarantine | Anchoring the frontier on an illegal (forward-path-changing) inherited parent | [C08](../claims.md) |
| Novelty + arXiv pre-code gates | Re-inventing a known optimizer or running an algebraic no-op | [C12](../claims.md) |

## The four waves as a methodological arc

- **v1 — breadth then compression.** Screen the post-Muon optimizer space wide (NorMuon, Muon2F,
  Adam-mini survive; dozens ruled out as clean negatives), discover the schedule-horizon lever, and
  compress with tail-EMA. Submitted bin **3205**.
- **novelty — isolation stress test.** Hold the agent to genuinely-new mechanisms under hard
  isolation; the negative result ([C12](../claims.md)) is the methodological finding that a
  saturated track defeats novelty-as-a-constraint. Isolated subtree:
  [../novelty/novelty.md](../novelty/novelty.md).
- **v2 — inheritance hygiene then role structure.** Test an inherited parent, catch and quarantine
  its non-compliance, rebuild compliant, then exploit role-specific LR/WD + lookahead. Submitted bin
  **3037**.
- **v3 — reproduce, search, simplify.** Reproduce the public radial/Soft-Muon/SOAP frontier, run a
  long mechanism search to the sub-2900 boundary, then *simplify* via W258 leave-one-out to the
  submitted **nosphere** stack. Submitted bin **2949**.

The through-line is that the *largest* recurring wins are methodological (schedule decoupling,
significance gating, pruning) and the *content* wins (tail-EMA, factorized preconditioning,
role-LR, radial brake, SOAP sidecar) are each found, reproduced, and pruned under the same gauntlet.
