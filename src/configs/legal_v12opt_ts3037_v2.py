# Config: C04 — the architecture-COMPLIANT, statistically-VERIFIED v2 frontier (the central v2 recipe).
# Recipe slug: legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.
#
# Grounding: transcribed (the as-committed launched variant the C04 proof runs index)
#   v2/codex/scratchpad/variants/legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py
#   (Init & Optim Hyperparams block, lines 305-419; optimizer geometry in
#    src/execution/legal_v12opt_muon_contra.py).
#
# Crystallized by: logic/claims.md C04 (status: supported, depends on C05). Wave v2.
# Evidence: evidence/results/c04_legal_v12opt_statpass.md (the N78 cohort z-test:
#   ts3037 n=8, mean 3.2783775, (3.28-mean)*sqrt(8) = 0.004589 -> PASS, z=3.53, p~0.000208).
# Compliance premise: C05 — the base is byte-identical-Architecture (baseline RMSNorm.forward +
#   q/k F.rms_norm), enforced by src/execution/launch_variant_gate.sh. This recipe is SUBMITTABLE
#   (contrast the quarantined cc-v12 recipe, src/configs/ccv12_ts2999_v2_NONCOMPLIANT.py / C03).
#
# DIVERGENCE / SCOPE annotations (driver/materialize.md):
#   * train_steps=3037 is the AS-COMMITTED script literal AND the claim-validated frontier — they
#     AGREE here (unlike the v1 v12 case where the script literal 3025/0.045 diverged from the C03
#     narrated value). 3037 is "the EARLIEST common validation checkpoint that PASSES" the cohort
#     gate (step 3025 crosses per-run but its same-checkpoint cohort scores only 0.002454 -> FAIL).
#   * The window walked SINGLE-SEED legal crossings down to step 2962 (ts2962-r41 final 3.27992,
#     crossing @2962). Those are as-committed INPUTS of OTHER ts#### variants, NOT achieved bins:
#     by the SAME cohort gate they FAIL (ts2962 n=38 mean 3.28243 score -0.0150; ts2963 -0.0116;
#     ts2970 -0.0072; ts2982 -0.0054). A config pinning any sub-3037 stop as an ACHIEVED VALIDATED
#     bin would be FALSE — so this file pins 3037 (the n=8-verified frontier), not the low-step hits.
#   * body lr=0.045 / weight_decay=0.030 are the script literals (the v12-optimizer backbone values),
#     consistent with the v1 divergence note (v12 script body ran lr=0.045).
#   * Still well ABOVE the user's <2800 stretch target (not reached — trace N16); and the sub-3000
#     behavior on the NON-compliant cc-v12 base (C03) was "forward-path-assisted" (C05/N78) — removing
#     the forward-path change AND imposing the gate moved the verified frontier UP from sub-3000 to 3037.

# ---- Schedule / stop -----------------------------------------------------------------------------
train_steps    = 3037   # early-stop step = the n=8-verified C04 frontier (earliest passing checkpoint). [literal]
cooldown_frac  = 0.7    # WSD: stable LR until the final 70%-point, then decay to the eta floor. [literal]
eta_min        = 0.02   # nonzero LR TAIL FLOOR ("_ETA_MIN"); LR decays to 0.02*initial, not 0. [literal]
val_step_freq_coarse = 125  # validation cadence while step/train_steps < 0.9. [literal]
val_step_freq_fine   = 25   # validation cadence in the final 10% (the same-checkpoint scan basis). [literal]

# ---- optimizer2 = Muon (hidden 2D block weights) — base + cm0225 contra-direction ----------------
# Core update in src/execution/legal_v12opt_muon_contra.py (muon_update + Polar-Express NS5).
opt2_base_lr           = 0.045   # Muon base LR (role mults below scale this). [literal]
opt2_base_weight_decay = 0.030   # Muon base weight decay (role WDs below override per role). [literal]
contra_muon            = 0.225   # "_CONTRA_MUON" — cm0225 contra-direction strength. [literal]

# ---- Lever: role-split LR (rolelr2) + role-split weight decay (rolewd) ----------------------------
# Six per-role Muon groups off opt2_base_lr; attn.v mult 0.62500 is the "attn0625" slug.
# (builder: src/execution/legal_v12opt_muon_contra.build_role_split_muon_groups)
rolelr2_attn_q_mult    = 0.61875   # [literal]
rolelr2_attn_k_mult    = 0.61875   # [literal]
rolelr2_attn_v_mult    = 0.62500   # attn0625. [literal]
rolelr2_attn_proj_mult = 0.63750   # [literal]
rolelr2_mlp_fc_mult    = 1.01250   # [literal]
rolelr2_mlp_proj_mult  = 0.98750   # [literal]
rolewd_attn_q          = 0.02775   # [literal]
rolewd_attn_k          = 0.02775   # [literal]
rolewd_attn_v          = 0.02750   # [literal]
rolewd_attn_proj       = 0.02700   # [literal]
rolewd_mlp_fc          = 0.03150   # [literal]
rolewd_mlp_proj        = 0.03100   # [literal]

# ---- Lever: mu-schedule (warmup/cooldown on Muon's momentum mu) ----------------------------------
mu_lo               = 0.85   # mu floor (warmup start AND cooldown end). [literal]
mu_hi               = 0.95   # mu plateau. [literal]
mu_warmup_steps     = 300    # warm 0.85->0.95 over the first 300 steps. [literal]
mu_cooldown_steps   = 50     # cool 0.95->0.85 over the last 50 steps before train_steps. [literal]

# ---- Lever: lookahead (slow-weight pull on the Muon groups) --------------------------------------
lookahead_start_step = 2450  # begin slow-weight tracking at step 2450. [literal]
lookahead_interval   = 25    # sync every 25 steps. [literal]
lookahead_alpha      = 0.35  # slow <- slow + 0.35*(fast - slow). [literal]
lookahead_pull       = 0.15  # fast <- fast + 0.15*smooth*(slow - fast). [literal]
lookahead_ramp_steps = 150   # smoothstep ramp-in over 150 steps. [literal]

# ---- optimizer1 = AdamW (embeddings / output proj / all ndim<2 params) ---------------------------
# Unchanged from the v12-optimizer backbone; identical grouping to the v1 Adam-mini groups' LRs.
opt1_embed_lr      = 0.3        # embed.weight LR (with init embed *= 0.7 below). [literal]
opt1_head_lr       = 1/320      # proj.weight (output head) LR. [literal]
opt1_1d_lr         = 0.01       # all ndim<2 params (gains/biases). [literal]
opt1_betas         = (0.8, 0.95)  # [literal]
opt1_eps           = 1e-10        # [literal]
opt1_weight_decay  = 0.0          # [literal]
opt1_fused         = True         # [literal]

# ---- Init modifiers (Init & Optim Hyperparams) ---------------------------------------------------
init_proj_zero        = True   # zero every parameter whose name contains "proj" at init. [literal]
init_embed_mul        = 0.7    # embed.weight *= 0.7 at init (the v1 embed×0.7 lineage). [literal]

# ---- Imports / dependency provenance (reproducibility; N78) --------------------------------------
# stdlib + PyTorch ONLY: torch.optim.AdamW + the LOCAL Muon (src/execution/legal_v12opt_muon_contra).
# NO third-party optimizer library (verified per-seed in N78's reproducibility check).
