# reservas

Modelo de riesgo de cancelacion de reservas de hotel.

```
app/
  main.py               crea la API y registra los routers                 (HECHO)
  config.py             lee API_KEY del entorno / .env                     (TU, TODO 1)
  security.py           verificar_api_key: cabecera X-API-Key              (TU, TODO 2)
  dependencies.py       modelo con 503 si no esta disponible               (HECHO)
  routers/health.py     GET /health (publico)                              (HECHO)
  routers/predict.py    POST /predict protegido                            (TU, TODO 3)
.env.example            plantilla de configuracion sin secretos            (TU, TODO 4)
.gitignore              debe ignorar .env                                  (TU, TODO 4)
tests/                  tests                                              (HECHO, no tocar)
```

```bash
uv add python-dotenv
uv run entrenar
uv run pytest
cp .env.example .env        # y pon tu clave en .env
uv run uvicorn app.main:app --reload
```
