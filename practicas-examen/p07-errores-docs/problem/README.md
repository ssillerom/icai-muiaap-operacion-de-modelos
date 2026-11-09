# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/schemas.py   ejemplo para /docs                               (TU, TODO 3)
app/
  main.py                 crea la API y registra los routers               (HECHO)
  dependencies.py         503 si el modelo no esta disponible              (TU, TODO 1)
  routers/health.py       GET /health                                      (HECHO)
  routers/predict.py      summary, responses y docstring                   (TU, TODO 2)
frontend/                 interfaz Streamlit + gateway local               (HECHO)
tests/test_alumno.py      tus propios tests                                (TU, TODO 4)
tests/                    resto de tests                                   (HECHO, no tocar)
```

```bash
uv sync
uv run entrenar
uv run pytest
uv run uvicorn app.main:app --reload     # http://localhost:8000/docs
```
