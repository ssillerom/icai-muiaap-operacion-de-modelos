# Guion docente — Clase 2: taller de módulo local de inferencia

**Resultado:** cada pareja construye en el *starter* un comando local que lee
un CSV, valida y preprocesa cada fila, carga el artefacto entregado y escribe
predicciones sin salida parcial si hay un error.

## Antes de empezar

- Distribuir únicamente
  `exercises/01-local-inference/01.02-wine-quality-inference-module/problem/starter/`.
- Copiar el modelo preentrenado a `starter/models/wine_quality_classifier.joblib`.
  No se entrena ni se modifica durante el taller.
- Pedir que cada pareja trabaje en una copia propia del *starter* y cree
  `.tmp/` localmente; la carpeta está ignorada.
- La solución está en `solutions/` y se mantiene cerrada hasta el debrief.

## Secuencia de 120 minutos

| Minutos | Hito y guía que se da | Trabajo de las parejas | Comprobación docente |
| --- | --- | --- | --- |
| 0–10 | Abrir `problem/readme.md`, ejecutar `uv sync` y `uv run pytest`. Explicar que rojo es el punto de partida. | Instalan y leen el primer fallo, sin editar aún. | Todas entienden que el contrato público es el CLI. |
| 10–25 | “Implementad primero los tipos que el test importa.” Remitir al lienzo de clase 1. | Completan `contracts.py`: entrada estricta, salida con categoría, confianza y versiones. | Pydantic rechaza campos inesperados. |
| 25–45 | “Una sola función transforma solicitud en vector.” Recordar el orden de las 11 características. | Completan `preprocess.py`, incluida la versión del preprocesado. | `sample_id` no aparece en el vector. |
| 45–65 | “El artefacto no es confiable por defecto.” Dar la lista: estimador, versión, nombres y orden. | Completan `load_wine_quality_model()` e `infer_wine_quality()`. | Se comprueba compatibilidad antes de predecir. |
| 65–90 | “El CLI solo orquesta: leer, validar, transformar, inferir y escribir al final.” | Completan `predict_file.py` y lanzan un test cada vez. | Un CSV válido crea las cinco columnas de salida. |
| 90–105 | Entregar tres fallos de aceptación: columna extra, segunda fila inválida y artefacto incompatible. | Hacen pasar los tests de errores. | No queda fichero de salida parcial y el orden del modelo se verifica. |
| 105–115 | Intercambio entre parejas: una ejecuta el CLI de otra y revisa nombres/responsabilidades. | Corrigen solo lo que el test o el contrato demuestran. | `uv run pytest` y Ruff pasan. |
| 115–120 | Debrief con la solución proyectada por capas, no archivo completo de golpe. | Comparan decisiones y anotan una mejora. | Entregan su módulo y comando reproducible. |

## Pistas graduadas (dar solo si una pareja se bloquea)

1. **Contrato:** revisa qué acepta `WineQualityRequest` y qué deben producir
   los tests, no copies valores desde el CSV.
2. **Preprocesado:** fija `FEATURE_NAMES` una vez; usa ese orden para construir
   el vector.
3. **Inferencia:** el objeto cargado debe saber `predict` y `predict_proba`.
   Comprueba su diccionario antes de llamar a cualquiera de ambos.
4. **CLI:** valida todas las filas y conserva las predicciones en memoria antes
   de abrir el CSV de salida.

Si una pista no desbloquea, pedir a la pareja que dibuje los datos que recibe y
devuelve su función. Dar una pregunta, no el siguiente bloque de código.

## Comando de aceptación

Desde la copia de `starter/`:

```bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv run python -m model_inference.predict_file \
  --input assets/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

El comando final usa el modelo distribuido en `models/`. Los tests generan un
artefacto pequeño temporal: así verifican el contrato sin depender de un modelo
grande ni de una descarga.
