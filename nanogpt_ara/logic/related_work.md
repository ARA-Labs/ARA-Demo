# Related Work — typed dependency graph

This experiment sits on a public optimizer lineage (modded-nanogpt speedrun PRs + a few papers) and
two cross-agent touchpoints. Edges are typed: **baseline** (what we must beat), **imports** (used
directly), **extends** (used and modified), **bounds** (defines the frontier we compress toward),
**refutes/quarantines** (recorded as invalid). The Codex agent's own contribution is the *composition,
compliant rebuild, compression, pruning, and statistical validation* — not the underlying mechanisms,
which are attributed below.

Attribution is faithful and point-in-time: the hard novelty wave was read-isolated from all of this
(it could not look at other worktrees), and the v2/v3 hand-offs were curated to Codex-internal
knowledge (the blocklisted frontier tables were withheld). See PAPER.md and README provenance.

---

## Baselines (what the bins are measured against)

### RW-Muon — Muon optimizer (Keller Jordan, modded-nanogpt)
- **Type:** baseline
- **Delta:** The standing SOTA at mission start — 3.28 val loss in **3500 steps** (lr=0.025, wd=0.0125),
  final val 3.27658. Every wave's bin is "below 3500." Muon's orthogonalized-momentum update is the
  optimizer family the whole experiment builds on.
- **Used by:** all waves; problem.md O1.

### RW-AdamW — AdamW baseline
- **Type:** baseline
- **Delta:** The weak baseline at **5625 steps**; bounds the bottom of the field. AdamW is also retained
  as the auxiliary "optimizer1" for non-matrix parameters in the stacks.

## Public modded-nanogpt PR frontier (external SOTA — reproduced, not invented)

These are public submissions on the KellerJordan/modded-nanogpt fork. v3's strategy was to reproduce
them faithfully under the architecture guard and then compress. The submitted v3 script's own header
credits them.

### RW-PR291 — Contra → Soft-Muon schedule (@nilin, PR #291)
- **Type:** imports / extends
- **Delta:** Public bin ≈3030 (N=30, margin +0.00540). Contributes the Contra-Muon-early →
  normal-Muon-mid → Soft-Muon-late schedule, with the Gram-Frobenius/Schatten-4 input-norm estimate and
  Soft-Muon basis stacking (p=0.1, ending at 80% blend). **Kept** in the v3 stack (audited faithful).
- **Used by:** C07, C08; E14.

### RW-PR294 — Outward-radial dampening + radius correction (@nilin, PR #294)
- **Type:** imports / extends
- **Delta:** Public bin ≈2990 (N=11, margin +0.00442). Scales the radial (outward) update component down
  and applies a post-step weight-radius correction; its power-law cooldown is back-loaded (so early
  kills are invalid). The faithful **v48** parent the whole 2949 line is built on. **Kept** (the
  second-most load-bearing v3 component; see C08).
- **Used by:** C07, C08; E14, E15.

### RW-PR278 — MLP SOAP preconditioning (@samacqua, PR #278)
- **Type:** extends
- **Delta:** SOAP preconditioning machinery; v3 **extends** the SOAP set to MLP + attention value (V)
  matrices (`mlp_plus_v`). The **single most load-bearing** v3 component (nosoap is the worst ablation).
- **Used by:** C08; E14, E16.

### RW-PR287 — Power-law LR cooldown / PowerCool (@yash-oai, PR #287)
- **Type:** imports
- **Delta:** `min(flat_lr, c·(t_end − step)^1.2)` cooldown constants; the back-loaded schedule that makes
  early-curve loss a non-kill-signal and underpins the compression strategy.
- **Used by:** C07; E14, E15.

### RW-PR274 — Skylight / NorMuon-lite (@kumarkrishna, PR #274)
- **Type:** imports
- **Delta:** NorMuon-lite row/column variance normalization, u/w floor postprocessing, lr≈0.0375 Muon
  setup — incorporated into the v3 parent (credited in the submitted script header).

### RW-PR275 — Contra-Muon (@nilin, PR #275)
- **Type:** imports
- **Delta:** Introduces the Contra-Muon update term; the lineage cited for the v1 and v2 optimizer
  families and the v3 q/k Contra residual.

### RW-PR290 — KL-SOAP-H (@nilin, PR #290) — tested, not adopted whole
- **Type:** bounds / refuted-as-replacement
- **Delta:** Public bin ≈3125; a full-Muon-replacement preconditioner. Repeatedly failed as a drop-in
  on this backbone (zero-init projection froze; full replacement did not cross). Only its usable deltas
  (SOAP first-step warmup/skip, nonzero hidden-proj init) were borrowed. Recorded as a dead end.

### RW-PR288 — Muown (@nilin, PR #288) — tested, rejected
- **Type:** refuted-on-backbone
- **Delta:** Public bin ≈3075; direction/gain weight-norm decomposition (NS on direction, Adam on gain).
  A hard negative as a graft on the v37/v48 backbone (gain graft exploded). Not used.

## Papers (external method lineage)

### RW-PolarExpress — Polar Express (arXiv:2505.16932)
- **Type:** imports
- **Delta:** Non-uniform Newton-Schulz (NS-5) projection lineage; the NS-5 used in the v1 and v2 stacks.

### RW-MuonEq — MuonEq (arXiv:2603.28254)
- **Type:** imports
- **Delta:** Row/column-normalized Muon update lineage; the MuonEq row-normalized update in v1/v2.
  In v2 pruning, `noMuonEq` is one of the largest degraders.

### RW-Optimizers2509 — "the optimizers paper" (arXiv:2509.02046)
- **Type:** bounds / motivation
- **Delta:** Establishes that most claimed-SOTA optimizers are confounded by undertuned baselines and
  that AdamW LR at this scale wants ~4–8e-3, not the canonical 3e-4. Motivates the head-to-head
  framing and the aggressive HP sweeping doctrine. Cited in AGENTS.md.

## Cross-agent touchpoints (faithfully attributed, never claimed as Codex's own)

### RW-CCv12 — the cc/Claude-agent "v12" stack
- **Type:** extends → **quarantined** (non-compliant)
- **Delta:** The only known 3025-step parent at v2's start; adopted as the v2 backbone, then found to
  carry an illegal `RMSNorm.forward` / q-k-norm forward-path precision change. Every v12-derived result
  was **quarantined**; the submittable v2 frontier (3037) was rebuilt byte-identical-compliant. The
  cross-agent reference comes from Codex's own journals, not from a pre-loaded answer. → C05.

### RW-Opusv15 — the opus-agent v15 stack
- **Type:** baseline (cross-agent)
- **Delta:** At v3's start, the opus best was bin=3035 (v15 = v14 + AdamW b2=0.99, N=8 margin +0.00418);
  one of the two bars v3 was pushing below. Referenced as a point-in-time bar, not reused as a result.
