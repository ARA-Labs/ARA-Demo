# Decoupled WSD (stable-then-decay) LR schedule + beta2 warm-down (C01's schedule lever).
#
# Grounding: transcribed
#   (v1/codex/scratchpad/variants/train_gpt_simple_normuon_b090to082_mlpprojlr125_h3375_stop3345_seed0.py:305-318)
# This is the bare C01 backbone schedule (NorMuon + decoupled WSD + beta2 warm-down b090to082),
# the variant whose .py snapshot AND run log both exist and are cited by C01's Proof:. The C01
# stop3296 headline run uses the same set_hparams shape with the warm-down endpoint retuned to 0.80
# (b090to080) — see the log-embedded snapshot
#   v1/codex/scratchpad/runs/normuon-...-h3375-stop3296-seed0.log:391-397 (beta2_thaw_steps=3298).
#
# Wave: v1  |  Crystallized by: logic/claims.md C01 (supported).
# See logic/concepts.md "WSD / stable-then-decay schedule (incumbent schedule)".
#
# KERNEL MODE: the schedule function + its typed I/O signature only. Wired into the training loop as
# `set_hparams(step)` once per step, before opt.step() (frozen-loop call site, src/environment.md).

# ---- DECOUPLED horizon (the C01 lever) -----------------------------------------------------------
# The defining C01 move: schedule_steps (the LR-decay horizon) is set INDEPENDENTLY of train_steps
# (the early-stop step). The incumbent baseline ties them (decay over the whole run); C01 decouples
# them — typically schedule_steps >= train_steps (e.g. h3375 / stop3345 or stop3296) so the LR decays
# INTO the 3.28-crossing region rather than all the way to 0. These are module-level globals in the
# launched script (as-committed literals; pinned per recipe in src/configs/):
train_steps = 3345       # early-stop step == step_to_3.28 (the quantity minimized). [as-committed literal]
schedule_steps = 3375    # WSD decay horizon, DECOUPLED from train_steps. [as-committed literal]
# beta2 warm-down endpoint: 0.82 in this stop3345 variant (b090to082); 0.80 in the stop3296 headline
# (b090to080), with beta2_thaw_steps=3298 there. (Source: the two cited launched scripts.)


def set_hparams(step: int, cooldown_frac: float = 0.7) -> None:
    """Apply the WSD LR multiplier + the late beta2 warm-down to every optimizer group, in place.

    I/O signature:
        step          : int     current training step
        cooldown_frac : float   fraction of `schedule_steps` spent decaying (0.7 -> flat 30%, decay 70%)
        -> None  (mutates group["lr"] and group["beta2"] on each optimizer group)

    Behaviour:
      * eta = 1.0 while progress < 1 - cooldown_frac, else eta = (1 - progress)/cooldown_frac
        (stable-then-linear-decay; NO warmup), with progress = step / schedule_steps.
      * beta2 warm-down ("late beta2 thaw"): a NorMuon group's beta2 is held at 0.90, then linearly
        thawed to the endpoint (0.82 here; 0.80 in the stop3296 headline) over [2500, train_steps].
        C01's evidence basis notes the .90->.80 thaw beat the .82 endpoint by only +0.00006.

    Depends on module-level `optimizers`, `schedule_steps`, `train_steps` from the launched script.
    """
    progress = step / schedule_steps
    assert 0 <= progress < 1
    if progress < 1 - cooldown_frac:
        eta = 1.0
    else:
        eta = (1 - progress) / cooldown_frac
    for opt in optimizers:                                    # noqa: F821 (launched-script global)
        for group in opt.param_groups:
            group["lr"] = group["initial_lr"] * eta
            if "beta2" in group:
                thaw = max(0.0, min(1.0, (step - 2500) / (train_steps - 2500)))
                group["beta2"] = 0.90 + thaw * (0.82 - 0.90)  # endpoint 0.82 (b090to082, stop3345)
