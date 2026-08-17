# Documento de defensa del TFM

**Título:** Aprendizaje profundo aplicado a la microestructura de mercados de predicción: predicción de corto plazo en mercados de Bitcoin de Polymarket  
**Autor:** Marc Maldonado Lorca  
**Programa:** Máster de Formación Permanente en Deep Learning, UPM  
**Directora:** Dra. María Inmaculada Santamaría Valenzuela  

Este documento no sustituye a la memoria. Es una guía para defenderla: qué contar, en qué orden, qué números recordar y cómo responder a las preguntas difíciles sin sobreafirmar.

---

## 1. Tesis de la defensa

La idea que debe quedar clara al tribunal es esta:

> Este trabajo no demuestra que exista una estrategia de trading rentable en Polymarket. Demuestra una metodología reproducible para evaluar si hay señal explotable bajo coste y latencia realistas, y muestra que la ejecución domina a la precisión direccional.

La frase corta, para repetir al inicio y al cierre:

> Acertar la dirección no es suficiente: en microestructura, el coste y la latencia deciden.

---

## 2. Mensajes que deben quedar grabados

1. El problema no es predecir si Bitcoin sube o baja al final, sino anticipar movimientos locales del precio de un contrato binario en ventanas de segundos.
2. El sistema combina libro de órdenes de Polymarket con referencias externas de Bitcoin: spot, perpetuos y oráculo.
3. La validación es estrictamente temporal: entrenamiento, validación, test y un bloque fuera de muestra del 6 al 10 de junio de 2026.
4. El resultado más importante es metodológico: un clasificador puede acertar casi el 90 % de la dirección y aun así perder dinero al introducir latencia de entrada.
5. El especialista final conserva una señal modesta fuera de muestra: `+0.349` ticks por unidad al coste de referencia, con 754 unidades y 3 de 5 días positivos.
6. El filtro de baja volatilidad es prometedor, pero es diagnóstico `post-hoc`: `+1.069` ticks en 318 unidades y 5 de 5 días positivos, pero necesita validación prospectiva.
7. **Fe de erratas de comisiones:** el modelo de costes original subestimaba la comisión taker de 2026 en un factor ~8. Con la comisión oficial (`r·p(1-p)`, 1,75 ticks de media a la entrada), **ningún corte taker es positivo** (`-1.059` solo entrada; `-3.304` ida y vuelta). El error se declaró, se selló como fe de erratas y refuerza la tesis: acertar no es ganar.
8. La misma estructura de comisiones abre la vía maker: quien aporta liquidez no paga la comisión y cobra rebates (~20 % del fondo, mismo peso `p(1-p)`). El simulador maker da una banda bruta simulada de `$25-200`/día con el riesgo concentrado en el inventario terminal, no en el spread. Es evidencia para pre-registrar, no rentabilidad afirmada.
9. La escalera se completó con fundacionales: MOMENT (zero-shot → linear-probing → fine-tuning, mejora monótona 45,5 → 46,6 → 47,3 % de acierto) **no bate a naive-drift (53,1 %) ni a ARIMA (56,5 %)**, y la curva de escalado es plana: el techo es el régimen de datos, no la capacidad. El fundacional tabular (TabPFN) sí gana el ranking al GBDT ajustado con un tercio de los datos, sin entrenar.
10. El protocolo está **pre-registrado y sellado en la cadena de Bitcoin** (OpenTimestamps): candidato congelado con hashes, tres brazos de gate comprometidos, expectativa taker declarada negativa por adelantado. Cualquiera puede verificar que el compromiso es anterior a los datos.
11. La defensa honesta es una fortaleza del trabajo: no se afirma rentabilidad real, no se presenta un bot listo para desplegar y se declaran límites.

---

## 3. Estructura recomendada de la presentación

Duración objetivo: 10-12 minutos. Si te dan más tiempo, alarga resultados y preguntas metodológicas; si te dan menos, conserva el arco problema → protocolo → hallazgo → límites.

Las doce diapositivas siguen el arco en cinco actos de `docs/NARRATIVA_MAESTRA_TFM.md` (el documento que gobierna toda la entrega, memoria incluida). Tenerlo presente ayuda a no perder el hilo si el tribunal interrumpe: cada acto cierra con una verdad incómoda que el siguiente convierte en método.

| Acto | Diapositivas | Verdad incómoda → método |
|---|---|---|
| 1. La pregunta y el mercado | 1-2 | Un contrato binario no es Bitcoin → hay que definir con precisión qué se predice |
| 2. Medir antes de opinar | 3 | Sin captura propia de calidad no hay nada que evaluar → sistema multifuente propio |
| 3. Predecible ≠ rentable | 4-9 | El modelo acierta casi el 90 % y aun así pierde dinero → protocolo económico con costes, latencia y régimen |
| 4. La fe de erratas que refuerza | 9b (mitad) | La comisión real es ~8× la modelada: el taker queda estructuralmente muerto → error declarado y sellado |
| 5. El giro maker + validación honesta | 9b (mitad), 10-12 | El valor no desaparece, se desplaza → vía maker cuantificada, pre-registrada y sellada en Bitcoin |

### Diapositiva 1 — Portada

**Objetivo:** situar el trabajo y dar una frase de entrada clara.

**Visual sugerido:** título, autor, UPM, directora, una línea de subtítulo.

**Guion:**

> Buenos días. En este trabajo estudio si señales de microestructura pueden anticipar movimientos de muy corto plazo en mercados de Bitcoin de Polymarket. La idea central no es presentar un bot rentable, sino construir una metodología rigurosa para saber cuándo una señal predictiva sobrevive a costes, latencia y validación temporal.

**Frase clave:** “No defiendo rentabilidad; defiendo una metodología de evaluación.”

### Diapositiva 2 — Problema

