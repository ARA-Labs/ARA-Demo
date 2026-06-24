# Config: C02 Muon2F-hidden stepping stone — Adam-mini opt1 + Muon2F-hidden on the C01 parent.
#
# Grounding: transcribed (the launched_script.py of the run C02's Proof: names; N51 stepping stone)
#   v1/codex/scratchpad/variants/train_gpt_simple_normuon_b090to080_mlpprojlr124375_adamminiopt1_
#     muon2fhidden_b2p095_eps1e3_tailresrmsstack_aggmom3hidden_h3375_stop3250_seed0.py:408-451
#
# Crystallized by: logic/claims.md C02 (status: supported, depends on C01). Wave v1.
# Evidence: evidence/results/c02_compression_corridor.md (stop3250 3-seed: 3.27945/3.27965/3.27897).
#
# This is the building block BELOW the C01 3296 frontier: the first matrix-side preconditioner
# (Muon2F on the hidden group) that helped. It is a 3-seed reproduced STEPPING STONE at stop3250/3237
# — the narrator explicitly did NOT promote it as a formal frontier (gain over raw 3250 is under the
# step-noise gate). The promoted C02 frontier adds endpoint-EMA + mu_schedule on top
# (configs/v12iso_musched_v1_stop3220.py).
#
# DIVERGENCE POLICY: AS-COMMITTED script literals are primary; the stop here (3250) is a v1-internal
# as-committed INPUT, NOT an achieved/validated bin — the statistically-VALIDATED C02 frontiers are
# 3195/3220 (see the v12iso config + evidence). Do not read 3250 as a certified achieved bin.

# ---- Schedule / stop -----------------------------------------------------------------------------
train_steps      = 3250   # early-stop step (3-seed stepping stone, NOT a stat-validated bin). [literal]
schedule_steps   = 3375   # decoupled WSD horizon (inherited C01 lever). [literal]
cooldown_frac    = 0.7    # [literal]
beta2_thaw_steps = 3298   # late beta2 warm-down endpoint (b090to080). [literal]

# ---- optimizer1 = Adam-mini (REPLACES AdamW; the C02 opt1 change; see adam_mini.py) --------------
opt1_embed_lr     = 0.3       # [literal]
opt1_head_lr      = 1/320     # [literal]
opt1_1d_lr        = 0.01      # [literal]
opt1_betas        = (0.8, 0.95)  # [literal]
opt1_eps          = 1e-10        # [literal]
opt1_weight_decay = 0.0          # [literal]
# (Adam-mini = AdamW with a per-row / per-tensor shared second moment; the one optimizer-replacement
#  signal that survived the washout — trace N15/N22, staging O04.)

# ---- optimizer2 = NorMuon hidden WITH Muon2F + AggMo-3 (the C02 matrix-side core) ----------------
opt2_lr           = 0.030    # [literal]
opt2_weight_decay = 0.0125   # [literal]
opt2_beta2        = 0.90     # [literal start; warmed down to 0.80]
opt2_aggmo3       = True     # hidden AggMo-3 momentum. [literal flag]
opt2_muon2f       = True     # Muon2F row/col covariance pre-conditioner before NS5. [literal flag]
opt2_beta_pre     = 0.95     # Muon2F preconditioner EMA beta ("b2p095"). [literal]
opt2_pre_eps      = 1e-3     # Muon2F preconditioner eps ("eps1e3"). [literal]

# ---- optimizer3 = NorMuon MLP-proj WITH the tailresrmsstack error-feedback tail -----------------
opt3_lr           = 0.0373125  # MLP-proj LR ("mlpprojlr124375"). [literal]
opt3_weight_decay = 0.0100     # [literal]
opt3_beta2        = 0.90       # [literal start; warmed down]
opt3_error_feedback     = True   # orthogonalization error-feedback on MLP-proj. [literal flag]
opt3_base_feedback      = 0.04   # [literal]
opt3_tail_feedback      = 0.04804  # feedback ramps base->tail over [2875,3125]. [literal]
opt3_tail_feedback_start = 2875    # [literal]
opt3_tail_feedback_end   = 3125    # [literal]
opt3_base_residual_decay = 0.05    # [literal]
opt3_tail_residual_decay = 0.022   # residual_decay ramps base->tail over the same window. [literal]
opt3_momentum_refresh_step  = 3125 # one-shot momentum refresh. [literal]
opt3_momentum_refresh_alpha = 0.10 # [literal]
opt3_residual_pulse_step    = 3125 # one-shot residual-decay pulse. [literal]
opt3_residual_pulse_decay   = 0.1025  # [literal]
opt3_residual_rms_norm_step      = 3125  # one-shot residual-RMS renorm. [literal]
opt3_residual_rms_norm_min_scale = 0.80  # clamp. [literal]
opt3_residual_rms_norm_max_scale = 1.25  # clamp. [literal]
opt3_late_lr_start = 3250   # late-LR bump start. [literal]
opt3_late_lr_scale = 1.003  # [literal]
