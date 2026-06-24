# Config: C06 — proj-only Aurora on the architecture-COMPLIANT C04 stack (the FIRST new optimizer
# mechanism to clear the gate). Recipe slug: v3_aurora2b035projonly_rolelr2_lookahead_ts3037
# (the committed beta0.5 / beta0.35 proj-only cohorts).
#
# Grounding: transcribed (the as-committed launched variant the C06 proof runs index)
#   v3/codex/scratchpad/variants/v3_aurora2b035projonly_rolelr2_lookahead_ts3037.py
#   (Init & Optim Hyperparams block; Aurora geometry in src/execution/aurora_preconditioner.py;
#    the UNCHANGED C04 base geometry in src/execution/legal_v12opt_muon_contra.py).
#
# Crystallized by: logic/claims.md C06 (status: supported, depends on C04, C05). Wave v3.
# Evidence: evidence/results/c06_aurora_projonly_statpass.md (the N81 cohort gate:
#   proj-only beta0.5 ts3037 n=8, mean 3.277852, (3.28-mean)*sqrt(8) = +0.006074 -> PASS;
#   proj-only beta0.35 n=8, mean 3.278044, +0.005533 -> PASS).
# Compliance premise: C05 — byte-identical-Architecture base (baseline RMSNorm.forward + q/k
#   F.rms_norm), enforced by src/execution/launch_variant_gate.sh. SUBMITTABLE.
#
# DIVERGENCE / SCOPE annotations (driver/materialize.md):
#   * train_steps=3037 is BOTH the script literal AND the claim-validated frontier — they AGREE.
#     C06 clears the SAME bin as C04 (3037), by a LARGER margin (+0.006074 vs C04 +0.004589); it does
#     NOT lower the bin. A config pinning a sub-3037 stop as an ACHIEVED bin would be FALSE: the
#     lower-bin Aurora attempts FAIL the gate (direct all-rect beta0.25 ts3025 n=8 -0.001032; direct
#     proj-only beta0.5 ts3035 n=8 +0.003772 just-short; the 3025-checkpoint means of the passing
#     ts3037 schedules are near-misses +0.003939/+0.003408) — see N83 / the results file. So this file
#     pins 3037 (the n=8-verified frontier), and the lower stops are annotated as gate-FAILing inputs.
#   * The mask is LOAD-BEARING and part of the mechanism: proj-only (wide MLP m<n, via transpose)
#     PASSES; the all-rectangular mask at ts3037 is a NEAR-MISS (+0.003995); fc-only is bad (N81).
#     So `aurora_mask = "proj_only"` is pinned, not "all_rect".
#   * ALL C04 levers are PRESERVED unchanged (C06 only adds Aurora): rolewd/rolelr2 LR/WD, the
#     mu-schedule, the eta floor (0.02), lookahead (start 2450 / interval 25 / alpha 0.35 / pull 0.15),
#     and Contra beta 0.225 — pinned in src/configs/legal_v12opt_ts3037_v2.py, not re-pinned here.
#   * Still well ABOVE the v3 sub-2950/sub-2900 goal and at/above the ~2990 public PR #294 floor
#     (not reached at this claim — trace N16 / N89); the bin is lowered later by C07 (ts3027).

# ---- the C04 base recipe (UNCHANGED) -------------------------------------------------------------
base_recipe = "legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625"  # see legal_v12opt_ts3037_v2.py
# All Optimization + Init & Optim Hyperparams of the C04 base are inherited verbatim (C06 changes
# ONLY the addition of proj-only Aurora inside muon_update). Do NOT duplicate them; they are the
# single source of truth in src/configs/legal_v12opt_ts3037_v2.py.

# ---- Schedule / stop -----------------------------------------------------------------------------
train_steps   = 3037   # the n=8-verified C06 frontier (== C04's bin; larger margin, not lower). [literal]
cooldown_frac = 0.7    # inherited C04 WSD cooldown. [literal]
eta_min       = 0.02   # inherited C04 nonzero LR tail floor. [literal]

# ---- the NEW C06 lever: proj-only Aurora (leverage-aware preconditioner) --------------------------
# Core: src/execution/aurora_preconditioner.py (aurora_precondition + muon_update_aurora_projonly).
aurora_enabled = True
aurora_mask    = "proj_only"   # wide MLP `proj` matrices (m<n) ONLY, via transpose. LOAD-BEARING:
                               # fc-only hurts, all-rect is a near-miss (+0.003995), proj-only PASSES. [literal]
aurora_beta    = 0.50          # the COMMITTED frontier cohort (the larger-margin pass, +0.006074). [literal]
# aurora_beta = 0.35 also PASSES (mean 3.278044, +0.005533) — the secondary committed cohort. [literal]
aurora_style   = "static"      # static beta (NOT a tail-ramp — the ramp is the C07 lever, see
                               # src/configs/v3_aurora_tailtune_ts3027.py). [literal]

# ---- gate-FAILing lower-bin attempts (as-committed INPUTS, NOT achieved bins — N83) --------------
# Pinned here ONLY to document the rejected boundary (never as achieved frontiers):
#   direct all-rectangular beta0.25 @ ts3025, n=8 -> mean 3.280365, score -0.001032  (FAIL)
#   direct proj-only beta0.5    @ ts3035, n=8 -> mean 3.278666, score +0.003772       (FAIL, ~0.00008 short)
#   proj-only beta0.5 ts3037 schedule, checkpoint-3025 mean 3.278607 -> +0.003939     (near-miss, not the bin)
#   proj-only beta0.35 ts3037 schedule, checkpoint-3025 -> +0.003408                  (near-miss, not the bin)
# These confirm the verified bin is 3037; the sub-3037 single-seed crossings (e.g. the proj-tail
# eta-min screen's best single seed 2975, `v3aur2projtail-etamin001-3034` 3.27558) are noise-floor
# artifacts that wall at the stop, NOT gated cohorts.

# ---- Imports / dependency provenance (reproducibility) -------------------------------------------
# stdlib + PyTorch ONLY: torch.optim.AdamW + the LOCAL Muon (legal_v12opt_muon_contra) + the LOCAL
# Aurora hook (aurora_preconditioner). NO third-party optimizer library (the v3 launches each passed
# py_compile + byte-identical Architecture + exact baseline RMSNorm/q-k norm + forbidden norm/gain grep).
