# Problem Specification

The benchmark is `track_3_optimization` from [modded-nanogpt](https://github.com/KellerJordan/modded-nanogpt):
reach validation loss **3.28** on GPT-124M in as few training steps as possible, changing only the
optimizer / schedule / initialization / a few hyperparameters. Architecture, batch size, and data
are fixed. The headline metric is `step_to_3_28` = the first training step whose validation loss
<= 3.28 (lower is better). Wall-clock is irrelevant by design.

## Observations

### O1: A strong published baseline already exists
- **Statement**: The Muon reference reaches 3.28 in **3500 steps** (run `00001-muon-baseline`,
  `train.log` ends `step:3500 val_loss:3.28027`). The AdamW baseline needs **5625 steps**. The best
  public record at the start of the experiment was **3225** (README).
- **Evidence**: §0 of INSIGHTS.md; `runs.csv` row `00001-muon-baseline-1` (`final_step=3500`,
  `final_val_loss=3.28027`); goal.md reference points.
- **Implication**: The starting point is already near a well-tuned optimum; remaining headroom is small.

### O2: The baseline is a two-optimizer recipe with hand-set per-group learning rates
- **Statement**: AdamW handles the 1-D / embedding / output params (`embed.weight lr=0.3`,
  `proj.weight lr=1/320~=0.0031` zero-initialized, scalars `lr=0.01`, betas (0.8,0.95), eps 1e-10,
  wd 0); Muon handles every 2-D block weight (lr=0.025, wd=0.0125, mu=0.95) via Nesterov momentum ->
  12-iteration Newton-Schulz orthogonalization -> scale by `max(1, rows/cols)**0.5`. Schedule is WSD
  (stable 30%, then linear cooldown to 0 over the final 70%, `cooldown_frac=0.7`).
- **Evidence**: §0; `agents/cc_v1/runs/00001-muon-baseline-1-*/launched_script.py`.
- **Implication**: There are many independent knobs (per-group LR, NS conditioning, schedule shape,
  init scale) — gains, if any, must come from second-order details, not the core update.

### O2b: Single levers are individually tiny
- **Statement**: Documented integrated levers are each worth only -0 to -0.005 val loss:
  embed-init x0.7 = **dval -0.00091**, NorMuon = **-0.00155**, MuonEq = **-0.00484** (3-seed means).
- **Evidence**: §2, §9.1; cc_v1 `ideas.md` 3-seed deltas.
- **Implication**: No single substitution can move the frontier far; gains must compound.

### O3: The seed noise floor is comparable to the single-lever gains
- **Statement**: Within one config, `final_val_loss` std is ~**0.0004-0.0010** (8-seed frontier
  group A std 0.00043; safe group B std 0.00100; seed_reverify pooled 0.0009-0.0011). At the
  frontier ~**9-12% of seeds miss 3.28 entirely** (1/8 in group A; 14/152 = 9% pooled).
- **Evidence**: §9, §21; `seed_reverify` metadata (13 groups, 152 runs).
- **Implication**: A single-best-seed record overstates; small-lever claims need multi-seed
  reproducers, and step counts below ~15 steps are within noise.

### O4: `step_to_3_28` is quantized by the validation cadence
- **Statement**: The default cadence logs validations every 125 steps (and densely near the end), so
  the model crosses 3.28 *between* logged validations. Forcing a validation at step 3450 reproduces a
  hit (3.27844) the default 3500-cadence "misses"; 3425 misses (3.28178).
- **Evidence**: §6.1, §8.3; `v1/codex/scratchpad/picklist.md` §1a.
- **Implication**: Part of the train-steps "gain" is a *measurement* artifact; the metric is too
  coarse to resolve its own frontier without dense late validation or seed-averaging on `min_val_loss`.

### O5: Under a novelty constraint, the frontier got *worse*
- **Statement**: Forbidding "known methods + hyperparameter tweaks", both agents' best fell from
  ~3000 (v1) to **3375** (novelty wave). The top novel operator merely matched a re-validated plain-Muon
  baseline (also 3375).
- **Evidence**: §4, §10; `runs.csv` families `cc_novelty`/`codex_novelty` best 3375.
- **Implication**: On this saturated target, most available gain lives in tuning/stacking known-good
  levers, not in inventing new operators.

### O6: A method's effect flips sign with context
- **Statement**: Full-model SOAP asymptotes at ~3.39 (fails), but SOAP restricted to MLP + value-
  projection matrices is the single biggest *hitting* lever in v3 (~+85 steps when removed). Muon^2
  showed -175 steps against vanilla Muon in a public PR but regressed inside the stacked recipe.
- **Evidence**: §2.D, §3.2, §5.3, §16; `runs.csv` `family=muon2f` (best 3190), full-SOAP `00182`.
- **Implication**: Public-PR gains measured against vanilla Muon do not transfer additively; every
  lever must be re-tested at the *current* backbone.

## Gaps

### G1: "Which optimizer is best" is the wrong question for a saturated benchmark
- **Statement**: There is no single optimizer swap that captures the available gain.
- **Caused by**: O1 (strong baseline), O2b (tiny single levers), O6 (sign flips).
- **Existing attempts**: SOAP/Shampoo, Cautious-Muon, Lookahead-Muon, AdEMAMix-Muon, Muon^2 — all
  fail or regress as global substitutions (§2.D).
- **Why they fail**: Muon's Newton-Schulz orthogonalization already captures most cheap curvature at
  124M scale, so a substitute preconditioner adds cost without signal.

### G2: Single-best-seed records are not reproducible science
- **Statement**: Headline step counts are a lucky tail over a noisy floor.
- **Caused by**: O3 (seed std ~ lever size), O4 (cadence quantization).
- **Existing attempts**: Reporting best-of-N from large sweeps.
- **Why they fail**: ~9-12% of frontier seeds miss the target; two near-frontier configs differing by
  10-20 steps are dominated by the miss-rate tail.

### G3: A "good early loss curve" is not the objective
- **Statement**: The benchmark rewards crossing 3.28 early, not the lowest loss; an optimizer can be
  *behind* on the loss curve for ~1700 steps and still win on step-to-3.28.
- **Caused by**: O1, the step-count metric.
- **Existing attempts**: Greedy early-loss minimization (full SOAP) loses early *and* never recovers.
- **Why they fail**: A slow start only pays off if it buys conditioning, not always.

### G4: Where exactly does the ~17% gain come from, and how much is each piece worth?
- **Statement**: A stacked recipe of ~10 levers gives the gain, but their individual marginal
  contributions at the frontier were unknown.
- **Caused by**: O2b (compositional), O6 (context-dependence).
- **Existing attempts**: Per-lever 3-seed reproducers at the canonical point (good for sign, not for
  frontier marginal value).
- **Why they fail**: A lever neutral at the baseline can become critical (or dead) once the rest of
  the recipe saturates — needs leave-one-out at the frontier.

## Key Insight
- **Insight**: On a saturated step-count benchmark, the gain is a **compositional stack of many
  small, published levers re-tuned to a shared backbone**, organized as a **temporal curriculum**
  (explore early -> exploit late). A lever's value is a property of the *whole stack and the
  parameter subset it touches*, not of the lever in isolation; and because the per-seed noise floor
  is the same size as a single lever, claims must be seed-verified medians, not best-of-N.
- **Derived from**: O1, O2b, O3, O6.
- **Enables**: A leave-one-out ablation that ranks every component (C13); a per-role differentiation
  principle across LR, weight decay, and schedule (C06); a seed-budget rule matched to effect size
  (C17); and an honest account of what transfers vs what is benchmark-specific (C16).

## Assumptions
- A1: The architecture (GPT-124M: 12 layers, dim 768, vocab 50304), batch (8x64x1024 tokens), and
  data (FineWeb-10B) are fixed by the benchmark rules; all conclusions hold only inside that box.
- A2: `step_to_3_28` (first val <= 3.28) is the objective; wall-clock / per-step FLOPs are explicitly
  free (the benchmark permits slower-per-step methods).
- A3: The 3.28 threshold is exact; the recipe is tuned to cross *that specific number* as early as
  possible, not to minimize loss generally.
- A4: Numbers are taken from the run export and logs (`runs.csv`, `train.log`, `metadata.json`,
  agent scratchpads); they are never invented. Uncertain mechanistic claims are tagged `[HYP]`.
