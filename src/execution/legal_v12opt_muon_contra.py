# legal-v12opt Muon core — contra-Muon direction + Polar-Express NS5 + role-split groups +
# lookahead + mu-schedule (the C04 core module, ARCHITECTURE-COMPLIANT).
#
# Grounding: transcribed
#   (v2/codex/scratchpad/variants/legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py)
#     - zeropower_via_newtonschulz5 + _POLAR_EXPRESS_COEFFS : lines 163-185
#     - _CONTRA_MUON + muon_update (the cm0225 contra-direction)        : lines 187-211
#     - Muon optimizer class (+ lookahead slow-weight pull)             : lines 213-252
#     - role-split (rolewd/rolelr2) group construction (attn0625)       : lines 320-369
#     - mu-schedule + eta-floor LR schedule + lookahead wiring          : lines 377-419
# This is the indexed `variant:` source that each C04 proof run's `indexed_run` line names
# (e.g. runs/legal-v12opt-rolewd-rolelr2-lookahead-ts3037-cm0225-attn0625-sig-r1.log:
#  "variant": ".../variants/legal_v12opt_rolewd_rolelr2_lookahead_ts3037_cm0225_attn0625.py").
# The run also self-logs this exact source at the top of its worktree logs/<uuid>.txt
# (print0(code) + "="*100), so the variant file IS the executed-code snapshot (N78 verified
# "each indexed source_log begins with the exact ...py source").
#
# Wave: v2  |  Crystallized by: logic/claims.md C04 (supported, depends on C05) — "On an
# architecture-COMPLIANT (byte-identical forward/norm) v12-optimizer base, the
# rolewd-rolelr2-lookahead-cm0225-attn0625 stack reaches val 3.28 at step_to_3.28 = 3037,
# statistically verified (n=8 cohort gate)."
# Compliance premise: logic/claims.md C05 (the cc-v12 base VIOLATES the no-forward/no-norm rule;
# only byte-identical-Architecture variants are submittable) — enforced by
# src/execution/launch_variant_gate.sh.
#
# KERNEL MODE: this is the discovered OPTIMIZER + INIT/OPTIM core only (the part C04 is about:
# Optimization + Init & Optim Hyperparams). The FROZEN benchmark — the GPT model, RMSNorm/q-k-norm
# forward path, dataloader, training loop, distributed setup — is src/environment.md and is NOT part
# of the recipe; it is omitted here. CRITICAL (C05): on the compliant base the model's RMSNorm.forward
# is the BASELINE `F.rms_norm(x, (x.size(-1),), weight=self.gains.type_as(x))` and q/k norm is the
# BASELINE `F.rms_norm(q, ...), F.rms_norm(k, ...)` (variant lines 65 / 107) — NOT the cc-v12
# `(norm(x.float())*self.gains).type_as(x)` / `q,k = norm(q),norm(k)` forward-path change.

from torch import Tensor
import torch
import torch.distributed as dist


# Polar-Express quintic coefficients (per-iteration (a, b, c)); 5 iterations, replacing the v1
# fixed-(2,-1.5,0.5) NS5 of normuon.py. [literal coeffs from the variant; see configs for HP pins]
_POLAR_EXPRESS_COEFFS = [
    (8.156554524902461, -22.48329292557795, 15.878769915207462),
    (4.042929935166739, -2.808917465908714, 0.5000178451051316),
    (3.8916678022926607, -2.772484153217685, 0.5060648178503393),
    (3.285753657755655, -2.3681294933425376, 0.46449024233003106),
    (2.3465413258596377, -1.7097828382687081, 0.42323551169305323),
]


