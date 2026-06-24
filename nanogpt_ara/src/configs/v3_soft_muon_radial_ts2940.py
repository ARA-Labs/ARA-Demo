# Config: C08 — public Soft-Muon (PR #291) + outward-radial-tail (PR #294) + SOAP, rebuilt
# architecture-COMPLIANT on the codex v37 checkout. The FIRST compliant result below the ~2990
# public PR #294 floor: a STATISTICALLY-VERIFIED step_to_3.28 = 2940. Recipe slug (Worker70):
# v3u2900_worker70_tailradgate_early2775_lowratio_vfade2850_rad045_warmsoapskip_s3035_soft2925_ts3020;
# the leave-one-out canonical simplified stack is `nosphere` (sphere-lookahead pull removed).
#
# Grounding: transcribed (the AS-COMMITTED launched variants the C08 cohorts index)
#   v3/codex/scratchpad/variants/v3u2900_worker70_tailradgate_early2775_lowratio_vfade2850_rad045_warmsoapskip_s3035_soft2925_ts3020.py
#   v3/codex/scratchpad/variants/v3prune_w258loo_nosphere.py   (the N=16 pruned canonical stack)
#   (Soft-Muon + radial-tail mechanisms in src/execution/soft_muon_outward_radial.py; public parents
#    KellerJordan modded-nanogpt PR #291 (Soft-Muon/Contra) + PR #294 (outward-radial), N89.)
#
# Crystallized by: logic/claims.md C08 (status: supported, depends on C05). Wave v3.
# Evidence: evidence/results/c08_soft_muon_radial_statpass.md (the N90 cohorts + N90 leave-one-out:
#   Worker70 n=10 step-2940 mean 3.278606, +0.004408; W251/W258 tangent-sphere n=9 +0.004300;
#   PRUNED `nosphere` n=16 mean 3.278848, +0.004608). Concepts: logic/concepts.md "Soft-Muon (PR
#   #291)" + "outward-radial update dampening (PR #294)".
# Compliance premise: C05 — byte-identical-Architecture v37 checkout, enforced by launch_variant_gate.sh.
# SUBMITTABLE. User-directed pivot to the public frontier (N89).
#
# DIVERGENCE / SCOPE annotations (driver/materialize.md):
#   * train_steps=2940 is the n=10/n=9/n=16-VERIFIED step_to_3.28 frontier (the FIRST below the
#     ~2990 public floor). The script schedule literals are `ts3020` (the run's train_steps stop) with
#     `_OPT_SCHEDULE_STEPS`=3035 ("s3035") and the soft-ceiling/V-fade tail gated by step — these are
#     as-committed schedule INPUTS; the ACHIEVED/VALIDATED bin (step_to_3.28) the cohort gate certifies
#     is 2940 (the step the crossing is gate-verified at). They are annotated separately below so the
#     schedule literal is never mistaken for the validated bin.
#   * A config pinning sub-2940 as an ACHIEVED bin would be FALSE: step-2925 is NOT viable (W258 n=9
#     mean 3.279373, +0.001880); the entire sub-2900 worker-cascade is single-seed scratch (window
#     best 2875 `worker206`, every cohort reverts at N>=8 — N91). So this file pins 2940 and annotates
#     2925/sub-2900 as gate-FAILing noise.
#   * Mission target (under 2900) NOT met — the verified frontier is step-2940 (trace N16/N89).
#   * The radial-AS-TAIL distinction is load-bearing: radial-from-step-zero and base-Soft-only were
#     KILLED as too-slow/insufficient-tail-slope ablations (N90).

# ---- public parents (rebuilt compliant on the v37 checkout) --------------------------------------
public_parent_softmuon = "KellerJordan/modded-nanogpt PR #291 (Soft-Muon / Contra, Gram-Frobenius/Schatten-4, p=0.1 basis)"
public_parent_radial   = "KellerJordan/modded-nanogpt PR #294 (outward-radial update dampening, ~2990 floor)"
compliant_checkout     = "codex v37"   # byte-identical-Architecture rebuild under the C05 gate. [literal]

