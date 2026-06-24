# Problem Specification

> **t=0 FRAME.** This is the time-invariant problem statement known to the Codex agent at
> the very start of the experiment. It contains the mission, the two t=0 baselines, the
> target, and the open gaps — and NO findings. Every result crystallizes later through the
> replay.

## Observations

### O1: A fixed benchmark exists with a frozen architecture and a single success metric
- **Statement**: The task is to reach **3.28 validation loss** on the benchmark in
  `records/track_3_optimization/train_gpt_simple.py`. The architecture, batch size, and
  dataset are fixed by rule; each step is a single forward-backward pass. Success is defined
  solely by whether a run reaches val loss ≤ 3.28, and the quantity to minimize is the number
  of training steps required to get there.
- **Evidence**: `v1/codex/goal.md` (mission statement); `v1/codex/AGENTS.md` (lawful core
  rule 1, "Hard rules — benchmark"); `train_gpt_simple.py` (frozen setup — see
  `src/environment.md`).
- **Implication**: The search is over optimization recipes only (optimizer, schedule,
  init, per-group hyperparameters), not over the model or the data. The benchmark is a
  controlled, apples-to-apples comparison platform.

### O2: The current SOTA on this setup is Muon at 3500 steps; the AdamW baseline is 5625 steps
- **Statement**: At t=0 the best known recipe is **Muon** (lr=.025, wd=.0125) reaching the
  target in **3500 steps**. The **AdamW** baseline reaches it in **5625 steps**. Anything
  below 3500 steps is progress.
- **Evidence**: `v1/codex/goal.md`; `v1/codex/AGENTS.md` (header: "Current best: 3500 steps
  (Muon, lr=.025, wd=.0125). AdamW baseline: 5625 steps."). The Muon recipe is transcribed
  from the canonical baseline `launched_script.py` (see `src/environment.md`).
- **Implication**: 3500 steps is the bar every candidate must beat under the noise-floor
  gate. Muon already roughly 1.6× cheaper than AdamW establishes that optimizer choice is
  a large lever on this setup.

### O3: The optimization literature is a sea of unverified, often confounded SOTA claims
- **Statement**: There are hundreds to thousands of optimizer papers; most have never been
  compared head-to-head on the same setup. Some likely contain real ideas that have been
  ignored; some claimed-SOTA papers are confounded by undertuned baselines (the goal flags
  that, e.g., AdamW LR at this scale wants to be ~4–8e-3, not the canonical 3e-4).
- **Evidence**: `v1/codex/goal.md` ("Context"); `v1/codex/AGENTS.md` ("HP sweeps are
  first-class", citing the optimizers paper arXiv 2509.02046).
- **Implication**: The contribution is as much rigorous *verification* (including clean
  negative results on well-cited methods) as it is the discovery of a faster recipe.

## Gaps

### G1: It is unknown which post-Muon optimizers actually beat Muon when properly tuned here
- **Statement**: For the recent wave of optimizers (MuonClip, AdEMAMix, Adam-mini, Lion,
  Sophia, SOAP, Kron, Shampoo variants, sign-based methods, K-FAC / second-order methods,
  schedule-free methods, etc.), it is not known which — if any — beat Muon's 3500 steps on
  THIS exact setup once given a properly-tuned LR and schedule.
- **Caused by**: O3 (no head-to-head comparison on a common setup).
- **Existing attempts**: Not available at t=0 — no runs have been executed.
- **Why they fail**: Not available at t=0.

### G2: It is unknown whether older, under-benchmarked optimizers match Muon under a modern schedule
- **Statement**: Pre-2022 ideas (Lookahead, RAdam, NovoGrad, LARS / LAMB, AdaBelief, AggMo,
  QH-Adam, Polyak averaging, gradient surgery, sharpness-aware variants, Adan) may match or
  beat Muon when paired with a modern schedule (WSD, etc.), but this has not been tested here.
- **Caused by**: O3.
- **Existing attempts**: Not available at t=0.
- **Why they fail**: Not available at t=0.

### G3: It is unknown whether Muon's gain is orthogonal to other levers, and whether they stack
- **Statement**: Whether the gain from Muon is orthogonal to gains from {schedule changes,
  init / parameterization changes, second-order preconditioners, EMA tricks} — and whether
  those levers stack additively or interfere — is open.
- **Caused by**: O1 (each lever is independently in-scope), O2 (Muon is the incumbent).
- **Existing attempts**: Not available at t=0.
- **Why they fail**: Not available at t=0.

### G4: For each optimizer, the actually-best schedule is unknown and usually under-tuned in papers
- **Statement**: Most papers under-tune the schedule. The actually-best schedule shape
  (warmup, decay, WSD vs cosine vs trapezoid vs multi-stage vs schedule-free, end-of-training
  averaging) for a given optimizer on this setup is unknown.
- **Caused by**: O3.
- **Existing attempts**: Not available at t=0.
- **Why they fail**: Not available at t=0.

### G5: The noise floor and the seed budget needed to declare a step-gain significant are not yet pinned
- **Statement**: It is open where the noise floor sits and how many seeds it takes to declare
  a 50 / 100 / 200-step gain significant. AGENTS.md gives provisional estimates to recompute
  (`step_to_target` ≈ 50 steps; `final_val_loss` mean ≈ 0.001), but these must be re-measured
  from baseline-Muon at 3 seeds.
- **Caused by**: O1 (step count is the metric, so its variance gates every claim).
- **Existing attempts**: Provisional noise-floor estimates in AGENTS.md, not yet validated.
- **Why they fail**: Not available at t=0.

### G6: It is unknown whether a method that loses early on the loss-curve can still win on step-to-3.28
- **Statement**: There may be a regime where an optimizer with a worse early loss curve
  nonetheless reaches 3.28 in fewer steps; this "bin" metric (`step_to_3.28`) is not the same
  as final loss, and the relationship has not been characterized on this setup.
- **Caused by**: O1 (success is a threshold-crossing metric, not final loss).
- **Existing attempts**: Not available at t=0.
- **Why they fail**: Not available at t=0.

## Key Insight
- **Insight**: Because the architecture, batch, and data are frozen and one success metric
  (`step_to_3.28`) is fixed, a controlled head-to-head search over optimization recipes can
  separate real optimizer/schedule/init gains from the undertuned-baseline confounds that
  pervade the literature — provided every candidate is gated by a measured noise floor and
  reproduced across seeds.
- **Derived from**: O1 (fixed benchmark + single metric), O2 (a strong incumbent to beat),
  O3 (the literature's confound problem).
- **Enables**: A disciplined exploration of the optimizer / schedule / init space (the
  "lawful core" loop) whose positive AND negative results are both contributions.

## Assumptions
- A1: The benchmark is wallclock-irrelevant — methods that are slow per step are acceptable
  if they cut the step count (so full-matrix preconditioners like Shampoo / SOAP are fair
  game). (Source: `v1/codex/goal.md`.)
- A2: Compute is effectively unlimited in wall-clock terms: one node, 8×{H100,H200}, ~15 min
  per run, one run at a time, no calendar deadline. (Source: `v1/codex/goal.md` "Budget".)
- A3: Modifications are confined to the `Optimization` and `Init & Optim Hyperparams` sections
  of the script; init scaling and optimizer-schedule changes are fair game; submitted runs
  hardcode HPs (no CLI args). (Source: `v1/codex/AGENTS.md` "Hard rules — benchmark".)
- A4: Variance on this benchmark is real; nothing under ~50–100 steps is treated as signal
  until reproduced on a second seed. (Source: `v1/codex/AGENTS.md` "Interpreting results".)
