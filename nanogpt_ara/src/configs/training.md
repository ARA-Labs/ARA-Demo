# Training Configuration — Frontier Recipe Hyperparameters

Exact values from the v3 record (`cc_v3/07070-v88-aurora-proj-s2/launched_script.py`) and the
baseline (`00001-muon-baseline`). Cross-agent v3 constants are byte-identical except where noted
(§18). Format: Value / Rationale / Search range / Sensitivity / Source.

## MUON_LR (Muon base learning rate)
- **Value**: 0.0375 (v3 record); 0.025 (baseline); 0.045 (v2)
- **Rationale**: Normalization (MuonEq/Aurora) clamps per-step update variance, so a larger global
  step is stable; v3's heavier preconditioning re-lowers it from the v2 peak.
- **Search range**: 0.025 -> 0.045 -> 0.0375 across waves (non-monotonic).
- **Sensitivity**: high
- **Source**: §0, §5.2, §13.2

## MUON_WD (Muon weight decay)
- **Value**: 0.0125 (baseline); per-role in v2/v3 — attn 0.0275, MLP 0.03125
- **Rationale**: Decoupled shrinkage; attention matrices are more sensitive, so they decay less.
- **Search range**: per-role split (rolewd).
- **Sensitivity**: medium
- **Source**: §0, §13.3

## mu (Muon momentum) + mu-schedule
- **Value**: 0.95 (baseline constant); schedule 0.85 ->0.95 (warmup 0-300) ->0.85 (2850-2900)
- **Rationale**: Fresher gradients early, smoother averaging mid-run, less stale momentum vs the LR
  cooldown at the end. ~0 marginal alone but enabling/de-confounding.
- **Search range**: warmup length ~300 steps.
- **Sensitivity**: low (alone); LOO `mu_sched` ~+20 in stack.
- **Source**: §2.B.1, §17

## attn LR multiplier
- **Value**: ~0.6x of MLP (0.5-0.625 across runs)
- **Rationale**: Attention projections have different curvature/scale than MLP; uniform LR over-steps
  attn.
- **Search range**: 0.5-0.7x (cc note: attn=0.6x -> 3-seed final 3.26337 vs 3.26461 at 0.7x).
- **Sensitivity**: low-medium
- **Source**: §2.C.1, §13.1

## embed init scale
- **Value**: 0.7 (`model.embed.weight.data.mul_(0.7)`)
- **Rationale**: Smaller embeddings reduce early logit magnitude -> less saturation of the 15*tanh
  logit softcap -> informative gradients during the high-LR stable phase.
- **Search range**: 6-point sweep {0.5..1.5}; sharp local min at 0.7 (only cell with positive dval).
- **Sensitivity**: low (dval -0.00091 ~ 0.9 sigma; needs 3 seeds to detect).
- **Source**: §2.C.2, §9.1

## train_steps / FINAL_TRAIN_STEPS
- **Value**: 2900 (v3 record); 3500 (baseline); 3025/3040/3100 (v2 safe configs)
- **Rationale**: Baseline over-trains; trimming the horizon (and steepening the coupled cooldown)
  reaches 3.28 earlier. Largest single free lever.
- **Search range**: 3500 -> ~2900; hard floor (forced val at 3425 misses).
- **Sensitivity**: high
- **Source**: §2.A.1, §6.1

## cooldown_frac (baseline WSD)
- **Value**: 0.7
- **Rationale**: Long stable phase for bulk descent, linear cooldown into the minimum; near-optimal
  *shape* at the baseline (only length is the lever there).
- **Search range**: kept at 0.7; replaced by power-law cooldown at the frontier.
- **Sensitivity**: low at baseline / high at frontier (see FINAL_LR_POWER).
- **Source**: §0, §2.A.2

## FINAL_LR_POWER (power-law cooldown curvature)
- **Value**: 1.2 (both agents)
- **Rationale**: Convex decay holds LR higher through mid-training then drops steeply — matches the
  win-late dynamics; the single most critical frontier lever.
- **Search range**: power > 1 (convex); 1.0 = baseline linear.
- **Sensitivity**: high — removing the power cooldown makes all 4 LOO seeds miss.
- **Source**: §14.1, §15

