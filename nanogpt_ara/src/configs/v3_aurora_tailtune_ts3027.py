# Config: C07 — tail-tuned proj-only Aurora, the FIRST compliant gated stop below ts3037, COMMITTED
# to canonical train_gpt_simple.py. Recipe slug:
# v3_aurora2b035to050_sched3028_ts3027_laalign2451_p012_betaprelo_finalhi (the ts3027 frontier);
# the ts3028 stepping stone is v3_aurora2b035projtail_b035to050_t2450r350_ts3028.
#
# Grounding: transcribed (the AS-COMMITTED canonical file — C07's closure is an artifact commitment)
#   records/track_3_optimization/train_gpt_simple.py @ commit e76d686  (ts3027 beta-preload+endpoint-LA)
#   records/track_3_optimization/train_gpt_simple.py @ commit e8d7bbe  (ts3028 beta-ramp 0.35->0.50)
#   (tail-shaping schedule in src/execution/aurora_beta_tail_schedule.py; the C06 Aurora mechanism in
#    src/execution/aurora_preconditioner.py; the C04 base geometry in legal_v12opt_muon_contra.py).
#
# Crystallized by: logic/claims.md C07 (status: supported, depends on C06, C04, C05). Wave v3.
# Evidence: evidence/results/c07_aurora_tailtune_frontier.md (the N87 committed promotions:
#   ts3029 n=8 +0.006177; ts3028 n=8 +0.005547, n=12 +0.006914; ts3027 n=8 +0.004225, n=12 +0.005595).
# Compliance premise: C05 — byte-identical-Architecture base, enforced by launch_variant_gate.sh.
# SUBMITTABLE + COMMITTED (the first lineage claim whose closure is code committed to canonical).
#
# DIVERGENCE / SCOPE annotations (driver/materialize.md):
#   * train_steps=3027 is BOTH the script literal (the committed canonical stop) AND the
#     claim-validated frontier — they AGREE. It is the LOWEST committed n=8-gated stop; the recipe
#     keeps the C06 Aurora mechanism IDENTICAL (this is endpoint/schedule tail-shaping, NOT a new
#     optimizer family). The advance over C04/C06 is ~10 steps (ts3037 -> ts3027).
#   * A config pinning a sub-3027 stop as an ACHIEVED bin would be FALSE: the direct ts3026
#     beta-preload analog FAILS N=4 (mean 3.279435); the best conditional mechanism `rank8-subbrake`
#     FAILS on N=8 expansion (+0.003843); the entire sub-3000 (ts2999) mechanism hunt clusters at
#     ~3.280 and never gates below ts3027 (N88). So this file pins 3027 and annotates ts3026/sub-3000
#     as gate-FAILing.
#   * Stays ~37 steps ABOVE the ~2990 public PR #294 floor and ~87-127 steps above the v3
#     sub-2950/sub-2900 goal (NOT reached — trace N16). The public floor is broken later by C08 (2940).
#   * The ts3027 N=8 pass is MAX-LIMITED by a single high seed (3.28031) — the seed-fragility the gate
#     is designed to police; n=12 (mean 3.278385, +0.005595) confirms robustness.

# ---- the C06 base recipe (UNCHANGED Aurora mechanism) --------------------------------------------
base_recipe = "v3_aurora2b035projonly_rolelr2_lookahead_ts3037"   # see v3_aurora_projonly_ts3037.py
# proj-only Aurora (aurora_mask="proj_only") on the C04 stack; C07 changes ONLY the beta SCHEDULE and
# the lookahead endpoint ALIGNMENT (the tail-shaping), not the optimizer mechanism. C04 base levers
# (rolewd/rolelr2, mu-schedule, eta floor, lookahead cadence, Contra 0.225) inherited verbatim.

# ---- Schedule / stop (the COMMITTED ts3027 frontier) ---------------------------------------------
train_steps          = 3027   # the committed, n=8-gated frontier (commit e76d686). [literal]
opt_schedule_steps   = 3028   # `_OPT_SCHEDULE_STEPS` (split clock: train_steps <= schedule_steps). [literal]

