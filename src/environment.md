# Environment

> **t=0 FRAME.** The frozen benchmark, transcribed verbatim from the canonical baseline run's
> `launched_script.py` (the t=0 Muon SOTA recipe itself). By rule, the architecture, batch
> size, and data are fixed for the entire experiment — so everything in this file is
> time-invariant. The ONLY tunable surface (optimizer, schedule, init, per-group HPs) is the
> search space described in `logic/problem.md`; nothing here is a finding.

- **Language/runtime**: Python; PyTorch (version printed at runtime via
  `torch.version.__version__` / `torch.version.cuda` — exact version not pinned in the script).
- **Framework**: PyTorch (`torch`, `torch.nn`, `torch.nn.functional`, `torch.distributed`),
  with `torch.compile` / `model.compile(dynamic=False)` and `@torch.compile` on the Muon update.
- **Hardware**: 1 node, 8×{H100,H200} GPUs; launched with
  `torchrun --standalone --nproc_per_node=8`. The script asserts `8 % world_size == 0` and is
  stated to run equivalently on 1, 2, 4, or 8 GPUs.
- **Data sources**: FineWeb 10B token shards — train `data/fineweb10B/fineweb_train_*.bin`,
  validation `data/fineweb10B/fineweb_val_*.bin`. Binary shard format with a 256×int32 header
  (magic number `20240520`, version `1`); tokens stored as `uint16`. Sequence length 1024.
- **Key dependencies**: `torch` (with CUDA + NCCL backend), standard library (`os`, `sys`,
  `uuid`, `time`, `pathlib`). No version lockfile is present in the script.
- **Protocols**: Single training run launched by the one-liner above; the script self-logs its
  own source code at the top of each result log; validation is computed on a fixed grid and the
  objective is `step_to_3.28` (see `logic/concepts.md`). Source provenance: this benchmark
  descends from the NanoGPT speedrun (`https://github.com/KellerJordan/modded-nanogpt`),
  prepared as a simplified version for optimization research.
- **Random seeds**: No explicit seed is set in the baseline script; reproduction across seeds
  is a benchmark *rule* (two-seed reproduction), not a value hardcoded here. Seed-setting is
  part of the per-run protocol, not the frozen environment. ("Not available at t=0" as a fixed
  constant.)

## Frozen model architecture (transcribed)

A 12-layer pre-norm GPT (decompiled from the `GPT` / `Block` definitions):

- **`vocab_size = 50304`**, **`num_layers = 12`**, **`model_dim = 768`**.
- **Embedding**: `nn.Embedding(vocab_size, model_dim)` cast to bfloat16; its output passes
  through an RMSNorm (`norm1`) before the blocks.
- **Block** (×12, residual, pre-norm): `x = x + attn(norm1(x))` then `x = x + mlp(norm2(x))`,
  where `norm1`/`norm2` are per-block `RMSNorm(model_dim)` with a learnable `gains` parameter.
- **Attention** (`CausalSelfAttention`): `head_dim = 128`, so `num_heads = model_dim // head_dim
  = 6`. Separate `q`, `k`, `v`, and output `proj` linear layers (each with bias). Q and K are
  RMS-normalized (`norm(q)`, `norm(k)`) and then rotary-embedded before attention. Attention is
  `F.scaled_dot_product_attention(..., scale=0.12, is_causal=True)` (fixed scale 0.12, causal).
- **Rotary** (`Rotary`): half-truncated RoPE with base-frequency tuning —
  `angular_freq = (1/1024) ** linspace(0, 1, head_dim//4)`, concatenated with zeros over the
  other `head_dim//4`.
- **MLP**: hidden dim `4 * model_dim = 3072`; `fc` then ReLU-squared (`x.relu().square()`) then
  `proj`. Both linears have bias.
- **Output head**: a final `RMSNorm` (`norm2`) then `proj = Linear(model_dim, vocab_size)`.
- **Logit softcap**: logits are computed in float32 and softcapped as
  `15 * logits * (logits.square() + 15**2).rsqrt()` (cap constant 15) before the loss.
- **Loss**: `F.cross_entropy(..., reduction="sum")` over all target tokens.
- **`Linear`/`RMSNorm`**: custom `Linear` casts weight and bias to the input dtype; `norm(x) =
  F.rms_norm(x, (x.size(-1),))`.

> These constants (50304, 768, 12, 128, 3072, 1024, scale 0.12, softcap 15, RoPE base 1024)
> are FROZEN benchmark architecture, not tunable knobs.

## Frozen data / batch / step definition (transcribed)

- **`batch_size = 8 * 64 * 1024 = 524288` tokens** per optimizer step (global).
- **`mbs = 64`** microbatch size (sequences); microbatches are accumulated only to emulate
  fewer-than-8-GPU runs, NOT to change the effective batch — the benchmark rule is **one
  forward-backward per step**.
- **`seq_len = 1024`** tokens per sequence.
- **`val_tokens = 20 * 524288 = 10485760`** tokens held for validation (one fixed batch drawn
  once at startup).
- **Gradient reduction**: `dist.all_reduce(p.grad, SUM)` across ranks each step; Muon
  additionally `all_gather`s updated params across the world.
- **A "step"**: one fetch of `(inputs, targets)` from the train loader → forward+backward (one
  `.backward()`, accumulated over microbatches only for sub-8-GPU emulation) → grad all-reduce →
  `set_hparams(step)` → `opt.step()` for each optimizer → `zero_grad`. This is the unit that
  `step_to_3.28` counts and the quantity to minimize.

## t=0 optimizer recipe (the SOTA itself — transcribed, time-invariant baseline)

This is the canonical Muon baseline recipe, the t=0 SOTA at 3500 steps. It is the *starting
point* of the search, transcribed here as the frame's baseline. The tunable surface lives
entirely inside the `Optimization` and `Init & Optim Hyperparams` sections.

- **`train_steps = 3500`** (the quantity to minimize while still reaching 3.28; this is the
  incumbent SOTA value, NOT a discovered improvement).
- **Init**: every parameter whose name contains `"proj"` is zero-initialized
  (`p.data.zero_()`); all other parameters keep their default init.
- **`optimizer1` = AdamW** over three groups: `model.embed.weight` (lr 0.3),
  `model.proj.weight` (lr 1/320), and every parameter with `ndim < 2` (lr 0.01); shared
  `betas=(0.8, 0.95)`, `eps=1e-10`, `weight_decay=0`, `fused=True`.
- **`optimizer2` = Muon** over the 2D block weights
  (`[p for p in model.blocks.parameters() if p.ndim >= 2]`); **lr 0.025, weight_decay 0.0125**,
  `mu=0.95` (Nesterov), NS5 with 12 iterations. (See `logic/concepts.md` for Muon / NS5.)
- **Coverage assertion**: the union of all optimizer-group params equals all model params.
- **LR schedule**: `set_hparams(step, cooldown_frac=0.7)` — stable-then-decay (WSD-style):
  `eta = 1.0` while `progress < 1 - cooldown_frac`, else `eta = (1 - progress)/cooldown_frac`;
  applied multiplicatively to each group's `initial_lr`. No warmup.
- **Validation cadence**: every 125 steps and at the final step; `val_loss` is summed over all
  validation microbatches, all-reduced, and divided by `val_tokens`; logged to a per-run
  `logs/<uuid>.txt`.
