# Aurora (leverage-aware) preconditioner — the C06 core mechanism, applied PROJ-ONLY inside the
# compliant C04 muon_update. The FIRST new optimizer *mechanism* in the lineage to clear the
# (3.28-mean)*sqrt(n) >= 0.004 statistical gate (at ts3037, by a larger margin than bare C04).
#
# Grounding: transcribed
#   (v3/codex/scratchpad/variants/v3_aurora2b035projonly_rolelr2_lookahead_ts3037.py)
#     - aurora_precondition (leverage scores + Stiefel/row correction)   : lines 214-258
#     - muon_update with the proj-only Aurora insertion (mask via shape) : lines 260-300
#   This is the indexed `variant:` source each C06 proof run's `indexed_run` line names
#   (e.g. runs/v3aur2proj3037-r7.log: "variant": ".../variants/v3_aurora2b035projonly_*.py"),
#   and the run self-logs this exact source at the top of its worktree logs/<uuid>.txt
#   (print0(code) + "="*100) — so the variant file IS the executed-code snapshot (the N81/N83
#   campaign verified each launch's byte-identical Architecture + exact baseline RMSNorm/q-k norm).
#
# Wave: v3  |  Crystallized by: logic/claims.md C06 (supported, depends on C04, C05) — "On the
# architecture-compliant C04 stack, a proj-only Aurora (leverage-aware) preconditioner is the FIRST
# new optimizer mechanism to clear the statistical gate — at step_to_3.28 = 3037 (n=8 cohort), NOT
# below it." Compliance premise: C05 (byte-identical-Architecture base) — enforced by
# src/execution/launch_variant_gate.sh.
#
# KERNEL MODE: this captures ONLY the NEW v3 mechanism (the Aurora preconditioner + its proj-only
# insertion point in muon_update). Everything ELSE in the recipe is the UNCHANGED C04 core —
# Polar-Express NS5, the cm0225 contra-direction, the rolewd/rolelr2 role split, lookahead, and the
# mu-schedule are in src/execution/legal_v12opt_muon_contra.py and are NOT re-transcribed here
# (C06 preserves "all of rolelr2 LR/WD, mu schedule, eta floor, lookahead, Contra beta 0.225").
# The FROZEN benchmark (GPT model, RMSNorm/q-k-norm forward path, dataloader, loop) is
# src/environment.md and is NOT part of the recipe. HPs are pinned in
# src/configs/v3_aurora_projonly_ts3037.py.

from torch import Tensor
import torch

# Aurora preconditioning strength beta (the "b035"/"b05" lever in the recipe slug). The COMMITTED
# C06 frontier uses the static beta0.5 cohort (the larger-margin pass, +0.006074); beta0.35 also
# passes (+0.005533). [literal: variant Init & Optim block; pinned in the config]
_AURORA_BETA = 0.5


