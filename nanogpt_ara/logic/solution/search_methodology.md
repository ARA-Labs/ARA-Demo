# Search methodology — the autonomous research process

This is the *method* by which the Codex agent searched the optimizer space. It is as load-bearing as
any recipe: across all four waves, the process is what separated reported wins from defensible records
(C12). It is the agent-native analogue of a paper's "Methods" section.

## The orchestrator/subagent architecture

- **One orchestrator thread** holds the whole mission; its context is protected "ruthlessly." The bar
  for spawning a subagent is deliberately **low**: reading a paper, scanning a training log, a web
  search, prototyping an optimizer change, owning an HP sweep, or any "go check X and report back" is a
  subagent. The tree is one level deep (orchestrator → workers; workers don't spawn workers).
  [src: `v1/codex/AGENTS.md:51-69`]
- **Model routing:** Opus for synthesis / novel-optimizer design / "is this result real?" judgments;
  Sonnet for searching, log-scanning, single-paper summaries, owning one sweep; never Haiku for research.
- **Depth doctrine:** paper subagents return 800–2000 words with verbatim key equations, exact HP
  values, and a "To port to our setup" paragraph; idea subagents must return a math derivation,
  in-regime intuition, an arXiv search (≥3 refs), a novelty/improvement vector, an isolated ablation
  plan with bull/kill cells, and a pre-written kill criterion — or be sent back.

## The per-wave loop

1. **Re-read `goal.md`** at session start and after every major subagent return; mutate `plan.md`
   (the living state file) freely; append every significant moment to the append-only `THREAD.md`.
2. **Generate/triage a picklist** (`clusters.md` → `picklist.md`), ranked conservatively
   (schedule/LR/EMA before heavy optimizer replacements, which carry higher implementation risk and
   weaker local evidence).
3. **Screen one isolated lever per family**, killing at a pre-declared mid-curve gate. "Restate what the
   run was trying to learn before reading the result." Compare apples-to-apples against the 3500-step
   Muon bar.
4. **Reproduce before believing.** Assume nothing under ~50–100 steps is signal until a second seed
   confirms; a single-seed win's next launch is a *second seed of the same recipe*, not a new modifier
   (C11).
5. **Respect the stuck detector** (15 → "noise-floor-or-pivot?" subagent whose first action is a pruning
   round; 30 → mandatory pivot, family ruled out with a logged lesson).
6. **Prune** every 10 successful runs at the current best, when the stuck detector first fires, and
   before any submission (the mandatory pre-submission round). Leave-one-out, single seed first, second
   seed on borderline candidates; keep-tolerance wider than drop-tolerance (borderline is *keep*). → C09.
7. **Validate statistically** before submitting: fixed-step N-seed cohort, `(3.28 − μ)·√n ≥ 0.004`,
   earliest common checkpoint, anti-val-spam same-checkpoint scan. → C06.

## Throughput: preempt fanout

The main thread runs one job at a time on the dedicated node (the script grabs all 8 GPUs). Additional
runs are fanned out via `sbatch` into the cluster's **`preempt`** partition behind an **idle-node gate**
(submit only if `preempt` has ≥1 idle node, else queue on the main thread). Codex-owned jobs use a
`codex-` name prefix; `claude-code`-prefixed jobs belong to an independent agent's worktree and are
never touched. Preempted inner jobs are resubmitted **once** to `cluster` and otherwise left. This is a
"major throughput multiplier" and is why the run index holds 8,224 runs. [src: `v1/codex/AGENTS.md:229-273`]

## How this method shaped each wave (one line each)

- **v1** — Conservative screen of dozens of optimizer/schedule/init levers; most well-cited optimizers
  are clean negatives; the survivors (NorMuon corridor, factorized hidden preconditioning, Adam-mini,
  tail-EMA, mu-schedule) compose the v12iso stack; statistical pass fixes the bin at **3205**. (E01–E07)
- **novelty** — Read-isolated; the depth/novelty/compliance gates run *before* code; the search
  exhausts the reachable not-on-arXiv mechanism class into algebraic no-ops; documented **negative**.
  (E08)
- **v2** — Inherited a cross-agent parent; a compliance audit forced a **quarantine** and a
  byte-identical-compliant rebuild; the legal levers (role LR/WD, lookahead) descend a single-seed
  frontier that the statistical gate then trims to **3037**. (E09–E12)
- **v3** — A user hand-off of the public PR frontier triggers a **pivot** from local mechanisms to
  faithful public-parent reproduction; compression by phase-endpoint shift + variance control reaches a
  2940-viable parent; the W258 leave-one-out yields the **nosphere** simplification → **2949**.
  (E13–E16)
