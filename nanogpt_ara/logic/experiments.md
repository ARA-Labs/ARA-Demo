# Experiments

Declarative verification plans reconstructed from the agents' protocol. Directional outcomes only —
exact numbers live in `evidence/`. Each `Verifies` references claims in [claims.md](claims.md).
Common setup (unless noted): GPT-124M (12 layers, dim 768, vocab 50304), batch 8x64x1024 tokens,
FineWeb-10B; metric `step_to_3_28` plus `final_val_loss`/`min_val_loss`.

## E01: Single-lever integration ladder (3-seed reproducers)
- **Verifies**: C01, C03, C04
- **Setup**:
  - Model: GPT-124M (fixed)
  - Hardware: Not specified in INSIGHTS.md (modded-nanogpt cluster; per-step ms logged in metadata)
  - Dataset: FineWeb-10B (fixed)
  - System: Muon + AdamW two-optimizer baseline (§0) as the shared backbone
- **Procedure**:
  1. Start from the §0 baseline recipe.
  2. Add one candidate lever at a time (mu-schedule, Polar-Express NS, attn-LR split, train-steps
     trim, embed-init x0.7, NorMuon, MuonEq).
  3. Run a 3-seed reproducer at a canonical step count; record dval vs the seed mean.
  4. Keep levers with consistent negative dval (or that are "enabling" for later levers); integrate
     into the running backbone (v1 -> v2 -> v12 frozen frontier).
- **Metrics**: 3-seed mean `dval` at the canonical step; sign and sigma-multiple vs seed std.
- **Expected outcome**:
  - Pre-NS row-norm (MuonEq) is the strongest single lever; post-NS (NorMuon) is weaker; stacking the
    two does not add.
  - Each lever is small (fraction of a 0.005 val unit); the integrated stack compounds to the frontier.
  - Optimal Muon LR rises once normalization is present.
- **Baselines**: §0 Muon reference (3500 steps).
- **Dependencies**: none

## E02: Training-length and validation-cadence probes
- **Verifies**: C02
- **Setup**: Baseline Muon recipe; vary `train_steps` (and the coupled WSD cooldown length); vary the
  forced validation step near the end of a fixed-horizon run.
- **Procedure**:
  1. Sweep `train_steps` (e.g. 3500 -> ~2900) and record `step_to_3_28` / `min_val_loss`.
  2. On a canonical 3500-step trajectory, force an extra validation at intermediate steps (3450, 3425).
  3. Compare the "crossing" step under coarse vs dense validation cadence.
- **Metrics**: `step_to_3_28`, `min_val_loss`, whether the target is hit at the forced step.
- **Expected outcome**:
  - Shortening the horizon reaches 3.28 earlier with no loss in val quality (down to a hard floor).
  - Dense late validation finds an earlier crossing than coarse cadence — part of the lever is a
    measurement artifact; below the true crossing the target genuinely misses.
- **Baselines**: 3500-step Muon reference; default 125-step cadence.
- **Dependencies**: E01

## E03: SOAP parameter-subset comparison (full vs MLP+V)
- **Verifies**: C04, C05
- **Setup**: Muon backbone with SOAP added; vary the SOAP parameter set (full model vs `mlp_plus_v`
  vs none); co-vary the Muon LR.
- **Procedure**:
  1. Run full-model SOAP on top of Muon across an LR sweep.
  2. Run SOAP restricted to MLP `fc`/`proj` + attention value projection, basis refresh every 10 steps,
     Frobenius-norm-preserving, with the trust_gate.
  3. Compare convergence and `step_to_3_28`; re-tune Muon LR for each.
- **Metrics**: `final_val_loss`, `min_val_loss`, `step_to_3_28`; whether the target is reached.
- **Expected outcome**:
  - Full-model SOAP asymptotes above target (never hits); subset SOAP is part of the frontier stack.
  - Same operator, opposite sign depending on parameter subset; optimal LR depends on the stack.
- **Baselines**: Muon-only backbone; full-model SOAP.
- **Dependencies**: E01

## E04: Per-role LR / weight-decay differentiation
- **Verifies**: C06
- **Setup**: Split Muon into attention vs MLP parameter groups; vary per-group LR multiplier and per-
  group weight decay.
- **Procedure**:
  1. Sweep attn-LR multiplier (~0.5-0.7x of MLP).
  2. Sweep per-role weight decay (attn vs MLP).
  3. Combine with per-role cooldown onset (`power_c`); record frontier `step_to_3_28`.
- **Metrics**: 3-seed `final_val_loss`; `step_to_3_28`; boundary miss-rate.
- **Expected outcome**:
  - Down-scaling attention step size and decaying attention less than MLP both help slightly; the
    benefit generalizes from LR to WD to schedule onset.
