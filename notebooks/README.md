# Guía de notebooks

Los notebooks de este repositorio cumplen dos funciones:

1. contar el arco experimental de forma pedagógica;
2. permitir auditar las cifras finales sin publicar el corpus privado.

El corpus completo y los directorios `data/experiments/` no se publican por
tamaño y trazabilidad. Por eso algunos notebooks iniciales conservan outputs
históricos ya ejecutados, mientras que los notebooks finales trabajan solo con
CSV públicos del repositorio.

## Lectura recomendada

| Notebook | Papel en la memoria | Estado público |
|---|---|---|
| `00_eda_unificado.ipynb` | Exploración inicial, corpus y primer baseline | Ejecutado con outputs históricos |
| `01_splits_y_validacion.ipynb` | Justificación de validación temporal | Ejecutado con outputs históricos |
| `02_target_y_features.ipynb` | Definición de target y mapa de variables | Ejecutado con outputs históricos |
| `03_baseline_h16.ipynb` | Baseline direccional y primera señal fuerte | Ejecutado con outputs históricos |
| `04_stress_de_latencia.ipynb` | Ruptura entre accuracy y economía por latencia | Ejecutado con outputs históricos |
| `05_secuencias_orderbook.ipynb` | Resumen autocontenido de GRU/Conv1D/fusión | Ejecutable con CSV públicos |
| `06_correccion_adverse.ipynb` | Corrección metodológica del score adverso | Ejecutable con CSV públicos |
| `07_especialista_prestart.ipynb` | Candidato congelado y lectura final | Ejecutable con CSV públicos |
| `08_auditoria_final_ledger.ipynb` | Reproducción de tablas finales desde ledger | Ejecutable con CSV públicos |
| `09_eda_series_temporales.ipynb` | EDA formal de series (ADF/KPSS, ACF, STL, Fourier) | Ejecutable con CSV públicos |
| `10_baselines_clasicos.ipynb` | Baselines de la asignatura (Holt/ARIMA/kNN-DTW) | Ejecutable con CSV públicos |
| `11_regimenes_y_anomalias.ipynb` | Clustering de regímenes (mód. 5) y cruce maker | Ejecutable con CSV públicos |
| `12_economia_maker.ipynb` | Tamaño del premio (B0) y simulador maker (B1) | Ejecutable con CSV públicos |
| `13_fundacionales.ipynb` | Escalera MOMENT, escalado tabular-vs-deep, N1 y N3 | Ejecutable con CSV públicos |

## Auditoría final

Para verificar las cifras principales sin abrir notebooks:

```bash
python scripts/experiments/recompute_final_summary_from_public_ledger.py --check
```

Resultado esperado:

```text
Base OOS @0.5: n=754, mean=+0.349
Low-vol post-hoc @0.5: n=318, mean=+1.069
Market-cluster IC90: [+0.193, +2.004]
Public ledger check: OK
```

