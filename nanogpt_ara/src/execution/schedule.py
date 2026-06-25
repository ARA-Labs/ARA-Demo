"""Per-role power-law LR schedule, horizon decoupling, mu-schedule, dense late validation.

The schedule controller — orthogonal to the Muon update pipeline. The power-law cooldown is the
single most critical frontier lever: removing it makes all 4 LOO seeds miss (C13, §14.1, §15).
Backs C02 (train-steps trim + dense validation), C06 (per-role schedule), C13 (pow_cooldown).
Grounded in cc_v3/07070-v88-aurora-proj-s2/launched_script.py (lines ~63-69, 83, 837-847).
"""
from __future__ import annotations
from dataclasses import dataclass


# Per-role cooldown-onset constants (`power_c`): each group begins cooling on a different step (§15.3).
POWER_C: dict[str, float] = {
    "embed": 4.98e-5,
    "proj": 5.18e-7,
    "scalars": 1.66e-6,
    "muon": 3.32e-6,
}
FLAT_LR: dict[str, float] = {"embed": 0.3, "proj": 1 / 320, "scalars": 0.01, "muon": 0.0375}

FINAL_LR_POWER: float = 1.2          # convex cooldown curvature (>1 holds LR higher, then drops steep)
FINAL_SCHEDULE_STEPS: int = 2985     # t_end: schedule horizon
FINAL_TRAIN_STEPS: int = 2900        # stop: run halts here (LR then = 1.8% of flat)


def power_law_lr(step: int, role: str = "muon") -> float:
    """Per-role convex cooldown: lr = min(flat_lr, power_c * (t_end - step)^1.2) (C06, C13, §15).

    Three coupled knobs the linear WSD baseline lacks, co-tuned so val lands ~3.279 at ~2885-2900:
      - power_c[role]  : cooldown ONSET (per role)
      - FINAL_LR_POWER : cooldown CURVATURE (convex)
      - t_end != stop  : terminal-LR OFFSET (horizon decoupling)
    For the Muon group: flat at 0.0375 until step ~599, then convex decay; at stop=2900 LR=0.00069.
    """
    flat = FLAT_LR[role]
    if step >= FINAL_SCHEDULE_STEPS:
        return 0.0
    cooled = POWER_C[role] * (FINAL_SCHEDULE_STEPS - step) ** FINAL_LR_POWER
    return min(flat, cooled)


def should_stop(step: int) -> bool:
    """Horizon decoupling (§15.4): the schedule is computed for `t_end` but the run STOPS earlier.

    Harvest the trajectory while LR is still ~1.8% of flat; stop too early (<~2885) and loss hasn't
    crossed, let it fully anneal (stop=t_end) and you waste ~85 steps at near-zero LR.
    """
    return step >= FINAL_TRAIN_STEPS


def validation_steps(stop: int = FINAL_TRAIN_STEPS, coarse: int = 125,
                     dense_from: int = 2820, dense_every: int = 5) -> list[int]:
    """Validation cadence: coarse every 125 steps, DENSE every ~5-10 from ~2820 onward (C02, §8.3).

    Dense late validation de-quantizes `step_to_3_28`: once the recipe is known to cross ~2890, fine
    validation locates the FIRST sub-3.28 step (2885) instead of rounding up to the next 125-mark.
    Part of the train-steps 'gain' is this measurement effect (the rest is real over-training removal).
    """
    pts = list(range(coarse, dense_from, coarse))
    pts += list(range(dense_from, stop + 1, dense_every))
    return sorted(set(pts))


def trim_train_steps(baseline: int = 3500, target: int = 2900) -> int:
    """The largest single 'free' lever (C02, §2.A.1): shorten the horizon (and steepen the cooldown).

    Reaches 3.28 earlier with no loss in val quality at the target, down to a hard floor (forcing a
    validation at 3425 misses; 3450 hits). Strong runs encode this as `tsXXXX` tokens in their names.
    """
    return target if target < baseline else baseline
