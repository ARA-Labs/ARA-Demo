# Seed-verified frontier — distinct-seed re-verification of every wave's canonical record

**Source**: §30.1 / §30.3 tables in research_insights/INSIGHTS.md, transcribed from
`data/runs_self_contained/agents/seed_reverify/` (152 runs, export_ids 11000–11151):
`summary.json` per-record stats, independently recomputed from each `runs/<id>/metadata.json`
`val_at_bin` field (means/stds/margins reproduced exactly).
**Caption**: "Each prior wave's canonical record re-run with genuinely distinct `--seed N`
(N=0..7 or 0..15). Stat-sig criterion `(3.28 − mean)·sqrt(N) >= 0.004`."
**Extraction type**: raw_table

## Verified frontier (per canonical record)

| Wave | Agent | Record (family) | N | verified bin | mean val@bin | std | margin | pass |
|------|-------|-----------------|--:|-------------:|-------------:|----:|-------:|------|
| v1 | cc | v12 (Muon+Contra+MuonEq+embed0.7) | 8 | 3100 | 3.27692 | 0.00100 | +0.00872 | yes |
| v1 | codex | v12iso-musched | 16 | 3205 | 3.27897 | 0.00068 | +0.00411 | yes |
| v2 | cc | v15 (PolarExpress+MuonEq+CGI) | 16 | 3040 | 3.27888 | 0.00095 | +0.00446 | yes |
| v2 | codex | legal3037 (rolewd+rolelr2+lookahead+Contra0.225) | 16 | 3037 | 3.27853 | 0.00078 | +0.00588 | yes |
| v3 | cc | v18j (Aurora-on-mlp.proj K=3 beta=0.25) | 8 | 3035 | 3.27832 | 0.00102 | +0.00476 | yes |
| v3 | codex | nosphere (W258-loo) | 16 | 2950* | 3.27930 (@2940) | 0.00122 | +0.00477 (@2950) | yes |
| v3-opus | cc | v114 (full stack) | 16 | 2930 | 3.27856 | 0.00098 | +0.00577 | yes |

\* codex_v3 `nosphere` 2950 is derived: the N=16 distinct-seed runs trained at ts=2940 (which
fails — mean 3.27930, margin +0.00280) re-evaluated at step 2950 (passes, margin +0.00477).

## Verification penalty (verified bin − original headline bin)

| Record | original bin | verified bin | Delta |
|--------|-------------:|-------------:|------:|
| cc_v1 v12 | 3100 | 3100 | 0 |
| codex_v2 legal3037 | 3037 | 3037 | 0 |
| cc_v2 v15 | 3035 (fail, +0.00315) | 3040 | +5 |
| codex_v1 v12iso | 3195 (fail, +0.00296) | 3205 | +10 |
| cc_v3 v18j | 3025 (fail, +0.00274) | 3035 | +10 |
| codex_v3 nosphere | 2940 (fail, +0.00280) | 2950 | +10 |
| cc_v3-opus v114 | 2920 | 2930 | +10 |

## Failing-bin entries (included for auditability)

| Record | bin | N | margin | verdict |
|--------|----:|--:|-------:|---------|
| v1cdx_v12iso_s3195 | 3195 | 8 | +0.00296 | fail (original) |
| v1cdx_v12iso_s3200 | 3200 | 8 | +0.00242 | fail (+5) |
| v2cc_v15_ts3035 | 3035 | 16 | +0.00315 | fail (original) |
| v2cc_v15_ts3045 | 3045 | 8 | +0.00331 | fail (+10 lottery) |
| v3cc_v18j_ts3025 | 3025 | 8 | +0.00274 | fail (original) |
| v3cc_v18j_ts3030 | 3030 | 8 | +0.00323 | fail (+5) |
| v3cdx_nosphere_ts2940 | 2940 | 16 | +0.00281 | fail (original) |

## Key readings

- **Honest endpoint**: best distinct-seed-verified record is cc 2930 / codex 2950; the single-best
  headlines (cc 2885 `v88-aurora`, codex 2880 `v3u` worker76) are unverified single-seed draws of
  *different* recipes, 45 / 70 steps below the nearest verified bin — the best-of-N inflation, measured.
- **Launcher cause (cc-side)**: all `claude-code` waves + `codex_v2` ran `torchrun` without forwarding
  `--seed`, so their "N seeds" were N node-draws of nominal `seed=0` (variance = CUDA/DDP
  non-determinism, std ~0.00043 per §9 Group A) vs genuine-seed std ~0.00095 here. `codex_v1`
  (`torch.manual_seed(N)`) and `codex_v3` (env `SEED`) used real seeds; their +10 is the stricter
  N=16 stat-sig bar, not a seed=0 artifact.

Maps to claims: C09, C12, C16, C17.