**Objetivo:** explicar por qué esto es distinto de predecir Bitcoin.

**Visual sugerido:** contrato binario de Polymarket conectado a BTC spot/perp/oráculo.

**Guion:**

> Un contrato binario de Polymarket no es el precio de Bitcoin. Es una probabilidad negociada: cuánto paga el mercado por un resultado futuro. Aun así, en mercados de Bitcoin está acoplado a referencias externas. El objetivo del trabajo es estudiar si ese acoplamiento genera señales explotables a escala de segundos.

**Frase clave:** “No predigo el evento final; predigo movimientos locales del contrato.”

### Diapositiva 3 — Datos y sistema de captura

**Objetivo:** mostrar que hay ingeniería real detrás del dataset.

**Visual sugerido:** pipeline: Polymarket + spot + perpetuos + oráculo → malla 2 s → control de calidad → corpus.

**Guion:**

> Construí un sistema multifuente que alinea el libro de órdenes de Polymarket, trades, referencias externas y oráculo en una malla temporal de dos segundos. El corpus principal contiene del orden de 2,6 millones de filas. La unidad no es simplemente un mercado, sino una observación temporal del contrato con información causal disponible hasta ese instante.

**Frase clave:** “La parte de datos no es decorativa: define qué se puede afirmar después.”

### Diapositiva 4 — Protocolo de validación

**Objetivo:** anticipar la preocupación por leakage y sobreajuste.

**Visual sugerido:** línea temporal: 11-25 mayo entrenamiento/validación/test; 6-10 junio fuera de muestra.

**Guion:**

> El protocolo está diseñado para evitar autoengaño. Las particiones son temporales, las características son causales y el bloque fuera de muestra —del 6 al 10 de junio de 2026— se captura después de congelar el candidato base. Además, todos los resultados se reportan en ticks netos, incorporando costes de ejecución y latencia.

**Frase clave:** “La evaluación económica es la métrica que decide, no la accuracy.”

### Diapositiva 5 — Primer hallazgo: accuracy no es PnL

**Objetivo:** contar la lección más fuerte del trabajo.

**Visual sugerido:** dos cajas: accuracy cercana al 90 % vs neto negativo con latencia.

**Guion:**

> El primer baseline tabular parecía excelente si se miraba solo la clasificación: aciertos cercanos al 90 %. Pero al introducir una latencia de entrada realista de dos segundos, el resultado económico se vuelve negativo. Esto cambia el eje del trabajo: no basta con acertar la dirección; hay que entrar a un precio que todavía permita capturar valor.

**Frase clave:** “El modelo puede tener razón demasiado tarde.”

### Diapositiva 6 — Escalera de modelos

**Objetivo:** justificar por qué el trabajo usa aprendizaje profundo aunque el candidato final sea tabular.

**Visual sugerido:** escalera: baseline → latency-aware → secuencias/libro → especialista H60.

**Guion:**

> A partir de ahí evalué una progresión de modelos: baselines tabulares, modelos sensibles a latencia, arquitecturas secuenciales y convolucionales sobre el libro, y finalmente un especialista prestart H60. Los modelos profundos aprenden representación, pero con el soporte disponible no producen una política económica estable. La escalera se completó con los fundacionales: MOMENT mejora de forma monótona al adaptarlo —zero-shot, linear-probing, fine-tuning completo— pero ni siquiera el fine-tuning bate a la deriva simple ni a un ARIMA, y su curva de escalado es plana: el techo es el régimen de datos, no la capacidad. En cambio el fundacional tabular, TabPFN, sí gana el ranking al gradient boosting ajustado sin entrenar. Esto también es un resultado: la complejidad no se da por buena, debe ganarse su sitio.

**Frase clave:** “Deep learning sí se evaluó; lo honesto es no promocionarlo si no gana.”

### Diapositiva 7 — Candidato final

**Objetivo:** explicar el especialista congelado sin entrar en demasiada técnica.

**Visual sugerido:** dos cabezas: regresor EV + clasificador healthy fill → regla de entrada.

**Guion:**

> El candidato final es un especialista para la ventana prestart, entre -60 y -45 segundos antes de la apertura del mercado. Usa 36 características causales sin variables de reloj. Tiene dos cabezas: un regresor que estima valor esperado y un clasificador que estima si el relleno será sano. La regla opera solo si ambas condiciones se cumplen.

**Frase clave:** “No intenta operar todo: intenta seleccionar contextos ejecutables.”

### Diapositiva 8 — Resultado fuera de muestra limpio

**Objetivo:** presentar el resultado confirmatorio sin adornarlo.

**Visual sugerido:** tabla de 754 unidades y sensibilidad de coste.

**Números:**

- `n = 754` unidades de acción.
- 5 días: 6-10 junio 2026.
- Coste 0.25: `+0.537` ticks.
- Coste 0.5: `+0.349` ticks.
- Coste 1.0: `-0.026` ticks.
- 3 de 5 días positivos.

**Guion:**

> En el bloque fuera de muestra limpio, sin filtro decidido a partir de esos datos, el especialista selecciona 754 unidades. Al coste de referencia obtiene `+0.349` ticks por unidad, con tres de cinco días positivos. Bajo el coste completo pasa a `-0.026`. La lectura correcta es señal modesta fuera de muestra, no política robusta.

**Frase clave:** “Es positivo, pero no suficiente para afirmar robustez operativa.”

### Diapositiva 9 — Diagnóstico de volatilidad post-hoc

**Objetivo:** explicar el filtro sin venderlo como validación.

**Visual sugerido:** gráfico baja vs alta volatilidad.

**Números:**

- Baja volatilidad: `n = 318`, `+1.069` ticks @0.5.
- Alta volatilidad: `n = 435`, `-0.183` ticks @0.5.
- IC90 agrupado por mercado: `[+0.193, +2.004]`.
- 156 mercados, hasta 8 unidades por mercado.

