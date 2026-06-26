# Experiments

Declarative verification/analysis plans. **No exact numbers here** — exact values live in
[evidence/](../evidence/) and in the trace. Each experiment lists what it `Verifies` (claim IDs),
its `Setup`/`Procedure`/`Expected outcome`, where results are filed (`Evidence`), and the run family
that produced it (`Run`). "Experiment" generalizes to a benchmark eval run, a statistical test, an
ablation sweep, or a derivation check. Claims↔experiments are many-to-many.

The run index for every experiment is [src/artifacts.md](../src/artifacts.md)
(`data/runs_self_contained/runs.csv`, filtered to the four Codex waves, 8,224 runs).

---

## E01 — Horizon vs. stop decoupling (v1)
- **Verifies:** C01
- **Setup:** Muon baseline on `track_3_optimization`; a variant that sets `train_steps` below
  `schedule_steps` (forced early final validation under the uncompressed LR decay).
- **Procedure:** Compare the early-stop variant against (a) the 3500-step baseline and (b) schedules
  whose decay is compressed to the same stop; sweep the stop downward across seeds.
- **Expected outcome:** The decoupled variant crosses the target at a lower step than the baseline and
  than the compressed-decay schedules, until the stop is pulled below the useful cooldown tail.
- **Evidence:** evidence/tables/trajectory_summary.md (v1 entry).
- **Run:** `family=normuon`, `family=v12iso`, purpose=statistical_verification (codex_v1).

## E02 — Optimizer/schedule/init lever screen → NorMuon corridor (v1)
- **Verifies:** C12, C03 (negative space), C01
- **Setup:** Broad screen of post-Muon and pre-Muon optimizers, schedules, and inits against the
  3500-step Muon bar, under the ≤3-modifier slug cap and the stuck detector.
- **Procedure:** One isolated lever per family; kill at a pre-declared mid-curve gate; promote only on
  two-seed reproduction beating the bar by ≥2× the noise floor. NorMuon (β=0.90, lr=0.030) becomes the
  workhorse corridor.
- **Expected outcome:** Most well-cited optimizers are at parity or worse (clean negatives); a small
  set (NorMuon corridor, role-specific mlp.proj LR, beta2 tail-thaw) survives as the v1 backbone.
- **Evidence:** trace dead_end nodes; evidence/tables/v1_component_pruning.md.
- **Run:** `family=normuon` (507 runs), `family=muon2f` (413), `family=adammini` (66), codex_v1.

## E03 — Factorized hidden-matrix preconditioning ablation (Muon2F) (v1)
- **Verifies:** C03
- **Setup:** Two-factor preconditioner applied to different parameter-role partitions (hidden-only,
  attention-only, MLP-only, all/APOLLO-style).
- **Procedure:** Run each partition variant at matched stop/seed; compare mid-curve and target-step
  behavior; reproduce the positive partition across ≥3 seeds.
- **Expected outcome:** Only the hidden-only partition is a live positive; other partitions are
  neutral-to-negative.
- **Evidence:** evidence/tables/v1_component_pruning.md (`noMuon2f`).
- **Run:** `family=muon2f` (codex_v1).

## E04 — Tail-EMA evaluation sweep (v1)
- **Verifies:** C02
- **Setup:** Validation on an EMA of late-training weights (swap-in for eval, restore online), sweeping
  EMA start step and β; baselines = fixed-window SWA and EMA-extrapolated evaluation.
- **Procedure:** Bisect the stop boundary under tail-EMA; compare β=0.99 vs β=0.995; check seed
  robustness near the practical floor.
- **Expected outcome:** Tail-EMA evaluation converts near-misses to crossings; β=0.99 beats β=0.995;
  SWA and extrapolation are worse; the gain is seed-fragile below the practical stop.
- **Evidence:** evidence/tables/v1_component_pruning.md (`noTailEMA`, the top contributor).
- **Run:** EMA/SWA variants within codex_v1 (`tailresrmsstack`, `formalprune`).

## E05 — Transplanted "mu-schedule" isolation (v1)
- **Verifies:** C12 (stacking saturates)
- **Setup:** A handed-over "v12" idea set (Muon mu schedule, attn LR, cooldown floor, embed init,
  Contra) tested as full/simplified packages vs. each lever isolated.
- **Procedure:** Run the full package, a simplified package, and each isolated lever; reproduce the
  positive across seeds.
- **Expected outcome:** Full/simplified packages miss (combined levers wash out the late curve) while
  the **isolated mu-schedule** lever hits and reproduces — the load-bearing modifier, not the bundle.