# ---- the NEW C07 lever (a): late Aurora-beta RAMP 0.35 -> 0.50 (the ts3028 promotion) ------------
# Core: src/execution/aurora_beta_tail_schedule.aurora_beta_ramp_at_step.
aurora_beta_ramp_enabled = True
aurora_beta_lo           = 0.35   # ramp start. [literal]
aurora_beta_hi           = 0.50   # ramp end. [literal]
aurora_ramp_t0           = 2450   # ramp begins at step 2450 ("b035to050 t2450"). [literal]
aurora_ramp_len          = 350    # ramp over 350 steps ("r350"). [literal]

# ---- the NEW C07 lever (b): terminal beta-PRELOAD + endpoint-aligned lookahead (the ts3027 win) --
# Core: src/execution/aurora_beta_tail_schedule.{aurora_beta_preload_at_step, endpoint_aligned_lookahead_start}.
beta_preload_enabled   = True
beta_preload_lo        = 0.35   # low conditioning beta in the pre-window. [literal]
beta_preload_hi        = 0.50   # high beta in the final pulse ("finalhi"). [literal]
beta_preload_window    = 3014   # low-beta pre-window opens at step 3014. [literal]
beta_preload_pulse     = 3025   # high-beta pulse fires at/after step 3025. [literal]
lookahead_endpoint_align = 2451 # lookahead start L0 ("laalign2451"); (S-1-L0)%25==0 -> final pull on endpoint. [literal]
lookahead_pull_p012      = 0.12 # endpoint-aligned pull strength ("p012"). [literal]

# ---- the three COMMITTED promotions (provenance; N87) --------------------------------------------
# (1) direct beta0.35 proj-only ts3029: n=8 mean 3.277816, +0.006177; ckpt3025 +0.005360; n=10 +0.006002.
#     promoted v3_aurora2b035projonly_rolelr2_lookahead_ts3029.py ("lowers public 3030 by 1, private 3035 by 6").
# (2) late beta-ramp 0.35->0.50 ts3028: n=8 mean 3.278039, +0.005547; ckpt3025 +0.004890; n=12 +0.006914.
#     COMMIT e8d7bbe ("Promote Aurora beta ramp 3028 recipe").
# (3) beta-preload+endpoint-LA ts3027: n=8 losses [3.28031,3.27759,3.27725,3.27872,3.27974,3.27806,3.27816,3.27822]
#     mean 3.278506, +0.004225 (max-limited by the 3.28031 seed); n=12 mean 3.278385, +0.005595.
#     COMMIT e76d686 (docs 737b8b9).  <-- this file pins promotion (3), the LOWEST committed gated stop.

# ---- gate-FAILing lower-bin attempts (as-committed INPUTS, NOT achieved bins — N88) --------------
#   direct ts3026 beta-preload analog: N=4 mean 3.279435                       (FAIL — "does not port one step lower")
#   rank8-subbrake (best conditional): N=4 mean 3.278548 -> N=8 mean 3.278641, +0.003843  (FAIL on expansion)
#   dinertia-switch-b997-l012: N=4 mean ~3.27830 (barely) but step-3000 5-seed mean 3.280306 (NOT sub-3000)
#   entire ts2999 cascade (KL-SOAP sidecars / dual-momentum / depth-wave / cautious-WD / SOAP-Aurora-Contra):
#     cluster ~3.2780-3.2810, N=8 viability needs mean <= ~3.27859 — none gate below ts3027.
# These confirm the verified committed bin is 3027; sub-3027 is a clean negative (and triggered the
# public-frontier pivot N89 -> C08).

# ---- Imports / dependency provenance (reproducibility) -------------------------------------------
# stdlib + PyTorch ONLY: AdamW + LOCAL Muon (legal_v12opt_muon_contra) + LOCAL Aurora hook
# (aurora_preconditioner) + LOCAL tail schedule (aurora_beta_tail_schedule). NO third-party optimizer
# library. Committed code-only into canonical records/track_3_optimization/train_gpt_simple.py.