**Guion:**

> Al analizar el bloque fuera de muestra aparece un cambio de régimen: hay mucha más alta volatilidad que en el entrenamiento. Separando por el umbral de volatilidad aprendido históricamente, la baja volatilidad concentra la señal y la alta volatilidad la destruye. Pero la decisión de usar este filtro se tomó después de observar el bloque, por eso lo presento como diagnóstico post-hoc y no como evidencia confirmatoria.

**Frase clave:** “Prometedor no significa validado.”

### Diapositiva 9b — Fe de erratas y giro maker

**Objetivo:** contar el error de comisiones como fortaleza metodológica y presentar la vía maker.

**Visual sugerido:** izquierda, curva de la comisión oficial `r·p(1-p)` frente a la fórmula errónea (factor 8 en p=0,5); derecha, tabla taker-real (−1,059 / −3,304) y flecha hacia «maker: exento + rebates».

**Números:**

- Comisión oficial 2026: `r·p(1-p)`, `r = 0,07`; en `p = 0,5` son `1,75` ticks/contrato.
- Fórmula errónea: `~0,22` ticks → factor ~8 de subestimación.
- Taker con fee oficial: `-1.059` (solo entrada), `-3.304` (ida y vuelta). Baja volatilidad: `-0.342` / `-2.604`.
- Fondo de rebates maker estimado: `$1.100-3.000`/día en el universo BTC horario.
- Simulador maker: banda bruta simulada `$25-200`/día; markout corto favorable (~`+1` tick); el riesgo vive en el inventario terminal.

**Guion:**

> En la fase final detecté un error en el modelo de costes: la comisión taker de 2026 estaba subestimada en un factor ocho justo en la zona de precios donde opera el trabajo. Lo declaré como fe de erratas sellada y re-evalué la política congelada sin reentrenar nada: con la comisión oficial, ningún corte taker es positivo. Lejos de hundir el trabajo, esto confirma su tesis de forma estructural: la comisión media de entrada supera por sí sola el edge bruto de la señal. Y la misma estructura de comisiones señala la salida: el maker no paga esa comisión, la cobra, con un fondo de rebates de miles de dólares diarios en este universo. El simulador de colas y fills que construí indica que la señal de corto plazo que el taker no podía pagar es exactamente la que el maker cobra, y que el riesgo real está en el inventario que llega vivo a la resolución, no en el spread.

**Frase clave:** “El error, declarado y sellado, refuerza la tesis: el vehículo económico viable es cobrar el spread, no pagarlo.”

### Diapositiva 10 — Limitaciones y ética

**Objetivo:** convertir las limitaciones en rigor, no en debilidad.

**Visual sugerido:** lista corta de límites.

**Guion:**

> Las limitaciones principales son el soporte temporal reducido, la dependencia entre acciones del mismo mercado, la ausencia de fills reales en vivo, la reproducibilidad parcial porque el corpus completo no se publica por tamaño, y que el simulador maker asume que los creadores de mercado incumbentes no reaccionan a mis órdenes —ningún replay histórico puede medir esa respuesta competitiva—. Por eso no se reporta rentabilidad en dólares ni ROI, sino ticks netos y soporte. La postura ética es no convertir un diagnóstico retrospectivo en una promesa económica.

**Frase clave:** “El límite declarado es parte del resultado.”

### Diapositiva 11 — Aportaciones

**Objetivo:** cerrar con contribuciones claras.

**Visual sugerido:** cuatro bloques.

**Aportaciones:**

1. Sistema de captura multifuente y control de calidad por sesión.
2. Protocolo temporal con costes y latencia realistas, **pre-registrado y sellado en la cadena de Bitcoin** (OpenTimestamps): el compromiso es verificable por terceros sin confiar en el autor.
3. Evidencia cuantitativa de la ruptura entre accuracy y política económica.
4. Trazabilidad de resultados negativos, correcciones metodológicas (fe de erratas de comisiones sellada) y artefactos auditables (ledger anonimizado + cuadernos 00-13).

**Guion:**

> La aportación principal no es “este modelo gana”, sino un marco reproducible para evaluar señales de microestructura en mercados de predicción. El trabajo deja código, artefactos, resultados negativos y una hipótesis congelada para validación futura.

**Frase clave:** “La metodología es el entregable.”

### Diapositiva 12 — Cierre

**Objetivo:** terminar con una frase limpia.

**Guion:**

> En resumen: hay señal, pero es frágil; la ejecución importa más que la precisión; y cualquier afirmación económica necesita datos nuevos. El siguiente paso natural es una validación prospectiva con la política congelada, sin retocar umbrales, con una regla de exposición por mercado y registro de fills.

**Frase final:**

> En microestructura, una predicción solo cuenta si sobrevive al mercado.

---

## 4. Guion oral completo, versión 10-12 minutos

Buenos días. En este trabajo estudio si señales de microestructura pueden anticipar movimientos de muy corto plazo en mercados de Bitcoin de Polymarket. Es importante aclarar desde el principio qué se defiende y qué no se defiende. No presento un sistema de trading rentable ni un bot listo para producción. Lo que defiendo es una metodología para evaluar si una señal predictiva sobrevive a condiciones realistas de coste, latencia y validación temporal.

Polymarket es un mercado de predicción. En este caso, los contratos son binarios y están relacionados con el comportamiento futuro de Bitcoin. Pero el precio del contrato no es Bitcoin: es una probabilidad negociada. Aun así, ese precio se mueve influido por referencias externas como el mercado spot, los futuros perpetuos y el oráculo de precios. El objetivo del trabajo es aprovechar ese acoplamiento para anticipar movimientos locales del contrato en ventanas de segundos.

