# Experiments

Verification/analysis plans, directional only (no exact numbers — those live in `evidence/`).
"Experiment" here = a screening/ablation/statistical protocol on the fixed benchmark.

---

## E01 — Horizon/stop schedule-decoupling screen
**Verifies.** C01.
**Setup.** Muon-family run on the fixed nanoGPT; vary the LR-schedule denominator ("horizon",
`schedule_steps`) independently of the training stop step (`train_steps`), forcing a final
validation at the stop step.
**Procedure.** For a target stop, compare a compressed schedule (`horizon == stop`) against a
larger-horizon schedule (`horizon > stop`); reproduce each candidate on a second seed; record the
first step where `val_loss <= 3.28`. Descend the stop step, lowering the horizon ("colder") as
needed.
**Expected outcome.** Larger-horizon runs cross the target at a lower step than compressed runs at
matched stop; each lower stop needs a colder horizon to keep crossing.

---

## E02 — NorMuon beta2 / LR screen
**Verifies.** C02.
**Setup.** Replace canonical Muon with NorMuon (row second-moment normalization of the
orthogonalized update, RMS-matched to Muon scale) on hidden matrices.
**Procedure.** Sweep preconditioner momentum (`beta2`) and Muon LR; compare against a
canonical-Muon control at matched HPs without the row normalization; require two-seed reproduction
past the noise-floor gate before promoting a lower bin.
**Expected outcome.** A colder beta2 and a higher LR with row normalization reach the target at
fewer steps than canonical Muon; the row normalization contributes beyond the HP change.

---

## E03 — v12iso leave-one-out component pruning
**Verifies.** C03.
**Setup.** The full v1 v12iso stack at its low-step screen.
**Procedure.** For each stack component (tail-EMA, 2-factor preconditioning, mu-schedule,
error-feedback residual, AggMo3, tail residual mechanics, late-LR, beta2-thaw), remove it singly,
re-run a fixed seed cohort, and record the change in validation loss vs the full stack.
**Expected outcome.** Removing the endgame EMA evaluation shadow or the 2-factor preconditioning
degrades loss far more than removing any single tail-residual mechanism; some tail mechanics are
within noise.

---

## E04 — v2 legal-rebuild leave-one-out pruning
**Verifies.** C04.
**Setup.** The compliant "legal_v12opt" stack at its submitted screen.
**Procedure.** Singly remove each component (role-specific LR, role-specific WD, MuonEq update,
Muon schedule, lookahead, Contra-Muon, embed init, eta_min, Polar-Express NS); re-run the fixed
seed cohort; record removal deltas.
**Expected outcome.** Role-specific LR, the row-normalized (MuonEq) update and the Muon schedule
dominate the removal deltas; lookahead and role-WD are positive; Contra-Muon is near-noise.

---

## E05 — v3 W258 leave-one-out pruning
**Verifies.** C06.
**Setup.** The v3 frontier stack (Soft-Muon + radial dampening + MLP+V SOAP + LACV + sphere
lookahead) at the 2949 screen.
**Procedure.** Build one ablation per mechanism (nosoap, novsoap, noradial, notailradial, nosoft,
nocontra, noqkcontrascale, nolacv, nolacvfloor, nosphere, notangentsphere, and the combined
nosphere-notangent); run each cohort; record removal deltas. Keep only removals that tie or improve
the statistical boundary.
**Expected outcome.** SOAP and radial removals collapse the tail; the sphere-lookahead pull removal
(nosphere) holds the boundary and simplifies the stack; the two sphere removals do not compose.

---

## E06 — Novelty wave two-gate screen + reproduction
**Verifies.** C07.
**Setup.** Hard-isolated worktree; every candidate idea must pass (a) an arXiv/local novelty
existence check and (b) a benchmark-rule compliance check before any code is written.
**Procedure.** For each derived idea: scout → write idea doc → run both gates in parallel → if both
pass, implement a conservative first cell, screen by domination against the baseline curve, then
require a distinct-seed reproduction past the 2× step noise-floor gate. Kill on any gate failure or
on reduction to a published mechanism / algebraic no-op.
**Expected outcome.** No idea survives both reproduction and the noise-floor gate; novel pre-polar
optimizer perturbations frequently fail the math gate as exact-polar no-ops; the productive
schedule/HP directions fail the novelty gate. Net: no promotable submission.

---

## E07 — Fixed-step seed-cohort significance test
**Verifies.** C08.
**Setup.** A candidate submission recipe with `train_steps` (the bin) hardcoded.
**Procedure.** Run n distinct non-cherry-picked seeds at the fixed bin; at each common validation
checkpoint compute the cohort mean and the significance score `(3.28 - mean)*sqrt(n)`; accept the
earliest checkpoint whose score clears the threshold; evaluate only common checkpoints (no
per-run cherry-pick).
**Expected outcome.** Single-seed sub-step crossings fail the cohort test; the earliest passing
checkpoint (the submitted bin) sits above the single-seed frontier.

---

## E08 — Architecture byte-identity compliance gate
**Verifies.** C05.
**Setup.** A launcher-time static check over each candidate variant before submission.
**Procedure.** Diff the variant's Architecture block against the workspace `train_gpt_simple.py`;
fail (exit non-zero, no submission) on any non-empty diff, any change to `RMSNorm.forward`, any
change to the q/k `F.rms_norm` call, or any optimizer logic routed through norm-gain parameters;
audit active worktrees for residual violations after each launch wave.
**Expected outcome.** Non-byte-identical forward/norm paths are blocked before Slurm submission;
prior results built on a rewritten forward path are quarantined and excluded from the frontier.
