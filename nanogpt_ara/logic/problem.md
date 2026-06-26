# Problem

## Setting

`track_3_optimization` is a fixed-architecture optimizer speedrun on the modded-nanogpt
`train_gpt_simple.py` benchmark. With the model architecture, dataset, and batch size **frozen**,
and exactly **one forward-backward per step**, the objective is to reach **3.28 validation loss**
in as few optimizer steps as possible. The step count at which a cohort crosses 3.28 is the **bin**
(`step_to_3.28` / `first_step_le_3p28`); a lower bin is a better record. The benchmark is explicitly
**wallclock-irrelevant** — methods that are slow per step are fair game if they cut steps.

## Observations (with numbers)

- **O1 — The standing baselines.** The current SOTA optimizer is **Muon** (lr=0.025, wd=0.0125)
  crossing 3.28 at **3500 steps** (`baseline-muon-3500-seed0`, final val 3.27658). The **AdamW**
  baseline crosses at **5625 steps**. Anything below 3500 is progress. [src: `v1/codex/goal.md`,
  `data/.../runs.csv` baseline row]
- **O2 — Prior agents had reached the low-3000s.** At v2's start the best known parents were a
  cross-agent "v12" stack at **3025 steps** and Codex's own EMA branch at ~3195; at v3's start the
  bar was **3035 (opus v15)** and **3037 (codex)**. [src: `v2/codex/goal.md`, `v3/codex/goal.md`]
- **O3 — An empirical ~3000-step floor for optimizer-only mechanics.** The prior iteration "hit an
  empirical ts=3000 floor with optimizer-only mechanisms — Newton-Muon, Tail-EMA, AdamMini,
  Skylight, cubic Contra, and many others all came in at parity or worse." In v1, direct
  sub-3050 compression by tail/init/optimizer-state mechanics repeatedly landed ~3.29–3.30 at the
  target step. [src: `v2/codex/goal.md`; v1 trace]
- **O4 — Variance is real and large relative to the prize.** The per-seed noise floor is
  ≈50 steps on `step_to_3.28` and ≈0.001 on `final_val_loss`. A 50–100-step "win" on one seed is
  routinely inside the noise; the limiting seed (often "seed 2") fails brackets the mean clears.
  [src: `v1/codex/AGENTS.md` noise-floor section]
- **O5 — A public PR frontier existed below the local line.** The KellerJordan modded-nanogpt repo
  carried public submissions below ~2990 steps (PR #294 ≈2990, PR #291 ≈3030, PR #290 ≈3125,
  PR #288 ≈3075) built on Contra/Soft-Muon scheduling, outward-radial dampening, SOAP, and a
  power-law LR schedule. [src: `v3/codex/goal.md` "public-frontier pivot"]

## Gaps

- **G1 — Which levers actually stack vs. saturate?** The literature is "a sea of unverified SOTA
  claims"; most optimizers have never been compared head-to-head on one setup. Which post-Muon and
  pre-Muon ideas beat Muon *here*, and are their gains orthogonal or redundant when combined?
- **G2 — How do you break the ~3000-step optimizer-only floor?** Tail/init/state mechanics
  plateau near 3.29–3.30 below 3050. Is the floor a property of the mechanism class or of the
  parent it is attached to?
- **G3 — What is a *defensible* record, not a lucky crossing?** With ~50-step seed variance, when
  is a lower bin real? How many seeds, and what statistic, separate signal from a low-tail
  singleton?
- **G4 — Is there headroom under a hard novelty constraint?** If every submitted recipe must
  contain a not-on-arXiv idea, is the reachable mechanism space non-empty, or has the literature
  already occupied everything that matters?
- **G5 — What does "fixed architecture" actually bind?** When a strong parent is inherited from
  another agent, is its forward path compliant, and what does compliance cost in steps?

## Key insights (the load-bearing ideas)

- **KI1 — Decouple the training horizon from the schedule horizon ("horizon ≠ stop").** Set
  `train_steps` (the forced final-validation step) *below* `schedule_steps` (the LR-decay horizon).
  Because canonical Muon under the 3500-step schedule was 3.28106 at step 3375 but 3.27658 at 3500,
  a forced early validation can already cross the target **without compressing the cooldown**. Every
  promoted recipe carried `schedule_steps > train_steps`. → [C01]
- **KI2 — Evaluate on a tail-EMA of the weights.** Validating on an exponential moving average of
  the late-training weights (restoring the online weights afterward) is the strongest single
  endpoint-smoothing lever, converting near-misses into crossings; β=0.99 beats β=0.995. → [C02]
- **KI3 — A record is a *statistic*, not a crossing.** Submission is gated by
  `(3.28 − μ)·√n ≥ 0.004` over a fixed-step N-seed cohort. A lower single-seed bin is rejected when
  its cohort mean fails the z-test; trading a few steps for a tighter mean is the real win. → [C06]
- **KI4 — Break the floor by changing the parent, not the knob.** The ~3000 floor was a property of
  the *local optimizer-only family*. Reproducing a stronger **public** parent (Soft-Muon + radial +
  SOAP) faithfully, then compressing it by moving phase endpoints (not truncating the horizon),
  reached sub-2950. → [C07, C08]
- **KI5 — Prune before you submit.** Leave-one-out ablation of a converged stack reveals redundant
  modifiers (a component added when it helped can stop pulling weight as the stack changes), and is
  mandatory before a record. It is how the v3 "nosphere" simplification was found. → [C09]
- **KI6 — Under exact polar, most "novel" pre-polar mechanisms are inert.** A perturbation built
  from the polar factor U that preserves singular vectors satisfies `polar(Z)=polar(M)`; for square
  q/k/v and tall mlp.fc targets `UᵀU = I`, so off-diagonal commutator/metric tensors vanish
  identically. The genuinely-novel survivors collapse to a scalar Nesterov blend. → [C10]

## Assumptions

- **A1** The benchmark's hard rules are binding and non-negotiable; a result that changes the
  forward path / data / batch is invalid regardless of its loss. (Enforced; see [C05].)
- **A2** Per-seed variance is stationary enough that the noise floor (≈50 steps / ≈0.001 loss)
  estimated from baseline Muon transfers to the candidate stacks.
- **A3** The fixed-step cohort z-test with σ=0.0013 is the operative definition of a "passing"
  record (the Track-3 README threshold).
- **A4** Public modded-nanogpt PRs and external papers are legitimate parents/sources when
  reproduced faithfully under the architecture guard and attributed; they are not the agent's own
  contribution.
- **A5** The novelty wave's "not on arXiv" test is adjudicated by a search subagent before any code
  runs; a porting of a published method fails the mission even if it would lower the bin.

See [solution/constraints.md](solution/constraints.md) for the full lawful core and scope, and
[claims.md](claims.md) for the falsifiable claims these insights become.
