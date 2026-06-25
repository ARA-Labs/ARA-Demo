# Baseline recipe anatomy (the §0 starting point)

**Source**: §0 of research_insights/INSIGHTS.md
(`agents/cc_v1/runs/00001-muon-baseline-1-*/launched_script.py`).
**Caption**: "The shared two-optimizer baseline against which every insight is a delta. Muon reference
= 3500 steps to 3.28."
**Extraction type**: raw_table

| Component | Setting | Notes |
|---|---|---|
| AdamW: embed.weight LR | 0.3 | hand-set per-group |
| AdamW: proj.weight LR | 1/320 ~= 0.0031 | output proj is zero-initialized |
| AdamW: scalars (ndim<2) LR | 0.01 | |
| AdamW: betas / eps / wd | (0.8, 0.95) / 1e-10 / 0 | betas retuned in v3 (~+45-step lever) |
| Muon: applies to | every 2-D block weight (ndim>=2 in model.blocks) | |
| Muon: LR | 0.025 | -> 0.045 (v2) -> 0.0375 (v3) |
| Muon: weight decay | 0.0125 (decoupled, p*=1-lr*wd) | per-role 0.0275/0.03125 in v2/v3 |
| Muon: momentum mu | 0.95 | mu-schedule 0.85->0.95->0.85 added later |
| Muon: orthogonalization | 12-iter Newton-Schulz, (a,b,c)=(2,-1.5,0.5) | then scale by max(1, rows/cols)**0.5 |
| Schedule | WSD: hold eta=1.0 for 30%, linear decay to 0 over final 70% | cooldown_frac=0.7 |
| Logit softcap | 15 * logits * (logits^2 + 15^2).rsqrt() | embed*0.7 reduces early saturation |

**Reference run**: `00001-muon-baseline-1` — final_step 3500, final_val_loss 3.28027, step_avg_ms
157.54 (CSV).

Maps to claims: C01, C02, C03, C04, C06 (every lever is a delta vs this).
