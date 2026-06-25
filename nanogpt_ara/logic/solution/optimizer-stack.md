# The submitted recipes, component by component

The three submitted records as concrete stacks. Constants are grounded in the
`record_configs/*/README.md` (opened firsthand); per-component contributions are the leave-one-out
`Δval when removed` from each wave's `pruning_data.json` (positive ⇒ the component helped). Exact
numbers are evidence-layer facts, reached via the figures/tables in [../../evidence/](../../evidence/);
this file is the structured method description, not the record.

---

## v1 — `v12iso` / MuSched stack → bin 3205 (n=16)

The v1 record keeps the fixed contract and combines (per
`record_configs/20260515_codex_v1_v12iso_3205/README.md:5-11`):

1. **NorMuon** with Polar-Express-style Newton–Schulz projection and row/column preconditioning on
   the hidden matrices.
2. **Split hidden optimizers**: non-`mlp.proj` matrices use AggMo3 + 2-factor preconditioning;
   `mlp.proj` uses error-feedback residuals.
3. **Tail mechanics on `mlp.proj`**: feedback ramp `0.04 → 0.04804`, residual-decay ramp
   `0.05 → 0.022`, a momentum refresh at step 3125, and residual pulse/RMS normalization at 3125.
4. **Tail-EMA evaluation** from step 2000 (`β=0.99`).
5. **Muon `μ` schedule** `0.85 → 0.95` over 300 steps and `0.95 → 0.85` over the last 50; linear LR
   cooldown on `schedule_steps=3375`; β2 thaw `0.90 → 0.80` after step 2500.

**Component ranking (leave-one-out at the 3195 screen, n=8).** Largest first; the top two dominate:

| Component removed | Δval | Verdict |
|---|---:|---|
| Tail-EMA (`noTailEMA`) | +0.00251 | keep — largest ([C02](../claims.md)) |
| Muon2F (`noMuon2f`) | +0.00229 | keep — 2nd ([C03](../claims.md)) |
| μ-schedule (`noMuSched`) | +0.00091 | keep |
| `mlp.proj` error feedback (`noErrorFeedback`) | +0.00076 | keep |
| AggMo3 (`noAggMo3`) | +0.00024 | keep |
| residual-decay / tail feedback / resRMSnorm | +0.00017 … +0.00011 | keep (small) |
| late-LR / β2-thaw / mom-refresh / res-pulse | +0.00002 … −0.00007 | net-removable ([C07](../claims.md)) |

Source: [../../evidence/data/v1_pruning_data.json](../../evidence/data/v1_pruning_data.json),
[../../evidence/figures/v1_pruning.md](../../evidence/figures/v1_pruning.md).

