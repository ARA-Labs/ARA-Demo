# NV — Novelty wave (hard-isolated negative-result subtree)

> **Isolation scope.** This subtree is read-scoped *off* the v1/v2/v3 lineage. The novelty wave ran
> in its own worktree under a rule forbidding inspection of any other worktree
> (`../../novelty/codex/scratchpad/THREAD.md:33-36`). It produced **no promotable submission** — a
> real negative result, symmetric to the cc-only slice's documentation of Claude testing Codex's
> methods (`README.md:79-82`). Its terminal finding feeds the lineage only as
> [C12](../claims.md), linked at the seal step; nothing here is a Codex frontier result.

## NV01 — The wave's mandate and the tightening novelty bar

The wave was tasked to beat Muon at 3500 steps using **genuinely novel** mechanisms, under two
mandatory pre-code gates (an arXiv novelty check and a benchmark-rule/architecture compliance
check) and a novelty bar the human operator **ratcheted three times**:

- **v1 of the bar** — every idea needs a dedicated rule-compliance subagent before code, confirming
  it stays within optimizer/init/LR/WD-schedule surfaces and changes no architecture/data/batch/
  validation/one-fwd-bwd semantics (`../../novelty/codex/scratchpad/THREAD.md:130-134`).
- **v2 of the bar** — "optimizer+schedule and schedule-only combinations do not count as novel …
  Optimizer-level combinations can count only when one optimizer mechanism's output materially
  shapes another mechanism's behavior" (`../../novelty/codex/scratchpad/THREAD.md:248-250`).
- **v3 of the bar** — "optimizer-level combinations are allowed only when the interaction is
  materially non-additive" (`../../novelty/codex/scratchpad/THREAD.md:455-457`).

The benchmark bar to beat: cross `val ≤ 3.28` below 3500 steps, robust to a ~2× step noise floor
and a distinct-seed reproduction (baseline Muon crosses `3.27673` first at 3500).

## NV02 — What ran, and the two failure modes

Roughly three dozen genuinely-new mechanisms cleared both gates and were benchmarked — e.g.
residual-corrected Muon (TRM), eta-coupled cooldown memory (STM), alignment-thermostat Muon (ALR),
function-preserving init rescales (RSI, VFG, NGI), polar-disagreement split (PDS), commutator
correction (CMU), gain-gradient shear (GMS), cross-branch input-Gram exchange (BIGE), and
delta-gated polar-stretch exchange (DPS). Their outcomes fell into two modes:

- **NV02a — single-seed crossings that fail reproduction.** NGI crossed at 3475 on one seed
  (`3.27986`) but the second seed missed (`3.28080`); NDF crossed 3375 (`3.27999`) but seed-1234
  failed; VFG reproduced (`3.27960 → 3.27962`) but was a 25-step gain "below the required 2× step
  noise floor" (`../../novelty/codex/scratchpad/THREAD.md:577-580`).
- **NV02b — "3450-only" crossings.** PDS, CMU, WMS, GMS, BPG, XOB, HFS, ABP, PAM, BIGE, DDM, BCW,
  GSB, PSE all reached at best a single 125-step grid bin below baseline (3450) on one seed — never a
  reproducible 3375 crossing.

The **best robust result of the entire wave** is the reproduced 3475 crossing — one grid bin below
baseline, explicitly below the noise floor.

## NV03 — The dominant dead-end: killed before code

As the bar tightened, the agent's invented ideas increasingly **failed the gate without ever
running**, in two ways:

- **Reduction to known priors.** Candidate mechanisms repeatedly mapped onto existing work:
  Muon²/Muon²-F, OrthoGrad/perpGrad/Mano, Gradient Centralization, low-rank orthogonalization
  (Dion/GaLore/SUMO), Fixup/DeepNet init, Stiefel/Cayley transport, classical error-feedback,
  PCGrad/gradient surgery (`../../novelty/codex/scratchpad/THREAD.md:326-2027`, scattered).
- **Algebraic no-ops the math gate caught.** Several couplings built from the *exact* polar factor
  vanish identically: "for exact polar `U`, input-column norms satisfy `‖U[:,j]‖² = 1`" so a
  column-energy imbalance "collapses to ordinary Muon" (`THREAD.md:1214`); "exact Muon polar has
  `UᵀU = I` … so `C = 0`" (`THREAD.md:1855-1856`); first-order linearizations reduce to a scalar
  Nesterov blend (`THREAD.md:1783-1784`).

## NV04 — The negative result (→ C12)

The agent never writes a single summary verdict (the journal is append-only and ends mid-stream on
a kill), but its recurring explanation is consistent and is crystallized as [C12](../claims.md):
**under hard isolation + a triple-tightened novelty bar on an already-saturated optimizer track,
every genuinely-new mechanism on the optimizer/init surface was either already in the Muon
literature, an exact-polar algebraic no-op, or a one-bin/single-seed effect indistinguishable from
the 125-step noise floor — so the wave yielded no promotable submission.** The metric-moving
surfaces (schedule, optimizer+schedule) had been ruled non-novel by construction, which is *why* the
remaining surface could not move the bin.

### Provenance

All `ai-executed` (mechanisms invented and run by the agent); the novelty bar itself is
`user-revised` (the operator tightened it three times). Outcomes table:
[../../evidence/tables/novelty_outcomes.md](../../evidence/tables/novelty_outcomes.md); trajectory:
the isolated `NV##` nodes in [../../trace/exploration_tree.yaml](../../trace/exploration_tree.yaml).
