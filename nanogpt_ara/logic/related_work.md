# Related Work

Typed dependency graph of the methods this experiment imports, extends, baselines against, bounds, or
refutes. Full `RW` blocks for methods with a specific technical delta; brief citations at the end for
the remaining intellectual neighborhood. arXiv IDs / PR numbers are taken verbatim from INSIGHTS.md
and the run code headers.

## RW01: Jordan et al. — Muon optimizer / modded-nanogpt
- **DOI**: github.com/KellerJordan/modded-nanogpt (benchmark + reference recipe)
- **Type**: baseline
- **Delta**:
  - What changed: This work takes the Muon reference (3500 steps) as the starting point and stacks
    levers on top; it does not replace Muon.
  - Why: Muon's orthogonalized-momentum update already captures most cheap curvature at 124M.
- **Claims affected**: C01, C03, C05, C10
- **Adopted elements**: Two-optimizer partition (AdamW + Muon), Newton-Schulz orthogonalization, WSD
  schedule, the `track_3_optimization` benchmark and `step_to_3_28` metric.

## RW02: MuonEq — pre-NS per-row normalization
- **DOI**: arXiv:2603.28254
- **Type**: imports
- **Delta**:
  - What changed: Per-row L2-normalize the momentum *before* Newton-Schulz.
  - Why: Equalized rows give NS a better-conditioned input -> more faithful orthogonalization.
- **Claims affected**: C03, C04
- **Adopted elements**: The pre-NS row-normalization operator; found to be the strongest single
  Muon-internal lever (dval -0.00484).

## RW03: NorMuon — post-NS per-row 2nd-moment normalization
- **DOI**: arXiv:2510.05491 (microsoft/dion)
- **Type**: imports
- **Delta**:
  - What changed: Divide the orthogonalized update by a per-row 2nd-moment EMA *after* NS.
  - Why: Per-row update-magnitude control.
- **Claims affected**: C03, C13
- **Adopted elements**: The post-NS row-norm; found weaker than MuonEq and redundant once Aurora/MuonEq
  are present (LOO ~0).

## RW04: SOAP — Adam in Shampoo's eigenbasis
- **DOI**: arXiv:2409.11321
- **Type**: refutes (as a global add-on) / imports (as a subset preconditioner)
- **Delta**:
  - What changed: Second-order preconditioning in the gradient-covariance eigenbasis. Applied globally
    on top of Muon it fails (~3.39); restricted to MLP+V it is the biggest hitting v3 lever.
  - Why: NS already conditions Q/K-style matrices (SOAP duplicates it there); MLP/V carry persistent
    curvature anisotropy NS leaves on the table.
- **Claims affected**: C05, C13, C16
- **Adopted elements**: The eigenbasis-Adam preconditioner, norm-preserving and amortized (basis every
  10 steps), gated by trust_gate; benchmarked originally against AdamW (hence the backbone mismatch).

## RW05: Cautious optimizers (Cautious-Muon)
- **DOI**: arXiv:2411.16085
- **Type**: refutes
- **Delta**:
  - What changed: Mask update components that disagree in sign with the fresh gradient.
  - Why: Intended to enforce monotone descent.
- **Claims affected**: C07
- **Adopted elements**: None — both agents found it regresses/diverges (codex 3.30833; all 4 cautious
  modes regress at the cc v8 backbone). The masking destroys NS's orthogonality. The experiment's most
  robust cross-agent clean negative.

## RW06: Polar Express — tuned Newton-Schulz coefficients
- **DOI**: arXiv:2505.16932
- **Type**: extends
- **Delta**:
  - What changed: Per-iteration NS coefficients tuned to reach good spectral shape in 5 iterations
    instead of the canonical 12.
  - Why: Cheaper orthogonalization; tests whether the NS target is the bottleneck.
- **Claims affected**: C01
- **Adopted elements**: The Polar-Express coefficient tuple (used in the v3 records); ~neutral on
  quality at 124M but enabling/cheaper.

## RW07: Contra-Muon (modded-nanogpt PR275)
- **DOI**: modded-nanogpt PR #275
- **Type**: imports
- **Delta**:
  - What changed: Add a ramping negative fraction of the unit-norm raw gradient to the orthogonalized
    update early, annealing to pure Muon (`contra_coeff` -0.2 -> 0 by ~step 1920).
  - Why: Decorrelate the early update from the greedy gradient direction (exploration/conditioning).
- **Claims affected**: C08, C14
- **Adopted elements**: The contrastive term and its ramp; member of the v3 stack and the engineered
  crossover.

## RW08: SOAP-on-subset preconditioning (modded-nanogpt PR278)
- **DOI**: modded-nanogpt PR #278
- **Type**: extends
- **Delta**:
  - What changed: Extends the SOAP parameter set to MLP + value projection (`mlp_plus_v`), with a
    gentler 95%/5% SOAP/raw blend on V.
  - Why: Apply second-order preconditioning only where curvature is anisotropic and persistent.