> **Reconciliation (L2).** The v1 *journal* trails off at a provisional `s3220` (and a rejected
> `s3170`); the **submitted bin is 3205**, from a later pruning-rerun captured in `record_configs/`.
> The lineage credited: Contra-Muon (PR #275), Polar Express NS, MuonEq; Codex additions: the
> v12iso role split, AggMo3 + 2-factor preconditioning, the `mlp.proj` error-feedback path, tail-EMA
> evaluation, and the late residual refresh/pulse/RMS schedule
> (`record_configs/20260515_codex_v1_v12iso_3205/README.md:66-71`).

---

## v2 — `legal_v12opt` (compliant rebuild) → bin 3037 (n=16)

Descends from the v12 optimizer stack but keeps the Track-3 architecture block **compliant** after
the legal rebuild ([C08](../claims.md)). The winning recipe layers (per
`record_configs/20260515_codex_v2_legal_3037/README.md:5-11`):

1. **Polar Express NS-5 + MuonEq** row-normalized update.
2. **Role-specific Muon LR multipliers**: q/k `0.61875`, v `0.625`, attn.proj `0.6375`,
   mlp.fc `1.0125`, mlp.proj `0.9875` of base LR `0.045` ([C04](../claims.md)).
3. **Role-specific weight decay** around `0.027..0.0315` instead of one body-wide value.
4. **Muon lookahead** from step 2450, interval 25, α 0.35, pull 0.15, with a 150-step smoothstep
   ramp.
5. **Embed init `×0.7`**, AdamW betas `(0.8, 0.95)`, `eta_min=0.02`, and the `0.85 → 0.95 → 0.85`
   Muon schedule.

**Component ranking (leave-one-out at 3037, n=8 unless noted).** Inherited levers dominate; the
v2-specific additions (role-LR/WD, lookahead) are real but smaller:

| Component removed | Δval | Verdict |
|---|---:|---|
| μ-schedule (`noMuSched`, n=3) | +0.00459 | keep — inherited, largest |
| cooldown-floor 1.0 (`cf1.0`, n=3) | +0.00388 | keep — inherited |
| MuonEq (`noMuonEq`) | +0.00353 | keep — inherited content ([C03](../claims.md)) |
| Role-LR (`noRoleLR`) | +0.00292 | keep — largest v2-specific ([C04](../claims.md)) |
| Lookahead (`noLookahead`) | +0.00117 | keep — v2-specific |
| Polar Express (`noPolarExpress`) | +0.00117 | keep |
| eta_min / embed-init | +0.00097 / +0.00092 | keep |
| Role-WD (`noRoleWD`) | +0.00041 | keep — small v2-specific |
| Contra-Muon (`noContraMuon`) | +0.00008 | near-zero |

Source: [../../evidence/data/v2_pruning_data.json](../../evidence/data/v2_pruning_data.json),
[../../evidence/figures/v2_pruning.md](../../evidence/figures/v2_pruning.md). This matches the
record's own summary that "Lookahead and role LR/WD are the main v2-specific additions; MuonEq and
the Muon schedule remain the largest inherited contributors"
(`record_configs/20260515_codex_v2_legal_3037/README.md:56`). The submitted variant filename is
`legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py`
(`v2/codex/scratchpad/THREAD.md:810`).

> The single-seed frontier reached **2962/2963** but those cohorts' means *miss* 3.28; the
> significance gate ([C06](../claims.md)) selected the fixed `ts3037` cohort as the earliest common
> passing checkpoint.

---

## v3 — `nosphere` (public-PR reproduction + W258 prune) → bin 2949 (n=16)

Starts from the public PR #291/#294 lineage and compresses it with the W258 leave-one-out prune,
keeping the fixed contract (per `record_configs/20260515_codex_v3_nosphere_2949/README.md:5-13`):

1. **PR #291 Contra → normal → Soft-Muon** schedule with `SOFT_MUON_CEIL=0.75`, Soft ramp ending at
   step 2905, q/k Contra residual scaled to `0.125`.
2. **PR #294-style radial control**: base outward scale `0.45`, tail guard active `2775..2895`, tail
   outward scale `0.38`, with post-update radius correction ([C09](../claims.md)) — **tail-only**,
   radial-from-step-zero was a kill.
3. **MLP+V SOAP** preconditioning (`SOAP_PARAM_MODE=mlp_plus_v`), V SOAP blend `0.95`, attention
   trust floor/cap, attention SOAP fade `2850..3020` ([C10](../claims.md)).
4. **LACV q/k floor relaxation** (`λ=0.060`, ramp `2550..2900`, fade `2949..3020`) and lookahead-CV
   gating on q/k/mlp.proj.
5. **CGI gain split** (`α=0.14`), depth-scaled `mlp.fc` init (`α=0.30`), zero-init proj weights,
   embed init `×0.7`, and PR #287 power-law cooldown constants with `train_steps=3020`,
   `schedule_steps=3025`.
6. **W258 pruning choice**: the sphere-lookahead pull is disabled (`SPHERE_LOOKAHEAD_PULL=0.0`),
   hence the submitted **`nosphere`** stack ([C11](../claims.md)).

**Component ranking (W258 leave-one-out at 2949, n=3 unless noted).** SOAP and radial dominate;
`nosphere` is itself a *removal* (the baseline of this table):

| Component removed | Δval | Verdict |
|---|---:|---|
| SOAP sidecar (`nosoap`) | +0.00528 | keep — largest ([C10](../claims.md)) |
| radial brake (`noradial`) | +0.00374 | keep — 2nd ([C09](../claims.md)) |
| V-SOAP (`novsoap`) | +0.00228 | keep |
| Soft-Muon (`nosoft`) | +0.00186 | keep |
| Contra (`nocontra`) | +0.00133 | keep |
| LACV (`nolacv`) | +0.00075 | keep |
| combined sphere removal (`nosphere-notangent`, n=12) | +0.00070 | **do not compose** ([C11](../claims.md)) |
| q/k Contra scale (`noqkcontrascale`) | +0.00047 | keep |
| tail radial (`notailradial`, n=8) | +0.00019 | keep (small) |
| LACV floor (`nolacvfloor`) | +0.00003 | keep (≈0) |

(The `nosphere` baseline itself is the submitted stack: removing the sphere-lookahead pull is the
chosen simplification, kept because it preserves the boundary while shrinking the stack.) Source:
[../../evidence/data/v3_pruning_data.json](../../evidence/data/v3_pruning_data.json),
[../../evidence/figures/v3_pruning.md](../../evidence/figures/v3_pruning.md).

> The runs continue to `train_steps=3020`; the submitted bin is the logged step-2949 checkpoint,
> "matching the same intermediate-checkpoint style as the existing PR #1 on this fork"
> (`record_configs/20260515_codex_v3_nosphere_2949/README.md:16`). The v3 stack is statistically
> viable to ~2940 at N=16. Lineage credited: PR #291 (Soft-Muon), PR #294 (radial), PR #278 (MLP
> SOAP extended to MLP+V), PR #287 (power-law cooldown); Codex additions: q/k Contra scaling, LACV
> q/k floor, lookahead-CV gating, W258 no-sphere pruning, and the 2949 checkpoint compression
> (`record_configs/20260515_codex_v3_nosphere_2949/README.md:67-73`).

---

## The lineage in one view

```
Muon baseline (3500)
  └─ v1: + schedule-horizon decoupling + NorMuon/Muon2F + AggMo3 + Adam-mini(opt1)
         + mlp.proj error-feedback + tail-EMA(β=0.99) + μ-schedule        → 3205
  └─ v2: (inherit cc v12 → QUARANTINE forward-path change → compliant rebuild)
         legal MuonEq + role-LR + role-WD + lookahead(2450) + embed×0.7    → 3037
  └─ v3: (reproduce public v48 = PR#294 + CGI + di-fc + AdamW b2=0.99)
         Soft-Muon(PR#291) + radial brake(PR#294, tail-only)
         + MLP+V SOAP sidecar(PR#278) + LACV q/k floor + PR#287 cooldown
         → W258 leave-one-out → drop sphere-lookahead pull = "nosphere"    → 2949
  (novelty: hard-isolated, no promotable submission — see ../novelty/novelty.md)
```
