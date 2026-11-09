# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/
  config.py          rutas y semilla
  schemas.py         contratos Pydantic: ReservaEntrada y PrediccionSalida
  train.py           entrenamiento (uv run entrenar)
  data/features.py   variables del modelo y preparacion de la fila
  model/cargador.py  carga del joblib (una sola vez)
  inference.py       predecir() y clasificar_riesgo()
  predict.py         CLI (uv run predecir --input ejemplos/reserva.json)
tests/               tests con pytest
```

```bash
uv sync
uv run entrenar
uv run predecir --input ejemplos/reserva.json
uv run pytest
```
