# Evidence logs — linked proof-run train.logs (waves v1, v2, v3)

These are **symlinks**, not copies (link, do not bulk-import — driver/materialize.md). Each points to
a single `train.log` under `v{1,2,3}/codex/scratchpad/runs/` that a crystallized claim's `Proof:`
pointer (from a wave ≤ this gate) **already names** — the replay contract permits opening a run
pointer named in a packet. No `runs.csv` / `runs.jsonl` bulk import; no non-cited runs.

For **v1**, each `.log` self-embeds the launched_script.py source at its top (the `====` separator ends
the code region), so these are also the exact executed-code snapshots the v1 core modules in
`src/execution/` were transcribed from. For **v2**, the `.log` is the stdout log (it carries the
`indexed_run {…}` JSON line with `final_val_loss` / `first_step_le_3p28` / the `variant:` source);
the executed-code snapshot lives in the worktree `logs/<uuid>.txt` (the run self-logs `code` via
`print0(code)` + `"="*100`), and the v2 core modules were transcribed from the indexed `variant:`
file in `v2/codex/scratchpad/variants/`.

## C01 — NorMuon + decoupled-WSD sub-3500 frontier (claims.md C01; trace N12)
| link | run_id | role |
|---|---|---|
| c01_normuon_stop3296_seed0.log | normuon-b090to080-mlpprojlr124375-tailresrmsstack-aggmom3hidden-h3375-stop3296-seed0 | 2-seed frontier (3.27914) |
| c01_normuon_stop3296_seed1.log | …stop3296-seed1 | 2-seed frontier (3.27872) |
| c01_normuon_stop3345_seed0.log | normuon-b090to082-mlpprojlr125-h3375-stop3345-seed0 | earlier reproduced point (3.27992) |
| c01_normuon_stop3345_seed1.log | …stop3345-seed1 | earlier reproduced point (3.27928) |

## C02 — compression corridor + statistical pass (claims.md C02; trace N51 / N59)
| link | run_id | role |
|---|---|---|
| c02_muon2f_stop3250_seed0.log | normuon-…-adamminiopt1-muon2fhidden-b2p095-eps1e3-tailresrmsstack-aggmom3hidden-h3375-stop3250-seed0 | Muon2F stepping stone (3.27945) |
| c02_v12iso_s3220_seed0.sbatch.log | v12iso-musched-h3375-s3220-seed0 | claimable frontier member (3.27791) |
| c02_v12iso_s3220_seed9.sbatch.log | v12iso-musched-h3375-s3220-seed9 | claimable frontier member (3.27663) |
| c02_v12iso_s3195_seed20.sbatch.log | v12iso-musched-h3375-s3195-seed20 | claimable frontier member (3.27727) |
| c02_formalprune_norespulse_stop3296_seed5.sbatch.log | formalprune-norespulse-from-tailresrmsstack-aggmom3hidden-h3375-stop3296-seed5 | pruned formal stack member (3.27903) |
| c02_v12iso_s3170_seed23_REJECTED.sbatch.log | v12iso-musched-h3375-s3170-seed23 | REJECTED by the n=15 gate (3.27980) — the rigor counter-example |

## C03 — cc-v12 step-count frontier (claims.md C03; trace N68) — base NON-COMPLIANT / quarantined
| link | run_id | role |
|---|---|---|
| c03_ccv12_ts2999_r4.log | v12-ts2999-r4 | 2-seed anchor (3.27985, crosses @2999) |
| c03_ccv12_ts2999_r7.log | v12-ts2999-r7 | 2-seed anchor (3.27996, crosses @2999) |
| c03_ccv12_ts3000_r3.log | v12-ts3000-r3 | plain ts3000 crossing (3.27987) |
| c03_ccv12_ts3022_r1_first_below_record.log | v12-ts3022-r1 | "FIRST confirmed below-record hit" (3.27969) |
| c03_ccv12_ts3012_r2.log | v12-ts3012-r2 | 3012-denominator schedule crossing @ val-step 3000 (3.27901) |

> NB these are on the cc-v12 base, which VIOLATES the no-forward/no-norm rule (C05) and is quarantined
> as non-submittable; C03 is existence/2-seed only, superseded for the compliant benchmark by C04.

