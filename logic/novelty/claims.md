# Claims — NOVELTY LANE (isolated sub-namespace inside the single ara/)

> **wave: novelty | isolation: hard.** Crystallized claims for the novelty wave only. NO
> dependencies on the v1/v2/v3 lineage (those files are not read in this lane). Each entry is a
> present-state snapshot; history lives in `trace/novelty/`. Crystallized only on a closure
> signal; mutable per Stage 4.

## CV01: A rigorously-explained negative on the agent's own novel derivation is a wave deliverable
- **Statement**: For this wave, success is NOT strictly a sub-3500-step recipe. A clean negative
  result on the agent's OWN derived (non-arXiv) idea — accompanied by the mathematical reason it
  did not beat Muon@3500 — is itself a real contribution and a valid deliverable.
- **Status**: supported
- **Provenance**: user
- **Falsification criteria**: Would be falsified if the mission later declared that only a
  sub-3500 recipe counts and explained negatives carry no value, or if the negatives produced
  were not actually explained (no math reason / no retained gate evidence).
- **Proof**: NV06, NV07, NV08 (this turn produced ~40 explained negatives — each killed idea has
  a math-grounded reduction to a prior or a no-op/additive argument, and each run-family close
  states the empirical reason); staging OV03 (the framing) + OV06 (the empirical instantiation).
- **Dependencies**: [NVC01]
- **Tags**: success-definition, explained-negative, contribution
- **Crystallized via**: empirical-resolution + artifact-commitment (the turn's negatives
  instantiate it; CV02 cites it as its framing premise). From staging OV03.

## CV02: In this window, no dual-gated novel mechanism beat Muon@3500 under the 2-seed gate
- **Statement**: Across the ~40 dual-gated (rule + arXiv) novel mechanisms explored in turn
  novelty-002 (254 runs) — spanning init-only branch-gain/hidden-basis rescales, optimizer-only
  pre-polar Muon couplings, transport/commutator/skew variants, and cross-optimizer feedback —
  NONE beat the Muon@3500 floor under the lawful-core 2-seed / noise-floor gate. The best
  single-seed `step_to_3.28` was 3375 (NGI `n0875/m1125/t3450`), which FAILED 2-seed
  reproduction; the only 2-seed-reproduced crossing (VFG `gain080/lr026/t3475`) sat at 3475 —
  a 25-step grid improvement, BELOW the required ~2x step noise floor. Single-seed crossings
  clustered at 3450/3475, i.e. inside the noise band of the 3500 floor.
- **Status**: supported
- **Provenance**: ai-suggested
- **Falsification criteria**: Falsified if a re-examination of this window's runs shows a member
  family with a 2-seed reproduction at >= ~2x the noise floor below 3500 (i.e. <= ~3300) that was
  missed; or if a later turn reproduces one of these exact mechanisms below the gate (which would
  reclassify it from this window's negative to a genuine result).
- **Proof**: NV03 (TRM/STM/ALR ruled down), NV04 (init family preserves early edge, no crossing
  gain), NV09 (dual-gate-surviving optimizer mechanisms all 3450/3475-only or missed), NV10 (NGI
  3375 single-seed FAILED reproduction: seed1234 3.28081, seed2 first target only at 3450), NV11
  (VFG 2-seed reproduced @3475 but below noise floor; NDF 3375 single-seed failed reproduction).
  Runs table: best step_to_3.28 this window = 3375; statistical_verification rows all confirm the
  reproductions did not hold below the floor.
- **Dependencies**: [CV01]
- **Tags**: negative-result, two-seed-gate, noise-floor, Muon-3500-floor, this-window-only
- **Crystallized via**: empirical-resolution (every reproduction and family close resolved
  within this turn and was commented on). From staging OV06.
