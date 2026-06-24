# Heuristics — NOVELTY LANE (isolated sub-namespace inside the single ara/)

> **wave: novelty | isolation: hard.** Implementation/interpretation rules with rationale,
> crystallized only on a closure signal. Present-state snapshots; history in `trace/novelty/`.

## HV01: Init-only branch-gain rescales preserve the early loss edge but do not move step_to_3.28; truncating the schedule confounds the readout
- **Rationale**: Across the init family this window (RSI value/fc & q/k/hidden gains, VFG
  value+fc gain, NGI block-RMSNorm gain imbalance, SVC square-law branch gain), the strongest
  cells preserved the early-to-mid-training loss edge but flattened to the baseline curve by
  mid-run, so they did not improve the `step_to_3.28` crossing at the full 3500 schedule. Apparent
  crossings appeared only under shortened `train_steps` probes (t3450/t3475), which confounds the
  init effect with cooldown-schedule truncation and did NOT reproduce across seeds (NV10). Read
  init-family signals at the full schedule, and reproduce a crossing on a distinct seed with the
  SAME script (not a shorter `train_steps` variant) before believing it.
- **Status**: active
- **Provenance**: ai-suggested
- **Sensitivity**: high — the crossing depended on the exact cooldown horizon and the seed; a
  25-50 step apparent gain was inside the noise band and vanished on reproduction.
- **Code ref**: `novelty/codex/scratchpad/variants/{rsi001_gain090.py, vfg001_gain090.py,
  ngi001_n095_m105.py}` (init-only edits; proj zero-init preserved)
- **Crystallized via**: empirical-resolution (the init crossings were resolved as
  non-reproducible / schedule-confounded within this turn). From staging OV07.
- **Bound to**: NV04, NV10