Para poder estudiar esto construí un sistema de captura multifuente. El sistema alinea el libro de órdenes de Polymarket, trades, referencias externas y oráculo en una malla temporal de dos segundos. Sobre esa base se aplica control de calidad por sesión y se construye un corpus con del orden de 2,6 millones de filas. Esta parte es relevante porque en un problema de microestructura los detalles de alineación temporal, latencia y calidad de datos condicionan completamente lo que se puede afirmar después.

El protocolo de validación se diseñó para evitar leakage. Las particiones son temporales y las variables son causales: solo usan información disponible hasta el instante de decisión. Además, el trabajo reserva un bloque fuera de muestra del 6 al 10 de junio de 2026, capturado después de congelar el candidato base. Los resultados no se evalúan solo con métricas de clasificación, sino en ticks netos después de coste y latencia.

El primer hallazgo fuerte del trabajo aparece con un baseline tabular. El modelo alcanza una precisión direccional cercana al 90 %, que a primera vista parece excelente. Pero cuando se introduce una latencia realista de entrada de dos segundos, el resultado económico se vuelve negativo. Esto es la lección central del proyecto: acertar la dirección no basta. El modelo puede tener razón, pero demasiado tarde o a un precio que ya no permite capturar valor.

A partir de ahí evalué una escalera de modelos. Primero, modelos tabulares; después, modelos sensibles a latencia; después, arquitecturas secuenciales y convolucionales sobre el libro de órdenes; y finalmente un especialista prestart H60. Los modelos profundos aprenden representaciones útiles, pero con el volumen de datos disponible no producen una política económica más estable. Por eso el candidato final no es el modelo más complejo, sino el que mejor sobrevive al protocolo económico.

El candidato final es un especialista para la ventana prestart, concretamente entre -60 y -45 segundos antes de la apertura del mercado. Usa 36 características causales y no incluye variables de reloj para evitar atajos temporales. Tiene dos cabezas: un regresor de valor esperado y un clasificador de calidad de relleno. La política opera solo cuando ambas señales son favorables.

En el bloque fuera de muestra limpio, sin aplicar ningún filtro decidido a partir de esos datos, el especialista selecciona 754 unidades de acción. Al coste de referencia obtiene un neto medio de `+0.349` ticks por unidad, con tres de cinco días positivos. En el escenario optimista de coste 0.25 obtiene `+0.537`, y en el escenario de coste completo queda en `-0.026`. Por tanto, la conclusión confirmatoria es una señal positiva pero modesta, no una estrategia robusta.

Después aparece un análisis importante de régimen. El bloque fuera de muestra tiene mucha más alta volatilidad que los periodos históricos. Al separar las acciones por baja y alta volatilidad, el patrón es claro: la baja volatilidad concentra el resultado positivo, con 318 unidades y `+1.069` ticks al coste de referencia; la alta volatilidad cae a `-0.183`. Ahora bien, esta separación se estudia después de observar el bloque, así que se reporta explícitamente como diagnóstico post-hoc. Es una hipótesis prometedora, no una validación confirmatoria.

En la fase final del trabajo detecté un error en el modelo de costes que merece contarse de frente. La comisión taker que Polymarket aplica desde 2026 a los mercados de cripto sigue la fórmula `r·p(1-p)`, máxima justo en la zona de precios donde opera el trabajo; mi implementación original la subestimaba en un factor ocho. Lo declaré como fe de erratas, la sellé con el mismo procedimiento criptográfico que el pre-registro, y re-evalué la política congelada sin reentrenar nada: con la comisión oficial, ningún corte taker es positivo — ni siquiera la cota optimista que solo carga la comisión de entrada. La comisión media de entrada, 1,75 ticks, supera por sí sola el edge bruto de la señal. Este resultado negativo no debilita el trabajo: confirma estructuralmente su tesis. Y la misma estructura de comisiones abre la alternativa: quien aporta liquidez está exento y además cobra parte del fondo de comisiones como rebate. Medí el tamaño de ese premio —entre 1.100 y 3.000 dólares diarios en este universo— y construí un simulador de colas y fills para evaluar la vía maker sin operar: la banda bruta simulada es de 25 a 200 dólares al día, con un hallazgo de diseño claro: la selección adversa de corto plazo es favorable al maker, y el riesgo real vive en el inventario que llega vivo a la resolución del contrato. Por eso la palanca dominante es aplanar inventario antes del tramo terminal, que es exactamente cuando el precio se vuelve informativo según la calibración que medí: en la apertura el precio es casi una moneda al aire sobre el desenlace, y solo en los últimos quince o veinte minutos se vuelve resolutivo.

También completé la escalera de modelos con los fundacionales de series temporales. MOMENT, evaluado en tres regímenes de adaptación creciente, mejora de forma monótona —del 45,5 al 47,3 % de acierto— pero ni siquiera el fine-tuning completo en GPU bate a la deriva simple (53,1 %) ni a un ARIMA (56,5 %); y la curva de escalado es plana: más datos no cierran la brecha. En paralelo, el fundacional tabular TabPFN gana el ranking al gradient boosting ajustado usando un tercio de los datos y sin entrenar. La lectura conjunta es coherente con todo el trabajo: el cuello de botella es el régimen de datos, no la capacidad del modelo, y el tipo de dato que manda aquí es el tabular.

Todo el protocolo de validación futura quedó pre-registrado y sellado en la cadena de Bitcoin con OpenTimestamps: el candidato congelado con sus hashes, tres brazos de gate de régimen comprometidos por adelantado, y la expectativa taker declarada negativa antes de mirar los datos. Cualquier miembro del tribunal puede verificar que el compromiso es anterior a la ventana de evaluación sin confiar en mi palabra.

