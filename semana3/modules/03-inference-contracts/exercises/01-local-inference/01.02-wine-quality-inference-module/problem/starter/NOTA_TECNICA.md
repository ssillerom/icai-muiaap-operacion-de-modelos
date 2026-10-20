# Nota técnica — Módulo local de inferencia (S3.2)

## Responsabilidad de cada módulo

- contracts.py: define qué datos son válidos. WineQualityRequest valida las 11 características de entrada (tipos, rangos y sin columnas extra). WineQualityPrediction valida la salida (sample_id, categoría, confianza entre 0 y 1 y versiones).
- preprocess.py: convierte una petición ya validada en el vector del modelo, siguiendo el orden de FEATURE_NAMES. Fija PREPROCESSING_VERSION. No lee ficheros.
- inference.py: carga el .joblib y comprueba antes de usarlo que tiene un estimador con predict y predict_proba, y que su feature_names coincide con FEATURE_NAMES. Predice y devuelve una WineQualityPrediction validada.
- predict_file.py: CLI. Lee el CSV, separa sample_id, valida todas las filas, carga el modelo, predice y escribe el CSV de salida. No carga joblib directamente ni repite el preprocesado.

## Decisiones de diseño

1. Todo o nada. Primero se validan todas las filas y se calculan todas las predicciones; el fichero de salida solo se abre al final. Si cualquier fila, el modelo o una predicción es inválida, el programa muestra el error por stderr, termina con código 2 y no deja ningún CSV parcial.
2. sample_id fuera del vector. sample_id identifica la muestra pero no es una característica: se separa de la fila antes del contrato de entrada y se valida (no vacío) en el contrato de salida. Así nunca puede llegar al modelo.

## Evidencias

- uv run pytest: 11 passed.
- uv run ruff check src tests: All checks passed.
- uv run ruff format --check src tests: 7 files already formatted.
- Comando: uv run python -m model_inference.predict_file --input assets/inference_samples.csv --output .tmp/wine_predictions.csv

Salida:

sample_id,quality_band,confidence,model_version,preprocessing_version
red-001,acceptable,1.0,dummy-test-v1,wine-red-features-v1
red-002,acceptable,1.0,dummy-test-v1,wine-red-features-v1
red-003,acceptable,1.0,dummy-test-v1,wine-red-features-v1
red-004,acceptable,1.0,dummy-test-v1,wine-red-features-v1
red-005,acceptable,1.0,dummy-test-v1,wine-red-features-v1

Nota: no disponía del modelo real del docente (wine_quality_classifier.joblib), así que, como indica el assignment, usé un clasificador de prueba igual al de los tests (DummyClassifier que siempre predice "acceptable"). Por eso todas las filas salen "acceptable" con confianza 1.0. El artefacto no se sube al repositorio (models/ está en .gitignore).
