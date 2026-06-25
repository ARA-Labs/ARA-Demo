"""Muon update pipeline — the frontier levers layered on the orthogonalized-momentum core.

Implements the NOVEL contributions of the v3 recipe (INSIGHTS.md §2, §5, §16, §17), as typed,
boilerplate-free stubs grounded in cc_v3/07070-v88-aurora-proj-s2/launched_script.py:

  Nesterov momentum -> MuonEq pre-NS row-norm -> Newton-Schulz / soft-Muon -> Aurora row-rescale
  -> Contra-Muon early decorrelation -> (SOAP-on-subset; see soap_subset.py) -> shape scale -> step.

Backs claims C03 (MuonEq), C04 (normalization buys LR), C08/C14 (Contra-Muon, soft-Muon curriculum).
"""
from __future__ import annotations
import torch
from torch import Tensor


def mu_schedule(step: int, warmup_end: int = 300, cool_start: int = 2850,
                cool_end: int = 2900, lo: float = 0.85, hi: float = 0.95) -> float:
    """Momentum schedule mu: 0.85 ->0.95 over warmup, hold, ->0.85 at the end (§2.B.1, §17).

    Lower mu early = fresher gradients while the landscape changes fast; higher mu mid-run =
    smoother averaging; lower mu at the end = less stale momentum fighting the LR cooldown.
    """
    if step <= warmup_end:
        return lo + (hi - lo) * (step / max(1, warmup_end))
    if step >= cool_end:
        return lo
    if step >= cool_start:
        return hi + (lo - hi) * ((step - cool_start) / max(1, cool_end - cool_start))
    return hi


def nesterov_momentum(grad: Tensor, buf: Tensor, mu: float) -> tuple[Tensor, Tensor]:
    """Update the momentum buffer and return the Nesterov lookahead direction `g + mu*buf`."""
    buf = buf.mul_(mu).add_(grad)
    return grad.add(buf, alpha=mu), buf


def muoneq_row_norm(m: Tensor, eps: float = 1e-7) -> Tensor:
    """MuonEq: per-row L2-normalize the momentum BEFORE Newton-Schulz (C03, §2.B.3).

    Equalizes per-row scale so NS sees a better-conditioned input; the single strongest
    Muon-internal lever (3-seed dval -0.00484). Distinct from NorMuon, which divides AFTER NS.
    """
    return m / (m.norm(dim=1, keepdim=True) + eps)


def newton_schulz(g: Tensor, steps: int = 5,
                  coeffs: tuple[float, float, float] = (2.0, -1.5, 0.5)) -> Tensor:
    """Newton-Schulz orthogonalization: push singular values of `g` toward 1 without an SVD.

    Baseline = 12 iters with (2,-1.5,0.5); Polar-Express = ~5 iters with tuned per-iter coeffs
    (§2.B.2). `coeffs` here is a single triple for brevity; the real recipe varies it per iter.
    """
    x = g / (g.norm() + 1e-7)
    a, b, c = coeffs
    for _ in range(steps):
        gg = x @ x.mT
        x = a * x + b * (gg @ x) + c * (gg @ gg @ x)
    return x


def soft_via_newton_schulz(g: Tensor, p: float = 0.1, steps: int = 5) -> Tensor:
    """soft-Muon: raise singular values to a small power `p` instead of forcing them to 1 (§17.3).

    Used only in the endgame (blended in over steps 2400-2890) so updates keep more natural
    magnitude structure for gentle fine-tuning. Mechanism partly [HYP].
    """
    # Stub: orthogonalize then re-inject a softened spectrum. Real code blends NS variants.
    o = newton_schulz(g, steps=steps)
    return o * (g.norm() ** p)  # placeholder for the spectrum-softening blend


def aurora_row_rescale(x: Tensor, row_state: Tensor, beta: float = 0.25) -> tuple[Tensor, Tensor]:
    """Aurora: per-row magnitude EMA rescale interleaved with NS (C04, §5.2).

    Clamps per-neuron update variance, which is what makes the larger global LR (0.0375) stable.
    Renders post-NS NorMuon redundant (same mechanism).
    """
    row_mag = x.norm(dim=1, keepdim=True)
    row_state = beta * row_state + (1 - beta) * row_mag
    return x / (row_state + 1e-7), row_state


def _linear_ramp(step: int, start_val: float, end_val: float,
                 start_step: int = 0, end_step: int = 1) -> float:
    """Linear ramp from start_val to end_val over [start_step, end_step], clamped outside."""
    if step <= start_step:
        return start_val
    if step >= end_step:
        return end_val
    frac = (step - start_step) / max(1, end_step - start_step)
    return start_val + (end_val - start_val) * frac


def contra_muon_term(ortho_update: Tensor, grad: Tensor, step: int,
                     start_coeff: float = -0.2, end_step: int = 1920) -> Tensor:
    """Contra-Muon: add a ramping fraction of the unit-norm raw gradient (C08, C14, §16.4).

    contra_coeff ramps -0.2 -> 0 by `end_step`. Early training subtracts a slice of the greedy
    gradient direction from the orthogonalized update (decorrelation/exploration), then anneals to
    pure Muon — the engineered cause of the lose-early/win-late crossover (~step 1750).
    """
    coeff = _linear_ramp(step, start_coeff, 0.0, end_step=end_step)
    g_unit = grad / (grad.norm() + 1e-7)  # unit operator-norm raw gradient (op-norm in real code)
    return ortho_update + coeff * g_unit


def muon_update(grad: Tensor, buf: Tensor, row_state: Tensor, step: int,
                rows: int, cols: int, soft_blend_ceiling: float = 0.80) -> tuple[Tensor, Tensor, Tensor]:
    """Full Muon update for one 2-D weight: the temporal-curriculum pipeline (C14, §17).

    Explore (early): mu warmup, hard NS, Contra-Muon decorrelation.
    Soften (late):   soft-Muon blends in over 2400-2890, power cooldown steepens.
    Returns (update, momentum_buffer, aurora_row_state). SOAP-on-subset (soap_subset.py) is applied
    by the caller between the contra term and the shape scale, only for MLP+V params.
    """
    nag, buf = nesterov_momentum(grad, buf, mu_schedule(step))
    m = muoneq_row_norm(nag)                                  # C03
    hard = newton_schulz(m)
    soft = soft_via_newton_schulz(m)                         # C14
    soft_blend = _linear_ramp(step, 0.0, soft_blend_ceiling, start_step=2400, end_step=2890)
    o = (1 - soft_blend) * hard + soft_blend * soft
    o, row_state = aurora_row_rescale(o, row_state)          # C04
    o = contra_muon_term(o, grad, step)                      # C08
    update = o * (max(1.0, rows / cols) ** 0.5)              # shape-aware scale
    return update, buf, row_state
