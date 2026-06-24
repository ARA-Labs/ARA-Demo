# NorMuon — normalized-Muon hidden-matrix optimizer (the C01 core module).
#
# Grounding: transcribed
#   (v1/codex/scratchpad/runs/normuon-b090to080-mlpprojlr124375-tailresrmsstack-
#    aggmom3hidden-h3375-stop3296-seed0.log:168-258)   # NS5 + normuon_update + NorMuon class
# The cited file is the log-embedded launched_script.py snapshot of the EXACT run C01's Proof:
# names (the script self-logs its own source at the top of each result log; the `====` separator
# at line 493 ends the code region). The identical core also appears in the C01 stop3345 variant
# v1/codex/scratchpad/variants/train_gpt_simple_normuon_b090to082_mlpprojlr125_h3375_stop3345_seed0.py:168-225.
#
# Wave: v1  |  Crystallized by: logic/claims.md C01 (supported) — "NorMuon under a decoupled WSD
# horizon/early-stop schedule reaches val 3.28 in fewer than the 3500-step Muon baseline".
# See logic/concepts.md "Muon" / "Newton–Schulz orthogonalization (NS5)" for the conceptual layer.
#
# KERNEL MODE: this is the core optimizer module + its typed I/O signature, NOT the full ~373-600
# line training script. The frozen GPT model, dataloader, training loop, and distributed setup are
# the FROZEN benchmark (src/environment.md), not part of the discovered recipe, and are omitted.

from torch import Tensor
import torch
import torch.distributed as dist


def zeropower_via_newtonschulz5(G: Tensor) -> Tensor:
    """Approximate the orthogonal polar factor of G via 5th-order Newton-Schulz (NS5).

    I/O signature:
        G: Tensor, ndim >= 2 (a momentum/update matrix)
        -> Tensor, same shape as G, ~orthogonalized (spectral norm normalized to <= 1 first).

    Fixed quintic coefficients (a, b, c) = (2, -1.5, 0.5); 12 iterations in bfloat16; transposes
    when rows > cols so the iteration runs on the smaller dimension. "not optimizing for wallclock
    speed" (a per-step-slow, step-count-cheap routine — assumption A1, logic/solution/constraints.md).
    """
    assert G.ndim >= 2
    X = G.bfloat16()
    if G.size(-2) > G.size(-1):
        X = X.mT

    # Ensure spectral norm is at most 1
    X = X / (X.norm(dim=(-2, -1), keepdim=True) + 1e-7)
    # Perform the NS iterations, not optimizing for wallclock speed
    a, b, c = 2, -1.5, 0.5
    for _ in range(12):
        A = X @ X.mT
        B = b * A + c * A @ A
        X = a * X + B @ X

    if G.size(-2) > G.size(-1):
        X = X.mT
    return X


@torch.compile
def normuon_update(grad: Tensor, momentum: Tensor, second_moment: Tensor,
                   mu: float = 0.95, beta2: float = 0.95, eps: float = 1e-8,
                   nesterov: bool = True) -> Tensor:
    """The NorMuon update: Muon's orthogonalized direction + a ROW-WISE second-moment normalization.

    This is the single mechanism C01 is about. Over plain Muon, the orthogonalized update is divided
    by the sqrt of an EMA of per-row second moments (`row_second`), then rescaled back to the
    canonical Muon RMS — i.e. a normalized-Muon ("NorMuon").

    I/O signature:
        grad          : Tensor [rows, cols]      gradient of a 2D hidden weight (mutated in place)
        momentum      : Tensor [rows, cols]      Nesterov momentum buffer (state, mutated in place)
        second_moment : Tensor [rows]  (float32)  EMA of per-row update energy (state, mutated)
        mu, beta2, eps, nesterov : scalars
        -> update Tensor [rows, cols], to be applied as  p <- p*(1 - lr*wd) - lr*update.

    HPs at the C01 frontier: mu=0.95 (Nesterov), beta2 warmed down 0.90 -> 0.80/0.82 via the WSD
    schedule (see wsd_schedule.py), eps=1e-8. (Source HPs: the cited launched_script.py snapshot.)
    """
    momentum.lerp_(grad, 1 - mu)
    update = grad.lerp_(momentum, mu) if nesterov else momentum
    update = zeropower_via_newtonschulz5(update)
    canonical_update = update * max(1, grad.size(-2) / grad.size(-1))**0.5
    target_rms = canonical_update.norm(dim=(-2, -1), keepdim=True) / (canonical_update.numel()**0.5)
    row_second = update.square().mean(dim=-1).float()
    second_moment.lerp_(row_second, 1 - beta2)
    update = update / (second_moment.sqrt().unsqueeze(-1) + eps)
    update *= target_rms / (update.norm(dim=(-2, -1), keepdim=True) / (update.numel()**0.5) + eps)
    return update


class NorMuon(torch.optim.Optimizer):
    """Distributed NorMuon optimizer over 2D hidden block weights (Muon's role in the recipe).

    I/O signature:
        params : list[nn.Parameter]   2D weights (ndim >= 2), e.g. block attn/mlp matrices
        lr, weight_decay, mu, beta2, eps : scalars
        .step() -> None   (in-place param update + dist.all_gather of updated params across the world)

    The benchmark applies NorMuon to the hidden 2D block weights only; embeddings, the output
    projection, and all ndim<2 params go to optimizer1 (AdamW / Adam-mini). The recipe splits the
    hidden matrices into two NorMuon instances: optimizer2 over `other_hidden_params`
    (lr=0.030, wd=0.0125, beta2=0.90) and optimizer3 over the MLP-proj group `mlp_proj_params`
    (lr=0.0373125, wd=0.0100, beta2=0.90). (Source HPs: the cited launched_script.py snapshot;
    see configs/normuon_v1_stop3296.py.)

    NOTE (wave scoping): this transcription keeps ONLY the plain-NorMuon dispatch path. The C01
    stop3296 headline run additionally toggles `aggmo3` (hidden) and `error_feedback` (MLP-proj)
    group flags; those modifier update-rules are transcribed in muon2f_hidden.py / and are part of
    the C02 stack. The dispatch shown here is the base path normuon_update.
    """
    def __init__(self, params, lr=0.02, weight_decay=0, mu=0.95, beta2=0.95, eps=1e-8):
        assert isinstance(params, list) and len(params) >= 1 and isinstance(params[0], torch.nn.Parameter)
        params = sorted(params, key=lambda x: x.size(), reverse=True)
        defaults = dict(lr=lr, weight_decay=weight_decay, mu=mu, beta2=beta2, eps=eps)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self):
        world_size = dist.get_world_size()
        rank = dist.get_rank()
        for group in self.param_groups:
            params = group["params"]
            params_pad = params + [torch.empty_like(params[-1])] * (world_size - len(params) % world_size)
            for base_i in range(0, len(params), world_size):
                if base_i + rank < len(params):
                    p = params[base_i + rank]
                    state = self.state[p]
                    if len(state) == 0:
                        state["momentum"] = torch.zeros_like(p)
                        state["second_moment"] = torch.zeros_like(p[..., 0], dtype=torch.float32)
                    update = normuon_update(p.grad, state["momentum"], state["second_moment"],
                                            mu=group["mu"], beta2=group["beta2"], eps=group["eps"])
                    p.mul_(1 - group["lr"] * group["weight_decay"])
                    p.add_(update, alpha=-group["lr"])
                dist.all_gather(params_pad[base_i:base_i + world_size], params_pad[base_i + rank])
