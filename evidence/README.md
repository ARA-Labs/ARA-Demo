# Evidence Index

> **t=0 FRAME — INTENTIONALLY EMPTY.** No evidence exists at the start of the experiment. The
> agent has run nothing, so there are no result tables, figures, sweeps, or logs to file yet.
> Evidence accretes LATER: the `compiler` runs again only at each main wave's *artifact exit
> gate* (`../driver/materialize.md`), where it extracts that wave's now-crystallized
> recipes / configs / metrics into `src/` + `evidence/`. Nothing is filed during bootstrap.
>
> The frozen benchmark setup (architecture / batch / data / step) is documented as
> reproducibility material in `src/environment.md`, not as result evidence.

## Tables

| File | Source | Claims | Description |
|------|--------|--------|-------------|
| _none yet_ | — | — | — |

## Figures

| File | Source | Claims | Description |
|------|--------|--------|-------------|
| _none yet_ | — | — | — |

## Conventions for the replay (when evidence is added later)
- Every numbered result table/figure gets BOTH a markdown transcription AND a screenshot `.png`.
- Raw source objects stay separate from derived subsets (`derived_`/`subset_` filenames declare
  their parent).
- Each evidence file carries a **Source** field; figures declare type / extraction method /
  reading confidence, and estimated readings are marked `≈`.
- Evidence binds to claims by claim ID (C##); the index above maps every file to the claims it
  supports.