- **Baselines**: uniform LR/WD across attn and MLP.
- **Dependencies**: E01

## E05: Clean-negative optimizer screen
- **Verifies**: C05, C07
- **Setup**: Muon backbone with one well-cited modification at a time (Cautious masking, Lookahead,
  AdEMAMix, Muon^2, SOAP-global, LR-floor-in-cooldown, EMA/SWA endgame).
- **Procedure**:
  1. Add each modification at its recommended HPs to the current backbone.
  2. Run to completion (or early-kill on divergence); record whether it beats the plain-Muon baseline.
  3. Where possible, confirm the result with the second agent.
- **Metrics**: `final_val_loss`, `step_to_3_28`, divergence signature.
- **Expected outcome**:
  - Each modification regresses or diverges at the current backbone; several are cross-agent confirmed
    negatives; a method validated against vanilla Muon can flip negative in the stack.
- **Baselines**: plain-Muon at the same backbone.
- **Dependencies**: E01

## E06: Training-curve crossover extraction
- **Verifies**: C08
- **Setup**: Extract `val_loss` vs `step` from `train.log` for the baseline (3500 steps) and the v3
  record (2900 steps), plus a full-SOAP run.
- **Procedure**:
  1. Read per-validation points from each `train.log`.
  2. Align on matched steps; compute the record-minus-baseline delta over the run.
  3. Identify the crossover step where the record overtakes the baseline.
- **Metrics**: `val_loss` at matched steps; crossover step; whether each run eventually hits 3.28.
- **Expected outcome**:
  - The record is behind early, crosses over around the point where its early-exploration levers
    anneal off, then wins; full SOAP loses early and never recovers.
- **Baselines**: 3500-step Muon reference; full-SOAP run.
- **Dependencies**: E01

## E07: Seed-reverify noise-floor and miss-rate
- **Verifies**: C09, C16, C17
- **Setup**: Run fixed configs at many seeds (8-16) across 13 config groups (the `seed_reverify` wave),
  spanning frontier and safe configs; dense vs coarse validation cadence.
- **Procedure**:
  1. For each config, run 8-16 seeds; record `final_val_loss`, `min_val_loss`, `step_to_3_28`, miss.
  2. Compute within-config std of each metric and the pooled miss-rate.
  3. Derive the seeds-per-arm needed to resolve a given step gain.
- **Metrics**: std(`final_val_loss`), std(`step_to_3_28`), miss-rate, seeds-for-significance.
- **Expected outcome**:
  - Final-val std is the same size as a single-lever gain; ~9-12% of frontier seeds miss; step-std is
    ~0 under coarse cadence and ~15-21 under dense cadence; seeds needed scale inversely with the
    squared effect size.
- **Baselines**: a safe (always-hitting) config vs a frontier (boundary) config.
- **Dependencies**: E01

## E08: Novelty-constrained wave
- **Verifies**: C10
- **Setup**: Same benchmark, but ideas must pass a novelty check (no known methods / HP tweaks) and a
  code-location compliance rule (changes confined to Optimization and Init & Optim Hyperparams).
- **Procedure**:
  1. Generate genuinely-new operators (trust-region-muon, anisotropic, spectral-pre-clip, NS-coeff
     inits, Schatten-p, ...).
  2. Re-validate a plain-Muon baseline under the same harness for reference.
  3. Audit each operator for novelty and compliance; early-kill diverging runs.
- **Metrics**: `step_to_3_28`; novelty/compliance verdict; early-kill step.
- **Expected outcome**:
  - The best novel operator merely matches the re-validated plain-Muon baseline; operators touching
    the NS core degrade orthogonalization; some compliant ideas are blocked by the code-location rule.
- **Baselines**: re-validated plain-Muon under the novelty harness.
- **Dependencies**: E01

## E09: Stability / divergence taxonomy
- **Verifies**: C11
- **Setup**: Collect runs that completed (or were early-killed) far above target across all waves;
  read their `train.log` curves and status flags.
- **Procedure**:
  1. Classify each diverging trajectory by signature (monotone-slow, spike-and-recover, NaN/no-learn).
  2. Attribute each to a mechanism (preconditioner scale, pathological HP, normalization x warmup).
  3. Tally hard-fails vs early-cancellations across the export.
- **Metrics**: divergence signature, NaN count, step at which the signature is detectable, status mix.
- **Expected outcome**:
  - Three recurring modes, all visible by step ~750; most non-completions are early cancellations, not
    crashes — instability is predictable and early-killable.
- **Baselines**: a stable frontier run.
- **Dependencies**: E01

