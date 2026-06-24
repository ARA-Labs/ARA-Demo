# Aurora-beta tail-shaping schedule — the C07 mechanism: a late beta-ramp 0.35->0.50 + a terminal
# beta-preload (low-beta pre-window then a high-beta final pulse) + an endpoint-aligned lookahead
# congruence. ENDPOINT-ONLY tail tuning of the C06 proj-only Aurora recipe; it lowers the COMMITTED,
# n=8-gate-verified compliant frontier from ts3037 (C06) to ts3027 — the FIRST compliant gated stop
# below ts3037 — WITHOUT changing the Aurora optimizer mechanism itself (it is schedule/endpoint
# shaping, NOT a new optimizer family).
#
# Grounding: transcribed
#   (records/track_3_optimization/train_gpt_simple.py @ commit e76d686  — the CANONICAL committed file)
#     - aurora_beta_at_step (late ramp 0.35->0.50, t0=2450 ramp=350)               : lines 388-404
#     - aurora_beta_preload (low-beta 3014..3024 pre-window then high-beta >=3025)  : lines 406-422
#     - endpoint-aligned lookahead congruence (the (S-1-L0)%25==0 final-pull check) : lines 424-436
#   C07's closure is an ARTIFACT COMMITMENT: the ts3028 beta-ramp recipe is commit e8d7bbe ("Promote
#   Aurora beta ramp 3028 recipe"); the ts3027 beta-preload+endpoint-lookahead recipe is commit
#   e76d686 (docs 737b8b9). The variants are also indexed under v3/codex/scratchpad/variants/ as
#   `v3_aurora2b035projtail_b035to050_t2450r350_ts3028.py` and
#   `v3_aurora2b035to050_sched3028_ts3027_laalign2451_p012_betaprelo_finalhi.py` (the files the
#   C07 proof runs' `indexed_run` lines name); each proof run self-logs the source at the log top.
#
# Wave: v3  |  Crystallized by: logic/claims.md C07 (supported, depends on C06, C04, C05) —
# "Tail-tuning the C06 proj-only Aurora recipe ... lowers the COMMITTED, n=8-gate-verified compliant
# frontier from ts3037 to step_to_3.28 = 3027 — the FIRST compliant gated stop below 3037; sub-3027
# does NOT gate." Compliance premise: C05 (byte-identical Architecture) — enforced by
# src/execution/launch_variant_gate.sh.
#
# KERNEL MODE: this captures ONLY the NEW v3 tail-shaping schedule (how the Aurora beta and the
# lookahead endpoint are scheduled near the stop). The Aurora mechanism itself is
# src/execution/aurora_preconditioner.py (C06); the base optimizer geometry (NS5, cm0225, rolewd/
# rolelr2, lookahead, mu-schedule) is src/execution/legal_v12opt_muon_contra.py (C04); neither is
# re-transcribed. The FROZEN benchmark is src/environment.md. HPs pinned in
# src/configs/v3_aurora_tailtune_ts3027.py.

# ---- (1) late Aurora-beta RAMP 0.35 -> 0.50 (the ts3028 promotion, commit e8d7bbe) --------------
_AURORA_BETA_LO, _AURORA_BETA_HI = 0.35, 0.50   # ramp endpoints. [literal]
_RAMP_T0, _RAMP_LEN = 2450, 350                 # ramp begins at step 2450, over 350 steps. [literal]


def aurora_beta_ramp_at_step(step: int) -> float:
    """Late linear ramp of the Aurora beta from 0.35 to 0.50 (I/O: step -> aurora_beta).

    Used as the `beta` argument to src/execution/aurora_preconditioner.aurora_precondition each step.
    Flat at 0.35 until step 2450, then linearly ramps to 0.50 by step 2800, flat 0.50 after. This is
    the `b035to050` lever; on its own it lowered the committed frontier ts3029 -> ts3028.
    """
    if step <= _RAMP_T0:
        return _AURORA_BETA_LO
    frac = min(1.0, (step - _RAMP_T0) / _RAMP_LEN)
    return _AURORA_BETA_LO + frac * (_AURORA_BETA_HI - _AURORA_BETA_LO)


# ---- (2) terminal beta-PRELOAD: low-beta pre-window then a high-beta final pulse (the ts3027 win) -
# The `p012-betaprelo-finalhi` lever (commit e76d686). A low-beta pre-window 3014..3024 conditions
# the optimizer state, then a high-beta pulse fires for the final steps (>= 3025). It is max-limited
# by a single high seed (the gate's seed-fragility check) — exactly why N=8 is required.
_PRELOAD_LO_BETA = 0.35    # beta during the pre-window. [literal]
_PRELOAD_HI_BETA = 0.50    # beta during the final high pulse. [literal]
_PRELOAD_WINDOW_START = 3014   # low-beta pre-window opens. [literal]
_PRELOAD_PULSE_STEP = 3025     # high-beta pulse fires at/after this step. [literal]


def aurora_beta_preload_at_step(step: int) -> float:
    """Terminal beta-preload schedule (I/O: step -> aurora_beta), the ts3027 frontier lever.

    Before the pre-window: the ramp value (aurora_beta_ramp_at_step). In the pre-window
    [3014, 3025): a low conditioning beta (0.35). At/after the 3025 pulse step: the high beta (0.50).
    """
    if step < _PRELOAD_WINDOW_START:
        return aurora_beta_ramp_at_step(step)
    if step < _PRELOAD_PULSE_STEP:
        return _PRELOAD_LO_BETA
    return _PRELOAD_HI_BETA


# ---- (3) endpoint-aligned lookahead congruence (the p012 final-pull alignment) ------------------
# The committed recipe aligns the lookahead start L0 so that the FINAL lookahead pull lands exactly
# at the last step: it requires (S - 1 - L0) % interval == 0 (interval = 25, the C04 lookahead
# cadence), so the terminal slow-weight pull coincides with the endpoint. `p012` is the pull
# strength used with this alignment.
_LOOKAHEAD_INTERVAL = 25      # the C04 lookahead sync cadence (legal_v12opt_muon_contra). [literal]
_LOOKAHEAD_PULL_P012 = 0.12   # the endpoint-aligned pull strength ("p012"). [literal]


def endpoint_aligned_lookahead_start(train_steps: int, desired_start: int = 2451) -> int:
    """Choose the lookahead start L0 nearest `desired_start` satisfying (S-1-L0) % 25 == 0.

    I/O: (train_steps S, desired_start) -> L0 such that the final pull lands on step S-1. At
    train_steps=3027 the committed alignment is L0=2451 ("laalign2451"); this helper reproduces that
    congruence for any stop so the endpoint pull is exact. Used with pull = _LOOKAHEAD_PULL_P012.
    """
    S = train_steps
    target_mod = (S - 1) % _LOOKAHEAD_INTERVAL
    L0 = desired_start - ((desired_start % _LOOKAHEAD_INTERVAL) - target_mod) % _LOOKAHEAD_INTERVAL
    return L0
