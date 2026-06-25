# Constraints, assumptions and limitations

## Binding benchmark rules (the fixed contract)

These surfaces of `train_gpt_simple.py` are fixed and must not be changed by any submitted run.
A change to any of them is out of scope and (for the forward path) a disqualifying architecture
violation (see C05). Source: the agent's own `existing_results_summary.md` "Baseline Constants to
Preserve" plus the goal.md scope sections.

- **Data / batching (fixed).** Training shards `data/fineweb10B/fineweb_train_*.bin`; validation
  shards `fineweb_val_*.bin`; `val_tokens = 20 * 524288`; `batch_size = 8 * 64 * 1024`; `mbs = 64`;
  sequence length 1024.
- **Model (fixed).** `GPT(vocab_size=50304, num_layers=12, model_dim=768)`; attention `head_dim=128`,
  causal, `scale=0.12`; MLP hidden `4*dim`, squared ReLU; final logit soft cap
  `15 * logits * (logits.square() + 15**2).rsqrt()`; RMSNorm with learned gains; Linear `bias=True`;
  embedding `.bfloat16()`; half-truncated RoPE.
- **Forward path (fixed, byte-for-byte).** `GPT.forward`, `RMSNorm.forward`, attention q/k
  normalization, logits, loss/objective. Even a mathematically-equivalent rewrite is invalid because
  it can change bf16 precision behavior (C05).
- **Init partition (fixed).** Zero every parameter whose name contains `"proj"` before optimizer
  creation; aux AdamW owns `embed.weight`, `proj.weight` and all `ndim < 2`; the matrix optimizer
  owns `[p for p in blocks.parameters() if p.ndim >= 2]`.
- **Step semantics (fixed).** Exactly one forward-backward per step; no multi-step inner loops, grad
  accumulation tricks, batch-size or data changes.
- **Success criterion (fixed).** `val_loss <= 3.28`, observed on the `step % 125 == 0` grid plus the
  explicit final validation; the submitted step is the bin.

## What is in scope (the only allowed degrees of freedom)

Optimizer changes (any), per-parameter-group HPs, schedules (warmup/decay/WSD/cosine/trapezoid/
schedule-free), init scale and per-module init differences, LR/WD/β/ε/momentum. Diagnostic
instrumentation is allowed but submitted runs use the canonical script with HPs hardcoded.

## Assumptions carried by the claims

- The noise floor (~50 steps / ~0.001 val_loss) is stationary across the 3000–3500 region (A3).
- `sigma = 0.0013` is the per-seed val_loss std used in the significance z-test (A4).
- Seed control fixes the validation batch so cross-seed variation is init/optimizer-state only (A2).

## Limitations of this artifact

- **L1 — Single-agent slice.** Only Codex's own runs are included. Cross-agent touchpoints (cc v12,
  opus v15/v48) are recorded as attributed provenance, not as Codex results. The blocklisted v2/v3
  `goal.md` frontier tables (which headline other agents' bins) are deliberately excluded.
- **L2 — Leave-one-out is one-at-a-time.** Pruning deltas (C03, C04, C06) do not capture
  super-additive interactions among components removed together; the one documented composition test
  (v3 `nosphere-notangent`) shows the two sphere removals do not compose.
- **L3 — Per-component ablations use small cohorts.** Several v3 LOO ablations are n=3; only the
  submitted baselines use n=16. Removal deltas from small-n ablations are directional.
- **L4 — Internal tension in v1.** The wave's running notes promoted a 3170 "practical floor", but
  the final statistical pass rejected 3170 (negative score) and settled the submission at 3205. The
  artifact reports the conservative, statistically-passing bin; the aggressive single-seed frontier
  is recorded as stepping-stone evidence only.
- **L5 — Numbers are point-in-time.** The bins and means are the submitted-record values; the raw
  per-seed logs (~3 GB) are git-ignored on disk and not reproduced here (the run *index* is).
