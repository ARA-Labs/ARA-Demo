# Novelty wave — isolated NV subtree (a documented negative result)

> **Read-scope note.** The novelty wave was **hard-isolated** (its rules forbade looking at any
> other worktree). It is recorded here as an isolated `NV##` subtree, off the v1/v2/v3 lineage, and
> produced **no promotable submission**. Its terminal negative result is linked into the lineage only
> at the seal step. See C07 and `trace/exploration_tree.yaml` (the `nv_*` nodes).

## The mission and constraint

Same benchmark (reach `val_loss <= 3.28` at fewer steps than Muon's 3500), with a hard differentiator:
**every submitted recipe must contain at least one idea not published on arXiv.** Existing
optimizers/schedules/inits are inspiration only; porting and tuning a published method fails the
mission. Novelty had to be a derivation with a math backbone whose update rule does not reduce to a
published one under any HP setting, or a combination whose *interaction* is non-additive and
un-analysed.

## How novelty was operationalized (the two-gate rule)

Before any optimizer code was written, each idea passed two mandatory subagent checks in parallel:
1. an **arXiv / local novelty existence check** (verdict `novel-enough` or `not-novel`), with the
   search results saved as evidence in the idea writeup; and
2. a **benchmark-rule compliance check** (must stay within optimizer/init/LR/WD surfaces, not touch
   architecture/data/batch/sequence/validation/one-fwd-bwd semantics).
A failure on **either** gate killed the idea with no run. The bar was refined twice: schedule/LR/WD
plumbing does not count as novel (even if signal-driven), and an optimizer combination counts only
when one mechanism's output **materially and non-additively** shapes another's.

## What happened — the shape of the negative result

Roughly **~40 ideas ran** and **~60 were killed before code**. The headroom turned out to be
inaccessible under the constraint, for two structural reasons (C07):

- **The productive directions were ruled non-novel.** Everything that actually moves the bin on this
  benchmark — schedule shape, LR/WD tuning, additive optimizer combinations — is "plumbing" under the
  refined bar. Several already-running ideas (alr/stm/cdm/dsl/mhs/wdi/wdr/zpb/rzb…) were retroactively
  invalidated as schedule/LR/WD plumbing.
- **The novel directions collapsed to algebraic no-ops.** The most interesting novel constructions
  were pre-polar perturbations built from Muon's orthogonalized factor `U`. But for the exact polar
  factor, `U^T U = I` (and input columns have unit norm), so disagreement/commutator/imbalance terms
  built from `U` vanish **identically**. Ideas like GLC001, MNL001, CPD001, NMA001, ITP001, PJD001
  were killed pre-code on this math (`C = offdiag((U^T U)D − D(U^T U)) = 0`). This is the single most
  common kill reason for "clever" optimizer math here.

Among ideas that did run, the recurring failure pattern was: a single-seed crossing at 3450/3475
(a 25–50 step gain, **below the noise floor**) that either failed to reproduce on a distinct seed
(e.g. ngi001, ndf001) or fell inside the 2× step noise-floor gate. The **best reproduced** result was
`vfg001` (value/fc-only gain init) at a 25-step gain — **signal, not a win**.

## Catalog of attempted novel ideas (mechanism families)

Init-side: residual-stream isometric init (rsi), value-fc gain (vfg, the best near-miss),
norm-gain imbalance (ngi), projection micro-init (pmi), square-law branch-gain (svc), q/k-norm
preconditioned init (qkp), value-norm coupled (vng), complementary channel-/source-gain (cgi, csi),
hidden-spectrum split (hfs), embedding Fourier anchor (efa).

Optimizer-side (all `novel-enough` narrowly, all closed negative): polar-disagreement split (pds),
weight-seeded Muon state (wms), commutator-transport Muon (cmu), polar-path momentum (ppm),
reciprocal-variance metric (rvm), q/k polar-agreement (qkt), reciprocal polar-transport (rpt),
gain-gradient shear (gms), polar-work gain coupling (pwg), bidirectional polar-gain (bpg),
orthogonal-surprise momentum (osm, failed hard), AdamW-delta polar shear (adv/abp/sam),
secant-cancelled (scm), NS-defect feedback (ndf), product-adjoint (pam), branch input-Gram exchange
(bige), depth-diffused (ddm), branch-covariance whitened (bcw), branch defect-mirror (bdm),
q/k skew-coupled (qks), cross-block branch covariance (cbc), gain-sheared branch-Gram (gsb),
polar-stretch exchange (pse), hidden-strain coupled (hsm), cross-optimizer descent-budget (xob),
delta-gated polar-stretch (dps), polar gradient-momentum metric (pgm).

Killed by the novelty gate as reductions to published methods: tgm (OrthoGrad/Mano), rcm (Muon²-F),
gcm (Gradient Centralization), sec (low-rank/Dion/GaLore/SUMO), dgb (Fixup/DeepNet), prc (MuonEq),
efo (classical error-feedback) and ~50 others.

## Why this is a contribution

A clean, well-instrumented **negative result on the agent's own derivations**, including the math
reason they failed (exact-polar no-op) and the structural reason the constraint is hard (the
productive levers are non-novel). It is symmetric to the v3 finding that the real gains came from
*reproducing and pruning* published mechanisms, not from inventing new ones.
