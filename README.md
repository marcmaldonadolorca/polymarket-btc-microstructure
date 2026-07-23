# Polymarket BTC — short-horizon microstructure and prediction

> Master's thesis (MSc in Deep Learning, UPM, 2025/26).
> Author: **Marc Maldonado Lorca**.
>
> This repository accompanies the thesis. It documents a full methodology for
> data capture, temporal validation and cost control for BTC markets on
> Polymarket, and the **model ladder** that runs from a tabular baseline to a
> frozen specialist and a subsequent regime-change diagnosis.

## What it is and what it isn't

This is a **methodological, academic** work. It is not a production trading
system and **makes no claim of real profitability**. All results are reported in
**net ticks** (not dollars or ROI) and always with their support (number of
trades and days) and their uncertainty.

The out-of-sample validation is **5 days** (6–10 June 2026). The base specialist
was frozen before that block; the volatility filter was proposed after observing
the regime change and is reported as a post-hoc analysis. Distinguishing the two
kinds of evidence is central to the work.

## The core lesson

```text
A tabular baseline gets direction right ~90% of the time at 16 s... and still
loses money. With a realistic 2 s entry latency, net on the terminal set drops
to -1.48 ticks. Getting the direction right is not winning: cost and latency
decide. The whole project is reorganized around this lesson.
```

## The model ladder (the project's arc)

The narrative follows an incremental model progression, requiring at each step
that the added complexity be justified by evidence
(baseline → linear → features → deep model → final model):

```text
tabular baseline H16 (90% dir., looks excellent)
  -> dies with realistic latency (-1.48 ticks at 2 s)          [CORE LESSON]
  -> latency-aware models (AUC 0.79, negative economic policy)
  -> sequences + order book (GRU, Conv1D, fusion, TCN): representation yes, policy no
  -> methodological correction of the adverse score            [RIGOR]
  -> strict OOF protocol + horizon selection (H60 lives, H120/H240 collapse)
  -> prestart H60 specialist FROZEN before seeing fresh data
  -> clean OOS, 5 days: +0.349 ticks/action @0.5, 3/5 positive days
  -> post-hoc diagnosis: regime change and volatility filter
  -> diagnostic subset: +1.069 ticks/action, 5/5 days (non-confirmatory)
  -> regime-adaptation experiments: all NO_GO (valuable negatives)
  -> offline shadow replay + prospective validation design
```

## Out-of-sample result and post-hoc diagnosis

The prestart H60 specialist (HistGradientBoosting: EV regressor + "healthy"
session classifier) was first evaluated with no decided filter on the new block:

```text
clean OOS: n = 754 units, 5 days (6-10 Jun 2026)
Net@0.5 = +0.349 ticks/unit; 3/5 positive days
Sensitivity: @0.25 = +0.537   @0.5 = +0.349   @1.0 = -0.026

post-hoc low-volatility diagnosis: n = 318
Net@0.5 = +1.069; 5/5 positive days
Market-clustered 90% CI = [+0.193, +2.004]
Status = FROZEN HYPOTHESIS PENDING PROSPECTIVE VALIDATION
```

The full policy is frozen **after** the diagnosis and is not retrained to improve
these numbers. Only later dates can validate it (see
[`config/frozen_policy_thresholds.yaml`](config/frozen_policy_thresholds.yaml)).


## Repository structure

```text
config/         Frozen policy thresholds + arc configs
docs/           18 canonical arc documents (01..18), renamed
notebooks/      9 pedagogical/audit notebooks (EDA, splits, target, baseline,
                latency, sequences, adverse correction, specialist, final ledger)
scripts/        Reproducible entrypoints (scripts/experiments/)
src/edgerunner/ Package with the shared logic (data, features, models, eval)
results/        key_results.csv and decision_register.csv filtered to the arc
sql/            Schema of the base training query
data/samples/   Contract and documentation of the published data
reports/        Canonical thesis (`memoria.pdf`) and official LaTeX source
```

## Reproducibility

```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

The scripts in `scripts/experiments/` are the arc's entrypoints. By design they
expect to run from the repository root (they resolve relative paths). The full
dataset (~2.6M cross-venue rows and the SQLite source) is **not published** due
to size. The repository includes the schema (`sql/`), the code and an anonymized
ledger of 754 units in `results/final_candidate_actions_anonymized.csv`, enough
to recompute the final tables and the clustered uncertainty. Full training is not
reproducible without the private corpus and is declared as a limitation.

Key documents to understand the pipeline, in order:
`docs/01_sistema_de_datos.md` -> `docs/04_splits_validacion_temporal.md` ->
`docs/07_stress_de_latencia.md` -> `docs/14_especialista_prestart_h60.md` ->
`docs/16_validacion_fresh.md` -> `docs/18_paper_shadow.md`.

The reading guide for `docs/` is in `docs/README.md`: it explains which documents
are canonical, which internal artifacts are not published and how to audit the
final numbers.

The final audit does not need the private corpus:

```bash
python scripts/experiments/recompute_final_summary_from_public_ledger.py --check
```

It is also available as a notebook in
`notebooks/08_auditoria_final_ledger.ipynb`.
The notebooks guide is in `notebooks/README.md`.

## Status and future work

Research **paused** as of the submission date. Open lines: prospectively validate
the full policy without touching thresholds, define a maximum per-market
exposure, test the U-shaped pattern (hypothesis) and revisit deep learning with
60+ days of data.

## License

MIT — see [`LICENSE`](LICENSE).
