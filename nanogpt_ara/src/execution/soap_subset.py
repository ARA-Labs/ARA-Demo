"""SOAP-on-subset preconditioner + trust_gate — the biggest hitting v3 lever (C05, C13).

Grounded in cc_v3/07070-v88-aurora-proj-s2/launched_script.py (lines ~375-565, decoded in §16).
SOAP = Adam in the gradient-covariance eigenbasis (Shampoo factors), but applied ONLY to the
matrices where Muon's orthogonalization leaves curvature on the table (MLP fc/proj + attention V),
amortized (basis every 10 steps), Frobenius-norm-preserving, and gated against its own stale basis.

Same operator helps (MLP+V) or hurts (full model / Q/K) depending on the parameter subset — the
param-subset-dependence of C05. Backs C05 and C13.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import torch
from torch import Tensor


def should_soap_param(name: str, mode: str = "mlp_plus_v") -> bool:
    """Select the SOAP subset (§16.2). `mlp_plus_v` = MLP fc/proj + attention value projection.

    NOT Q/K: those are 'geometric' matrices that want to stay well-conditioned, which is exactly
    what Muon's NS gives — SOAP there duplicates/erodes Muon's work (full-model SOAP -> ~3.39).
    """
    if mode == "full":
        return name.endswith(".weight")
    is_mlp = ("mlp" in name) or (".fc" in name) or ("proj" in name and "attn" not in name)
    is_value = ("attn" in name) and (".v" in name or "value" in name)
    return is_mlp or is_value


@dataclass
class SoapState:
    """Per-parameter SOAP buffers."""
    row_gg: Tensor  # EMA of g g^T   (left Shampoo factor)
    col_gg: Tensor  # EMA of g^T g   (right Shampoo factor)
    q_row: Tensor   # cached row eigenbasis (refreshed every `freq` steps)
    q_col: Tensor   # cached col eigenbasis
    exp_avg_sq: Tensor  # Adam 2nd moment IN the eigenbasis


def soap_update_preconditioner(update: Tensor, st: SoapState, step: int,
                               beta2: float = 0.90, freq: int = 10) -> SoapState:
    """Update Gram EMAs every step (cheap); refresh the eigenbasis via QR every `freq` steps.

    The covariance drifts slowly, so a stale-by-<=10-steps basis is a fine approximation — this
    amortization (§16.3) is what makes SOAP's +~22% per-step cost tolerable rather than prohibitive.
    """
    st.row_gg = beta2 * st.row_gg + (1 - beta2) * (update @ update.mT)
    st.col_gg = beta2 * st.col_gg + (1 - beta2) * (update.mT @ update)
    if step % freq == 0:
        st.q_row = torch.linalg.qr(st.row_gg).Q
        st.q_col = torch.linalg.qr(st.col_gg).Q
    return st


def soap_precondition_momentum(update: Tensor, st: SoapState,
                               beta2: float = 0.90, denom_power: float = 0.50) -> Tensor:
    """Project into the eigenbasis, Adam-normalize in-basis, project back, preserve Frobenius norm.

    Keeps the per-direction curvature scaling Muon's orthogonalization throws away (C05/§16.1):
    persistently high-curvature directions get damped, flat directions amplified. The final
    norm-match means SOAP changes the update's SHAPE within the matrix, not its magnitude, so it
    composes on top of the Muon-normalized pipeline instead of fighting it.
    """
    projected = st.q_row.mT @ update @ st.q_col
    st.exp_avg_sq = beta2 * st.exp_avg_sq + (1 - beta2) * projected.pow(2)
    denom = st.exp_avg_sq.pow(denom_power) + 1e-12
    precond = st.q_row @ (projected / denom) @ st.q_col.mT
    return precond * (update.norm() / (precond.norm() + 1e-12))  # norm-preserve


def trust_gate(raw: Tensor, soap: Tensor, grad: Tensor,
               cos_floor: float = 0.20, early_trust_floor: float = 0.0) -> Tensor:
    """Stale-basis safety net (C14, §17.2): accept the SOAP update per-element only when trusted.

    Trust SOAP only when it (a) agrees with raw momentum (cos > cos_floor) AND (b) is at least as
    gradient-aligned as raw momentum; else fall back to plain Muon. `early_trust_floor` (=0.45,
    fading 1375->1625) forces SOAP-trust while early gradients are too noisy to measure cosines.
    The amortization saves compute; the gate pays a tiny per-step cost to catch the misleading cases.
    """
    def _cos(a: Tensor, b: Tensor) -> Tensor:
        return (a * b).sum(dim=1, keepdim=True) / (a.norm(dim=1, keepdim=True)
                                                   * b.norm(dim=1, keepdim=True) + 1e-12)
    agree = _cos(raw, soap)
    soap_galign = _cos(soap, grad)
    raw_galign = _cos(raw, grad)
    trusted = (agree > cos_floor) & (soap_galign >= raw_galign)
    trusted = trusted | (torch.full_like(agree, early_trust_floor) > 0.0)  # early floor forces trust
    return torch.where(trusted, soap, raw)


def soap_subset_update(update: Tensor, grad: Tensor, name: str, st: SoapState, step: int,
                       v_blend: float = 0.95) -> Tensor:
    """End-to-end SOAP-on-subset step for one param, with the trust gate and the V-specific blend."""
    if not should_soap_param(name):
        return update
    st = soap_update_preconditioner(update, st, step)
    soap = soap_precondition_momentum(update, st)
    gated = trust_gate(update, soap, grad)
    if ("attn" in name) and (".v" in name or "value" in name):
        gated = v_blend * gated + (1 - v_blend) * update  # V dialed down (more curvature-sensitive)
    return gated