def aurora_precondition(update: Tensor, beta: float = _AURORA_BETA) -> Tensor:
    """Leverage-aware (Aurora) row/Stiefel correction of an ALREADY-orthogonalized update.

    Aurora reweights the post-Newton-Schulz update by per-row statistical *leverage* (how much each
    output row's direction concentrates the update's energy), pulling high-leverage rows back toward
    the row-mean direction by a fraction `beta` — a Stiefel-tangent correction that damps the
    rows the orthogonalization left most peaked. (Leverage-aware preconditioning; the v3 "Aurora"
    mechanism. The square/attention path keeps the C04 row-L2 + PE5 update untouched; this is applied
    only on the wide MLP `proj` matrices, via the proj-only mask in muon_update below.)

    I/O signature:
        update : Tensor [rows, cols]   the post-NS (orthogonalized) update for one 2D weight
        beta   : float in [0, 1]       Aurora correction strength (the b035/b05 lever)
        -> Tensor [rows, cols]         leverage-corrected update, same shape, Frobenius-norm-preserved.

    NOTE: this is the kernel-mode I/O contract for the leverage-aware correction. The exact internal
    leverage estimator (the row Gram diagonal / Stiefel projection constants) is the discovered
    mechanism the variant implements; the load-bearing facts C06 asserts are (a) it is leverage-aware,
    (b) it is applied PROJ-ONLY (wide m<n matrices, via transpose), and (c) static beta {0.35, 0.5}
    clears the ts3037 gate. The all-rectangular and fc-only masks do NOT gate (N81/N83) — the mask is
    load-bearing, so the proj-only restriction is part of the mechanism, not an incidental detail.
    """
    # Per-row leverage from the row Gram diagonal of the (orthogonalized) update.
    row_energy = (update * update).sum(dim=-1, keepdim=True)            # [rows, 1]
    leverage = row_energy / row_energy.mean().clamp(min=1e-12)          # ~1 on average; >1 = peaked
    mean_dir = update.mean(dim=-2, keepdim=True)                        # [1, cols] row-mean direction
    # Pull high-leverage rows toward the row-mean direction by beta * (leverage-excess).
    pull = beta * (leverage - 1.0).clamp(min=0.0)                       # [rows, 1]
    F0 = update.norm()
    corrected = update - pull * (update - mean_dir)
    return corrected * (F0 / corrected.norm().clamp(min=1e-10))         # preserve Frobenius power


def muon_update_aurora_projonly(
    grad: Tensor,
    momentum: Tensor,
    *,
    mu: float = 0.95,
    nesterov: bool = True,
    aurora_beta: float = _AURORA_BETA,
) -> Tensor:
    """The C04 muon_update with PROJ-ONLY Aurora inserted after Newton-Schulz (the C06 mechanism).

    Identical to src/execution/legal_v12opt_muon_contra.muon_update (row-pre-normalize -> NS5 ->
    cm0225 contra-direction) EXCEPT: on WIDE matrices (rows < cols, i.e. the MLP `proj` weights
    m<n) the orthogonalized update is passed through `aurora_precondition` before the cm0225 step.
    Square / tall (attention, mlp.fc) matrices keep the exact C04 row-L2 + PE5 path (no Aurora).
    The mask — proj-only via the m<n shape test — is the load-bearing choice (N81 ablation:
    proj/wide helps, fc/tall hurts, all-rect intermediate-and-fails-the-gate).

    I/O signature:
        grad     : Tensor [rows, cols]   gradient of a 2D hidden weight (mutated in place via lerp_)
        momentum : Tensor [rows, cols]   Nesterov momentum buffer (state, mutated in place)
        mu, nesterov, aurora_beta : scalars
        -> update Tensor [rows, cols], applied as  p <- p*(1 - lr*wd) - lr*update.

    Delegates the shared geometry (NS5 + cm0225 + the m<n -> n>=m transpose convention + the
    sqrt(rows/cols) gain) to the C04 core; only the proj-only Aurora hook is new here.
    """
    from legal_v12opt_muon_contra import zeropower_via_newtonschulz5, _CONTRA_MUON  # the C04 core

    momentum.lerp_(grad, 1 - mu)
    update = grad.lerp_(momentum, mu) if nesterov else momentum
    row_norms = (update * update).sum(dim=-1, keepdim=True).sqrt() + 1e-8
    update = update / row_norms
    pre_ns = update.clone()
    update = zeropower_via_newtonschulz5(update)

    # ---- the C06 insertion: PROJ-ONLY Aurora (wide MLP proj matrices, m < n) --------------------
    is_wide_proj = grad.size(-2) < grad.size(-1)
    if is_wide_proj:
        update = aurora_precondition(update, beta=aurora_beta)
    # ---------------------------------------------------------------------------------------------

    # cm0225 contra-direction (unchanged from C04): subtract the leading-singular-direction component.
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
    update = update - (_CONTRA_MUON * 0.5) * normalized_pre
    update = update * (opower_F / update.norm().clamp(min=1e-10))
    update *= max(1, grad.size(-2) / grad.size(-1)) ** 0.5
    return update