def zeropower_via_newtonschulz5(G: Tensor) -> Tensor:
    """Approximate the orthogonal polar factor of G via the Polar-Express coefficient schedule.

    I/O signature:
        G: Tensor, ndim >= 2 (a momentum/update matrix)
        -> Tensor, same shape as G, ~orthogonalized (spectral norm normalized to <= 1 first).

    Differs from the v1 NS5 (src/execution/normuon.py) only in the iteration: a per-iteration
    coefficient tuple from `_POLAR_EXPRESS_COEFFS` (5 steps) rather than a fixed (2, -1.5, 0.5) x12,
    and a (1 + 2e-2) spectral-norm pad with eps 1e-6. Transposes when rows > cols.
    """
    assert G.ndim >= 2
    X = G.bfloat16()
    if G.size(-2) > G.size(-1):
        X = X.mT
    X = X / (X.norm(dim=(-2, -1), keepdim=True) * (1 + 2e-2) + 1e-6)
    for a, b, c in _POLAR_EXPRESS_COEFFS:
        A = X @ X.mT
        B = b * A + c * A @ A
        X = a * X + B @ X
    if G.size(-2) > G.size(-1):
        X = X.mT
    return X


# Contra-Muon strength (the "cm0225" lever in the recipe slug). [literal: variant line 187]
_CONTRA_MUON = 0.225


@torch.compile
def muon_update(grad: Tensor, momentum: Tensor, mu: float = 0.95, nesterov: bool = True) -> Tensor:
    """Muon update with row-pre-normalization + a CONTRA-Muon correction (the cm0225 mechanism).

    Over plain Muon, this (a) row-normalizes the (Nesterov) momentum before Newton-Schulz, then
    (b) subtracts `_CONTRA_MUON * 0.5` of the top-singular-direction component of the *pre-NS*
    update (estimated by 5 power-iteration steps for the leading singular pair), renormalizing the
    update's Frobenius norm back to the orthogonalized power. This is the single optimizer-geometry
    lever C04 names as `cm0225`; combined with role-split LR/WD (`rolewd`/`rolelr2`) and `lookahead`.

    I/O signature:
        grad     : Tensor [rows, cols]   gradient of a 2D hidden weight (mutated in place via lerp_)
        momentum : Tensor [rows, cols]   Nesterov momentum buffer (state, mutated in place)
        mu, nesterov : scalars
        -> update Tensor [rows, cols], applied as  p <- p*(1 - lr*wd) - lr*update.

    HPs at the C04 frontier: mu warmed 0.85->0.95 over 300 steps and cooled 0.95->0.85 over the last
    50 (the mu-schedule below); _CONTRA_MUON=0.225. (Source HPs: the cited variant; see
    src/configs/legal_v12opt_ts3037_v2.py.)
    """
    momentum.lerp_(grad, 1 - mu)
    update = grad.lerp_(momentum, mu) if nesterov else momentum
    row_norms = (update * update).sum(dim=-1, keepdim=True).sqrt() + 1e-8
    update = update / row_norms
    pre_ns = update.clone()
    update = zeropower_via_newtonschulz5(update)
    # 5-step power iteration for the leading singular pair of the pre-NS (row-normalized) update.
    X = pre_ns.float()
    v = torch.ones(X.size(-1), dtype=X.dtype, device=X.device)
    v = v / v.norm().clamp(min=1e-10)
    for _ in range(5):
        u_ = X @ v
        u_ = u_ / u_.norm().clamp(min=1e-10)
        v = X.mT @ u_
        v = v / v.norm().clamp(min=1e-10)
    op_norm = (X @ v).norm().clamp(min=1e-10)
    normalized_pre = pre_ns / op_norm.to(pre_ns.dtype)
    opower_F = update.norm()
    update = update - (_CONTRA_MUON * 0.5) * normalized_pre   # the contra-Muon correction (cm0225)
    update = update * (opower_F / update.norm().clamp(min=1e-10))
    update *= max(1, grad.size(-2) / grad.size(-1))**0.5
    return update