- **Evidence:** trace v1 nodes; evidence/tables/trajectory_summary.md.
- **Run:** `family=v12iso` (120), `family=v12musched` (27), codex_v1.

## E06 — v1 leave-one-out component pruning (v1)
- **Verifies:** C02, C03, C09
- **Setup:** Leave-one-out ablation of the v1 stack at the pruning step, single seed first, second seed
  on borderline candidates (the lawful-core pruning procedure).
- **Procedure:** For each modifier, remove it and compare cohort val loss; rank by delta; drop only on a
  2-seed mean inside ±0.5× the noise floor.
- **Expected outcome:** Tail-EMA and factorized preconditioning are the largest contributors; several
  tail mechanics (respulse, momrefresh, late_lr) are droppable.
- **Evidence:** evidence/figures/v1_pruning.png, evidence/tables/v1_component_pruning.md.
- **Run:** `family=formalprune` (162), `family=prune` (codex_v1).

## E07 — v1 statistical-claimability cohort (v1)
- **Verifies:** C06, C11
- **Setup:** Fixed-step N-seed cohorts of the v12iso/mu-schedule stack at several stops; the z-margin
  `(3.28 − μ)·√n ≥ 0.004`.
- **Procedure:** Recompute cohort means/scores from individual trainer logs; reject stops with negative
  or sub-threshold score; submit the earliest passing common checkpoint.
- **Expected outcome:** The lowest crossing (`s3170`) is rejected (negative score); a +25-step / 16-seed
  cohort passes → submitted record bin **3205**.
- **Evidence:** evidence/tables/v1_record_seeds.md, evidence/figures/v1_loss_curves.png.
- **Run:** purpose=statistical_verification (codex_v1), record_configs/…_v1_v12iso_3205.

## E08 — Novelty-constrained derivation screen (novelty wave; isolated)
- **Verifies:** C10
- **Setup:** Hard-isolated wave; every recipe must carry a not-on-arXiv idea, adjudicated by a search
  subagent and a benchmark-compliance subagent before any run.
- **Procedure:** Derive a novel pre-polar Muon / init mechanism; pass both gates; run a small α-sweep +
  target-step probes; reproduce any crossing on a distinct seed; record the math reason for failure.
- **Expected outcome:** Survivors reach at best a sub-noise-floor single-seed crossing; genuine
  crossings fail seed reproduction; the search tail collapses into algebraic no-op / scalar-collapse
  proofs. No promotable submission.
- **Evidence:** trace `NV##` subtree; evidence/tables/trajectory_summary.md (novelty row).
- **Run:** `version=novelty` (254 runs), codex_novelty.

## E09 — v2 v12 compliance audit & quarantine (v2)
- **Verifies:** C05
- **Setup:** The inherited cross-agent "v12" parent; an Architecture-section diff against the workspace
  baseline `train_gpt_simple.py`.
- **Procedure:** Diff the forward path; on a flagged `RMSNorm.forward` / q-k-norm precision change,
  quarantine every v12-derived result and rebuild a byte-identical-compliant optimizer family.
- **Expected outcome:** The v12-derived sub-3000 frontier is non-compliant; the compliant rebuild
  reaches the target but the illegal change had materially helped — compliance costs real steps.
- **Evidence:** trace v2 decision node; quarantined config noted in src/artifacts.md.
- **Run:** `family=v12` (2,672 runs, includes quarantined), codex_v2.

## E10 — Legal rebuild + role-LR/WD + lookahead descent (v2)
- **Verifies:** C04, C01
- **Setup:** The byte-identical-compliant `legal_v12opt` base; orthogonal legal levers (Contra-Muon
  scale, attention Muon LR) then role-specific WD, role-specific LR, and Muon lookahead.
- **Procedure:** Combine the two live legal signals, then add role-split decay/LR and lookahead;
  walk the crossing step down across seeds while preserving horizon≠stop.
- **Expected outcome:** Role-LR/WD + lookahead move the crossing step earlier where train-step
  shortening stalls, reaching a low single-seed crossing (not yet a record).
- **Evidence:** evidence/tables/v2_component_pruning.md; trace v2 nodes.
- **Run:** `family=v12` (legal_v12opt variants), codex_v2.

## E11 — v2 significance cohort → record bin 3037 (v2)
- **Verifies:** C06, C11
- **Setup:** Fixed-step cohorts at +25/+50/+75 steps of the clean stack; the z-margin and an
  anti-val-spam same-checkpoint scan.
