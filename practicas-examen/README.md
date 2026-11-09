# Prácticas de preparación del examen

Operación de Modelos (MUIAAp) · Comillas ICAI

Serie de prácticas cortas y guiadas para repasar lo que entra en el examen:

- **S2–S4:** estructura de proyecto con `uv`, entornos y dependencias, carga y
  uso de un modelo, contratos Pydantic y validadores.
- **S4–S5:** conectar un frontend Streamlit (que viene hecho) con el backend.
- **S8–S10:** proyecto FastAPI, errores sencillos y una API key en cabecera.

Todas las prácticas usan el mismo caso: **riesgo de cancelación de una reserva
de hotel**. Cada práctica parte de la solución de la anterior, así que quien se
atasque puede continuar desde la carpeta `problem/` de la siguiente.

> El dataset es **sintético**: la relación entre variables y cancelación es
> inventada y solo sirve para practicar.

## Itinerario

| # | Semana | Práctica | Qué se practica | Estado |
|---|---|---|---|---|
| [P1](p01-proyecto-uv/) | S2 | Del script al proyecto | `uv init --package`, layout `src/`, dependencias normales y de desarrollo, `.gitignore`, rutas y semilla, comando `uv run entrenar` | Disponible |
| [P2](p02-inferencia-local/) | S3 | Inferencia local separada | `data/` y `model/`, orden de variables, cargar el joblib una sola vez, `predecir()` y un CLI | Disponible |
| [P3](p03-contratos-pydantic/) | S4 | Contratos Pydantic | `Field` con rangos, `Literal`, `extra="forbid"`, `field_validator`, `model_validator` y salida validada | Disponible |
| [P4](p04-artefacto-manifiesto/) | S4 | Artefacto con manifiesto | `model.joblib` + `manifest.json` validado con Pydantic, comprobar las variables al cargar, `version_modelo` en cada predicción | Disponible |
| [P5](p05-streamlit-local/) | S4–S5 | Streamlit → backend local | Completar solo el *gateway* entre el formulario (hecho) y `predecir()`: errores con la etiqueta del formulario y mensaje genérico si falta el modelo | Disponible |
| [P6](p06-fastapi/) | S8 | API FastAPI | Estructura `app/` (main, dependencies, routers), `GET /health`, `POST /predict` con `Depends`, `TestClient` y `dependency_overrides` | Disponible |
| [P7](p07-errores-docs/) | S9 | Errores y documentación | Un error concreto: `503 {"detail": "Modelo no disponible"}` con `HTTPException` en la dependencia; `summary`, `responses`, docstring y ejemplo en `/docs`; dos tests propios | Disponible |
| [P8](p08-api-key/) | S10 | API key | Cabecera `X-API-Key` comparada con `API_KEY` leída de un `.env` (`python-dotenv`); `401` si falta o no coincide; `/health` público; `.env.example` y `.env` en `.gitignore` | Disponible |
| [P9](p09-streamlit-api/) | S5 + S8–S10 | Streamlit → API | Mismo `app.py` que en P5; completar el cliente `httpx` del gateway: `API_URL`, cabecera, timeout y mensajes para 401/422/503 y API caída | Disponible |
| [P10](p10-simulacro-examen/) | Todas | Simulacro de examen (2 h) | Dominio nuevo (retraso de envíos): A) arreglar `pyproject`/`.gitignore`/`.env.example`; B) contrato Pydantic, carga de un payload joblib e inferencia; C) 503, API key, `POST /predict` y cliente `httpx` del Streamlit. `scripts/nota.py` da una nota orientativa por bloques | Disponible |

## Formato de cada práctica

```
pNN-nombre/
  problem/      enunciado, código con TODOs y tests completos
```

- El enunciado es `problem/ENUNCIADO_ALUMNOS.md`.
- Los ficheros indican si están **(HECHO)** o son **(TÚ)**. Los TODOs dan la
  regla y la pista, no la solución.
- Los tests vienen completos y no se modifican. La práctica está terminada
  cuando `uv run pytest` sale en verde.
- Cada `problem/` incluye resuelta la práctica anterior: si te atascas en una,
  puedes seguir con la siguiente y comparar.
- El modelo **no** se versiona (`models/` está en `.gitignore`). Se genera con
  `uv run entrenar` y, a partir de P2, los tests lo generan solos si falta.
- Las soluciones de referencia no están en este repositorio.

## Para el profesor

- `_herramientas/generar_dataset.py` regenera `reservas_hotel.csv` (semilla 42)
  en todas las prácticas que lo usan (P1-P9). P10 genera sus datos en `train.py`.