Las limitaciones son relevantes. El soporte temporal es de cinco días; hay dependencia entre unidades del mismo mercado; no hay fills reales en vivo; el simulador maker asume que los creadores de mercado incumbentes no reaccionan a mis órdenes, algo que ningún replay histórico puede medir; y el corpus completo no se publica por tamaño, aunque sí se publican código, esquema y ledger anonimizado. Por eso todos los resultados se dan en ticks netos con soporte e incertidumbre, y no se convierten en rentabilidad monetaria.

Las aportaciones del trabajo son cuatro. Primero, un sistema de captura y control de calidad multifuente. Segundo, un protocolo de validación temporal que incorpora coste y latencia. Tercero, evidencia cuantitativa de que accuracy y valor económico pueden desacoplarse. Y cuarto, trazabilidad completa del arco experimental, incluyendo resultados negativos y correcciones metodológicas.

En resumen: hay señal, pero es frágil; el coste y la latencia deciden — con la comisión oficial, hasta el punto de invertir el vehículo económico viable, del taker al maker; y tanto el filtro de volatilidad como la vía maker quedan como hipótesis congeladas, pre-registradas y selladas, pendientes de validación prospectiva. La continuación natural es ejecutar esa validación sin retocar umbrales en fechas posteriores, con una regla de exposición por mercado y registro de fills reales.

---

## 5. Números que debes saber de memoria

| Concepto | Valor |
|---|---:|
| Malla temporal | 2 segundos |
| Corpus principal | ~2,6 millones de filas |
| Bloque fuera de muestra | 6-10 junio 2026 |
| Ventana del especialista | -60 a -45 segundos antes de apertura |
| Horizonte final | H60 |
| Unidades OOS limpias | 754 |
| Neto OOS @0.5 | +0.349 ticks |
| Días positivos OOS limpio | 3/5 |
| Neto OOS @1.0 | -0.026 ticks |
| Unidades baja volatilidad post-hoc | 318 |
| Neto baja volatilidad @0.5 | +1.069 ticks |
| Días positivos baja volatilidad | 5/5 |
| Mercados en diagnóstico baja volatilidad | 156 |
| Máximo de acciones por mercado | 8 |
| IC90 agrupado por mercado | [+0.193, +2.004] |
| Drawdown diagnóstico | 88.1 ticks |
| Comisión taker oficial 2026 | r·p(1-p), r=0,07 → 1,75 ticks en p=0,5 |
| Factor de subestimación de la fee errónea | ~8 |
| Taker con fee oficial (n=754) | −1.059 solo entrada / −3.304 ida y vuelta |
| Taker con fee oficial, baja vol (n=318) | −0.342 / −2.604 |
| Fondo de rebates maker (universo BTC horario) | $1.100–3.000/día |
| Banda bruta del simulador maker | $25–200/día (cota optimista) |
| Escalera MOMENT (acierto H60) | 45,5 → 46,6 → 47,3 % (monótona) |
| Baselines clásicos (acierto H60) | naive-drift 53,1 % · ARIMA 56,5 % |
| Brier del precio en apertura | 0,234 (moneda al aire ≈ 0,25; acierto 58 %) |
| Precio informativo | últimos 15–20 min (Brier < 0,10) |
| Latencia real del ciclo de orden (p95) | 0,43 s (se trabaja con 1–2 s) |
| AUC cabeza `healthy` (entrenamiento → fuera de muestra) | 0,79 → 0,56 (casi azar) |
| Diagnóstico del fallo (deep ensemble, 10 semillas) | estable entre semillas (±0,005); no es varianza (0,544→0,547 al promediar) |
| AUC clasificador de dominio mayo-vs-junio | 0,90 (liderado por `perp_basis`) → concept drift, no ruido ni capacidad |

---

## 6. Preguntas difíciles y respuestas recomendadas

### 1. ¿Por qué el título habla de aprendizaje profundo si el candidato final es tabular?

Porque el trabajo sí evalúa aprendizaje profundo en la escalera experimental: GRU, Conv1D, fusión y TCN sobre secuencias y libro de órdenes. El resultado es que, con el soporte disponible, esas arquitecturas aprenden representación pero no generan una política económica estable. El candidato final se elige por evidencia, no por complejidad.

Respuesta corta:

> El deep learning se evaluó; lo que no hago es promocionarlo si no supera el protocolo económico.

### 2. ¿Hay leakage en el filtro de volatilidad?

La respuesta honesta es: el umbral numérico viene del entrenamiento, pero la decisión de convertirlo en filtro se toma después de inspeccionar el bloque fuera de muestra. Por eso no se presenta como validación, sino como diagnóstico post-hoc e hipótesis congelada para datos posteriores.

Respuesta corta:

> No lo vendo como OOS confirmatorio. Es exactamente por eso que lo llamo post-hoc.

### 3. ¿Entonces cuál es el resultado real fuera de muestra?

El resultado confirmatorio es el especialista base sin filtro de volatilidad: 754 unidades, `+0.349` ticks al coste de referencia, 3 de 5 días positivos y `-0.026` bajo coste completo.

Respuesta corta:

> El resultado limpio es modesto: positivo a coste de referencia, no robusto bajo estrés.

### 4. ¿Por qué no reportas ROI o dinero?

Porque traducir ticks a dinero exige suponer tamaño de posición, restricciones de capital, fills reales y exposición simultánea. Eso introduciría supuestos no validados. El tick neto es la unidad natural para comparar señales en el libro.

Respuesta corta:

> Prefiero una métrica menos espectacular pero más honesta.

### 5. ¿Qué significa una “unidad de acción”?

Es una decisión candidata en un instante y contrato concreto. No equivale necesariamente a una operación independiente de cartera, porque puede haber varias unidades relacionadas con el mismo mercado.

Respuesta corta:

> Es una unidad de decisión del replay, no una operación financiera independiente garantizada.

### 6. ¿Por qué el 90 % de accuracy pierde dinero?