- **Procedure:** Evaluate cohort means; reject low-step families and intermediate steps that fail;
  submit the earliest common checkpoint that passes.
- **Expected outcome:** All low-step single-seed frontiers fail; only the +75-step cohort passes; step
  3025 fails the same-checkpoint scan → submitted record bin **3037**.
- **Evidence:** evidence/tables/v2_record_seeds.md, evidence/figures/v2_loss_curves.png.
- **Run:** purpose=statistical_verification (codex_v2), record_configs/…_v2_legal_3037.

## E12 — v2 leave-one-out component pruning (v2)
- **Verifies:** C04, C09
- **Setup:** Leave-one-out ablation of the legal 3037 stack at step 3037.
- **Procedure:** Remove each modifier; rank by delta; identify load-bearing vs. droppable.
- **Expected outcome:** Mu-schedule, cooldown-floor, and MuonEq are largest; role-LR is a major v2
  addition; Contra-Muon is nearly free.
- **Evidence:** evidence/figures/v2_pruning.png, evidence/tables/v2_component_pruning.md.
- **Run:** pruning-rerun (codex_v2).

## E13 — Aurora local sub-line (v3)
- **Verifies:** C07 (the floor it failed to break), C12
- **Setup:** Transplant leverage-aware row/Stiefel correction + KL/SOAP preconditioning into the
  strongest local (rolewd/rolelr2/lookahead/Soft-Muon) stacks.
- **Procedure:** Walk the Aurora frontier (3037→3027) with dozens of adaptive-mechanism variants; test
  sub-3000.
- **Expected outcome:** The family passes down to ~3027 but every distribution recenters near 3.280 at
  2999 — a clean negative that motivates the parent pivot.
- **Evidence:** trace v3 Aurora nodes.
- **Run:** Aurora `v3aur…` variants, codex_v3.

## E14 — Faithful public-PR reproduction (v3)
- **Verifies:** C07, C08
- **Setup:** Faithful reproduction of the public modded-nanogpt frontier — PR #291 (Contra→Soft-Muon,
  Gram-Frobenius/Schatten-4 norm), PR #294 (outward-radial dampening + radius correction), PR #278
  (MLP SOAP, extended to MLP+V), PR #287 (power-law LR) — under the architecture guard.
- **Procedure:** Audit each ported mechanism against the public code; verify the radial projection/sign/
  placement and the Soft-Muon/Frobenius norm match; extend SOAP to MLP+V.
- **Expected outcome:** A faithful, stronger parent (v48) than the local family, reproducing the public
  bin before compression.
- **Evidence:** src/artifacts.md (submitted script header credits); related_work.md.
- **Run:** `v3u2950…v48…` families, codex_v3.

## E15 — Compression by phase-endpoint shifting (v3)
- **Verifies:** C07
- **Setup:** The faithful v48/PR#294 parent; compression by moving the Soft-Muon / radial / LR phase
  endpoints earlier while keeping the long back-loaded cooldown horizon.
- **Procedure:** Contrast phase-endpoint shifts (W205/W211) against hard horizon truncation (W198–W200);
  add variance-control levers (LACV) to fix mid-run seed offset.
- **Expected outcome:** Phase-endpoint shifts reach a statistically-viable 2940-boundary parent; hard
  horizon truncation is cold.
- **Evidence:** trace v3 compression nodes; evidence/tables/trajectory_summary.md.
- **Run:** `v3u2900-worker…` families (Worker70/98/171/188/205/211/247/251), codex_v3.

## E16 — W258 leave-one-out pruning → "nosphere" (v3)
- **Verifies:** C08, C09
- **Setup:** Leave-one-out ablation of the W258 stack at step 2949 (11 ablations: nosoft, nocontra,
  noqkcontrascale, noradial, notailradial, nolacv, nolacvfloor, nosphere, notangentsphere, nosoap,
  novsoap), plus the combined sphere removal.
- **Procedure:** Rank by delta; confirm the redundant removal at N=16; test whether two
  individually-removable terms compose.
- **Expected outcome:** SOAP and radial are load-bearing; the sphere-lookahead pull is redundant
  (`nosphere`, viable at N=16) but the two sphere terms do not compose → submitted record bin **2949**.
- **Evidence:** evidence/figures/v3_pruning.png, evidence/tables/v3_component_pruning.md,
  evidence/tables/v3_record_seeds.md.
- **Run:** `family=v3prune-w258loo-nosphere` (16 runs), `v3/codex/scratchpad/w258_2940_leave_one_out_pruning_20260513.md`, codex_v3.
