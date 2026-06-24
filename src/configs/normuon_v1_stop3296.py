# Config: C01 headline recipe — NorMuon + decoupled-WSD, the 2-seed reproduced sub-3500 frontier.
#
# Grounding: transcribed (the log-embedded launched_script.py snapshot of the run C01's Proof: names)
#   v1/codex/scratchpad/runs/normuon-b090to080-mlpprojlr124375-tailresrmsstack-aggmom3hidden-
#     h3375-stop3296-seed0.log:335-353  (Init & Optim Hyperparams; code region ends at the ==== at :493)
#
# Crystallized by: logic/claims.md C01 (status: supported). Wave v1.
# Evidence: evidence/results/c01_normuon_wsd_frontier.md  (seed0 3.27914, seed1 3.27872 @ step 3296).
#
# DIVERGENCE POLICY (driver/materialize.md): this file pins the AS-COMMITTED SCRIPT LITERALS as the
# primary reproducible values; where a crystallized claim narrates a different (interpretation) value
# it is recorded inline as an annotation, never silently substituted. C01 narrates the bare Muon
# backbone as "lr≈0.30" and "lr≈0.040" in places and asserts only the EXISTENCE/seed-reproducibility
# of a sub-3500 recipe (not any single step count); the committed script literals below are what
# actually ran and reproduced 2-seed at step 3296.

# ---- Schedule / stop (the C01 decoupled-WSD lever) ----------------------------------------------
train_steps    = 3296    # early-stop step == step_to_3.28; the 2-seed reproduced C01 frontier. [literal]
                         #   Annotation: C03's stat-validated defensible budget is narrated higher
                         #   (3100-style framing); C01 fixes only that a sub-3500 recipe EXISTS and
                         #   reproduces — 3296 is the as-committed reproduced stop, not a "best".
schedule_steps = 3375    # WSD LR-decay horizon, DECOUPLED from train_steps (h3375 > stop3296 -> LR
                         #   decays INTO the 3.28 crossing). The C01 lever. [literal]
cooldown_frac  = 0.7     # WSD: LR flat for first 30%, linear-decay over last 70%; no warmup. [literal]
beta2_thaw_steps = 3298  # late beta2 warm-down endpoint step (the b090to080 thaw). [literal]

# ---- Init (frozen-benchmark zero-init of proj weights; NOT a discovered modifier) ---------------
# for name, p in model.named_parameters(): if "proj" in name: p.data.zero_()   # baseline init (env.md)

# ---- optimizer1 = AdamW over embed / head / 1D groups (baseline split; C01 keeps plain AdamW) ----
opt1_embed_lr   = 0.3        # embedding LR. [literal]  (baseline per-group split, src/environment.md)
opt1_head_lr    = 1/320      # output proj.weight LR (= 0.003125). [literal]
opt1_1d_lr      = 0.01       # LR for all ndim<2 params (gains/biases). [literal]
opt1_betas      = (0.8, 0.95)  # [literal]
opt1_eps        = 1e-10        # [literal]
opt1_weight_decay = 0.0        # [literal]
opt1_fused      = True         # [literal]

# ---- optimizer2 = NorMuon over the non-MLP-proj hidden matrices (the C01 core; see normuon.py) ---
opt2_lr           = 0.030    # NorMuon hidden LR. [literal]
                            #   Annotation: C01's Statement narrates the bare backbone as "lr≈0.30";
                            #   the committed hidden-group literal is 0.030 (the recipe value that ran).
opt2_weight_decay = 0.0125  # [literal]  (== the incumbent Muon wd; src/environment.md)
opt2_beta2        = 0.90    # NorMuon row-second-moment beta2 START; warmed DOWN to 0.80 over the tail
                            #   via the schedule (b090to080). [literal start; endpoint set in schedule]

# ---- optimizer3 = NorMuon over the MLP-proj group (mlp-proj LR split — a C01 modifier) -----------
opt3_lr           = 0.0373125  # MLP-proj NorMuon LR ("mlpprojlr124375" = 1.24375x the 0.030 base).
                               #   [literal]  This split is one of C01's named productive levers.
opt3_weight_decay = 0.0100     # [literal]
opt3_beta2        = 0.90       # [literal start; warmed down with opt2]

# ---- Stack modifiers active at the C01 stop3296 headline (group flags; see normuon.py dispatch) --
# optimizer2: aggmo3=True                      (hidden AggMo-3 momentum; muon2f_hidden.py)
# optimizer3: error_feedback=True + the tailresrmsstack tail schedule (base_feedback=0.04,
#             tail_feedback=0.04804 over [2875,3125], residual-RMS-norm pulse @3125 clamp[0.80,1.25],
#             momentum_refresh @3125 alpha 0.10, late_lr @3250 scale 1.003). [all literals]
# NOTE: optimizer1 here is PLAIN AdamW (Adam-mini enters only in the C02 stack). The "no respulse"
# pruned form of THIS stack (formalprune-norespulse-...-stop3296) is the n=72 formal member of C02.
