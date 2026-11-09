# Práctica 8 - Proteger la API con una API key

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de la semana 10

Duración orientativa: **45 minutos**.

## Qué vas a construir

Ahora mismo cualquiera que conozca la URL puede usar el modelo. Vas a añadir
la seguridad mínima: cada petición a `/predict` debe llevar una **API key** en
la cabecera `X-API-Key`, y la clave correcta se lee de la configuración, nunca
del código.

```
POST /predict
X-API-Key: mi-clave-secreta        <-- se compara con API_KEY (del entorno o de .env)
{ ...reserva... }

  clave correcta     -> 200 / 422 / 503 (como antes)
  falta o no coincide -> 401 {"detail": "API key incorrecta o ausente"}
```

`GET /health` sigue siendo **público**: lo usan los sistemas de monitorización,
que no tienen por qué conocer la clave.

## Material que recibes

El proyecto de la práctica 7 resuelto, más `app/config.py` y `app/security.py`
por completar. Los tests ya existentes envían la cabecera con la clave de
prueba (mira `CABECERAS` y el fixture `api_key_de_test` en `tests/conftest.py`).

## Qué tienes que hacer

### 0. Dependencia

`python-dotenv` lee el fichero `.env`. Añádelo con `uv` como dependencia del
proyecto.

```bash
uv run entrenar
uv run pytest        # tras añadirlo: 108 tests en verde y 11 en rojo
```

### 1-4. La API key

| TODO | Fichero | Qué hacer | Checkpoint |
|---|---|---|---|
| 1 | `app/config.py` | `load_dotenv()` y `obtener_api_key()` (variable vacía = no configurada) | 111 en verde |
| 2 | `app/security.py` | `verificar_api_key()`: `401` si no hay clave configurada, si falta la cabecera o si no coincide | |
| 3 | `app/routers/predict.py` | Proteger el router con `dependencies=[Depends(verificar_api_key)]` y documentar el `401` | 117 en verde |
| 4 | `.env.example` y `.gitignore` | Plantilla con `API_KEY=` y una clave de ejemplo (no la real); `.env` ignorado | 119 en verde |

Los TODO 2 y 3 van juntos: hasta que el router no usa `verificar_api_key`, la
función no se ejecuta.

### Reglas de seguridad que comprueban los tests

- **Cerrado por defecto:** si `API_KEY` no está configurada, no entra nadie.
  Que la API quede abierta por un olvido de configuración es peor que no
  funcione.
- **Mismo mensaje** si falta la cabecera o si la clave es incorrecta. No le des
  pistas a quien está probando claves.
- **Comparación en tiempo constante** con `secrets.compare_digest`.
- **Autenticación antes que validación:** sin una clave válida, la respuesta es
  `401` aunque el cuerpo sea inválido, y el modelo no llega a cargarse.

## Cómo probarlo

```bash
uv run pytest
cp .env.example .env
```

Edita `.env` y pon tu propia clave. Después:

```bash
uv run uvicorn app.main:app --reload
```

En `http://localhost:8000/docs`, `POST /predict` muestra ahora un campo
`x-api-key`. Prueba sin clave, con una clave incorrecta y con la tuya. Desde
Git Bash:

```bash
curl -i -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @ejemplos/reserva.json
curl -i -X POST http://localhost:8000/predict -H "Content-Type: application/json" -H "X-API-Key: TU_CLAVE" -d @ejemplos/reserva.json
```

Comprueba con `git status` que `.env` **no** aparece y `.env.example` **sí**.

## Preguntas de repaso (para el examen)

1. ¿Por qué `401` y no `403`? ¿Cuándo usarías `403`?
2. ¿Por qué se sube `.env.example` al repositorio y `.env` no? ¿Qué debe
   contener cada uno?
3. `load_dotenv()` no pisa las variables que ya existen en el entorno. ¿Por
   qué es lo que quieres en un servidor?
4. ¿Por qué `obtener_api_key()` lee la variable en cada llamada y no una sola
   vez al importar el módulo?
5. ¿Qué diferencia hay entre poner `Depends(verificar_api_key)` en el
   `APIRouter` y ponerlo como parámetro de cada ruta?
6. Una API key en una cabecera, ¿es segura sobre `http://`? ¿Qué falta para
   que lo sea?

## Entrega

`uv run pytest` en verde (119 tests) y `git status` sin `.env`.