## FINAL_SCHEDULE_STEPS vs FINAL_TRAIN_STEPS (horizon decoupling)
- **Value**: t_end = 2985 (schedule horizon) > stop = 2900 (run stops); LR(2900) = 0.00069 = 1.8% flat
- **Rationale**: Harvest the trajectory while LR is still nonzero; stop too early and loss hasn't
  crossed, let it fully anneal and you waste ~85 steps at near-zero LR.
- **Search range**: stop and t_end jointly tuned.
- **Sensitivity**: medium-high
- **Source**: §15.1, §15.4

## per-role power_c (cooldown onset)
- **Value**: embed 4.98e-5, proj 5.18e-7, scalars 1.66e-6, Muon 3.32e-6
- **Rationale**: Each parameter group begins cooling on a different step; a third per-role axis after
  LR and WD.
- **Search range**: per-group.
- **Sensitivity**: medium
- **Source**: §15.3

## CONTRA_MUON_COEFF + CONTRA_TO_NORMAL_END_STEP
- **Value**: -0.2; ramp end 1920 (cc) / 1930 (codex)
- **Rationale**: Subtract a ramping fraction of the unit-norm raw gradient early (decorrelation/
  exploration), anneal to pure Muon; the crossover sits where this anneals off.
- **Search range**: coeff -0.2; `family=contra` standalone best 3000.
- **Sensitivity**: medium; LOO `contra` ~+15.
- **Source**: §5.4, §16.4, §8.1

## SOFT_MUON_P + NORMAL_TO_SOFT_END_STEP
- **Value**: p = 0.1; blend window 2400 -> 2890 (cc) / 2925 (codex), ceiling 0.80
- **Rationale**: Soften orthogonalization in the endgame (singular values -> s^0.1) for gentle
  fine-tuning near convergence.
- **Search range**: p small; blend late only.
- **Sensitivity**: low; LOO `softmuon` ~0 (refinement).
- **Source**: §17.3

## SOAP_PARAM_MODE / SOAP_PRECONDITION_FREQUENCY / SOAP_BETA2 / SOAP_DENOM_POWER / V_SOAP_BLEND
- **Value**: mode `mlp_plus_v`; freq 10; beta2 0.90; denom power 0.50; V blend 0.95
- **Rationale**: Apply eigenbasis-Adam preconditioning only to MLP fc/proj + attn V; amortize the QR
  every 10 steps; RMS denom; dial SOAP down on V (more curvature-sensitive than MLP).
- **Search range**: full vs `mlp_plus_v` (full fails ~3.39); freq 10.
- **Sensitivity**: high — `soap_mlp` LOO ~+85, `attn_soap` ~+35.
- **Source**: §5.3, §16

## ATTN_EARLY_TRUST_FLOOR / ATTN_TRUST_FLOOR_FADE_END_STEP
- **Value**: 0.45; fade end 1625 (both agents)
- **Rationale**: Force SOAP-trust while early gradients are too noisy to measure trust cosines; fade to
  fully data-driven once training stabilizes.
- **Search range**: floor 0.45.
- **Sensitivity**: medium (safety net for amortized SOAP).
- **Source**: §17.2

## _AURORA_BETA (row-rescale)
- **Value**: 0.25
- **Rationale**: Per-row magnitude EMA for the interleaved Aurora rescale; clamps per-neuron update
  scale -> enables the higher LR.
- **Search range**: not swept in INSIGHTS.
- **Sensitivity**: medium; LOO `aurora` ~+20.
- **Source**: §5.2, §14

## AdamW group (auxiliary params)
- **Value**: embed.weight lr 0.3; proj.weight lr 1/320 (~0.0031), zero-initialized; scalars lr 0.01;
  betas (0.8, 0.95) baseline, retuned in v3 (e.g. beta2 0.90); eps 1e-10; wd 0
- **Rationale**: Hand-set per-group LRs for the non-Muon params; the beta retune is a real ~+45-step
  lever (the group was not pre-optimal).
- **Search range**: betas retuned; AdamW LR ~1.10x probed (codex cluster 3).
- **Sensitivity**: medium; LOO `adamw_betas` ~+45.
- **Source**: §0, §7.2, §14.3

## NS coefficients (Polar-Express)
- **Value**: per-iteration tuple tuned for 5 iters (vs baseline (2,-1.5,0.5) over 12 iters)
- **Rationale**: Reach good spectral shape in fewer iters; ~neutral on quality at 124M (already
  converged) but cheaper/enabling.
- **Search range**: 5 vs 12 iters.
- **Sensitivity**: low
- **Source**: §2.B.2
