# Práctica 6 - El modelo como API REST con FastAPI

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de la semana 8

Duración orientativa: **60 minutos**.

## Qué vas a construir

El modelo ya funciona desde la terminal (P2-P4) y desde Streamlit (P5), pero en
los dos casos **dentro del mismo proceso** que lo usa. Ahora lo vas a exponer
como un servicio HTTP: cualquier programa (otra web, una app móvil, el
Streamlit de la práctica 9) podrá pedir una predicción con un `POST`.

```
cliente  ──POST /predict {json}──>  FastAPI  ──ReservaEntrada──>  predecir(entrada, artefacto)  ──>  PrediccionSalida
         <──── 200 {json} ────────          (422 si no valida)             ^
                                                                            | Depends(obtener_artefacto)
```

Lo importante es que **casi todo ya lo tienes hecho**. La API es una capa fina
que reutiliza:

| Pieza | De dónde sale |
|---|---|
| Validación del cuerpo de la petición | `ReservaEntrada` (P3), sin cambios |
| Validación y documentación de la respuesta | `PrediccionSalida` (P3-P4) |
| Carga del modelo, una sola vez | `cargar_modelo()` (P4) |
| Inferencia | `predecir(entrada, artefacto)` (P4) |

## Material que recibes

El proyecto de la práctica 5 resuelto, más la carpeta `app/` con la estructura
estándar de una API FastAPI (la misma que en la práctica 8 de clase):

```
app/
  main.py              crea FastAPI y registra los routers        (TU)
  dependencies.py      obtener_artefacto() y ArtefactoDep         (TU)
  routers/health.py    GET /health                                (TU)
  routers/predict.py   POST /predict                              (TU)
tests/test_api.py      tests de la API con TestClient             (HECHO, no tocar)
```

## Qué tienes que hacer

### 0. Dependencias

- `fastapi` y `uvicorn` (el servidor) son dependencias del proyecto.
- `httpx` solo lo necesita `TestClient` en los tests: es de **desarrollo**.

Añádelas con `uv add`. Hasta que no lo hagas, `pytest` se detendrá con
`ModuleNotFoundError: No module named 'fastapi'`.

```bash
uv run entrenar
uv run pytest        # tras añadir las dependencias: 75 en verde y 14 en rojo
```

> Con las versiones más recientes de Starlette puede aparecer un
> `StarletteDeprecationWarning` sobre `httpx`. Es solo un aviso y no afecta a
> los tests.

### 1-4. La API

| TODO | Fichero | Qué hacer | Checkpoint |
|---|---|---|---|
| 1 | `app/main.py` | Registrar los dos routers con `include_router` | |
| 2 | `app/routers/health.py` | `GET /health` → `{"status": "ok"}` | 76 en verde |
| 3 | `app/dependencies.py` | `obtener_artefacto()` devuelve el modelo cargado | 77 en verde |
| 4 | `app/routers/predict.py` | `POST /predict` con `ReservaEntrada`, `ArtefactoDep` y `PrediccionSalida` | 89 en verde |

```bash
uv run pytest tests/test_api.py -v
```

Fíjate en el fixture `modelo_falso` de `tests/test_api.py`: con
`app.dependency_overrides` sustituye el modelo real por uno que siempre
devuelve 0,8. Por eso la ruta **no** debe cargar el modelo por su cuenta: si lo
hiciera, el test no podría sustituirlo.

## Cómo probarlo

```bash
uv run pytest
uv run uvicorn app.main:app --reload
```

Abre `http://localhost:8000/docs` y, desde Swagger UI (**Try it out**), prueba
estos casos:

| Petición | Respuesta esperada |
|---|---|
| `GET /health` | `200 {"status": "ok"}` |
| `POST /predict` con `ejemplos/reserva.json` | `200` con probabilidad, riesgo y `version_modelo` |
| `POST /predict` con `ejemplos/reserva_invalida.json` | `422` con un error por campo en `detail` |
| `POST /predict` con 4 adultos y 4 niños | `422` con el mensaje de capacidad |
| `GET /predict` | `405 Method Not Allowed` |

También desde Git Bash:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @ejemplos/reserva.json
```

## Preguntas de repaso (para el examen)

1. ¿Por qué un dato inválido devuelve `422` sin que se ejecute tu función
   `predict`? ¿Quién genera la respuesta de error?
2. ¿Qué hace exactamente anotar el retorno como `-> PrediccionSalida`? Piensa
   en la validación y en `/docs`.
3. ¿Qué ventaja tiene recibir el modelo con `Depends` en vez de llamar a
   `cargar_modelo()` dentro de la ruta? ¿Cómo lo aprovechan los tests?
4. ¿Qué diferencia hay entre un `404` y un `405`? ¿Cuándo devuelve FastAPI
   cada uno?
5. Para la API y renombra `models/cancelacion`. Vuelve a arrancarla y llama a
   `POST /predict`. ¿Qué código devuelve? ¿Es correcto que sea un error del
   servidor? (Lo arreglarás en la práctica 7.)
6. ¿Por qué `/health` no usa `ArtefactoDep`? ¿Debería decir si el modelo está
   cargado?

## Entrega

`uv run pytest` en verde (89 tests) y una captura de `/docs` con una petición
`POST /predict` que devuelva `200` y otra que devuelva `422`.