## E10: Search-economy accounting
- **Verifies**: C12
- **Setup**: Tally each agent's launched runs and distinct recipe versions per wave from `runs.csv`
  and run-name `vNN` counters; order v1 runs by launch time.
- **Procedure**:
  1. Count runs per `agent_version`; count distinct families and max `vNN` per wave.
  2. For v1, tally the family distribution of the first ~120 launch-ordered runs per agent.
  3. Compare run-count, recipe-diversity, and the located best lever per agent.
- **Metrics**: runs/wave, families/wave, max recipe version, first-120 family histogram, v1 best.
- **Expected outcome**:
  - One agent reaches the frontier with ~1/4 the runs but ~3x the distinct recipes (breadth-first);
    the other runs narrow-and-deep sweeps; both reach the same ceiling, but breadth-first locates the
    stronger lever.
- **Baselines**: cross-agent comparison.
- **Dependencies**: E01

## E11: Leave-one-out ablation at the frontier (4-seed)
- **Verifies**: C01, C03, C06, C13
- **Setup**: The full v3 frontier recipe; remove exactly one component at a time; run 4 seeds each.
- **Procedure**:
  1. For each component (`pow_cooldown`, `soap_mlp`, `adamw_betas`, `attn_soap`, `uwfloor`, `radial`,
     `aurora`, `mu_sched`, `contra`, `muwarmup`, `normuon`, `cgi`, `softmuon`, ...), delete it.
  2. Run 4 seeds; record the median `step_to_3_28` (or all-miss) and the 4-seed range.
  3. Rank components by the cost of removing them.
- **Metrics**: median `step_to_3_28` per ablation; 4-seed range; miss flag.
- **Expected outcome**:
  - Removing the power-law cooldown makes all seeds miss (critical); SOAP-on-MLP is the biggest hitting
    contributor; the AdamW-beta retune is real and mid-pack; NorMuon (and a few others) are ~0. The
    contribution distribution is long-tailed (few essential, several useful, several dead).
- **Baselines**: full v3 recipe (~2925-2930 seed-verified).
- **Dependencies**: E01, E03

## E12: Temporal-curriculum decode
- **Verifies**: C14
- **Setup**: Read the v3 record's ramp constants and phase-active levers from `launched_script.py`;
  align them with the §8 crossover step.
- **Procedure**:
  1. Extract all ramp constants (Contra end-step, trust-floor fade, soft-Muon blend window, mu warmup/
     cool).
  2. Partition the run into Explore / Converge / Soften phases by which levers are active.
  3. Check that the phase boundaries bracket the measured crossover.
- **Metrics**: ramp-constant step values; phase boundaries; crossover step.
- **Expected outcome**:
  - The recipe is a time-scheduled curriculum; the explore-phase levers anneal off right at the
    crossover, i.e. the lose-early/win-late curve is engineered.
- **Baselines**: the static §0 baseline schedule.
- **Dependencies**: E06

## E13: Cross-agent recipe diff
- **Verifies**: C15
- **Setup**: Diff the two agents' v3 record scripts (`cc_v3/07070-...` vs `codex_v3/08953-...worker27`).
- **Procedure**:
  1. Compare the magic constants and helper functions component-by-component.
  2. Identify which fields are identical vs which differ.
  3. Contrast with the v1 records, where the agents diverged.
- **Metrics**: count of identical constants/functions; magnitude of any differences.
- **Expected outcome**:
  - The v3 records are component-for-component identical except tiny timing offsets — shared public-PR
    lineage, not independent rediscovery; the genuine independent signal is the v1 divergence.
- **Baselines**: the v1 records of both agents.
- **Dependencies**: E10

## E14: Generalization-limits audit
- **Verifies**: C16
- **Setup**: Aggregate per-wave median `step_avg_ms`, the `min_val_loss` distribution of v3 hitters,
  the SOAP scale caveat, and the fixed-scope rules.
- **Procedure**:
  1. Compute per-wave median per-step compute; compare v3 vs baseline.
  2. Measure how tightly v3 hitters cluster `min_val_loss` just below 3.28.
  3. Note the scale caveat (SOAP "may win at >=350M") and the fixed architecture/data/batch.
- **Metrics**: median `step_avg_ms`/wave; `min_val_loss` band; per-step-cost vs step-count tradeoff.
- **Expected outcome**:
  - v3 trades ~17% fewer steps for ~20% more compute/step (a net loss when FLOP-budgeted); the recipe
    is overfit to 3.28; the optimizer ranking is scale-bound; cheap v1/v2 levers transfer, expensive
    v3 machinery does not.
- **Baselines**: baseline per-step compute; the v1/v2 cheap-lever recipes.
- **Dependencies**: E07, E11
