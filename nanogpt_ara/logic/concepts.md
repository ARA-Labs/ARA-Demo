# Concepts

The technical vocabulary of this benchmark and the agent's stack. Definitions are formal and
field-specific; named optimizers credited to external work are detailed in
[related_work.md](related_work.md).

## Benchmark / protocol terms

- **track_3_optimization.** The modded-nanogpt speedrun track that fixes the model architecture,
  dataset (FineWeb-10B cache), batch size, sequence length, and the one-forward-backward-per-step
  contract of a ~124M-parameter GPT, and scores entrants by the number of training steps to reach
  **3.28 validation loss**. Only optimizer, hyperparameters, schedule, and init may change
  (`v1/codex/goal.md:3-8`).
- **Bin / step-to-target.** The training step at which validation loss first crosses ≤ 3.28. The
  submission metric; lower is better. A run that dips past 3.28 and back must have its crossing
  confirmed from the log, not inferred from the final loss (`v1/codex/AGENTS.md:224-226`).
- **Noise floor.** The agent's estimate of seed-to-seed variability used to judge whether a gain
  is real: `step_to_target ≈ 50 steps`, `final_val_loss mean ≈ 0.001`
  (`v1/codex/AGENTS.md:160-163`).
- **Fixed-cohort significance gate.** The acceptance rule `(3.28 − μ)·√n ≥ 0.004` over n
  non-cherry-picked seeds (equivalently z ≈ (3.28−μ)/(σ/√n) with σ ≈ 0.0013, requiring p < 0.001),
  with an anti-"val-spam" same-checkpoint scan so the bin is the earliest *common* checkpoint whose
  cohort mean passes (`record_configs/*/README.md`, `v2/.../THREAD.md:810`). See [C06](claims.md).
- **Lawful core.** The six always-binding rules in `v1/codex/AGENTS.md:11-28` (benchmark hard
  rules, noise-floor gate, stuck detector, ≤3-modifier slug stack, two-seed reproduction, mandatory
  pre-submission pruning). Detailed in [solution/constraints.md](solution/constraints.md).
- **Leave-one-out (LOO) pruning round.** Mandatory pre-submission step: for each modifier in the
  stack, build a variant with exactly that modifier removed, re-run, and measure the change in
  val loss (`Δval when removed`; positive ⇒ the component helped). Drops a modifier only on a
  two-seed mean inside ±0.5× the noise floor (`v1/codex/AGENTS.md:169-205`). See [C07](claims.md).
- **Slug / family / stuck detector.** A run is named by a `<optimizer>-<modifier>-…` slug capped at
  3 modifiers; the "family" is the slug prefix; the stuck detector rules a family out after 30
  consecutive runs without a step-to-target improvement (`v1/codex/AGENTS.md:141-154`).
- **Wave.** One mission segment with its own worktree and journal: **v1** (optimizer/schedule/init
  screening), **novelty** (hard-isolated, novelty-constrained), **v2** (role LR/WD + lookahead on a
  compliant rebuild), **v3** (public-PR reproduction + compression). The submitted lineage is
  v1 → v2 → v3; novelty is an isolated negative-result subtree.

## Optimizer / update terms

- **Muon.** The baseline matrix optimizer: momentum update orthogonalized by a Newton–Schulz
  iteration (polar factor) before application. Baseline lr=0.025, wd=0.0125, 3500 steps.
- **Newton–Schulz orthogonalization / polar factor `U`.** The iterative map producing the
  (approximate) orthogonal polar factor of the momentum matrix; "exact polar" satisfies UᵀU = I, a
  fact the novelty wave repeatedly used to detect algebraic no-ops ([C12](claims.md)).
- **NorMuon.** A Muon variant with row-wise second-moment normalization applied after Newton–Schulz
  and RMS-matched back to the canonical update scale (`v1/.../THREAD.md:124-126`).
- **Muon2F / MuonEq.** Factorized two-factor row/column second-moment preconditioning of the matrix
  update (Muon2F in v1; the compliant MuonEq row-normalized update in v2). The subject of
  [C03](claims.md).
- **Soft-Muon.** A scheduled softening of the Muon update (Contra → normal → Soft) with a ceiling
  (`SOFT_MUON_CEIL`) and ramp end step, from public PR #291; load-bearing in v3.
- **Contra-Muon.** A pre-Newton–Schulz shaping term (`_CONTRA_MUON` constant); v2 lowered it to
  0.225; v3 carries a reduced q/k Contra residual scale (0.125).
- **AggMo3.** Three-factor aggregated momentum on the hidden matrices (`aggmom3hidden`); a v1 stack
  component.
- **Adam-mini.** A memory-light Adam variant used as the AdamW-side ("optimizer1") replacement for
  embedding/head/scalar groups in v1.
- **SOAP (sidecar) / V-SOAP.** Second-moment preconditioning in a SOAP eigenbasis, applied to
  MLP (and attention-V) updates as a warm-started, step-0-skipped *sidecar* behind the matrix
  optimizer (`SOAP_PARAM_MODE=mlp_plus_v`). The subject of [C10](claims.md).
- **Outward-radial dampening / radial brake (PR #294).** Damping of the update's outward-radial
  component after it is formed, plus a post-step radius correction; tail-activated in v3. The
  subject of [C09](claims.md).
- **Tangent-sphere radial gate / sphere-lookahead pull.** Two tail-geometry mechanisms in the v3
  W258 stack that act as substitutes; `nosphere` removes the lookahead pull and keeps the radial
  gate ([C11](claims.md)).
- **LACV (lookahead control-variate).** A seed-offset correction that reuses lookahead state to
  remove seed-dependent tangent energy, with a q/k u/w "floor" (`LACV_FLOOR_LAMBDA = 0.060`) that
  refills exactly that energy on q/k.
- **Lookahead (Muon).** A slow-weight pull toward an averaged copy; a v2 frontier lever
  (from step 2450, interval 25, α 0.35, pull 0.15, 150-step ramp).
- **Tail-EMA evaluation.** Validation on an exponential moving average of late weights (swapped in
  for eval, then restored), β≈0.99 from a late start; the largest single v1 lever ([C02](claims.md)).
  Distinguished from **SWA** (uniform tail averaging), which was consistently worse.
- **Role-specific LR / WD (RoleLR2 / RoleWD).** Per-parameter-group LR multipliers and weight-decay
  values (q/k, v, attn.proj, mlp.fc, mlp.proj) instead of one body-wide value ([C04](claims.md)).
- **CGI (gain split) / di-fc init / embed init ×0.7.** Init-side levers inherited in v3 from the
  public "v48" parent (CGI Rademacher gain split shown variance-neutral; depth-scaled mlp.fc init;
  embedding init scaled by 0.7).
- **Horizon vs train_steps (schedule decoupling).** Running a longer LR-decay `schedule_steps`
  while taking fewer optimization `train_steps`, forcing final validation while the LR is still
  warm. The first sub-3500 lever ([C01](claims.md)).

## Compliance terms

- **Compliant / "legal" rebuild.** A submitted script whose `Architecture` and forward/normalization
  code is byte-identical to baseline `train_gpt_simple.py`; only `Optimization` and
  `Init & Optim Hyperparams` differ (`v2/.../THREAD.md:130-132`). The v2 `legal_v12opt` family.
- **Quarantine.** Disqualifying every result derived from a non-compliant parent (here the
  forward-path-altering v12) from the frontier, regardless of its score ([C08](claims.md)).
- **Cross-agent touchpoint.** A point where Codex's trajectory used another agent's (Claude/cc)
  output or a public PR; recorded attributed, never as Codex's own result (`README.md:57-82`).