## C04 — architecture-compliant statistical pass (claims.md C04; trace N77 / N78)
| link | run_id | role |
|---|---|---|
| c04_legal_ts3037_sig_r1.log … r8.log | legal-v12opt-rolewd-rolelr2-lookahead-ts3037-cm0225-attn0625-sig-r1..r8 | the n=8 PASS cohort (mean 3.2783775, score 0.004589); losses 3.27823/3.27882/3.27831/3.27862/3.27769/3.27845/3.27919/3.27771 |
| c04_legal_ts2962_r41_REJECTED.log | legal-v12opt-rolewd-rolelr2-lookahead-ts2962-cm0225-attn0625-r41 | low-step single-seed crossing (3.27992 @2962) whose ts2962 cohort (n=38) is REJECTED — the rigor counter-example |
| c04_legal_ts3012_sig_r3_FAIL_control.log | legal-v12opt-rolewd-rolelr2-lookahead-ts3012-cm0225-attn0625-sig-r3 | ts3012 cohort FAIL control (n=8 score 0.00052) |

## C06 — proj-only Aurora ts3037 gate pass (claims.md C06; trace N81 / N83) — the FIRST new-mechanism gate pass
| link | run_id | role |
|---|---|---|
| c06_aurora_proj3037_r7.log | v3aur2proj3037-r7 | proj-only beta0.5 ts3037 PASS cohort member (mean 3.277852, +0.006074) |
| c06_aurora_b035proj3037_r5.log | v3aur2b035proj3037-r5 | proj-only beta0.35 ts3037 PASS cohort member (mean 3.278044, +0.005533) |
| c06_aurora_b035proj3037_r6.log | v3aur2b035proj3037-r6 | proj-only beta0.35 ts3037 PASS cohort member |
| c06_aurora_allrect_b025_ts3025_r1_REJECTED.log | v3aur2b0253025-r1 | all-rect beta0.25 ts3025 cohort REJECTED (n=8 −0.001032) — the lower-bin rigor counter-example |
| c06_aurora_proj3035_r8_FAIL_justshort.log | v3aur2proj3035-r8 | proj-only beta0.5 ts3035 cohort FAIL (n=8 +0.003772, ~0.00008 short) |

## C07 — Aurora tail-tune committed frontier ts3037→ts3027 (claims.md C07; trace N87 / N88)
| link | run_id | role |
|---|---|---|
| c07_aurora_b035proj3029_r9.log | v3aur2b035proj3029-r9 | direct beta0.35 ts3029 committed PASS (n=8 +0.006177); canonical r9 replaced the cancelled r6 |
| c07_aurora_betaramp3028_r2_commit_e8d7bbe.log | v3aur2b035proj3028-b035to050-r2 | late beta-ramp 0.35→0.50 ts3028 committed PASS (n=8 +0.005547) — **commit e8d7bbe** |
| c07_aurora_betaprelo3027_r3_commit_e76d686.log | v3aur2b035proj3027-p012-betaprelofinalhi-r3 | beta-preload+endpoint-LA ts3027 committed PASS (n=8 +0.004225) — **commit e76d686**, the lowest committed gated stop |
| c07_aurora_3026_rank8subbrake_REJECTED.log | v3aur2b035proj3026-p012-betaprelo-rank8-subbrake | best conditional ts3026 mechanism, FAILS on N=8 expansion (+0.003843) — the sub-3027 rigor counter-example |

## C08 — public Soft-Muon + outward-radial + SOAP, step-2940 (claims.md C08; trace N90 / N91) — below the ~2990 public floor
| link | run_id | role |
|---|---|---|
| c08_worker70_step2940_r2.log | v3u2900-worker70-tailradgate-early2775-lowratio-vfade2850-rad045-warmsoapskip-s3035-soft2925-ts3020-r2-preempt | Worker70 step-2940 PASS cohort member (n=10 mean 3.278606, +0.004408) |
| c08_worker258_tangentsphere_step2940_r9.log | v3u2900-worker258-tailradgate-lacv-tangent-sphere-qk-spherela-…-ts3020-r9-preempt | W251/W258 tangent-sphere step-2940 PASS (n=9 +0.004300); r9 the fast-but-valid seed that rescued 2940 |
| c08_prune_nosphere_n16_canonical_r1.log | v3prune-w258loo-nosphere-r1-preempt | leave-one-out PRUNED canonical `nosphere` step-2940 PASS (n=16 +0.004608) — the simplified stack |
| c08_worker206_2875_singleseed_REJECTED.log | v3u2900-worker206-…-ts3020-r3-preempt | the window's best 2875 — a SINGLE seed (stat_verify=False); sub-2900 is noise-floor, EXCLUDED from the claim |

> NB the C08 v37-checkout base is byte-identical-Architecture (C05-compliant); the result is
> SUBMITTABLE and the FIRST compliant result below the ~2990 public PR #294 floor. The leave-one-out
> per-ablation means (nosoft/noradial/nosoap/…) live in `evidence/results/c08_soft_muon_radial_statpass.md`
> (the pruning round is aggregated there + in the run-tree node N90; not every ablation has a standalone
> linked log).

See `evidence/results/*.md` for the aggregated metric tables these logs back.