class Muon(torch.optim.Optimizer):
    """Distributed Muon over 2D hidden block weights, with an optional per-group LOOKAHEAD pull.

    I/O signature:
        params : list[nn.Parameter] | list[dict]   2D weights (ndim >= 2), or per-ROLE param groups
        lr, weight_decay, mu : scalars
        per-group keys set by the schedule each step: "mu", "current_step", and the lookahead keys
            "lookahead_start_step" / "lookahead_interval" / "lookahead_alpha" /
            "lookahead_pull" / "lookahead_ramp_steps"
        .step() -> None   (in-place param update + dist.all_gather across the world)

    LOOKAHEAD (the recipe's `lookahead` lever): once `current_step >= lookahead_start_step`, a slow
    weight clone tracks the fast weights; every `lookahead_interval` steps the slow weights move
    `lookahead_alpha` toward the fast weights and the fast weights are pulled `lookahead_pull` toward
    the slow weights, ramped in over `lookahead_ramp_steps` with a smoothstep. HPs at the C04
    frontier: start 2450, interval 25, alpha 0.35, pull 0.15, ramp 150 (see config).

    ROLE SPLIT (the recipe's `rolewd` + `rolelr2` levers): the benchmark passes SIX per-role groups
    — attn.q / attn.k / attn.v / attn.proj / mlp.fc / mlp.proj — each with its own LR multiplier and
    weight decay (constructed below), all off a base lr=0.045, weight_decay=0.030. Embeddings, the
    output projection, and all ndim<2 params go to optimizer1 (AdamW), not here.
    """
    def __init__(self, params, lr=0.02, weight_decay=0, mu=0.95):
        assert isinstance(params, list) and len(params) >= 1
        if isinstance(params[0], torch.nn.Parameter):
            params = sorted(params, key=lambda x: x.size(), reverse=True)
        else:
            for group in params:
                group["params"] = sorted(group["params"], key=lambda x: x.size(), reverse=True)
        defaults = dict(lr=lr, weight_decay=weight_decay, mu=mu)
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
                    update = muon_update(p.grad, state["momentum"], mu=group["mu"])
                    p.mul_(1 - group["lr"] * group["weight_decay"])
                    p.add_(update, alpha=-group["lr"])
                    current_step = group.get("current_step", 0)
                    lookahead_start = group.get("lookahead_start_step", None)
                    if lookahead_start is not None and current_step >= lookahead_start:
                        if "lookahead_slow" not in state:
                            state["lookahead_slow"] = p.clone()
                        elif (current_step - lookahead_start) % group["lookahead_interval"] == 0:
                            slow = state["lookahead_slow"]
                            slow.add_(p - slow, alpha=group["lookahead_alpha"])
                            ramp = (current_step - lookahead_start) / group["lookahead_ramp_steps"]
                            ramp = max(0.0, min(1.0, ramp))
                            smooth = ramp * ramp * (3.0 - 2.0 * ramp)
                            p.add_(slow - p, alpha=group["lookahead_pull"] * smooth)
                dist.all_gather(params_pad[base_i:base_i + world_size], params_pad[base_i + rank])


# ---- Role-split group construction (rolewd + rolelr2 + attn0625) ---------------------------------
# Typed builder for the six per-role Muon groups, off base lr=0.045 / weight_decay=0.030.
# Transcribed from the variant's Init & Optim Hyperparams block (lines 320-369). The per-role
# multipliers/decays are the discovered `rolewd`/`rolelr2` lever; attn.v's 0.62500 mult is the
# `attn0625` slug. Exact literals are pinned + annotated in src/configs/legal_v12opt_ts3037_v2.py.
#
# I/O signature:
#   model : nn.Module whose `.blocks` hold the per-role 2D weights (.attn.q/.k/.v/.proj, .mlp.fc/.proj)
#   -> list[dict]  ready to pass to Muon(...), one group per role.
_ATTN_Q_LR_MULT, _ATTN_K_LR_MULT = 0.61875, 0.61875
_ATTN_V_LR_MULT, _ATTN_PROJ_LR_MULT = 0.62500, 0.63750          # attn.v mult = the attn0625 slug
_MLP_FC_LR_MULT, _MLP_PROJ_LR_MULT = 1.01250, 0.98750
_ATTN_Q_WEIGHT_DECAY, _ATTN_K_WEIGHT_DECAY = 0.02775, 0.02775
_ATTN_V_WEIGHT_DECAY, _ATTN_PROJ_WEIGHT_DECAY = 0.02750, 0.02700
_MLP_FC_WEIGHT_DECAY, _MLP_PROJ_WEIGHT_DECAY = 0.03150, 0.03100


