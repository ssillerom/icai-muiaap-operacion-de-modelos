# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/
  config.py           rutas, version del modelo y semilla                 (HECHO)
  schemas.py          contratos Pydantic (salida con version_modelo)      (HECHO)
  train.py            entrenamiento (uv run entrenar)                     (HECHO)
  data/features.py    variables del modelo y preparacion de la fila       (HECHO)
  model/artefacto.py  guardar/cargar model.joblib + manifest.json         (TU)
  model/cargador.py   carga del artefacto (una sola vez)                  (HECHO)
  inference.py        predecir()                                          (HECHO)
  predict.py          CLI (uv run predecir --input ejemplos/reserva.json) (HECHO)
tests/                tests con pytest                                    (HECHO, no tocar)
```

```bash
uv sync
uv run pytest
uv run entrenar        # funciona cuando termines el TODO 2
uv run predecir --input ejemplos/reserva.json
```
