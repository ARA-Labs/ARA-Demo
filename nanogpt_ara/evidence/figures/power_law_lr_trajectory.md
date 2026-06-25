# Figure: Muon-group power-law LR trajectory (v3 record)

**Source**: §15 of research_insights/INSIGHTS.md (decoded from
`cc_v3/07070-v88-aurora-proj-s2/launched_script.py` lines 63-69, 83, 843-847).
**Caption**: "The Muon-group learning rate under the power-law cooldown lr=min(flat, power_c*(t_end-
step)^1.2), flat_lr=0.0375, power_c=3.32e-6, t_end=2985; run stops at 2900."
**Axes**: X = training step; Y = Muon-group learning rate.
**Extraction type**: figure_data (key trajectory points; values computed from the schedule formula)

| step | Muon LR | phase |
|---:|---:|---|
| 0 | 0.0375 | flat |
| ~599 | 0.0375 | cooldown onset (power curve drops below flat) |
| 1750 | ~0.0207 | convex decay (approx; crossover region) |
| 2400 | ~0.0103 | soft-Muon begins blending in |
| 2900 (stop) | 0.00069 | = 1.8% of flat; run halts 85 steps before t_end |
| 2985 (t_end) | 0.0 | schedule's zero (never reached — horizon decoupled) |

Note: intermediate values (1750, 2400) are approximate readings of the convex `(t_end-step)^1.2` curve
between the explicitly-stated anchor points (onset ~599, stop 2900 -> 0.00069, t_end 2985 -> 0); marked
"~". The exact anchors (0.0375 flat, 0.00069 at stop, 1.8% ratio, onset ~599) are from §15.

**Per-role onset** (`power_c`, §15.3): embed 4.98e-5 (cools earliest), scalars 1.66e-6, Muon 3.32e-6,
proj 5.18e-7 — each group begins cooling on a different step (a third per-role axis after LR and WD).

**Why critical**: removing this schedule (reverting to linear WSD) changes onset (~870 vs ~599), shape
(linear vs convex), and terminal LR (0 vs 0.00069) at once; at the sub-0.001 target margin every seed
slips from 3.279 to >3.280 -> the LOO `pow_cooldown` 0/4-hit result.

Maps to claims: C02, C06, C13.
