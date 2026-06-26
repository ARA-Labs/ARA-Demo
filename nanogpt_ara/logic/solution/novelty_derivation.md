# Novelty-wave derivation method and the no-op laws

The novelty wave (read-isolated `NV##` subtree) is a documented **negative result**: under a compound
constraint (init/optimizer-only, materially non-additive, **not on arXiv**), no derived mechanism
produced a promotable submission. This file records *how* the agent derived ideas and *why* the space
was structurally empty (C10) — the negative is a contribution, not an absence.

## The derivation gate (before any code runs)

Every candidate passed two mandatory subagent gates **before** implementation:
1. **Compliance gate** — benchmark hard rules + the architecture/forward-path boundary (softcap/logit
   changes are architecture → out).
2. **Novelty/existence gate** — an arXiv search; the idea's math must not reduce to a published method
   under any HP setting. A porting of a published method fails the mission even if it would lower the
   bin. [src: `novelty/codex/goal.md:9-36`]

The refined bar tightened twice mid-wave: (i) optimizer+schedule and schedule-only combinations do **not**
count as novel; (ii) optimizer-level combinations count **only** when one mechanism's output materially
shapes another's behavior (non-additive interaction), not as additive plumbing.

## What was actually derived and run

Dozens of pre-polar Muon mechanisms and init schemes were implemented and run (a small fraction of the
~100+ brainstormed). Representative families (idea code → mechanism → outcome):

- **Init-only gain families** — RSI (residual-stream isometric init), VFG (value/fc-only gain), NGI
  (norm-gain imbalance), SVC, QKP, VNG. The **best-performing class**, but all sit at Muon baseline
  parity; their apparent crossings come from cooldown-schedule truncation, which the agent refused to
  credit. VFG reproduced a 25-step crossing — below the 2× noise floor.
- **Pre-polar momentum/transport** — PDS (polar-disagreement split), CMU (commutator/tangent correction),
  QKT (q/k polar agreement), PPM (polar-path momentum), OSM (orthogonal-residual damping). At best a
  3450/3475-only single-seed crossing; several diverged.
- **Gain-gradient / branch-Gram families** — GMS, PWG, BPG, BIGE, BCW, CBC, GSB, PSE, DPS, PGM,
  DDM, BDM, QKS. All recenter near 3.282; the strongest reach a single 3450-only crossing.
- **Cross-optimizer / adjoint families** — SAM, ADV, ABP, PAM, RVM, XOB. All missed.

Three genuine deeper crossings (NGI n0875/m1125, NDF α=0.05, reaching ~3375) **failed distinct-seed
reproduction** — the decisive empirical failure mode.

## Why the space is empty — the no-op and scalar-collapse laws

The search tail collapsed into successive *algebraic* kills: the derived mechanism was provably inert.

- **Exact-polar no-op law.** For exact polar `U`, input-column norms satisfy `‖U[:,j]‖² = 1`; for the
  square q/k/v and tall `mlp.fc` targets `UᵀU = I`. Therefore any pre-polar signal built from column
  energy or off-diagonal commutators/metrics of `U` is **identically zero**, and the update reduces to
  ordinary Muon (+ decoupled WD). Killed CPD, GLC, NMA, DPF, MNL, BIC, JSP, … [src:
  `novelty/codex/scratchpad/THREAD.md:1212-1216`]
- **Scalar-collapse law.** Mechanisms that finite-difference or linearly blend the polar update,
  `Z = N + α(D − βN) = (1 − αβ)N + αD`, only produce a **scalar Nesterov/de-Nesterov blend coefficient**
  — non-novel plumbing under the refined bar. Killed ITP, PJD, …
- **Target-swap ≠ novelty.** Moving a cleared mechanism from mlp.fc/proj to attention v/proj or q/k
  (AVT, QAP, DGT, TAC) does not clear the novelty bar — the same surface is already occupied.

## The terminal conclusion

The genuinely-novel survivors are precisely the mechanisms that **cannot matter** (no-op / scalar
blend); the mechanisms that **would** matter are already published (Muon²/MuonEq, Dion/SUMO/GaLore
low-rank, OrthoGrad tangent, Cayley/Stiefel transport, Gradient Centralization, error-feedback SGD,
PCGrad). Under the compound constraint the reachable improvement set is effectively measure-zero. This
is the structural negative result C10 records, and it is symmetric to the rest of the experiment: a
clean negative on one's own derivations, with the math reason, is the deliverable.