Porque la métrica de clasificación no incorpora spread, coste, latencia ni magnitud del movimiento. En microestructura, acertar tarde o con poco margen puede ser económicamente negativo.

Respuesta corta:

> La accuracy mide dirección; el mercado paga ejecución.

### 7. ¿Qué haría falta para afirmar rentabilidad?

Una validación prospectiva posterior al 10 de junio de 2026 con umbrales congelados, registro de fills, control de exposición por mercado, costes reales y suficiente soporte temporal.

Respuesta corta:

> Datos nuevos, política congelada y ejecución registrada.

### 8. ¿Por qué solo cinco días fuera de muestra?

Porque el bloque se capturó después de congelar el candidato y era el soporte disponible en la fecha de entrega. Es suficiente para una prueba inicial, pero no para una afirmación operativa fuerte.

Respuesta corta:

> Cinco días sirven para detectar señal; no para declarar robustez.

### 9. ¿El trabajo es reproducible si no publicas todo el corpus?

Es parcialmente reproducible. Se publica código, esquema, configuración, resultados clave y un ledger anonimizado de las 754 unidades finales. El entrenamiento completo no es bit a bit reproducible sin el corpus privado, y se declara como limitación.

Respuesta corta:

> Reproducible en la auditoría final; parcialmente reproducible en el entrenamiento completo.

### 10. ¿Qué aporta frente a literatura de prediction markets?

El trabajo no se centra en predecir la resolución final del evento, sino el movimiento local del contrato en microestructura de segundos, incorporando costes, latencia y referencias externas.

Respuesta corta:

> El foco está en microestructura y ejecución, no solo en agregación de información.

### 11. ¿Por qué H60 y no otro horizonte?

Porque en la comparación de horizontes H60 conserva señal económica donde H120 y H240 colapsan. Es una decisión empírica dentro del protocolo.

Respuesta corta:

> H60 fue el único horizonte que sobrevivió a coste y validación.

### 12. ¿Por qué usar Polymarket?

Porque combina un contrato binario negociado, libro de órdenes visible y relación clara con referencias externas de Bitcoin. Es un laboratorio interesante para estudiar si la información cross-venue llega al contrato con retraso explotable.

Respuesta corta:

> Polymarket permite estudiar probabilidad negociada con microestructura observable.

### 13. ¿El filtro de volatilidad invalida la memoria?

No. La memoria separa dos evidencias: el OOS limpio del especialista base y el diagnóstico post-hoc del filtro. Lo que invalidaría el trabajo sería mezclarlas; precisamente se corrige esa lectura.

Respuesta corta:

> No lo invalida; obliga a ser preciso sobre qué está validado y qué queda como hipótesis.

### 14. ¿Por qué no desplegar en real?

Porque falta validación prospectiva, control de exposición, fills reales y soporte temporal. Desplegar antes sería convertir un diagnóstico en una promesa.

Respuesta corta:

> El siguiente paso es un registro de sombra prospectivo, no capital real.

### 15. Si con la comisión oficial ningún corte taker es positivo, ¿qué queda del trabajo?

Queda reforzado. El objeto del trabajo nunca fue afirmar rentabilidad, sino medir si una señal sobrevive a las condiciones reales; la comisión oficial es una de esas condiciones y su efecto se midió, se declaró como fe de erratas sellada y se reportó sin adornos. Además, el mismo régimen de comisiones que cierra la vía taker abre la maker, que queda cuantificada (fondo de rebates, simulador de colas y fills) y pre-registrada para validación prospectiva.

Respuesta corta:

> Queda la tesis confirmada estructuralmente y una vía maker cuantificada y pre-registrada.

### 16. ¿El error de la comisión no invalida el resto de números?

No: el error vivía en la capa de costes, no en la señal ni en el protocolo. Como control de integridad, antes de aplicar la comisión oficial se reprodujeron exactamente las cifras publicadas (+0.349 / +1.069). Todas las capas se reportan por separado: la histórica (comparabilidad), la taker-real y la maker simulada.

Respuesta corta:

> La señal no cambia; cambia el vehículo económico. Por eso se reportan las capas por separado.

### 17. ¿Por qué debería creer que el pre-registro es anterior a los datos?

Porque no depende de mi palabra: el documento y la política congelada están atestados con OpenTimestamps en la cadena de Bitcoin. Cualquiera puede ejecutar `ots verify` sobre la prueba publicada y comprobar el bloque —y por tanto la fecha— del compromiso. La atestación de Bitcoin no puede retro-fecharse.

Respuesta corta:

> No hace falta confiar en mí: el sello se verifica contra la cadena de Bitcoin.

### 18. ¿MOMENT no bate ni a un ARIMA — está mal aplicado?

La evaluación se hizo en tres regímenes de adaptación creciente y la mejora es monótona, lo que indica que la adaptación funciona; y la curva de escalado sobre subconjuntos crecientes de datos es plana, lo que descarta que falten datos de entrenamiento en el rango disponible. La lectura no es «MOMENT está roto», sino que a este horizonte el precio apenas contiene estructura direccional explotable por encima de la deriva: el techo lo pone el régimen de datos. El contraste con TabPFN —el fundacional del tipo de dato tabular, que sí gana— apunta a lo mismo.

Respuesta corta:

> La adaptación mejora de forma monótona y el escalado es plano: el techo es el problema, no el modelo.

### 19. ¿Por qué no operar ya la vía maker si el simulador da positivo?

Porque el simulador es una cota optimista declarada: el modelo de fill atribuye todo el flujo del frame a nuestro nivel, no captura la respuesta competitiva de los makers incumbentes, y el corpus no tiene validación prospectiva. Es evidencia suficiente para pre-registrar la validación, no para afirmar rentabilidad.

Respuesta corta:

> El simulador justifica la siguiente prueba, no un despliegue.

### 20. ¿Cuál es tu contribución principal en una frase?

