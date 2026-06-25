# Related Work

Typed dependency graph for the Codex speedrun. Edge types: `baseline` (the bar being beaten),
`extends` (built on / reproduced and modified), `imports` (mechanism reused), `bounds` (sets a
reference frontier), `refutes` (tried and rejected), `cross-agent` (another agent's work, attributed
not claimed).

---

## RW01 — Muon (Keller Jordan, modded-nanogpt) — `baseline`
The standing SOTA on this track: orthogonalized momentum via Newton-Schulz on block matrices,
canonical `lr=0.025, wd=0.0125`, first crossing `val_loss <= 3.28` at 3500 steps. Every Codex wave
is measured against this. Technical delta of the experiment: stack mechanisms on top of Muon and
push the crossing step down while preserving its block-matrix update core.

## RW02 — AdamW (block-matrix + aux groups) — `baseline`
The weaker reference family on this track (crosses ~5625 steps). Used as a sanity baseline and the
aux-group optimizer for embeddings/heads/1-D params in all recipes; not the SOTA bar.

## RW03 — Polar Express (arXiv:2505.16932) — `imports`
Non-uniform / 5-coefficient Newton-Schulz projection. Imported as the orthogonalization core
("Polar Express NS-5") in v1, v2 and v3.

## RW04 — MuonEq (arXiv:2603.28254) — `imports`
Row/column-normalized Muon update. Imported as the row-normalized update in v1 (NorMuon lineage)
and v2 ("MuonEq"); in v2's pruning it is the second-largest load-bearing component.

## RW05 — @nilin PR #275 / Contra-Muon (modded-nanogpt) — `imports`
Contra-Muon shaping / residual term. The optimizer-family lineage credited in v1 and v2; v3 reuses
the Contra residual and scales it down for q/k.

## RW06 — @nilin PR #291 / Contra→normal→Soft-Muon (modded-nanogpt) — `extends`
3030-step parent (N=30, margin +0.00540): Contra-Muon early, normal Muon mid, Soft-Muon late, with
a Gram-Frobenius / Schatten-4 input-norm estimate and basis stacking (p=0.1, 80% blend). v3
reproduces this faithfully and adds q/k Contra scaling 0.125 and a moved Soft endpoint (2905).

## RW07 — @nilin PR #294 / radial brake (modded-nanogpt) — `extends`
2990-step parent (N=11, margin +0.00442): outward-radial update dampening (scale outward component
by ~0.5, inward by 1.0) plus a post-step weight-radius correction. v3 reproduces it (base outward
scale 0.45, tail guard 2775..2895, tail outward 0.38); the v3 LOO shows it is load-bearing.

## RW08 — @samacqua PR #278 / MLP SOAP (modded-nanogpt) — `imports`
SOAP (Shampoo-family second-order) preconditioning machinery for MLP params; v3 extends it to
MLP+V (`mlp_plus_v`, V blend 0.95). The v3 LOO shows SOAP is the single most load-bearing component.

## RW09 — PR #290 / KL-SOAP-H (modded-nanogpt) — `refutes`
A full Muon-replacement (precondition every step, state from the first gradient) at 3125 steps.
Codex repeatedly tried KL-SOAP-H as a full replacement and it failed hard (diverged / froze
zero-init projections); only the SOAP machinery (as a partial preconditioner) survived.

## RW10 — PR #288 / Muown (modded-nanogpt) — `refutes`
Direction/gain split with NS on direction and Adam on gain, 3075 steps. Tried by Codex as a separate
parent and hard-killed (diverged to ~5.7 val_loss by step 2500).

## RW11 — @yash-oai PR #287 / power-law LR schedule (modded-nanogpt) — `imports`
Power-law cooldown constants; imported into v3 (`train_steps=3020`, `schedule_steps=3025`). Its
back-loaded shape is why early-trajectory kills were ruled invalid for public-frontier schedules.

## RW12 — cc / Claude "v12" optimizer stack — `cross-agent` / `refutes`
The other agent's 3025-step optimizer stack, inherited as v2's parent. Codex tested it, then (on a
user flag) found its rewritten `RMSNorm.forward` / q-k-norm to be a bf16-precision forward-path
change violating the no-architecture rule, and **quarantined** every v12-derived result (see C05).
Recorded as attributed cross-agent provenance, never as a Codex result.

## RW13 — opus "v15 / v48" stack — `cross-agent` / `extends`
Cross-agent stacks read as source material for v3's faithful reproduction: v48 = PR #294 verbatim +
CGI Rademacher channel-gain split (alpha=0.14) + di-fc init + AdamW `b2=0.99` (reported bin 2980,
N=15, +0.00418). v3's CGI gain split is ported from opus v15. Attributed, not claimed.

## RW14 — Aurora / KLShampoo-KLSoap — `refutes` / `bounds`
Local source mechanisms (leverage-aware row/Stiefel correction, KL-Shampoo). v3's Aurora branch
reached bin ~3027 via clean passes but was superseded by the stronger public Soft/radial parent;
KL-SOAP repeatedly failed. Used as inspiration and a reference frontier, not the submitted stack.

## RW15 — Broad post-Muon / classical optimizer literature — `refutes`
The v1 and novelty waves head-to-head screened a large catalog — SOAP, Shampoo/Kron, Lion, Sophia,
AdEMAMix, Adam-mini, MARS-M, Cautious-Muon, RAdam, NovoGrad, LARS/LAMB, AdaBelief, AggMo, QH-Adam,
Lookahead, NAdam, MADGRAD, SM3, AdaBound, SWATS, ADOPT, DION, Scion and more. Most were clean
negatives on this exact setup (e.g. SOAP and many second-order replacements diverged or finished
well above target), supporting the goal.md premise that the literature is full of unverified claims.
Adam-mini, Lookahead and AggMo survived as components; the rest are recorded dead ends.
