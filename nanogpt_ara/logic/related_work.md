# Related Work

Typed dependency graph of the external methods this trajectory built on, screened, or rejected.
Relation types: **baseline** (the bar to beat), **imports** (used essentially as-is), **extends**
(built on and modified), **bounds** (constrains / tested-and-found-limited), **refutes**
(contradicted here). PR numbers and arXiv links are grounded in the submitted record credits,
which the compiler opened firsthand; in-journal mentions are grounded in the wave THREADs.

> **Cross-agent attribution.** Two dependencies are *other-agent* outputs, recorded attributed and
> never as Codex's own result: the **cc v12** parent (from the Claude/Opus agent) and the **v48**
> public-frontier parent (an Opus thread). See `README.md:57-82` and [C08](claims.md).

---

## RW01 — Muon (modded-nanogpt baseline) — **baseline**

The matrix optimizer whose 3500-step result is the bar for every wave: momentum orthogonalized by
Newton–Schulz before application, lr=0.025, wd=0.0125. The whole experiment is defined relative to
it (`v1/codex/goal.md:6-7`, `v1/codex/AGENTS.md:5-6`). AdamW (5625 steps) is the secondary
baseline.

## RW02 — Contra-Muon / @nilin PR #275 — **extends**

The Contra-Muon lineage for the Muon optimizer family; the `_CONTRA_MUON` shaping term carried
through v1/v2 (lowered to 0.225 in v2) and the q/k Contra residual in v3.
**Delta here:** v2 tunes the Contra constant as a scalar lever; v3 reduces the q/k Contra residual
scale (0.125 / 0.0625).
**Source:** `record_configs/20260515_codex_v1_v12iso_3205/README.md:68` «[@nilin PR #275 / Contra-Muon](https://github.com/KellerJordan/modded-nanogpt/pull/275): Contra-Muon lineage for the optimizer family».

## RW03 — Polar Express (arXiv:2505.16932) — **imports**

Non-uniform / NS-5 Newton–Schulz projection used in the v1 and v2 stacks.
**Delta here:** used as the projection backbone under the role/precondition changes; in the v2
pruning table `noPolarExpress` costs `+0.00117`.
**Source:** `record_configs/20260515_codex_v2_legal_3037/README.md:69` «[Polar Express](https://arxiv.org/abs/2505.16932) NS-5 and [MuonEq](https://arxiv.org/abs/2603.28254) row-normalized Muon update».

## RW04 — MuonEq (arXiv:2603.28254, per record credits) — **extends**

The row/column-normalized Muon update; the compliant v2 stack's largest inherited *content*
contributor (`noMuonEq` `+0.00353`). The v1 analogue is the in-house "Muon2F" factorized
preconditioning. The subject of [C03](claims.md).
**Delta here:** combined with role-specific LR/WD and factorized two-factor preconditioning.
**Note:** the arXiv id `2603.28254` is transcribed exactly as it appears in the record credits; it
is an unusual identifier (cited per `record_configs`), flagged for the reader rather than
silently corrected.
**Source:** `record_configs/20260515_codex_v2_legal_3037/README.md:69` (same line as RW03).

## RW05 — @nilin PR #291 / Contra → Soft-Muon — **extends**

The Soft-Muon schedule (Contra → normal → Soft) plus Gram-Frobenius/Schatten-4 input norming and
p=0.1 basis stacking; reproduced and load-bearing in v3 (`nosoft` `+0.00186`).
**Delta here:** Codex applies the Frobenius/Schatten-4 switch across hard-polar, Contra, Soft, and
all norm restorations, tunes `SOFT_MUON_CEIL=0.75` and ramp end 2905, and scales the q/k Contra
residual to 0.125.
**Source:** `record_configs/20260515_codex_v3_nosphere_2949/README.md:69` «[@nilin PR #291 / Contra-Muon -> Soft-Muon](https://github.com/KellerJordan/modded-nanogpt/pull/291): Soft-Muon schedule and Gram-Frobenius/Schatten-4 input norm lineage».

## RW06 — @nilin PR #294 / radial brake — **extends**

Outward-radial dampening applied after update formation, then post-step radius correction; the v3
stack's second-largest contributor (`noradial` `+0.00374`). The subject of [C09](claims.md).
**Delta here:** Codex makes the brake **tail-activated** (guard window 2775..2895, tail outward
scale 0.38, base 0.45) with a WD-aware radius target — radial-from-step-zero was a kill.
**Source:** `record_configs/20260515_codex_v3_nosphere_2949/README.md:70` «[@nilin PR #294 / radial brake](https://github.com/KellerJordan/modded-nanogpt/pull/294): outward radial dampening and post-step radius correction».

## RW07 — @samacqua PR #278 / MLP SOAP — **extends**

SOAP preconditioning machinery, extended in v3 to **MLP+V** as a warm-started, step-0-skipped
sidecar; the v3 stack's largest contributor (`nosoap` `+0.00528`). The subject of [C10](claims.md).
**Delta here:** the warm-start SOAP-skip sidecar (`SOAP_PARAM_MODE=mlp_plus_v`, V SOAP blend 0.95),
which avoids the zero-init projection freeze that killed full KL-SOAP-H.
**Source:** `record_configs/20260515_codex_v3_nosphere_2949/README.md:71` «[@samacqua PR #278 / MLP SOAP](https://github.com/KellerJordan/modded-nanogpt/pull/278): SOAP machinery extended here to MLP+V».

## RW08 — @yash-oai PR #287 / power-law LR schedule — **imports**

The power-law cooldown constants used as the v3 schedule backbone (`train_steps=3020`,
`schedule_steps=3025`). Its back-loaded cooldown is *why* hard schedule truncation fails and only
phase-shifting works (see [C09](claims.md), E10).
**Source:** `record_configs/20260515_codex_v3_nosphere_2949/README.md:72` «[@yash-oai PR #287 / power-law LR schedule](https://github.com/KellerJordan/modded-nanogpt/pull/287): power-law cooldown constants».

## RW09 — PR #290 (KL-SOAP-H) — **bounds / refutes (here)**

A full KL-SOAP-H recipe Codex tried to port in v3; **not portable** as wired (zero-init projection
freeze), salvaged only as the warm-start SOAP-skip sidecar (RW07). Bounds the applicability of full
SOAP on this zero-init backbone.
**Source:** `v3/codex/scratchpad/THREAD.md:424` «PR #290's full KL-SOAP-H recipe is not portable as currently wired into this stack».

## RW10 — PR #288 (Muown) — **bounds / refutes (here)**

Muown-style post-step norm growth; **incompatible** with the v3 backbone as grafted and demoted.
**Source:** `v3/codex/scratchpad/THREAD.md:439` «Muown-style post-step norm growth is incompatible with this v37 backbone as grafted».

## RW11 — cc v12 (other-agent parent) — **extends → quarantined**

The 3025-step v12 parent inherited from the Claude/cc agent, used as the initial v2 backbone, then
**quarantined** when its `RMSNorm.forward` / q-k-norm forward-path change was flagged non-compliant
([C08](claims.md)). Recorded attributed; the submittable v2 frontier is the compliant rebuild, not
this parent.
**Source:** `v2/codex/scratchpad/THREAD.md:6` «use cc v12 as the experimental backbone … v12 is the only known 3025-step parent»; quarantine at `THREAD.md:128`.

## RW12 — v48 (other-agent public-frontier parent) — **imports**

An Opus thread's public-frontier parent (PR #294 verbatim + CGI Rademacher gain split + di-fc init
+ AdamW b2=0.99, bin 2980), reproduced as the v3 starting point. Recorded attributed.
**Source:** `v3/codex/scratchpad/THREAD.md:552` «v48 = PR #294 verbatim + CGI Rademacher + di-fc init + AdamW b2=0.99 reaches bin=2980 N=15 +0.00418».

## RW13 — Screened-and-mostly-rejected optimizer literature — **bounds**

Across the waves the agent screened and (mostly) ruled out a large body of optimizers as clean
negatives on this exact setup, including: MARS-M (arXiv:2510.21800), Adam-mini (kept on the AdamW
side in v1, near-parity on the v2 backbone), SOAP/Shampoo (full), APOLLO, Lookahead-NorMuon,
Sophia-F, CAME, NovoGrad, SM3, LAMB, MADGRAD, QHAdam, RAdamW, AdaBelief, ADOPT, LaProp, Lion,
Scion, MVR, DION, OLion, schedule-free NorMuon, and the novelty wave's blockers (Muon²/Muon²-F,
OrthoGrad/Mano, Gradient Centralization, GaLore/Dion, Fixup/DeepNet, Stiefel/Cayley transport,
error-feedback SGD, PCGrad/gradient-surgery). These constitute the "clean negative result" output
the goal explicitly values (`v1/codex/goal.md:52-53`).
**Source:** v1 picklist graveyard `v1/codex/plan.md:35-71`; novelty blockers
`novelty/codex/scratchpad/THREAD.md:326-2027`.