# ---- Schedule / stop -----------------------------------------------------------------------------
verified_step_to_3p28  = 2940   # the GATE-VERIFIED achieved bin (n=10/n=9/n=16). [validated frontier]
train_steps            = 3020   # as-committed run stop ("ts3020"). [literal — schedule INPUT, not the bin]
opt_schedule_steps     = 3035   # `_OPT_SCHEDULE_STEPS` ("s3035"). [literal]

# ---- the NEW C08 mechanism (1): Soft-Muon norming (PR #291) — LOAD-BEARING -----------------------
# Core: src/execution/soft_muon_outward_radial.soft_muon_norm.
soft_muon_enabled = True
soft_muon_p       = 0.1     # Schatten-4 / p=0.1 basis stacking. [literal]
soft_muon_ceil    = 0.075   # Soft-Muon ceiling ("softceil075"). [literal]
soft_muon_target  = 2925    # the soft-ceiling target step ("soft2925"). [literal]
# leave-one-out: nosoft demotes 2940-mean to 3.280623 (LOAD-BEARING).

# ---- the NEW C08 mechanism (2): outward-radial TAIL correction (PR #294) — LOAD-BEARING ----------
# Core: src/execution/soft_muon_outward_radial.outward_radial_tail_correction.
radial_enabled      = True
radial_strength     = 0.045   # "rad045". [literal]
radial_tail_start   = 2775    # tail-radial-gate opens ("tailradgate-early2775"); NOT from step 0. [literal]
radial_lowratio     = True    # "lowratio" gate variant. [literal]
# leave-one-out: noradial demotes 2940-mean to 3.282580 (the LARGEST demotion — most load-bearing).

# ---- the other LOAD-BEARING recipe levers (per the N90 leave-one-out) ----------------------------
# These are public-PR / sidecar components (pinned as recipe levers; not re-encoded as core modules).
soap_enabled        = True   # SOAP sidecar; "warmsoapskip"/"soapuw". leave-one-out nosoap -> 3.284390 (load-bearing). [literal]
vsoap_enabled       = True   # V-SOAP; novsoap -> 3.281063 (load-bearing). [literal]
vfade_start         = 2850   # value-fade ("vfade2850"). [literal]
lookahead_cv_enabled = True  # lookahead control-variate (LACV); nolacv -> 3.279513 (load-bearing). [literal]
qk_contra_scale     = 0.125  # reduced q/k Contra scaling ("qkcontra0125"); noqkcontrascale -> 3.279250 (load-bearing). [literal]
qk_lacv_floor       = 0.060  # q/k LACV-conditioned floor ("cvfloor060"); nolacvfloor -> 3.278793 (load-bearing). [literal]
tangent_sphere_gate = True   # tangent-sphere radial GATE; notangentsphere (W251) ties 3.278523 (load-bearing). [literal]
# PRUNED (the ONLY droppable lever): sphere-lookahead PULL removed -> the canonical `nosphere` stack
# (N=16 mean 3.278848, +0.004608). The two sphere removals do NOT compose (nosphere_notangent
# collapses at N=12, mean 3.279551).
sphere_lookahead_pull = False  # PRUNED by the leave-one-out (rule-6 mandatory prune). [literal: nosphere]

# ---- gate-FAILing lower bins (as-committed INPUTS, NOT achieved bins — N91) ----------------------
#   step-2925: W258 n=9 mean 3.279373, +0.001880                                   (FAIL — not viable)
#   sub-2900 worker-cascade: isolated 2880-2905 single seeds (Worker131 2885, W247 2 seeds <=2900,
#     window best `worker206` 2875) — EVERY cohort reverts 'too late' at N>=8/N>=11; step-2900 NEVER
#     stat-sig (W247 demoted at N=16, step-2900 mean 3.281334). All stat_verify=False.
# These confirm the verified frontier is step-2940; sub-2940/sub-2900 are noise-floor single seeds.

# ---- Imports / dependency provenance (reproducibility) -------------------------------------------
# Public modded-nanogpt PR #291/#294 mechanisms + a SOAP sidecar, rebuilt on the compliant v37
# checkout; stdlib + PyTorch + the public-PR optimizer code (NOT a forbidden third-party lib — the
# v37 rebuild passed the C05 byte-identical-Architecture + baseline RMSNorm/q-k norm + forbidden
# norm/gain gate). Each launch py_compile + Architecture-gated.