def build_role_split_muon_groups(model, base_lr: float = 0.045):
    """Return the six per-role Muon param groups (rolewd + rolelr2)."""
    def role(suffix):
        return [p for n, p in model.blocks.named_parameters() if p.ndim >= 2 and suffix in n]
    return [
        dict(params=role(".attn.q."),    lr=base_lr * _ATTN_Q_LR_MULT,    weight_decay=_ATTN_Q_WEIGHT_DECAY),
        dict(params=role(".attn.k."),    lr=base_lr * _ATTN_K_LR_MULT,    weight_decay=_ATTN_K_WEIGHT_DECAY),
        dict(params=role(".attn.v."),    lr=base_lr * _ATTN_V_LR_MULT,    weight_decay=_ATTN_V_WEIGHT_DECAY),
        dict(params=role(".attn.proj."), lr=base_lr * _ATTN_PROJ_LR_MULT, weight_decay=_ATTN_PROJ_WEIGHT_DECAY),
        dict(params=role(".mlp.fc."),    lr=base_lr * _MLP_FC_LR_MULT,    weight_decay=_MLP_FC_WEIGHT_DECAY),
        dict(params=role(".mlp.proj."),  lr=base_lr * _MLP_PROJ_LR_MULT,  weight_decay=_MLP_PROJ_WEIGHT_DECAY),
    ]


# ---- mu-schedule + eta-floor LR schedule (the schedule levers) -----------------------------------
# Transcribed from the variant's _muon_mu_at_step / set_hparams (lines 377-419). mu warms
# 0.85->0.95 over the first 300 steps and cools 0.95->0.85 over the last 50; the LR decays to a
# nonzero `_ETA_MIN` tail floor over the final `cooldown_frac` of training (WSD-style, the C01/C02
# schedule lineage). These act on the same Muon groups built above.
_MU_MIN, _MU_MAX = 0.85, 0.95
_MU_WARMUP_STEPS, _MU_COOLDOWN_STEPS = 300, 50
_ETA_MIN = 0.02


def muon_mu_at_step(step: int, train_steps: int) -> float:
    """The warmup/cooldown mu schedule (I/O: (step, train_steps) -> mu in [0.85, 0.95])."""
    cd_start = train_steps - _MU_COOLDOWN_STEPS
    if step < _MU_WARMUP_STEPS:
        return _MU_MIN + (step / max(_MU_WARMUP_STEPS, 1)) * (_MU_MAX - _MU_MIN)
    if step > cd_start:
        return _MU_MAX - ((step - cd_start) / max(_MU_COOLDOWN_STEPS, 1)) * (_MU_MAX - _MU_MIN)
    return _MU_MAX


def lr_eta_at_step(step: int, train_steps: int, cooldown_frac: float = 0.7) -> float:
    """WSD LR multiplier with a nonzero tail floor (I/O: (step, train_steps, cooldown_frac) -> eta).

    Multiply each group's `initial_lr` by this. Stable at 1.0 until the final `cooldown_frac` of
    training, then linearly decays toward `_ETA_MIN` (= 0.02, not 0). The optimizer-group base LRs
    (0.045 + the role mults above) are the `initial_lr`s this scales.
    """
    progress = step / train_steps
    assert 0 <= progress < 1
    eta_raw = 1.0 if progress < 1 - cooldown_frac else (1 - progress) / cooldown_frac
    return _ETA_MIN + (1.0 - _ETA_MIN) * eta_raw
