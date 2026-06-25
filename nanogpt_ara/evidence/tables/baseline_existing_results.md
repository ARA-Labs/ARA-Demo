# Table: starting bar — existing result logs (Muon / AdamW baselines)

**Source.** `novelty/codex/scratchpad/existing_results_summary.md` (transcribed verbatim). Crossing
steps use only observed validation log lines (`step % 125 == 0` plus the explicit final validation);
no interpolation. This is the bar the four waves were measured against.

| log (id) | optimizer family | key HPs | train_steps | final val | first val ≤ 3.28 |
| --- | --- | --- | -: | -: | -: |
| 311d7833… | Muon + AdamW aux | Muon lr=0.025, wd=0.0125; cooldown_frac=0.7 | 3500 | 3.27673 | 3500 |
| 9754c285… | Muon + AdamW aux | Muon lr=0.025, wd=0.01 | 3600 | 3.27655 | 3500 |
| dfe8f6ce… | Muon + AdamW aux | Muon lr=0.025, wd=0.0125 | 3600 | 3.27519 | 3500 |
| 7b8270c5… | Muon + AdamW aux | Muon lr=0.02, wd=0.01 | 3600 | 3.27765 | 3600 |
| c0ca36ae… | Muon + AdamW aux | Muon lr=0.02, wd=0.01 | 3550 | 3.27940 | 3550 |
| f00ed19c… | Muon + AdamW aux | Muon lr=0.02, wd=0.01 | 3550 | 3.28007 | none |
| 9a0b5bc5… | AdamW block + aux | block lr=0.0015, wd=0.10, warmup=250 (all groups) | 5750 | 3.27152 | 5500 |
| a63a68d1… | AdamW block + aux | block lr=0.0015, wd=0.10, warmup=250 (all groups) | 5625 | 3.27903 | 5625 |
| 63b551e7… | AdamW block + aux | block lr=0.0015, wd=0.10, warmup=250 (block only) | 5750 | 3.27430 | 5625 |
| fca8cb20… | AdamW block + aux | block lr=0.0015, wd=0.1125, warmup=250 (block only) | 5750 | 3.27594 | 5625 |
| 43d49634… | AdamW block + aux | block lr=0.0015, wd=0.075, warmup=250 (block only) | 5750 | 3.27787 | 5750 |
| e7781785… | AdamW block + aux | block lr=0.0015, wd=0.125, warmup=250 (block only) | 5750 | 3.27917 | 5750 |
| 7739713a… | AdamW block + aux | block lr=0.001, wd=0.125 | 5750 | 3.28409 | none |
| 78591da3… | AdamW block + aux | block lr=0.0015, wd=0.10 (all groups) | 5500 | 3.28082 | none |
| dd79d7db… | AdamW block + aux | block lr=0.002, wd=0.125 | 5750 | 3.28018 | none |

## Starting bar and noise floor (verbatim findings)
- The local baseline script is already the best-known Muon recipe: `train_steps=3500`, Muon
  `lr=0.025`, `wd=0.0125`, final `val_loss=3.27673`.
- The same Muon HPs at 3600 steps reach 3.27829 at step 3500 and 3.27519 at 3600; the 3500-step
  crossing margin is only ~0.0017–0.0033 below target — sub-125-step claims near here are noise-sensitive.
- The next meaningful observed grid target below 3500 is 3375, where existing Muon logs are still
  above threshold (≈3.281–3.287); a real 3375 result needs a several-thousandths improvement, not noise.
- AdamW is a much weaker starting family (crosses at 5500–5625); useful as a sanity baseline, not the bar.

**Supports.** O1, O2, O3 (problem.md); the bar for C01–C08 and every exploration-tree outcome.