Una metodología auditable —pre-registrada y sellada criptográficamente— para evaluar señales de microestructura en mercados de predicción bajo costes y latencia medidos, mostrando que el valor económico puede desaparecer aunque la predicción direccional parezca excelente, y hacia dónde se desplaza ese valor (el lado maker).

### 21. ¿Qué has cambiado respecto a la versión que no obtuvo el visto bueno?

Es la pregunta más previsible en una defensa que llega tras una primera revisión no superada. La respuesta se ancla en los cuatro puntos concretos que se señalaron y se responde con evidencia, no con promesas:

1. **Estructura y formato.** El glosario estaba como apéndice; ahora está en los preliminares, en su posición correcta, y los anexos se han reordenado (características, hiperparámetros, pre-registro y verificación del sello, auditoría del ledger).
2. **Rigor bibliográfico.** Se pasó de 15 referencias, en su mayoría anteriores a 2020, a 43 referencias todas citadas en el cuerpo, con más de 25 posteriores a 2020 —incluidos los cinco estudios académicos de Polymarket de 2026 y la teoría canónica de market making (Avellaneda-Stoikov, Guéant)—.
3. **Contenido visual.** Se pasó de una memoria con pocas figuras a 26 figuras y 12 tablas: diagrama del sistema, partición temporal, modelo de dos cabezas, escalera de modelos, curva latencia-PnL, EDA completo, fe de erratas de comisiones, diagnóstico de régimen y economía maker.
4. **Análisis técnico de series temporales.** Se añadió un EDA formal con las técnicas de la asignatura —ADF/KPSS de estacionariedad, ACF/PACF, descomposición STL, espectro de Fourier— y una escalera de baselines de la asignatura (naive-drift, ARIMA, Holt, kNN-DTW y el fundacional MOMENT), cada uno con su decisión de diseño asociada.

Además, la memoria creció de 46 a 76 páginas, y se incorporaron dos aportaciones nuevas que no estaban en la versión anterior: la fe de erratas de comisiones sellada y el giro maker cuantificado.

Respuesta corta:

> Se resolvieron los cuatro puntos señalados —estructura, bibliografía, contenido visual y análisis de series temporales— y además el trabajo ganó dos resultados nuevos: la fe de erratas sellada y la vía maker.

### 22. La cabeza `healthy` de la política congelada cae de AUC 0,79 en entrenamiento a 0,56 fuera de muestra —casi azar—. ¿Eso no invalida el resultado sellado?

Es una debilidad conocida y diagnosticada, no oculta. Se descompuso con un *deep ensemble* de diez réplicas con semillas distintas: la caída es estable entre semillas (desviación ±0,005) y el desacuerdo entre réplicas no crece fuera de muestra, lo que descarta que sea varianza —promediar las diez apenas mueve el AUC (0,544→0,547)—. Un clasificador de dominio entrenado para distinguir mayo de junio con las mismas variables lo consigue con AUC 0,90, liderado por la base del perpetuo: las réplicas no fallan por ruido ni por falta de capacidad, fallan porque el régimen de las variables externas cambió. El resultado sellado (`n=754`, `+0,349`) es el que produjo la política congelada tal cual, con este componente incluido; el diagnóstico no lo recalcula ni lo corrige a posteriori. Lo que sí hace es fijar el techo de la siguiente iteración: reentrenar con más datos de mayo no ayuda, hace falta cobertura del régimen de junio.

Respuesta corta:

> No es varianza ni falta de capacidad: es concept drift diagnosticado con un ensemble (dominio AUC 0,90). No cambia el resultado sellado; fija el techo del reentreno v2.

### 23. El runbook fijaba el corte el 10 de agosto y la ventana termina el 13. ¿Por qué se movió la fecha?

No se movió: se acabó. El 14 de agosto a las 11:05 UTC el disco del recolector se desconectó del bus USB de la Raspberry Pi y la captura se detuvo; el último día completo es el 13. El 10 de agosto era una fecha operativa que yo mismo había elegido y que no llegué a ejecutar. Lo que quedó no es una fecha elegida sino la que impuso el hardware, y quedó fijada tres días antes de que se calculara la primera métrica de resultado. El pre-registro sellado no fija un día concreto: fija el inicio de la ventana —10 de julio, excluyendo del 6 al 9 por contaminación de desarrollo— y una puerta de al menos 25 días evaluados. La ventana real tiene 35 días completos, un 40 % por encima de ese mínimo.

Respuesta corta:

> No la moví yo, la cerró un cable. El pre-registro exige ≥25 días y hay 35 completos; el punto de corte quedó fijado antes de mirar ningún resultado.

### 24. ¿Cómo sé que no miró los datos antes y luego decidió cuándo parar?

Por tres cosas comprobables sin fiarse de mí. Primera: el pre-registro está sellado con OpenTimestamps en la cadena de Bitcoin, con atestación completa, y su fecha es anterior al primer día de la ventana. Segunda: el final de la ventana lo produjo un fallo de hardware que dejó su propio rastro independiente —el registro del kernel de la Raspberry Pi, con marca de tiempo, y el contador de sesiones del recolector reiniciado al reanudarse—. Tercera: la evaluación es una sola corrida, y los tres brazos se reportan siempre, salga lo que salga; no hay ninguna configuración que se pueda tocar después, porque las huellas criptográficas de los cinco artefactos ejecutables están en el documento sellado y se verifican en cada corrida.

Respuesta corta:

> Sello en Bitcoin anterior a la ventana, cierre causado por un fallo con rastro propio en el log del sistema, y una única corrida con los tres brazos reportados pase lo que pase.

### 25. Han estado tres días sin capturar. ¿Eso no rompe la continuidad que exige el protocolo?

