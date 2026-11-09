# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/
  config.py          rutas y semilla
  schemas.py         contratos Pydantic: ReservaEntrada y PrediccionSalida
  train.py           entrenamiento (uv run entrenar)
  data/features.py   variables del modelo y preparacion de la fila
  model/artefacto.py guardar/cargar model.joblib + manifest.json
  model/cargador.py  carga del artefacto (una sola vez)
  inference.py       predecir() y clasificar_riesgo()
  predict.py         CLI (uv run predecir --input ejemplos/reserva.json)
app/main.py          API FastAPI (registra los routers)
app/dependencies.py  dependencia que entrega el modelo a las rutas (503 si falta)
app/routers/         health.py (GET /health) y predict.py (POST /predict)
frontend/app.py      interfaz Streamlit
frontend/gateway.py  puente entre la interfaz y el backend local
tests/               tests con pytest
```

```bash
uv sync
uv run entrenar
uv run predecir --input ejemplos/reserva.json
uv run uvicorn app.main:app --reload     # API en http://localhost:8000/docs
uv run streamlit run frontend/app.py
uv run pytest
```
