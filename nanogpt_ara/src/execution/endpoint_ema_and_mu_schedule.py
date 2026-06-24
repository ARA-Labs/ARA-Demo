# Endpoint EMA (validation-time weight averaging) + the isolated v12 mu_schedule lever (C02 cores).
#
# Grounding: transcribed
#   (v1/codex/scratchpad/variants/train_gpt_simple_v12iso_musched_h3375_s3220_seed0.py:
#      471-477   # mu_schedule block inside set_hparams
#      527-541   # endpoint-EMA buffer + update_tail_ema
#      554-576)  # validation-time swap-in / restore of the averaged weights
# This is the exact run named by C02's Proof: as the cleaner claimable frontier (v12iso-musched
# s3220, n=12, mean 3.278060, speedrun-rule score 0.006720). Identical code in the s3195-seed20
# proof script.
#
# Wave: v1  |  Crystallized by: logic/claims.md C02 (supported, depends on C01).
# See logic/concepts.md "Endpoint EMA (validation-time weight averaging)" and
# "v12 mu_schedule (isolated momentum-schedule lever)".
#
# KERNEL MODE: the two levers + typed I/O signatures only; the frozen training/validation loop is
# src/environment.md. Both are run-control / schedule changes — GPT.forward stays byte-identical
# (N16 strict boundary).

from torch import Tensor
import torch


# ============================ Lever 1: endpoint EMA (validation-time) ============================
# As-committed literals (this run): start step 2000, beta 0.99. ("ema099 / start2000".)
tail_ema_start_step = 2000
tail_ema_beta = 0.99
tail_ema_params = None      # lazily allocated float32 shadow of model_params


@torch.no_grad()
def update_tail_ema(next_step: int) -> None:
    """Maintain a float32 EMA of the model weights from `tail_ema_start_step` onward, in place.

    I/O signature:
        next_step : int   the step about to begin (called as update_tail_ema(step + 1) post-opt.step)
        -> None  (mutates the module-global `tail_ema_params`; reads module-global `model_params`)

    Online training is NOT touched — this only accumulates the average. The averaged weights are
    swapped in only at validation time (see validate_with_tail_ema). The strongest endpoint-smoothing
    signal on the Muon2F stack (trace N53); fixed uniform SWA was consistently worse.
    """
    global tail_ema_params
    if next_step < tail_ema_start_step:
        return
    if tail_ema_params is None:
        tail_ema_params = [p.detach().float().clone() for p in model_params]   # noqa: F821 (loop global)
        return
    for avg, p in zip(tail_ema_params, model_params):                          # noqa: F821
        avg.mul_(tail_ema_beta).add_(p.detach().float(), alpha=1 - tail_ema_beta)


@torch.no_grad()
def swap_in_tail_ema_for_validation():
    """Temporarily replace online weights with the EMA average for one validation pass; return the
    saved online weights so the caller can restore them in a finally-block.

    I/O signature:
        -> list[Tensor] | None   saved online params (None if EMA not yet active)

    Transcribed from the validation section (:554-559 swap-in, :573-576 restore). The first SWA
    implementation had a `p.copy_` outside `torch.no_grad()` bug (a run-control bug, corrected, not
    evidence — see concepts.md / trace N53); this version is correct under no_grad().
    """
    if tail_ema_params is None:
        return None
    online_params = [p.detach().clone() for p in model_params]                 # noqa: F821
    for p, avg in zip(model_params, tail_ema_params):                          # noqa: F821
        p.copy_(avg.to(dtype=p.dtype))
    return online_params


@torch.no_grad()
def restore_online_weights(online_params) -> None:
    """Restore the online training weights saved by swap_in_tail_ema_for_validation (finally-block)."""
    if online_params is None:
        return
    for p, online in zip(model_params, online_params):                        # noqa: F821
        p.copy_(online)


# ============================ Lever 2: the isolated v12 mu_schedule ==============================
# The single lever isolated (by leave-one-out, trace N57) from another agent's "v12" recipe bundle
# handed over by the user (trace N56). The full v12 PACKAGE washed out; this lever ALONE carries the
# gain. It is a schedule on the optimizer momentum `mu` (applied to any group that carries a `mu`,
# i.e. the NorMuon hidden groups). It lives INSIDE set_hparams (transcribed here as a standalone
# block with its typed signature; the surrounding WSD LR + beta2/feedback machinery is wsd_schedule.py
# and the muon2f stack).

def apply_mu_schedule(group: dict, step: int, train_steps: int) -> None:
    """Warm UP mu 0.85->0.95 over the first 300 steps, hold 0.95, then warm DOWN 0.95->0.85 over the
    last 50 steps before `train_steps`.

    I/O signature:
        group       : dict   an optimizer param group carrying key "mu" (mutated in place)
        step        : int    current step
        train_steps : int    the early-stop step (== step_to_3.28; e.g. 3220 for the s3220 frontier)
        -> None

    As-committed constants (this run): warmup_steps=300, mu_lo=0.85, mu_hi=0.95, warmdown_window=50.
    """
    if "mu" not in group:
        return
    if step < 300:
        group["mu"] = 0.85 + (0.95 - 0.85) * (step / 300)
    elif step >= train_steps - 50:
        group["mu"] = 0.95 + (0.85 - 0.95) * ((step - (train_steps - 50)) / 50)
    else:
        group["mu"] = 0.95
