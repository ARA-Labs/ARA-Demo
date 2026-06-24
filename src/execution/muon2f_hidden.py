# Muon2F-hidden update + hidden AggMo-3 momentum (a C02 core module).
#
# Grounding: transcribed
#   (v1/codex/scratchpad/variants/train_gpt_simple_normuon_b090to080_mlpprojlr124375_adamminiopt1_
#    muon2fhidden_b2p095_eps1e3_tailresrmsstack_aggmom3hidden_h3375_stop3250_seed0.py:200-238)
# This is the exact run named by C02's Proof: (the N51 3-seed Muon2F-hidden stepping stone at
# stop3250: seed0 3.27945, seed1 3.27965, seed2 3.27897).
#
# Wave: v1  |  Crystallized by: logic/claims.md C02 (supported, depends on C01).
# See logic/concepts.md "Muon2F (hidden-matrix orthogonalized update variant)".
#
# KERNEL MODE: the two hidden-matrix update rules + typed I/O signatures only. They are dispatched
# from the same NorMuon.step() loop (see normuon.py) via the per-group flags aggmo3 / muon2f; the
# dispatch wiring is shown in the NOTE at the bottom, not duplicated as a full class.

from torch import Tensor
import torch

from normuon import zeropower_via_newtonschulz5  # NS5, transcribed in normuon.py


@torch.compile
def normuon_update_aggmo3(grad: Tensor, momentum0: Tensor, momentum1: Tensor, momentum2: Tensor,
                          second_moment: Tensor, beta2: float = 0.95, eps: float = 1e-8) -> Tensor:
    """NorMuon update with AGGREGATED-momentum (AggMo-3): three momentum buffers at different decays.

    Replaces the single Nesterov buffer with the mean of three EMAs (lerp rates 0.15 / 0.05 / 0.01),
    orthogonalized by NS5 then row-normalized exactly like the base normuon_update.

    I/O signature:
        grad                       : Tensor [rows, cols]   (mutated via the momentum lerps)
        momentum0/1/2              : Tensor [rows, cols]   three momentum buffers (state, in place)
        second_moment             : Tensor [rows] float32  per-row second-moment EMA (state, in place)
        beta2, eps                : scalars
        -> update Tensor [rows, cols]
    """
    momentum0.lerp_(grad, 0.15)
    momentum1.lerp_(grad, 0.05)
    momentum2.lerp_(grad, 0.01)
    update = (momentum0 + momentum1 + momentum2) * (1.0 / 3.0)
    update = zeropower_via_newtonschulz5(update)
    canonical_update = update * max(1, grad.size(-2) / grad.size(-1))**0.5
    target_rms = canonical_update.norm(dim=(-2, -1), keepdim=True) / (canonical_update.numel()**0.5)
    row_second = update.square().mean(dim=-1).float()
    second_moment.lerp_(row_second, 1 - beta2)
    update = update / (second_moment.sqrt().unsqueeze(-1) + eps)
    update *= target_rms / (update.norm(dim=(-2, -1), keepdim=True) / (update.numel()**0.5) + eps)
    return update


@torch.compile
def normuon_update_aggmo3_2f(grad: Tensor, momentum0: Tensor, momentum1: Tensor, momentum2: Tensor,
                             second_moment: Tensor, row_pre: Tensor, col_pre: Tensor,
                             beta2: float = 0.95, eps: float = 1e-8,
                             beta_pre: float = 0.95, pre_eps: float = 1e-3) -> Tensor:
    """Muon2F-hidden: AggMo-3 momentum + a ROW/COLUMN gradient-covariance PRE-conditioner before NS5.

    The "2F" modifier: before orthogonalizing, the aggregated update is scaled by a separable
    row-/col- second-moment preconditioner (EMAs `row_pre`, `col_pre` of grad^2 means), each
    normalized by its own mean. The post-NS update is then RMS-matched to the *parent* (un-pre-
    conditioned) orthogonalized update so the step magnitude is unchanged — only the direction is
    re-conditioned. This is the FIRST matrix-side preconditioning found to help this corridor
    (APOLLO / OLion / DION all washed out — staging O15; trace N38/N46/N52).

    I/O signature:
        grad                  : Tensor [rows, cols]
        momentum0/1/2         : Tensor [rows, cols]      AggMo-3 buffers (state, in place)
        second_moment         : Tensor [rows] float32    per-row second-moment EMA (state, in place)
        row_pre               : Tensor [rows] float32    row gradient-covariance EMA (state, in place)
        col_pre               : Tensor [cols] float32    col gradient-covariance EMA (state, in place)
        beta2, eps, beta_pre, pre_eps : scalars   (frontier: beta_pre=0.95, pre_eps=1e-3 == "eps1e3")
        -> update Tensor [rows, cols]
    """
    momentum0.lerp_(grad, 0.15)
    momentum1.lerp_(grad, 0.05)
    momentum2.lerp_(grad, 0.01)
    raw_update = (momentum0 + momentum1 + momentum2) * (1.0 / 3.0)
    g2 = grad.square().float()
    row_pre.lerp_(g2.mean(dim=-1), 1 - beta_pre)
    col_pre.lerp_(g2.mean(dim=-2), 1 - beta_pre)
    row_scale = row_pre / (row_pre.mean() + pre_eps)
    col_scale = col_pre / (col_pre.mean() + pre_eps)
    precond = raw_update / ((row_scale.unsqueeze(-1) * col_scale.unsqueeze(-2) + pre_eps).sqrt().to(raw_update.dtype))
    update = zeropower_via_newtonschulz5(precond)
    parent_update = zeropower_via_newtonschulz5(raw_update)
    parent_canonical = parent_update * max(1, grad.size(-2) / grad.size(-1))**0.5
    target_rms = parent_canonical.norm(dim=(-2, -1), keepdim=True) / (parent_canonical.numel()**0.5)
    row_second = update.square().mean(dim=-1).float()
    second_moment.lerp_(row_second, 1 - beta2)
    update = update / (second_moment.sqrt().unsqueeze(-1) + eps)
    update *= target_rms / (update.norm(dim=(-2, -1), keepdim=True) / (update.numel()**0.5) + eps)
    return update


# NOTE — dispatch wiring (transcribed from the same script, NorMuon.step() at :291-301):
# Inside NorMuon.step(), per the group flags set on optimizer2 (the hidden group):
#     group["aggmo3"] = True; group["muon2f"] = True; group["beta_pre"] = 0.95; group["pre_eps"] = 1e-3
# the state is initialized with momentum0/1/2 + row_pre + col_pre, and the update dispatches to
# normuon_update_aggmo3_2f(...). With aggmo3=True but muon2f=False it dispatches to
# normuon_update_aggmo3(...). This is the stack-level, optimizer2-only change C02/Muon2F describes
# (optimizer1 and optimizer3 logic intact; GPT.forward byte-identical).
