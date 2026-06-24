#!/bin/bash
# Architecture-compliance launch gate — the C05 ENFORCEMENT ARTIFACT (kernel mode: the gate checks
# only; the Slurm worktree/stub plumbing is omitted as benchmark infrastructure, not the recipe).
#
# Grounding: transcribed (v2/codex/scratchpad/launch_variant.sh:18-44).
# Wave: v2  |  Crystallized by: logic/claims.md C05 (supported, provenance user-revised) — "The
# cc-v12 base used by the v2 line VIOLATES the no-forward/no-norm hard rule ... only
# byte-identical-Architecture variants are submittable." Operationalized as this hard launch-time
# gate: launch_variant.sh exits BEFORE Slurm submission on any non-compliant variant.
# See logic/claims.md C04 (the compliant frontier this gate admits) and src/environment.md (the
# frozen baseline Architecture / RMSNorm / q-k-norm this gate diffs against). Trace: N76 (the
# compliance STOP / build+strengthen), N79 (the C03-vs-C05 contradiction).
#
# This is a CONCRETE artifact (a real shell gate), not re-encoded prose — captured per compiler
# Stage 3 / driver/materialize.md (Rule 14: concrete artifacts are captured in native form).
#
# Effect (the four hard-rule checks, in order; the FROZEN baseline is $TRACK_DIR/train_gpt_simple.py):
#   exit 64 = compliance violation (NOT submittable); exit 75 = preempt idle-node gate (capacity).
# It RECLASSIFIES as non-promotable not only the cc-v12 forward-path change
# (`norm(x.float())` / `q,k = norm(q),norm(k)`) but also gain-path optimizer plumbing (PWG/GMS-style:
# `norm1.gains`, `gains.grad`, ...) that routes optimizer logic through the norm gains even while
# preserving forward code (N76).

set -euo pipefail
RUN_ID="$1"
VARIANT_PATH="$(realpath "$2")"
TRACK_DIR="/beegfs/elie/v2-iteration-codex/records/track_3_optimization"   # holds the frozen baseline

# (1) The variant's `Architecture` block (everything between the `#  Architecture` and `#  Optimizer`
#     banners) must be BYTE-IDENTICAL to the baseline train_gpt_simple.py. Only `Optimization` +
#     `Init & Optim Hyperparams` may differ.
if ! diff -q \
  <(sed -n '/#             Architecture/,/#              Optimizer/p' "$TRACK_DIR/train_gpt_simple.py") \
  <(sed -n '/#             Architecture/,/#              Optimizer/p' "$VARIANT_PATH") >/dev/null; then
  echo "architecture gate blocked submission for $RUN_ID: non-byte-identical Architecture block" >&2
  exit 64
fi

# (2) RMSNorm.forward must be the BASELINE form (not the cc-v12 `(norm(x.float())*self.gains).type_as(x)`).
if ! rg -q 'return F\.rms_norm\(x, \(x\.size\(-1\),\), weight=self\.gains\.type_as\(x\)\)' "$VARIANT_PATH"; then
  echo "architecture gate blocked submission for $RUN_ID: RMSNorm.forward differs from baseline" >&2
  exit 64
fi

# (3) Attention q/k normalization must be the BASELINE direct F.rms_norm (not the helper `norm(q),norm(k)`).
if ! rg -q 'q, k = F\.rms_norm\(q, \(q\.size\(-1\),\)\), F\.rms_norm\(k, \(k\.size\(-1\),\)\)' "$VARIANT_PATH"; then
  echo "architecture gate blocked submission for $RUN_ID: q/k norm differs from baseline" >&2
  exit 64
fi

# (4) No special RMSNorm/gain-path optimizer plumbing (catches PWG/GMS gain-routed variants AND the
#     cc-v12 forward-path failure modes even if (2)/(3) were spoofed).
if rg -q 'norm[12]\.gains|gains\.grad|gain_refs|gain_names|_branch_gain_link|norm\(x\.float\(\)\)|q, k = norm\(q\), norm\(k\)' "$VARIANT_PATH"; then
  echo "architecture gate blocked submission for $RUN_ID: special RMSNorm/gain-path treatment is disallowed" >&2
  exit 64
fi

# Capacity gate (not a compliance check): only submit when the preempt partition has an idle node.
idle=$(sinfo -p preempt -h -o '%T %D' | awk '$1=="idle"{s+=$2}END{print s+0}')
if (( idle <= 0 )); then
  echo "preempt idle-node gate blocked submission for $RUN_ID" >&2
  exit 75
fi

# ... (passing here) the original then builds a detached git worktree, copies the variant in as
#     train_gpt_simple.py, writes the `v2cxleg-t3-<run-id>` sbatch stub, and submits — see
#     v2/codex/scratchpad/launch_variant.sh:46-87 (benchmark plumbing, omitted in kernel mode).
