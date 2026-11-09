# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/          backend: contratos, artefacto e inferencia          (HECHO)
app/
  main.py              crea la API y registra los routers                  (TU)
  dependencies.py      dependencia que entrega el modelo a las rutas       (TU)
  routers/health.py    GET /health                                         (TU)
  routers/predict.py   POST /predict                                       (TU)
frontend/              interfaz Streamlit + gateway local (practica 5)     (HECHO)
tests/test_api.py      tests de la API                                     (HECHO, no tocar)
```

```bash
uv add fastapi uvicorn
uv add --dev httpx
uv run entrenar
uv run pytest
uv run uvicorn app.main:app --reload     # http://localhost:8000/docs
```
