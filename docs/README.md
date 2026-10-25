# Reading guide for `docs/`

## English summary

The documents in this folder are written in Spanish: they are a curated version of the research
notebook used to build the thesis. Their job is to explain the experimental arc, not to publish
every internal artifact. The official thesis is [`reports/memoria.pdf`](../reports/memoria.pdf)
(Spanish, with an English abstract); where a historical document and the thesis differ in wording,
the thesis prevails.

**Canonical reading order** (enough to follow the main narrative):

| # | Document | What it covers |
|---|---|---|
| 1 | [`01_sistema_de_datos.md`](01_sistema_de_datos.md) | Data model of the capture database (tables, joins, quality and tradability filters) and a snapshot of the corpus |
| 2 | [`04_splits_validacion_temporal.md`](04_splits_validacion_temporal.md) | Why rows cannot be shuffled: consecutive 2 s frames are near-duplicates and labels look forward, so every split is temporal |
| 3 | [`07_stress_de_latencia.md`](07_stress_de_latencia.md) | The core lesson: the baseline policy that looks excellent at zero latency turns negative with a 2 s entry delay |
| 4 | [`10_secuencias_y_orderbook.md`](10_secuencias_y_orderbook.md) | Sequence and order-book models (GRU, Conv1D): some incremental signal, no selectable policy |
| 5 | [`11_correccion_score_adverse.md`](11_correccion_score_adverse.md) | A methodological correction: one experiment ranked observations by adverse-fill probability in the wrong direction (riskiest first); the "robust" candidate built on it is withdrawn as evidence |
| 6 | [`14_especialista_prestart_h60.md`](14_especialista_prestart_h60.md) | The prestart H60 specialist (HistGradientBoosting, two heads) that was frozen before the fresh data |
| 7 | [`16_validacion_fresh.md`](16_validacion_fresh.md) | Out-of-sample result on 6–10 June 2026 (+0.349 ticks per action, 754 actions, 3/5 positive days) and the post-hoc regime diagnosis |
| 8 | [`18_paper_shadow.md`](18_paper_shadow.md) | Offline shadow replay of the frozen low-volatility rule and the design of the prospective validation still pending |

**What is not published, and why.** Some documents still mention original notebook, script or
`data/experiments/` names from the private workspace. Those artifacts are left out on purpose:
they depend on the full private corpus, are exploratory branches not needed to audit the
deliverable, or duplicate steps summarised in the published notebooks. The repository contains the
code, the decisions and the evidence needed to audit the final numbers, but not the full corpus or
every intermediate run.

**Public notebooks** are pedagogical: they summarise the path without requiring the private
workspace. `notebooks/08_auditoria_final_ledger.ipynb` works only on the anonymised ledger and
reproduces the thesis' final figures.

**Reproducible final audit**, without the private corpus or trained models:

```bash
python scripts/experiments/recompute_final_summary_from_public_ledger.py --check
```

---

*Versión original en español:*

## Guía de lectura de `docs/` (original)

Estos documentos son una versión curada del cuaderno de investigación usado para
construir la memoria. Su función es explicar el arco experimental, no publicar
cada artefacto interno generado durante el trabajo.

## Qué está completo y es canónico

Para seguir la narrativa principal basta con leer, en este orden:

1. `01_sistema_de_datos.md`
2. `04_splits_validacion_temporal.md`
3. `07_stress_de_latencia.md`
4. `10_secuencias_y_orderbook.md`
5. `11_correccion_score_adverse.md`
6. `14_especialista_prestart_h60.md`
7. `16_validacion_fresh.md`
8. `18_paper_shadow.md`

La memoria oficial está en `reports/memoria.pdf`. Si hay una diferencia de
redacción entre un documento histórico y la memoria, la memoria manda.

## Qué no se publica

Algunos documentos conservan referencias a nombres originales de notebooks,
scripts o directorios de `data/experiments/` que pertenecían al workspace
privado. Esos artefactos no se publican porque:

- dependen del corpus completo privado;
- son ramas exploratorias no necesarias para auditar la entrega;
- o duplican pasos resumidos en los notebooks pedagógicos publicados.

Esto es deliberado: el repositorio público contiene el código, las decisiones y
la evidencia necesaria para auditar las cifras finales, pero no el corpus
completo ni cada ejecución intermedia.

## Notebooks públicos

Los notebooks publicados son pedagógicos: resumen el camino del proyecto sin
exigir el workspace privado completo. El notebook final
`notebooks/08_auditoria_final_ledger.ipynb` trabaja solo con el ledger
anonimizado y permite verificar las cifras de la memoria.

## Auditoría final reproducible

Las cifras finales se pueden recalcular desde el ledger público con:

```bash
python scripts/experiments/recompute_final_summary_from_public_ledger.py --check
```

Ese comando no necesita el corpus privado ni modelos entrenados.
