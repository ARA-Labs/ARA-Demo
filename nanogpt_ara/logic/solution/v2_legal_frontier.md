# v2 — the legal frontier (submitted bin 3037) and the compliance quarantine

The v2 wave is two stories: a **research-integrity event** (C05) and a **role-split optimizer
frontier** (C04). Concrete artifact:
[`src/execution/v2_legal_v12opt_ts3037.py`](../../src/execution/v2_legal_v12opt_ts3037.py)
(transcribed verbatim). Evidence: `evidence/tables/v2_seed_table.md`,
`evidence/figures/v2_loss_curves.md`, `evidence/figures/v2_pruning.md`.

## The compliance quarantine (the central narrative)

v2 was handed a **"v12" parent that traces to the cc / Claude agent** — chosen as the experimental
backbone because it was the only known 3025-step parent. A code-comparison check flagged early that
v12 differed from the public script in numerics, but the work proceeded provisionally and pushed the
v12-derived frontier **below 3000 steps** (single-seed crossings ~2999).

Then the **user flagged a real forward-path violation**: every v12-derived variant had rewritten
`RMSNorm.forward` as `(norm(x.float()) * self.gains).type_as(x)` instead of the workspace baseline
`F.rms_norm(x, (x.size(-1),), weight=self.gains.type_as(x))`, with attention q/k normalization routed
through the same helper. **Under bf16 this is a precision/behavior change in the forward path and is
invalid even though mathematically close.** Codex:

1. **Stopped the live push and quarantined** every v12-derived `v2cx` result — they may not be
   reported as frontier improvements (the sub-3000 numbers are invalid).
2. **Adopted a byte-identity rule** — never change `RMSNorm`, attention normalization, or any
   `forward` path; build only from the workspace `train_gpt_simple.py`.
3. **Rebuilt a compliant "legal_v12opt" family** with an empty Architecture-block diff, and changed
   the launcher prefix `v2cx → v2cxleg` (separate worktree root) so invalid and valid runs cannot mix.
4. **Added a launcher-time static gate** (E08) that exits before Slurm submission on any non-byte-
   identical Architecture diff, any `RMSNorm.forward` / q-k `F.rms_norm` change, or optimizer logic
   routed through norm-gain parameters.

The honest cost: the agent noted the *illegal* forward-path change had **materially helped** the
sub-3000 behavior, so the legal stack is higher-variance and slower to cross — the byte-identical
rebuild gave back frontier. This is the C05 evidence that compliance must be by byte-identity, not by
equivalence judgement.

## The legal stack (built on the byte-identical base)

1. **Polar Express NS-5 + MuonEq row-normalized update**, `_CONTRA_MUON = 0.225` (the `cm0225`
   signal). MuonEq is the second-largest load-bearing component (LOO `noMuonEq` +0.00353).
2. **Role-specific Muon LR multipliers** of base LR 0.045: q/k 0.61875, v 0.625, attn.proj 0.6375,
   mlp.fc 1.0125, mlp.proj 0.9875. **The dominant lever** (LOO `noRoleLR` +0.00292) (C04).
3. **Role-specific weight decay** ~0.027..0.0315 instead of one body-wide value (LOO `noRoleWD`
   +0.00041).
4. **Muon lookahead** from step 2450, interval 25, alpha 0.35, pull 0.15, 150-step smoothstep ramp
   (LOO `noLookahead` +0.00117).
5. **embed init ×0.7, AdamW betas (0.8, 0.95), eta_min 0.02, Muon schedule 0.85→0.95→0.85** (the
   schedule LOO `noMuSched` +0.00459 at n=3; `noEmbedInit` +0.00092; `noEtaMin` +0.00097).

`noContraMuon` (+0.00008) is near-noise — Contra shaping is inherited but not load-bearing at this
operating point.

## How the bin was reached

The single-seed legal frontier descended 3000 → 2998 → … → 2962 (rolelr2 + lookahead). But the
**fixed-step cohort significance test failed at every step below ~3012**; the earliest passing
checkpoint was **3037** (+75 over the single-seed frontier), submitted at n=16 (mean 3.27853, score
0.00588; C08). The single-seed 2962/2963 crossings are recorded as stepping stones, not the bin.
