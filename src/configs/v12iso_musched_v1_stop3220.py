# Config: C02 headline claimable frontier — v12iso-musched (mu_schedule + endpoint-EMA on Muon2F).
#
# Grounding: transcribed (the launched_script.py of the run C02's Proof: names as "the cleaner v12
# claim")  v1/codex/scratchpad/variants/train_gpt_simple_v12iso_musched_h3375_s3220_seed0.py:408-541
#
# Crystallized by: logic/claims.md C02 (status: supported, depends on C01). Wave v1.
# Evidence: evidence/results/c02_compression_corridor.md + evidence/results/c02_statistical_pass.md
#   (v12iso-musched s3220: n=12, mean 3.278060, speedrun-rule score 0.006720 — PASSES the gate).
#
# This is the promoted C02 frontier: the muon2f stepping stone (configs/muon2f_v1_stop3250.py) PLUS
# two run-control levers — endpoint EMA and the isolated v12 mu_schedule. It clears the speedrun
# claim rule ((3.28 - mean)*sqrt(n) >= 0.004) and is materially below the C01 3296 frontier.
#
# DIVERGENCE / SCOPE annotations (driver/materialize.md):
#   * train_steps=3220 is an AS-COMMITTED INPUT that is statistically validated at n=12 (this run is
#     the "+25 steps" cleaner claim the user suggested). The companion s3195 run validates at n=39.
#   * The lower stop3170 was REJECTED by the n=15 gate (mean 3.280266, negative score) — so a config
#     pinning 3170 as an achieved bin would be FALSE. This file pins 3220 (validated), not 3170.
#   * Still ~400 steps ABOVE the user's <2800 stretch target (not reached — trace N16).

# ---- Schedule / stop -----------------------------------------------------------------------------
train_steps      = 3220   # early-stop step; statistically-validated C02 frontier (n=12). [literal]
schedule_steps   = 3375   # decoupled WSD horizon (C01 lever, inherited). [literal]
cooldown_frac    = 0.7    # [literal]
beta2_thaw_steps = 3298   # late beta2 warm-down endpoint (b090to080). [literal]

# ---- Lever A: isolated v12 mu_schedule (the lever C02 isolates; see endpoint_ema_and_mu_schedule) -
# Applied to any optimizer group carrying "mu" (the NorMuon hidden groups). The full v12 PACKAGE
# washed out; this lever ALONE carries the gain (leave-one-out, trace N57).
mu_warmup_steps   = 300   # warm mu 0.85->0.95 over the first 300 steps. [literal]
mu_lo             = 0.85  # mu floor (warmup start AND warm-down end). [literal]
mu_hi             = 0.95  # mu plateau value. [literal]
mu_warmdown_window = 50   # warm mu 0.95->0.85 over the last 50 steps before train_steps. [literal]

# ---- Lever B: endpoint EMA (validation-time weight averaging; see endpoint_ema_and_mu_schedule) ---
tail_ema_start_step = 2000  # begin accumulating the weight EMA at step 2000 ("start2000"). [literal]
tail_ema_beta       = 0.99  # EMA decay ("ema099"); strongest endpoint-smoothing signal (N53). [literal]
# (Validation-only swap: averaged weights are used for the val pass, online weights restored after;
#  GPT.forward byte-identical. Fixed uniform SWA was consistently worse — concepts.md / N53.)

# ---- optimizer1 = Adam-mini (inherited from the C02 muon2f stack; see adam_mini.py) --------------
opt1_embed_lr     = 0.3       # [literal]
opt1_head_lr      = 1/320     # [literal]
opt1_1d_lr        = 0.01      # [literal]
opt1_betas        = (0.8, 0.95)  # [literal]
opt1_eps          = 1e-10        # [literal]
opt1_weight_decay = 0.0          # [literal]

# ---- optimizer2 = NorMuon hidden + Muon2F + AggMo-3 (inherited; see muon2f_hidden.py) ------------
opt2_lr           = 0.030    # [literal]
opt2_weight_decay = 0.0125   # [literal]
opt2_beta2        = 0.90     # [literal start; warmed down to 0.80]
opt2_aggmo3       = True     # [literal flag]
opt2_muon2f       = True     # [literal flag]
opt2_beta_pre     = 0.95     # [literal]
opt2_pre_eps      = 1e-3     # [literal]
# NOTE: optimizer2's NorMuon groups carry "mu", so the mu_schedule (Lever A) acts on them.

# ---- optimizer3 = NorMuon MLP-proj + tailresrmsstack error-feedback tail (inherited) -------------
# Identical to configs/muon2f_v1_stop3250.py opt3_* block (error_feedback=True, base_feedback=0.04,
# tail_feedback=0.04804 over [2875,3125], residual-RMS-norm pulse @3125 clamp[0.80,1.25],
# momentum_refresh @3125 alpha 0.10, residual_pulse @3125 decay 0.1025, late_lr @3250 scale 1.003).
# All [literals]; see that file for the per-HP annotations (not duplicated here).
opt3_lr           = 0.0373125  # MLP-proj LR ("mlpprojlr124375"). [literal]
opt3_weight_decay = 0.0100     # [literal]
opt3_beta2        = 0.90       # [literal start; warmed down]
