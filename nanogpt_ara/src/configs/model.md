# Model Configuration — Fixed GPT-124M (Benchmark-Frozen)

The architecture, batch, and data are **fixed by the benchmark rules** (`track_3_optimization`). They
are NOT levers — they are the frozen substrate against which all optimizer/schedule changes are made.
Source: INSIGHTS.md §0; `agents/cc_v1/runs/00001-muon-baseline-1-*/launched_script.py`.

## Architecture
- **Model**: GPT (nanoGPT / modded-nanogpt lineage), ~124M parameters.
- **Layers**: 12 transformer blocks.
- **Hidden dim**: 768.
- **Vocab size**: 50304.
- **Parameter partition** (drives the two-optimizer split):
  - 2-D block weight matrices (`ndim>=2` in `model.blocks`) -> Muon.
  - 1-D / embedding / output / scalar params -> AdamW.

## Initialization
- **Output projection**: zero-initialized (`if "proj" in name: p.data.zero_()`).
- **Embedding**: default init, then scaled x0.7 in the frontier recipe (a lever, §2.C.2 — listed here
  because it is an init detail; treated as a training config in `training.md`).

## Logit softcap
- **Form**: `15 * logits * (logits^2 + 15^2).rsqrt()` (a 15*tanh-style softcap).
- **Relevance**: the embed-init x0.7 lever works by reducing early saturation of this softcap.

## Data
- **Corpus**: FineWeb-10B (fixed).
- **Tokenization**: vocab 50304 (fixed).

## Batch / token budget
- **Batch**: 8 x 64 x 1024 tokens per step (fixed).
- **Step definition**: one forward-backward over the batch.

## Fixed-scope note
Per goal.md "Out of scope": architecture, batch size, and data may not be changed. Every conclusion in
this ARA is conditioned on this exact substrate; an architecture or data change could move the entire
frontier (constraints.md, C16, A1).
