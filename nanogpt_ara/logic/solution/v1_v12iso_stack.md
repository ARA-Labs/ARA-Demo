# v1 — the v12iso / MuSched stack (submitted bin 3205)

The v1 wave was an open-ended search from canonical Muon. It produced two things: (1) the
**horizon/stop schedule-decoupling lever** (C01) that unlocked the first improvements over the 3500
baseline, and (2) the accreted **v12iso** stack whose load-bearing structure is characterized by
leave-one-out pruning (C03).

Concrete artifact: [`src/execution/v1_v12iso_musched_s3195.py`](../../src/execution/v1_v12iso_musched_s3195.py)
(transcribed verbatim from the wave's `variants/` directory). Submitted record + figures:
`evidence/tables/v1_seed_table.md`, `evidence/figures/v1_loss_curves.md`,
`evidence/figures/v1_pruning.md`.

## Stack composition (top of the accretion)

1. **NorMuon** — Polar-Express Newton-Schulz orthogonalization + row second-moment normalization on
   hidden matrices; colder preconditioner momentum (`beta2 0.90 → 0.80` thaw) and Muon LR ~0.030 (C02).
2. **Muon2F (2-factor preconditioning)** — factorized row/column preconditioning of the matrix
   gradient before orthogonalization (`pre_eps=1e-3`). **Load-bearing** (LOO removal +0.00229).
3. **Split hidden optimizers** — non-`mlp.proj` hidden matrices use **AggMo3** (3-term aggregated
   momentum) + 2-factor preconditioning; **`mlp.proj`** uses an **error-feedback residual** path that
   reinjects the orthogonalization residual (LOO `noErrorFeedback` +0.00076 — the third-largest).
4. **Adam-mini** aux optimizer — rowwise second-moment denominators for embed/head, tensorwise for
   1-D params.
5. **Tail-EMA evaluation shadow** — full-model EMA started at step 2000, `beta=0.99`, swapped in only
   for validation. **The single most load-bearing component** (LOO `noTailEMA` +0.00251).
6. **Tail residual mechanics on `mlp.proj`** — feedback ramp 0.04→0.04804, residual decay ramp
   0.05→0.022, a momentum refresh at step 3125, residual pulse / RMS-normalization at step 3125.
   Individually near-noise in the LOO (residual pulse, momentum refresh, beta2-thaw, late-LR all
   within ±0.0001) — i.e. tuning, not structure (C03).
7. **Muon mu schedule** — `0.85 → 0.95` over 300 steps, `0.95 → 0.85` over the last 50; beta2 thaw
   after 2500; linear LR cooldown on `schedule_steps=3375`. Isolating this mu-schedule lever beat the
   full v12 packages (LOO `noMuSched` +0.00091).

## How the bin was reached

The descent ran 3500 → 3450 (horizon decoupling) → 3350 (NorMuon + colder horizon) → 3296 (residual
stack + AggMo) → 3250 (Adam-mini / Muon2F) → ~3195 (tail-EMA + isolated mu-schedule). The aggressive
single-seed region (~3170) was statistically **rejected** in the final pass; the user added a margin
and the submission settled at **bin 3205**, validated over n=16 seeds (mean 3.27897, score 0.004112;
see C08).

## Why these and not the rest

The wave screened a very large optimizer/init catalog (SOAP, MARS-M, Cautious-Muon, gradient
centralization, dozens of second-order replacements, clean-init families) — almost all clean
negatives on this setup (see `trace/exploration_tree.yaml` dead-end nodes and `related_work.md`
RW15). The surviving stack is exactly the set whose leave-one-out removal degrades the boundary.