El hueco va del 14 de agosto a las 11:05 UTC al 17 a las 09:23 UTC, y está fuera de la ventana de evaluación, que termina el 13. Dentro de la ventana no hay ni un solo día incompleto: se verificó día a día sobre el registro de sesiones del recolector, con unas 225 sesiones diarias sostenidas. El protocolo sellado contempla además este caso explícitamente: permite excluir días por fallo de captura siempre que esté documentado en el monitor de la Pi y se cite el log, que es exactamente lo que se hace. La captura está reanudada desde el 17.

Respuesta corta:

> El hueco cae fuera de la ventana. Dentro no falta ningún día, y el protocolo ya contemplaba la exclusión por fallo documentado.

### 26. Si el disco se desconectó mientras escribía, ¿cómo sabe que los datos no están corruptos?

Porque se verificó antes de evaluar nada, y porque el fallo fue de conexión, no de medio. El registro del kernel muestra una desconexión del bus USB y una reconexión limpia tres segundos después, sin un solo error de lectura ni antes ni después; el sistema de ficheros se recuperó reejecutando su diario, que es el mecanismo diseñado para exactamente este caso, y la base de datos quedó cerrada sin transacciones pendientes. Sobre eso se comprobó la cobertura diaria completa de la ventana. Es la misma disciplina que se aplicó al resto del trabajo: no dar por bueno un dato porque el fichero exista.

Respuesta corta:

> Fue una desconexión del bus, no un fallo de medio: cero errores de lectura, diario reejecutado, base cerrada limpia y cobertura verificada día a día antes de evaluar.

### 27. En el anexo el pre-registro dice que el corte nº 1 es el 24 de agosto, y el capítulo 4 evalúa hasta el 13. ¿Cuál de los dos vale?

Son dos documentos encadenados, no dos versiones del mismo. El pre-registro v2 fija el protocolo general y anuncia que el simulador maker, cuando existiera, tendría su propia adenda sellada; esa adenda es el pre-registro del simulador, con su propia ventana desde el 10 de julio. Lo que evalúa el capítulo 4 es la adenda, y su ventana la cerró el fallo de captura. El corte del protocolo general mantiene su propia fecha y su propia ventana.

Respuesta corta:

> No compiten: el segundo es la adenda sellada que el primero anuncia, con su propia ventana. El capítulo 4 reporta la adenda.

### 28. La huella del motor que consta en el pre-registro no coincide con la del motor que ejecutó. ¿No invalida eso el sello?

Al contrario: es lo que hace que el sello sirva de algo. La divergencia es deliberada, está documentada y tiene su propia marca de tiempo. El 13 de julio se detectó que el motor sellado no podía ejecutar el brazo base —fallaba al invocarlo sin señal—, se corrigió y se selló la corrección. Revertir al artefacto original para que las huellas cuadraran habría dado un experimento imposible de correr, no uno más honesto. Lo que un sello garantiza no es que nada cambie, sino que todo cambio quede fechado y sea auditable, y esta cadena —sello, errata, sello de la errata— lo está.

Respuesta corta:

> La divergencia está sellada aparte y documentada. El motor original no podía ejecutar el brazo base; revertir habría roto el experimento, no salvado el sello.

---

## 7. Cosas que conviene no decir

Evita estas frases:

- “El modelo es rentable.”
- “El filtro de volatilidad está validado.”
- “El resultado demuestra que se puede ganar dinero.”
- “El deep learning no funciona.”
- “El dataset es completamente reproducible.”
- “Las 318 acciones son 318 operaciones independientes.”
- “La comisión oficial destruyó el trabajo.”
- “El maker es rentable: el simulador lo demuestra.”
- “La cabeza `healthy` no sirve / es ruido.”

Sustitúyelas por:

- “El modelo conserva una señal modesta fuera de muestra.”
- “El filtro de volatilidad es una hipótesis post-hoc congelada para validación futura.”
- “No afirmo rentabilidad real.”
- “Las arquitecturas profundas no superaron el protocolo económico con este soporte.”
- “La auditoría final es reproducible; el entrenamiento completo requiere el corpus privado.”
- “Son unidades de acción, con dependencia por mercado.”
- “La comisión oficial confirma la tesis y desplaza el valor al lado maker.”
- “El simulador maker es una cota optimista que justifica la validación prospectiva.”
- “Su fallo fuera de muestra es concept drift diagnosticado, no ruido; fija el techo del reentreno v2.”

---

## 8. Transiciones útiles

Para pasar de datos a validación:

> Una vez construido el corpus, la pregunta importante no es solo qué predice el modelo, sino si esa predicción puede evaluarse sin mirar el futuro.

Para pasar de accuracy a coste:

> Aquí aparece la primera sorpresa: el modelo acierta, pero el mercado no paga la dirección; paga la ejecución.

Para pasar de modelos profundos al especialista:

> La escalera experimental no premia la complejidad por sí misma. Por eso el candidato final es el que mejor sobrevive al protocolo, no el más sofisticado.

Para explicar el post-hoc:

> Este resultado es interesante precisamente porque no lo convierto en victoria: lo convierto en hipótesis.

Para cerrar:

> La pregunta futura ya no es “¿funcionó en este bloque?”, sino “¿sobrevive congelado al siguiente?”.

---

## 9. Diapositiva final recomendada

Título:

> Conclusión

Contenido:

```text
1. Accuracy ≠ valor económico.
2. Coste y latencia dominan la microestructura.
3. OOS limpio: señal modesta (+0.349 ticks, n=754); con la fee oficial, el taker es inviable.
4. Baja volatilidad: hipótesis post-hoc prometedora (+1.069 ticks, n=318).
5. El valor se desplaza al lado maker: cuantificado, simulado y pre-registrado.
6. Próximo paso: validación prospectiva congelada y sellada en Bitcoin.
```

Frase de cierre:

> En microestructura, una predicción solo cuenta si sobrevive al mercado.
