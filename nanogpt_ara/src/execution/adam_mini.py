# Adam-mini optimizer1 (AdamMiniW) — the C02 optimizer1 replacement on the embed/head/1D groups.
#
# Grounding: transcribed
#   (v1/codex/scratchpad/variants/train_gpt_simple_normuon_b090to080_mlpprojlr124375_adamminiopt1_
#    muon2fhidden_b2p095_eps1e3_tailresrmsstack_aggmom3hidden_h3375_stop3250_seed0.py:317-355)
# Same run named by C02's Proof: (the N51 Muon2F stepping stone). Adam-mini also descends from the
# earlier adammini-only stop3296 run (trace N13) whose .py snapshot + log also exist.
#
# Wave: v1  |  Crystallized by: logic/claims.md C02 (supported, depends on C01).
# See logic/concepts.md "AdamW baseline / per-group optimizer split" (Adam-mini replaces AdamW here).
#
# KERNEL MODE: the optimizer class + its typed I/O signature only.

import torch


class AdamMiniW(torch.optim.Optimizer):
    """Adam-mini with decoupled weight decay: a memory-light AdamW whose second moment is shared
    per-row (2D params) or per-tensor (1D params) instead of per-element.

    The ONE difference from AdamW: exp_avg_sq is reduced over the row dimension for 2D params
    (`grad_sq.mean(dim=1)` -> one value per output row) and over the whole tensor for ndim<2 params
    (`grad_sq.mean()` -> one scalar). The numerator (bias-corrected first moment) and the
    p.addcdiv_ update are standard AdamW. It is the one non-NorMuon optimizer signal that survived
    the broad optimizer-replacement washout (trace N15/N22; staging O04/O07).

    I/O signature:
        params : list[dict]   per-group param dicts, each with its own `lr` (recipe groups below)
        betas  : tuple(float, float)   (0.8, 0.95) at the frontier
        eps    : float        1e-10
        weight_decay : float  0.0 on these groups
        .step() -> None       (in-place AdamW-with-shared-second-moment update)

    Recipe groups (C02 optimizer1, transcribed from the same script :419-422):
        embed.weight                 lr = 0.3
        proj.weight (output head)    lr = 1/320
        all params with ndim < 2     lr = 0.01
    (As-committed literals; pinned in src/configs/. NOTE: optimizer1 owns embed/head/1D only — the
    2D hidden block weights go to NorMuon (normuon.py), never to Adam-mini.)
    """
    def __init__(self, params, betas=(0.8, 0.95), eps=1e-10, weight_decay=0.0):
        defaults = dict(betas=betas, eps=eps, weight_decay=weight_decay)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            beta1, beta2 = group["betas"]
            lr = group["lr"]
            eps = group["eps"]
            weight_decay = group["weight_decay"]
            for p in group["params"]:
                if p.grad is None:
                    continue
                grad = p.grad
                state = self.state[p]
                if len(state) == 0:
                    state["step"] = 0
                    state["exp_avg"] = torch.zeros_like(p)
                    if p.ndim == 2:
                        state["exp_avg_sq"] = torch.zeros(p.shape[0], device=p.device, dtype=torch.float32)
                    else:
                        state["exp_avg_sq"] = torch.zeros((), device=p.device, dtype=torch.float32)
                state["step"] += 1
                exp_avg = state["exp_avg"]
                exp_avg_sq = state["exp_avg_sq"]
                exp_avg.lerp_(grad, 1 - beta1)
                grad_sq = grad.float().square()
                if p.ndim == 2:
                    exp_avg_sq.lerp_(grad_sq.mean(dim=1), 1 - beta2)
                    denom = (exp_avg_sq / (1 - beta2 ** state["step"])).sqrt().unsqueeze(1).add_(eps)
                else:
                    exp_avg_sq.lerp_(grad_sq.mean(), 1 - beta2)
                    denom = (exp_avg_sq / (1 - beta2 ** state["step"])).sqrt().add_(eps)
                if weight_decay != 0:
                    p.mul_(1 - lr * weight_decay)
                update = exp_avg / (1 - beta1 ** state["step"])
                p.addcdiv_(update, denom.to(dtype=update.dtype), value=-lr)
