# Config: C03 — the cc-v12 step-count anchor (ts2999).  *** NON-COMPLIANT / QUARANTINED ***
#
# >>> THIS RECIPE IS NOT SUBMITTABLE FOR THIS TRACK. <<<
# Its base (the inherited cc / Claude-Code "v12" parent) VIOLATES the no-forward/no-norm hard rule
# (logic/claims.md C05): its RMSNorm.forward is `(norm(x.float()) * self.gains).type_as(x)` via a
# module-level `norm()` helper, and attention q/k normalization routes through that helper —
# a forward-path PRECISION change (it can alter bf16 behavior), INVALID even though math-close.
# The USER confirmed this first-person; the agent QUARANTINED every v12-derived `v2cx` result
# (C03's entire evidence basis). This config is materialized ONLY because C03 is a `supported`
# claim that names a Proof: run pointer (pointer-resolution rule) — it records WHAT RAN on the
# non-compliant base, NOT a submittable/valid recipe. For the SUBMITTABLE, gate-passing v2 frontier
# see src/configs/legal_v12opt_ts3037_v2.py (C04).
#
# Grounding: transcribed (the as-committed launched variant the C03 ts2999 proof runs index)
#   v2/codex/scratchpad/variants/v12_ts2999.py
#     - the VIOLATING forward path: `def norm(x)` line 61-62; RMSNorm.forward
#       `(norm(x.float())*self.gains).type_as(x)` line 70; q/k `norm(q),norm(k)` line 112
#     - train_steps = 2999 : line 310
#
# Crystallized by: logic/claims.md C03 (status: supported — EXISTENCE + 2-seed reproducibility of a
#   sub-3000 crossing on the cc-v12 parent via step-count tuning; depends on nothing; CONTRADICTION
#   flagged vs C04/C05 at trace N79, status flip deferred). Wave v2. Source node N68.
# Evidence: evidence/results/c03_ccv12_stepcount_frontier.md.
#
# DIVERGENCE / SCOPE annotations (driver/materialize.md):
#   * train_steps=2999 is the AS-COMMITTED script literal and C03's anchor (the 2-seed-reproduced
#     stop: r4 final 3.27985, r7 final 3.27996, both crossing @2999). It is an as-committed INPUT,
#     NOT a noise-floor-validated bin: every run this line is stat_verify=False and WALLS at the stop
#     (final ~3.2799, ~1-2e-4 below 3.28, inside the ~0.001 noise floor). C03 is scoped to EXISTENCE +
#     2-seed reproducibility ONLY — it does NOT assert a gate-cleared sub-3000 result (no statistical
#     pass, no pruning round this turn). The lower single-seed SCRATCH hits (step 2992-2998) are NOT
#     pinned — C03 explicitly excludes them.
#   * SUPERSEDED for the compliant benchmark by C04 (ts3037): when this recipe's *optimizer/init* is
#     rebuilt on a byte-identical-Architecture base AND made to clear the cohort gate, the sub-3000
#     crossings VANISH into the noise floor (C05/N78: "the invalid forward-path change materially
#     helped the sub-3000 behavior"). So the sub-3000 number here is forward-path-assisted, not a
#     compliant achievement.
#   * body lr=0.045 / train_steps=2999 are the v12 script literals (same backbone family as C04).

# ---- Schedule / stop -----------------------------------------------------------------------------
train_steps   = 2999   # C03 anchor (2-seed-reproduced crossing). AS-COMMITTED INPUT, not a validated bin. [literal]
cooldown_frac = 0.7    # decoupled-WSD cooldown fraction (the operative lever — pure run-control). [literal]
# The WORKING LEVER for C03 is the literal `train_steps` itself: the explicit schedule-denominator
# transfer (holding _SCHEDULE_STEPS=3012 under an earlier stop) was 0/8 NEGATIVE (trace N70) — plain
# step-count tuning crosses where the denominator trick does not.

# ---- Backbone (INHERITED cc-v12 optimizer/init) --------------------------------------------------
# NOTE: the optimizer/init geometry is the cc-v12 backbone; C03 added NO new optimizer/init lever
# (the cheap orthogonal levers PMI/SVC/QKP/AdaGrad-Muon and Mousse-Lite/QKT/pow1.5+attn0.5 ALL
# closed negative or at parity — trace N63/N69; the margin is run-control, not a new mechanism).
# The discovered-recipe content of C03 is therefore the STEP COUNT, not an optimizer module — so no
# new src/execution core module is materialized for C03 (the cc-v12 forward path is a FORBIDDEN
# architecture change, NOT an optimizer contribution, and is quarantined; capturing it as a "recipe"
# would mis-state it). The optimizer backbone lineage is the v1 NorMuon/Muon family
# (src/execution/*), re-parameterized; the only C03-specific tunable is train_steps above.
opt2_base_lr  = 0.045   # v12 backbone Muon base LR. [literal]

# ---- COMPLIANCE STATUS (the load-bearing field) --------------------------------------------------
submittable          = False   # C05: non-byte-identical forward path -> INVALID for this track.
quarantined          = True    # all v12-derived v2cx results quarantined (trace N76).
forward_path_baseline = False  # RMSNorm.forward / q-k norm DIVERGE from baseline F.rms_norm (C05).
superseded_by        = "C04 (legal_v12opt_ts3037_v2.py) — the compliant, gate-passing frontier."
