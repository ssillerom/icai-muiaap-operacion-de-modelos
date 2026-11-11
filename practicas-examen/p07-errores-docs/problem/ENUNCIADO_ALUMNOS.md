# Práctica 7 - Un error concreto y una API bien documentada

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de la semana 9

Duración orientativa: **45 minutos**.

## Qué vas a construir

Al final de la práctica 6 viste que, si falta el modelo, `POST /predict`
devuelve **500 Internal Server Error**. Eso le dice al cliente "algo ha
explotado", y además un 500 suele avisar al equipo como si fuera un bug.
Pero no es un bug: la petición era correcta y el servicio simplemente no
puede atenderla **ahora**.

Para eso existe **503 Service Unavailable**:

| Situación | Código | ¿De quién es el problema? |
|---|---|---|
| Datos de la reserva incorrectos | `422` | Del cliente: debe corregir la petición |
| Modelo no disponible | `503` | Del servicio, y temporal: puede reintentar más tarde |
| Bug en nuestro código (`TypeError`...) | `500` | Nuestro: hay que arreglarlo |

Además vas a mejorar `/docs` para que quien use la API sepa qué hace cada
ruta, qué puede responder y con qué datos probarla, sin tener que preguntarte.

## Material que recibes

El proyecto de la práctica 6 resuelto. Mira el `README.md` para ver qué ficheros
tocas.

```bash
uv sync
uv run entrenar
uv run pytest        # al empezar: 93 tests en verde y 12 en rojo
```

## Qué tienes que hacer

| TODO | Fichero | Qué hacer | Checkpoint |
|---|---|---|---|
| 1 | `app/dependencies.py` | Capturar los fallos de carga del modelo y lanzar `HTTPException(503, "Modelo no disponible")` | 99 en verde |
| 2 | `app/routers/predict.py` | `summary`, `responses={503: ...}` y docstring con los códigos 200, 422 y 503 | 102 en verde |
| 3 | `src/reservas/schemas.py` | Ejemplo en el esquema de `ReservaEntrada` con `json_schema_extra` | 103 en verde |
| 4 | `tests/test_alumno.py` | Escribir dos tests propios | 105 en verde |

La respuesta de error tiene que ser **exactamente**:

```json
{"detail": "Modelo no disponible"}
```

Es el formato estándar de `HTTPException` en FastAPI. No añadas el texto de la
excepción: puede contener rutas del servidor.

### Pistas

- El sitio adecuado para el 503 es la **dependencia**, no la ruta: así
  cualquier ruta futura que use `ArtefactoDep` tendrá el mismo comportamiento
  sin repetir código.
- Recuerda el `raise ... from` si quieres conservar la causa en los logs, pero
  **no** la pongas en `detail`.
- `status.HTTP_503_SERVICE_UNAVAILABLE` se lee mejor que un `503` suelto.

## Cómo probarlo

```bash
uv run pytest
uv run uvicorn app.main:app --reload
```

1. Abre `http://localhost:8000/docs`. Comprueba que `POST /predict` muestra el
   resumen, el docstring y la respuesta 503, y que **Try it out** ya viene
   relleno con el ejemplo.
2. Para la API, renombra `models/cancelacion` y vuelve a arrancarla.
   `POST /predict` debe devolver `503`, y `GET /health` seguir devolviendo `200`.
3. Deja la carpeta como estaba.

## Preguntas de repaso (para el examen)

1. ¿Por qué `503` y no `500` ni `404` cuando falta el modelo?
2. ¿Por qué capturar solo esas tres excepciones y no `except Exception`? Mira
   `test_otros_errores_no_se_ocultan_como_503`.
3. Con el modelo ausente y una reserva inválida a la vez, ¿qué responde la
   API, 422 o 503? Pruébalo. ¿Por qué? (Pista: ¿cuándo se ejecutan las
   dependencias?)
4. ¿Qué diferencia hay entre `summary`, el docstring y `description` en
   FastAPI? ¿Dónde aparece cada uno en `/docs`?
5. En tu test 4b limpias `app.dependency_overrides` en un `finally`. ¿Qué
   pasaría con los demás tests si no lo hicieras?
6. `/health` sigue diciendo `ok` aunque falte el modelo. ¿Es correcto? ¿Qué
   distinguirías entre *liveness* y *readiness*?

## Entrega

`uv run pytest` en verde (105 tests) y una captura de `/docs` con la respuesta
503 documentada.
