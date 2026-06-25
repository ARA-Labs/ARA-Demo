"""Search-discipline diagnostics: seed-significance sizing, miss-rate, early-kill divergence test.

These sit OUTSIDE the optimizer recipe — they govern how claims are validated and how bad runs are
pruned. Backs C09 (noise floor), C11 (divergence taxonomy / early kill), C17 (seeds for significance).
Grounded in INSIGHTS.md §9, §11, §21.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import ceil


# Measured noise floor (§9, §21): within-config std of step_to_3_28 at densely-validated frontier
# configs is ~14-21 steps; std of final_val_loss is ~0.0009-0.0011.
FRONTIER_STEP_STD: float = 15.0


def seeds_for_significance(delta_steps: float, sigma: float = FRONTIER_STEP_STD,
                           k_sigma: float = 2.0) -> int:
    """Seeds per arm to resolve a `delta_steps` gain at ~k_sigma (C17, §21): n ~ 8*sigma^2/Delta^2.

    With sigma ~15 steps: ~1 seed for 200 steps, 2-3 for 50, ~16 for 10, impractical below ~5.
    Below the step-quantization floor, prefer ranking on min_val_loss (continuous, std ~0.001).
    """
    if delta_steps <= 0:
        return 10 ** 9  # below the floor: step metric cannot resolve it
    n = 2.0 * (k_sigma ** 2) * (sigma ** 2) / (delta_steps ** 2)
    return max(1, ceil(n))


def miss_rate(step_to_target: list[float | None]) -> float:
    """Fraction of seeds that never reach the target (step_to_3_28 is None) (C09, §9.2).

    At the frontier this is ~9-12% (1/8 in group A; pooled 14/152 = 9%), so the single-best-seed
    record overstates by ~30-50 steps. Report median + miss-rate, not best-of-N.
    """
    if not step_to_target:
        return 0.0
    misses = sum(1 for s in step_to_target if s is None)
    return misses / len(step_to_target)


@dataclass
class DivergenceVerdict:
    mode: str       # "A_slow_stuck" | "B_spike_recover" | "C_nan_no_learn" | "ok"
    kill: bool
    reason: str


def classify_divergence(val_curve: dict[int, float], nan_count: int,
                        baseline_at: dict[int, float], kill_margin: float = 0.25) -> DivergenceVerdict:
    """Early-kill divergence test (C11, §11): all three modes are visible by step ~750.

    Mode A slow-and-stuck  : monotone but far above baseline (mis-scaled preconditioner; KL-Shampoo).
    Mode B spike-and-recover: clean descent, a mid-training spike up, incomplete recovery (bad HP eps).
    Mode C NaN/no-learn    : never learns, NaN/Inf log lines (normalization x warmup interaction).
    Kill once val exceeds baseline by `kill_margin` at a checkpoint (e.g. +0.29 at step 2000 for SPM).
    """
    if nan_count > 0:
        return DivergenceVerdict("C_nan_no_learn", True, f"{nan_count} NaN/Inf lines")
    steps = sorted(val_curve)
    # spike: a later checkpoint is worse than an earlier one (non-monotone blow-up)
    for i in range(1, len(steps)):
        if val_curve[steps[i]] > val_curve[steps[i - 1]] + 0.5:
            return DivergenceVerdict("B_spike_recover", True,
                                     f"spike {val_curve[steps[i-1]]:.2f}->{val_curve[steps[i]]:.2f}")
    # slow-and-stuck: monotone but well above baseline at a shared checkpoint
    for s in steps:
        if s in baseline_at and val_curve[s] > baseline_at[s] + kill_margin:
            return DivergenceVerdict("A_slow_stuck", True,
                                     f"+{val_curve[s] - baseline_at[s]:.2f} vs baseline @ {s}")
    return DivergenceVerdict("ok", False, "within margin")
