# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/          backend: contratos, artefacto e inferencia          (HECHO)
frontend/app.py        interfaz Streamlit                                  (HECHO, no tocar)
frontend/gateway.py    puente entre la interfaz y el backend local         (TU)
tests/test_gateway.py  tests del puente                                    (HECHO, no tocar)
tests/test_app.py      tests de la app completa con AppTest                (HECHO, no tocar)
```

```bash
uv sync
uv run entrenar
uv run pytest
uv run streamlit run frontend/app.py
```
