# Public Soft-Muon (PR #291) + outward-radial update dampening (PR #294, applied as a TAIL
# correction) — the C08 core mechanisms. After the USER-directed pivot (N89) off the Codex Aurora/
# C04 backbone onto the public modded-nanogpt PR frontier, this stack — rebuilt architecture-
# COMPLIANT on the codex `v37` checkout under the C05 byte-identical-Architecture gate, with a SOAP
# sidecar and a fixed tail-radial-gate schedule — reaches a STATISTICALLY-VERIFIED step_to_3.28 =
# 2940 (the FIRST compliant result below the ~2990 public PR #294 floor). A leave-one-out pruning
# round found Soft-Muon, the PR#294 radial damping, SOAP, V-SOAP, lookahead-CV, reduced q/k Contra
# scaling, the q/k LACV-floor, and the tangent-sphere radial GATE all LOAD-BEARING.
#
# Grounding: transcribed
#   (v3/codex/scratchpad/variants/v3u2900_worker70_tailradgate_early2775_lowratio_vfade2850_rad045_warmsoapskip_s3035_soft2925_ts3020.py
#    — the indexed Worker70 variant the C08 N=10 cohort's runs name; the `nosphere` prune variant is
#      v3/codex/scratchpad/variants/v3prune_w258loo_nosphere.py)
#     - soft_muon_norm (Gram-Frobenius / Schatten-4 softening of the orthogonalization) : lines 188-214
#     - outward_radial_tail_correction (PR#294 radial decomp + post-step radius correction, TAIL-only) : lines 216-252
#   Each C08 proof run self-logs its source at the log top (print0(code) + "="*100); the public
#   parents are KellerJordan modded-nanogpt PR #291 (Soft-Muon/Contra) and PR #294 (outward-radial),
#   read by the agent from refs/pr/291 and refs/pr/294 (N89) and rebuilt on the compliant v37 checkout.
#
# Wave: v3  |  Crystallized by: logic/claims.md C08 (supported, depends on C05) — "On the public
# modded-nanogpt Soft-Muon + outward-radial (PR #294/#291) + SOAP stack, an architecture-compliant
# tail-radial-gate recipe reaches a STATISTICALLY-VERIFIED step_to_3.28 = 2940 — the FIRST compliant
# result below the ~2990 public PR #294 floor; sub-2900 (and sub-2940) is NOT statistically viable."
# Concepts: logic/concepts.md "Soft-Muon (PR #291)" + "outward-radial update dampening (PR #294)".
# Compliance premise: C05 (byte-identical-Architecture v37 checkout) — enforced by
# src/execution/launch_variant_gate.sh.
#
# KERNEL MODE: this captures the TWO NEW load-bearing v3 mechanisms (Soft-Muon norming + the
# radial-AS-TAIL-correction). The other load-bearing ingredients (SOAP / V-SOAP sidecar,
# lookahead-CV, the q/k LACV-floor, the tangent-sphere radial gate) are recipe levers pinned/listed
# in src/configs/v3_soft_muon_radial_ts2940.py with their leave-one-out demotion deltas; the SOAP
# sidecar machinery is a public-PR component (captured by reference, not re-encoded). The FROZEN
# benchmark is src/environment.md. Note the load-bearing ABLATION evidence: radial-FROM-STEP-ZERO
# and base-Soft-only were KILLED as too-slow/insufficient-tail-slope (N90) — the radial-as-TAIL
# distinction is part of the mechanism.

from torch import Tensor
import torch


# Soft-Muon softening exponent / Contra scale (PR #291: Gram-Frobenius / Schatten-4 norming with
# p=0.1 basis stacking). [literal: the worker70 variant Optimization block]
_SOFT_MUON_P = 0.1
_SOFT_MUON_CEIL = 0.075   # the Soft-Muon ceiling ("softceil075"/"soft2925" lever in the slug)


def soft_muon_norm(update: Tensor, p: float = _SOFT_MUON_P, ceil: float = _SOFT_MUON_CEIL) -> Tensor:
    """Soft-Muon norming (PR #291): a SOFTENED orthogonalization via Gram-Frobenius / Schatten-4.

    Instead of a hard Newton-Schulz polar factor, Soft-Muon scales the update by a soft function of
    its singular spectrum (Gram-Frobenius / Schatten-4 norm with p=0.1 basis stacking), capped by a
    ceiling — interpolating between the raw update and its fully-orthogonalized form. This is the
    PR #291 Soft-Muon / Contra mechanism; per the C08 leave-one-out it is LOAD-BEARING (removing it
    demotes the 2940 boundary: nosoft 2940-mean 3.280623).

    I/O signature:
        update : Tensor [rows, cols]   the (momentum) update for one 2D weight
        p, ceil : floats               softening exponent (Schatten-4 / p=0.1) and the Soft ceiling
        -> Tensor [rows, cols]         softly-orthogonalized update, same shape.

    KERNEL-MODE contract: the load-bearing facts are (a) it is a SOFT (Gram-Frobenius/Schatten-4)
    norming, not a hard polar factor; (b) p=0.1 basis stacking; (c) a Soft-Muon ceiling. The exact
    Schatten-4 closed form is the public PR #291 implementation rebuilt on the v37 checkout.
    """
    gram = update @ update.mT                                   # [rows, rows]
    schatten4 = (gram @ gram).diagonal(dim1=-2, dim2=-1).sum().clamp(min=1e-12).sqrt().sqrt()
    soft_scale = (update.norm() / schatten4.clamp(min=1e-12)).clamp(max=1.0 / ceil)
    return update * (soft_scale ** p)


# Outward-radial dampening strength + the TAIL window it is gated to (PR #294). The radial correction
# is applied ONLY as a tail correction (NOT from step zero — radial-from-zero was KILLED, N90).
_RADIAL_STRENGTH = 0.045        # "rad045" lever. [literal]
_RADIAL_TAIL_START = 2775       # tail-radial-gate opens here ("tailradgate-early2775"). [literal]


def outward_radial_tail_correction(
    param: Tensor,
    update: Tensor,
    *,
    step: int,
    strength: float = _RADIAL_STRENGTH,
    tail_start: int = _RADIAL_TAIL_START,
) -> Tensor:
    """PR #294 outward-radial update dampening, applied as a TAIL correction (the C08 radial lever).

    Decompose the update into a radial component (along the current weight direction param/||param||)
    and a tangential remainder; dampen the OUTWARD radial component by `strength` to slow norm growth
    near the end of training. Applied ONLY once `step >= tail_start` (the tail-radial-gate) — the
    radial-AS-TAIL distinction is load-bearing: radial-from-step-zero tracks the slow radial-only
    curve (~0.04 behind Soft-only at step 1000) and was killed (N90); noradial demotes 2940 to
    mean 3.282580 (the single largest leave-one-out demotion).

    I/O signature:
        param    : Tensor [rows, cols]   the current 2D weight (read-only here; gives the radial axis)
        update   : Tensor [rows, cols]   the (Soft-Muon-normed) update to correct
        step     : int                   current training step (gates the tail window)
        strength : float                 outward-radial dampening fraction (rad045)
        tail_start : int                 first step the radial gate is active (tailradgate-early2775)
        -> Tensor [rows, cols]           radially-dampened update, same shape. Pair with a post-step
                                         radius correction on `param` (PR #294's post-step radius fix).
    """
    if step < tail_start:
        return update
    axis = param / param.norm().clamp(min=1e-12)
    radial_mag = (update * axis).sum()
    radial_comp = radial_mag * axis
    outward = radial_comp if radial_mag > 0 else torch.zeros_like(radial_comp)
    return update - strength * outward
