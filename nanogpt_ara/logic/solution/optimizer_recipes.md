# Optimizer recipes — the four wave stacks (mechanism level)

The concrete submitted scripts are pointers in [../../src/artifacts.md](../../src/artifacts.md) (they
persist in the run store; not copied here per the "no re-encoded prose" rule). This file describes each
submitted stack at the mechanism level and how it was built. Per-component contributions are in
[../../evidence/](../../evidence/) (the pruning tables/figures). Exact recipe constants are quoted from
the record-config READMEs.

---

## v1 — "v12iso / MuSched", submitted bin **3205** (n=16)

The validated composition of the v1 screen. [src: `record_configs/20260515_codex_v1_v12iso_3205/README.md:5-11`]

1. **NorMuon** with Polar-Express NS projection and row/column preconditioning on hidden matrices.
2. **Split hidden optimizers:** non-`mlp.proj` matrices use **AggMo3 + 2-factor preconditioning**;
   `mlp.proj` uses **error-feedback residuals**.
3. **Tail mechanics on `mlp.proj`:** feedback ramp `0.04 → 0.04804`, residual decay ramp `0.05 → 0.022`,
   a momentum refresh at step 3125, and residual pulse / RMS normalization at step 3125.
4. **Tail-EMA evaluation** from step 2000 (β=0.99). *(Largest pruning contributor — C02.)*
5. **Muon μ schedule** `0.85 → 0.95` over 300 steps and `0.95 → 0.85` over the last 50; linear LR
   cooldown on `schedule_steps=3375`; beta2 thaw `0.90 → 0.80` after step 2500.

**How it was built:** a conservative screen (E02) found NorMuon (β=0.90, lr=0.030) as the corridor and
factorized hidden preconditioning (Muon2F, hidden-only — C03) and Adam-mini as the live optimizer
signals; tail-EMA evaluation (E04) was the strongest endpoint lever; the transplanted **mu-schedule**
worked *isolated* where the full v12 package washed out (E05). The horizon≠stop lever (C01) carried
every promoted recipe. The statistical pass rejected the lower `s3170` crossing and submitted 3205 (E07).

**Pruning ranking (drop-order, least→most load-bearing):** noResPulse, noMomRefresh, noBeta2Thaw,
noLateLR, noResRMSNorm, noTailFeedback, noTailRD, noAggMo3, noErrorFeedback, noMuSched, **noMuon2f**,
**noTailEMA**. The last two are the load-bearing pair.

---

## novelty — hard-isolated, novelty-constrained: **negative result** (no submission)

No promotable stack. The wave derived and ran dozens of not-on-arXiv pre-polar Muon / init mechanisms
(see [novelty_derivation.md](novelty_derivation.md)); the best reproduced only a sub-noise-floor 25-step
crossing, genuine crossings failed seed reproduction, and the reachable mechanism class collapsed into
algebraic no-ops (C10). Recorded as an isolated `NV##` trace subtree and a documented negative — a clean
negative on one's own derivations is a real contribution under the mission's own framing.

---

## v2 — "legal" frontier, submitted bin **3037** (n=16)

Descends from the v12 optimizer stack but **byte-identical-compliant** after the legal rebuild (C05).
[src: `record_configs/20260515_codex_v2_legal_3037/README.md:5-11`]

1. **Polar Express NS-5 + MuonEq** row-normalized update.
2. **Role-specific Muon LR multipliers** (of base LR 0.045): q/k `0.61875`, v `0.625`, attn.proj
   `0.6375`, mlp.fc `1.0125`, mlp.proj `0.9875`. *(Large pruning contributor — C04.)*
3. **Role-specific weight decay** ≈ `0.027..0.0315` instead of one body-wide value.
4. **Muon lookahead** from step 2450, interval 25, α=0.35, pull 0.15, with a 150-step smoothstep ramp.
5. **Embed init ×0.7**, AdamW betas `(0.8, 0.95)`, `eta_min=0.02`, and the `0.85 → 0.95 → 0.85` Muon
   schedule.

**How it was built:** after the v12 quarantine (E09), two orthogonal legal levers (Contra-Muon 0.225,
attention Muon LR 0.625) were combined, then role-WD, role-LR2, and lookahead descended the crossing
step to a single-seed ~2962 (E10). The significance cohort (E11) failed every low-step family and passed
only the +75-step cohort → bin 3037. The single-seed 2962/2963 crossing is recorded as journey, not a
record.

**Pruning ranking (least→most load-bearing):** noContraMuon, noRoleWD, noEmbedInit, noEtaMin,
noPolarExpress, noLookahead, **noRoleLR**, **noMuonEq**, **cf1.0** (cooldown floor), **noMuSched**. The
mu-schedule, cooldown floor, and MuonEq are the largest; role-LR is the key v2-specific addition.

---

## v3 — "nosphere", submitted bin **2949** (n=16; statistically viable to ~2940 at N=16)

Starts from the public PR #291/#294 lineage and compresses it with W258 pruning; keeps the fixed
architecture/data/batch contract. [src: `record_configs/20260515_codex_v3_nosphere_2949/README.md:5-13`]

1. **PR #291** Contra → normal → Soft-Muon schedule with `SOFT_MUON_CEIL=0.75`, Soft ramp ending at
   step 2905, q/k Contra residual scaled to `0.125`.
2. **PR #294** radial control: base outward scale `0.45`, tail guard active `2775..2895`, tail outward
   scale `0.38`, with post-update radius correction. *(Second-most load-bearing — C08.)*
3. **MLP+V SOAP** (`SOAP_PARAM_MODE=mlp_plus_v`), V SOAP blend `0.95`, attention trust floor/cap, SOAP
   fade `2850..3020`. *(Most load-bearing component — C08.)*
4. **LACV** q/k floor relaxation (λ=0.060, ramp `2550..2900`, fade `2949..3020`) and lookahead-CV gating
   on q/k/mlp.proj.
5. **CGI gain split** (α=0.14), depth-scaled `mlp.fc` init (α=0.30), zero-init proj weights, embed init
   ×0.7, and PR #287 power-law cooldown constants with `train_steps=3020`, `schedule_steps=3025`.
6. **W258 pruning choice:** the sphere-lookahead pull is disabled (`SPHERE_LOOKAHEAD_PULL=0.0`) — hence
   "nosphere". *(C09.)*

**How it was built:** the local Aurora sub-line recentered near 3.280 at 2999 (E13); the user
hand-off of the public frontier triggered the pivot to faithful PR #294/#291 reproduction (E14);
compression by shifting phase endpoints (not truncating the horizon) plus LACV variance control reached
the 2940-viable Worker70→W211→W258 parents (E15); the W258 leave-one-out (E16) found the sphere-lookahead
pull redundant (nosphere) while showing the two sphere terms don't compose → submitted bin 2949.

**Pruning ranking (least→most load-bearing):** nolacvfloor, notailradial, noqkcontrascale,
nosphere-notangent, nolacv, nocontra, nosoft, novsoap, **noradial**, **nosoap**. SOAP and radial
dampening are load-bearing; the sphere-lookahead pull is the one redundant term.

> Note on the submitted-run example: one nosphere reproduction run (`10389-…-nosphere-r3`) trains to
> `train_steps=3020`, crosses 3.28 at step **2940** on that seed, and ends at final val **3.27689**
> (569.166 s, 188.47 ms/step, Slurm 17851). The **submitted bin 2949** is the N=16 cohort checkpoint,
> distinct from any single seed's crossing. [src: nosphere run `metadata.json` / `train.log`]
