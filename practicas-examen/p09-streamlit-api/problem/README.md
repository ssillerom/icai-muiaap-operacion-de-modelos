# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
src/reservas/          backend: contratos, artefacto e inferencia          (HECHO)
app/                   API FastAPI con 503 y API key (practicas 6-8)       (HECHO)
frontend/app.py        interfaz Streamlit (identica a la practica 5)       (HECHO, no tocar)
frontend/gateway.py    cliente HTTP de la API                              (TU)
.env.example           API_KEY y API_URL                                   (HECHO)
tests/                 tests                                               (HECHO, no tocar)
```

```bash
uv remove --dev httpx && uv add httpx
uv run entrenar
uv run pytest
cp .env.example .env
uv run uvicorn app.main:app --reload       # terminal 1
uv run streamlit run frontend/app.py       # terminal 2
```
