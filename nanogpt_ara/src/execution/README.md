# src/execution — submitted recipe scripts

These are the three submitted record recipes, captured in their native form (full
`train_gpt_simple.py`-derived training scripts with all hyperparameters hardcoded). Each is a
concrete, runnable artifact — not a re-encoding of prose.

`# Grounding: transcribed` — each file is copied **verbatim** (byte-for-byte) from the source repo;
no line was authored or modified by the compiler. Source paths:

| File here | Bin | Transcribed from |
|---|---|---|
| `v1_v12iso_musched_s3195.py` | 3205 (v1) | `v1/codex/scratchpad/variants/train_gpt_simple_v12iso_musched_h3375_s3195_seed0.py` |
| `v2_legal_v12opt_ts3037.py` | 3037 (v2) | `v2/codex/scratchpad/variants/legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py` |
| `v3_nosphere_ts3020.py` | 2949 (v3) | `v3/codex/scratchpad/variants/v3prune_w258loo_nosphere_spherela_p012_qkcontra0125_cvfloor060_softceil075_end2905_sched3025_vfade2850_rad045_warmsoapskip_ts3020.py` |

Notes:
- The v1 file is the `s3195` seed-0 variant of the v12iso/MuSched stack; the submitted bin 3205 is
  the conservative, statistically-passing checkpoint of this same stack family (see C08 / L4).
- The v3 file runs to `train_steps=3020` (`schedule_steps=3025`); the submitted bin 2949 is the
  logged step-2949 checkpoint of this run, with `SPHERE_LOOKAHEAD_PULL = 0.0` (the nosphere prune).
- Each recipe's per-component contribution is in the matching `src/configs/v{1,2,3}_pruning_data.json`
  and charted in `evidence/figures/v{1,2,3}_pruning.md`.
- The architecture/forward block in each file is byte-identical to the workspace baseline
  `train_gpt_simple.py` (the v2 compliance rule, C05); only the optimizer / init / schedule sections
  differ.
