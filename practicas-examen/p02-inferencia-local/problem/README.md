# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/
  config.py          rutas y semilla                                  (HECHO)
  train.py           entrenamiento (uv run entrenar)                  (HECHO)
  data/features.py   variables del modelo y preparacion de la fila    (TU)
  model/cargador.py  carga del joblib (una sola vez)                  (TU)
  inference.py       predecir() y clasificar_riesgo()                 (TU)
  predict.py         CLI (uv run predecir --input ejemplos/reserva.json) (TU)
tests/               tests con pytest                                 (HECHO, no tocar)
pyproject.toml       falta el script "predecir"                       (TU)
```

```bash
uv sync
uv run entrenar
uv run predecir --input ejemplos/reserva.json
uv run pytest
```
