# Ejercicio 4 · Cargar el modelo, predecir y validar la salida (35 min)

Tests: `tests/test_inference.py` y `tests/test_cli.py`. El modelo esta en `models/claims_triage_model.joblib`: es un diccionario con `estimator` (el modelo), `feature_names` y `model_version`.

## Parte A · Modelo de salida, en `contracts.py`
`ClaimPrediction`: `claim_id`, `decision` (solo `revision_manual` o `tramitacion_normal`), `risk_probability` (entre 0 y 1) y `model_version`.

## Parte B · `inference.py`
- `load_model(path)`: cargar el modelo y comprobar que las columnas con las que se entreno son exactamente las que usa vuestro codigo (`FEATURE_NAMES`). Si no, no debe usarse: avisad con un `ValueError`.
- `predict(model, request)`: preparar el siniestro con `preprocess`, pedir al modelo la probabilidad de riesgo (`predict_proba` da una probabilidad por clase, en el orden [no riesgo, riesgo]) y decidir: `revision_manual` si alcanza `THRESHOLD`, `tramitacion_normal` si no. Devolved un `ClaimPrediction`, con la probabilidad redondeada a 3 decimales.

## Parte C · Juntarlo en `cli.py`
```bash
uv run python -m claims_triage.cli --input data/claims.csv --output .tmp/predicciones.csv
```
Leer y validar el CSV (ejercicio 2), cargar el modelo, predecir cada siniestro y escribir el CSV de salida con `claim_id, decision, risk_probability, model_version`. El fichero solo se escribe cuando todo ha ido bien: si hay una fila mala, no debe quedar nada escrito.

## Checkpoint final
- `uv run pytest` todo en verde y `uv run ruff check .` limpio.
- Intercambio: ejecutad el CLI de otra pareja y comparad su salida con `tests/predicciones_esperadas.csv`.
- Commit. Extra si sobra tiempo: rama, `push` y pull request a `main` de **vuestro fork** (no al repo oficial).

## Pistas
- Para pensar: mirad los casos que quedan cerca de 0.5 (C006). ¿Quien deberia decidir el umbral?