- **Claims affected**: C05, C13
- **Adopted elements**: The subset selector (`should_soap_param`) and the V-SOAP blend.

## RW09: Aurora row-rescale + PR287 power-law cooldown
- **DOI**: modded-nanogpt PRs (Aurora; PR287 "power-law LR schedule")
- **Type**: imports
- **Delta**:
  - What changed: Aurora = K outer NS iterations with per-row `D` rescale between calls
    (`_AURORA_BETA=0.25`); PR287 = per-role convex `(t_end - step)^1.2` cooldown with horizon
    decoupled from the stop step.
  - Why: Per-row magnitude control (enables higher LR) + a co-tuned terminal LR trajectory.
- **Claims affected**: C04, C13, C14
- **Adopted elements**: The Aurora rescale and the power-law schedule constants — the latter the single
  most critical frontier lever (LOO: removing it -> all seeds miss).

## RW10: Muon^2 / "MuonSq" (Adam-style 2nd-moment precond before NS)
- **DOI**: modded-nanogpt PR (community; "MuonSq")
- **Type**: refutes (in-stack)
- **Delta**:
  - What changed: `M_tilde = M / (sqrt(V) + eps)` before NS.
  - Why: A public PR showed -175 steps against *vanilla* Muon.
- **Claims affected**: C05
- **Adopted elements**: None in the final recipe — it conflicts with the already-present Nesterov +
  mu-schedule + Polar-Express stack and regresses monotonically (`family=muon2f` best 3190). The
  canonical example that a lever's sign depends on the backbone.

## RW11: AdEMAMix and Lookahead (as Muon variants)
- **DOI**: AdEMAMix arXiv:2409.03137; Lookahead arXiv:1907.08610
- **Type**: refutes
- **Delta**:
  - What changed: AdEMAMix adds a slow (beta=0.999) + fast EMA; Lookahead periodically blends slow
    weights.
  - Why: Tested as Muon add-ons for better averaging.
- **Claims affected**: C07
- **Adopted elements**: None — the slow components under-converge in <3200 steps and the periodic blend
  halves the effective update rate at the short budget.

## RW12: Shampoo / KL-Shampoo (second-order baselines)
- **DOI**: Shampoo arXiv:1802.09568 (KL-Shampoo: community variant)
- **Type**: bounds
- **Delta**:
  - What changed: Full second-order preconditioning; KL-Shampoo is a KL-regularized variant.
  - Why: Tested as heavier curvature preconditioners.
- **Claims affected**: C11, C16
- **Adopted elements**: None directly — KL-Shampoo is the Mode-A "slow-and-stuck" divergence example
  (final 5.49); bounds where second-order helps (scale-dependent, "may win at >=350M").

## RW13: SWA / EMA endgame weight averaging
- **DOI**: SWA arXiv:1803.05407
- **Type**: refutes
- **Delta**:
  - What changed: Average weights over the late trajectory (EMA decay 0.995 from step 2000; finite-
    window averaging).
  - Why: Variance reduction near convergence.
- **Claims affected**: C07
- **Adopted elements**: None — under WSD the late LR is ~0 so the trajectory is near-stationary;
  averaging adds bias without variance reduction (EMA final 3.28010, misses).

## RW14: ARA methodology (Agent-Native Research Artifacts)
- **DOI**: arXiv:2604.24658
- **Type**: imports
- **Delta**:
  - What changed: Provides the artifact structure (cognitive / physical / exploration-graph / evidence
    layers) this document is compiled into.
  - Why: To make the synthesis machine-executable, addressing the "Storytelling Tax" (discarded
    failures) and "Engineering Tax" (unwritten implementation detail).
- **Claims affected**: (structural — all)
- **Adopted elements**: The four-layer ARA schema; the exploration tree preserves the dead ends
  (novelty wave, clean negatives) that a conventional write-up would discard.

## Brief citations (intellectual neighborhood, no distinct in-stack delta)
- **AdamW** (Loshchilov & Hutter, arXiv:1711.05101) — the non-Muon optimizer for 1-D/embedding/output
  params (baseline 5625 steps); its betas were retuned (LOO ~+45). Affects C06.
- **MARS, KronPSGD** — additional preconditioners screened and ruled out in cc_v1 (`ideas.md`); affect
  C05/C07. Cited as rejected alternatives.
- **AdaBelief / QHAdam** — tried for the AdamW-owned groups in codex cluster 3; affect C06.
- **RAdam / LAMB / NovoGrad / Adan** — older optimizers flagged in PROGRESS.md (goal Q2) as candidates
  to pair with a modern schedule; outcomes only partially explored. Affect C16 (open question).
- **WSD / stable-then-decay schedule** (cited in modded-nanogpt; "minimax/medium" speedrun recipes) —
  source of the baseline schedule and the mu-schedule port. Affects C02.
- **FineWeb-10B** (HuggingFace) — the fixed training corpus. Context for A1.
