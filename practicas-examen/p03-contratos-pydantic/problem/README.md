# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/
  config.py          rutas y semilla                                      (HECHO)
  schemas.py         contratos Pydantic: ReservaEntrada y PrediccionSalida (TU)
  train.py           entrenamiento (uv run entrenar)                      (HECHO)
  data/features.py   variables del modelo y preparacion de la fila        (HECHO)
  model/cargador.py  carga del joblib (una sola vez)                      (HECHO)
  inference.py       predecir() devuelve PrediccionSalida                 (TU)
  predict.py         CLI con errores de validacion legibles               (TU)
ejemplos/            reserva.json (valida) y reserva_invalida.json
tests/               tests con pytest                                     (HECHO, no tocar)
```

```bash
uv add pydantic
uv run entrenar
uv run predecir --input ejemplos/reserva.json
uv run pytest
```
