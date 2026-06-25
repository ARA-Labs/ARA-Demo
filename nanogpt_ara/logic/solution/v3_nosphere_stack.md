# v3 — the nosphere stack (submitted bin 2949)

The v3 wave pivoted from local mechanism search (Aurora / KL-Shampoo) to **faithfully reproducing
the public modded-nanogpt PR frontier, then compressing and pruning it** (C06). Concrete artifact:
[`src/execution/v3_nosphere_ts3020.py`](../../src/execution/v3_nosphere_ts3020.py) (transcribed
verbatim). Evidence: `evidence/tables/v3_seed_table.md`, `evidence/figures/v3_loss_curves.md`,
`evidence/figures/v3_pruning.md`.

## Strategy

1. **Aurora / KL-Shampoo branch** reached bin ~3027 (clean passes) but repeatedly centered near
   3.280 at 2999; superseded by the stronger public Soft/radial parent.
2. **Public-frontier pivot.** Reproduce the proven PR #294/v48 parent faithfully *under the codex
   byte-identity guard*, then compress its schedule below 2950 rather than inventing new mechanisms.
   A v41/PR294 early-kill mistake (killing on a slow 1250 trajectory) was corrected after the user
   flagged it — the PR #287 power-law cooldown is back-loaded, so early-trajectory kills are invalid.
3. **Compress** the v48 power-law schedule + Soft-Muon ramp earlier (`compress30`/`compress45`)
   toward 2949; first strong sub-2950 single seeds appeared here.
4. **Leave-one-out prune** (the W258 sweep) the assembled stack.

## The stack (W258 nosphere)

Reproduced public mechanisms:
- **Contra → normal → Soft-Muon** (PR #291): `SOFT_MUON_CEIL=0.75`, Soft ramp end 2905, q/k Contra
  residual scaled to 0.125 (codex addition). LOO `nosoft` +0.00186, `nocontra` +0.00133,
  `noqkcontrascale` +0.00047 — all kept.
- **Outward-radial dampening** (PR #294): base outward scale 0.45, tail guard 2775..2895, tail
  outward 0.38, post-step radius correction. **Load-bearing** (LOO `noradial` +0.00374; removal
  destroys tail catch-up).
- **MLP+V SOAP** (PR #278/#290 machinery): `SOAP_PARAM_MODE=mlp_plus_v`, V SOAP blend 0.95, attn
  SOAP fade 2850..3020. **The single most load-bearing component** (LOO `nosoap` +0.00528;
  `novsoap` +0.00228 — removing SOAP "breaks the whole tail").
- **Power-law cooldown** (PR #287): `train_steps=3020`, `schedule_steps=3025`.
- **CGI gain split** (alpha 0.14), depth-scaled `mlp.fc` init (alpha 0.30), zero-init proj, embed
  init ×0.7 (init block, ported from opus v48/v15).

Codex-specific additions:
- **LACV q/k floor relaxation** (`LACV_FLOOR_LAMBDA=0.060`, ramp 2550..2900, fade 2949..3020) and
  **lookahead-CV gating** on q/k/mlp.proj. LOO `nolacv` +0.00075, `nolacvfloor` +0.00003 — kept (the
  floor is small but positive).
- **The W258 pruning decision: disable the sphere-lookahead pull** (`SPHERE_LOOKAHEAD_PULL=0.0`).
  This is the one mechanism that both simplified the stack and held the boundary — hence the
  submitted **"nosphere"** stack. The tangent-sphere radial term is **kept**, because removing both
  (`nosphere-notangent`, +0.00070) does not compose (C06).

## How the bin was reached

The nosphere baseline holds the 2940 line at n=16 (score +0.004608 at step 2940; +0.006332 at step
2949). The submitted bin is **2949** (n=16, mean 3.27886, score 0.004555; C08), with the runs
continuing to `train_steps=3020` and the submitted bin being the logged step-2949 checkpoint
(matching the intermediate-checkpoint style of the public fork). Statistically viable to ~2940.

## Attribution

Public PRs (#275/#278/#287/#290/#291/#294) and cross-agent opus v15/v48 supplied the reproduced
mechanisms; **Codex's own contributions** are the q/k Contra scaling 0.125, the LACV q/k floor and
lookahead-CV gating, the W258 leave-one-out + nosphere prune, the tail-radial guard, and the 2949
checkpoint compression. KL-SOAP-H (PR #290 full replacement) and Muown (PR #288) were tried as
parents and hard-killed (RW09, RW10).
