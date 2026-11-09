# Práctica 9 - Conectar el frontend Streamlit con la API

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de las semanas 5, 8, 9 y 10

Duración orientativa: **60 minutos**.

## Qué vas a construir

Cierras el recorrido. En la práctica 5 el frontend llamaba al modelo **dentro
del mismo proceso**. Ahora el modelo vive detrás de la API protegida de las
prácticas 6-8, y el frontend tiene que pedirle las predicciones por HTTP.

```
terminal 2                                         terminal 1
Streamlit                                          uvicorn
frontend/app.py ─> gateway.py ── POST /predict ──> app/ (FastAPI) ─> reservas (modelo)
   (HECHO)          (TU)         X-API-Key         (HECHO)
               <── Respuesta <── 200/401/422/503 ──
```

**`frontend/app.py` es exactamente el mismo fichero que en la práctica 5.** Como
toda la comunicación con el backend estaba aislada en `gateway.py`, ahora solo
cambias ese fichero. Este es el tipo de ejercicio del examen: te dan la interfaz
hecha y tienes que conectarla con el backend.

## Material que recibes

El proyecto de la práctica 8 resuelto. `frontend/gateway.py` mantiene
`Respuesta`, `ETIQUETAS` y los mensajes, pero ya no importa `predecir`: tienes
que implementar el cliente HTTP.

| Configuración | Dónde | Para qué |
|---|---|---|
| `API_URL` | `.env` o entorno | URL base de la API (por defecto `http://localhost:8000`) |
| `API_KEY` | `.env` o entorno | La API la usa para validar y el frontend la envía en `X-API-Key` |

## Qué tienes que hacer

### 0. `httpx` pasa a ser dependencia del proyecto

Hasta ahora `httpx` solo lo usaban los tests (`TestClient`), por eso estaba en
el grupo `dev`. Ahora lo usa el frontend **en ejecución**: si alguien instala
el proyecto con `uv sync --no-dev`, el frontend fallaría. Muévelo:

```bash
uv remove --dev httpx
uv add httpx
uv run entrenar
uv run pytest        # tras moverlo: 111 tests en verde y 18 en rojo
```

### 1-3. El cliente HTTP

Todo está en `frontend/gateway.py`.

| TODO | Qué hacer | Checkpoint |
|---|---|---|
| 1 | `crear_cliente()`: `httpx.Client` con `base_url`, cabecera `X-API-Key` y `timeout` | 112 en verde |
| 2 | `traducir_errores_api()`: del `detail` del 422 a frases con la etiqueta del formulario | 114 en verde |
| 3 | `consultar_modelo()`: `POST /predict` y traducir cada código de estado a una `Respuesta` | 129 en verde |

Tabla de traducción del TODO 3:

| Lo que pasa | `Respuesta` |
|---|---|
| `200` | `ok=True` y `prediccion` validada con `PrediccionSalida` |
| `422` | `ok=False` y un mensaje por campo (`"Adultos: ..."`) |
| `401` | `MENSAJE_NO_AUTORIZADO` |
| `503` | `MENSAJE_MODELO_NO_DISPONIBLE` |
| La API no responde (apagada, URL mal, timeout) | `MENSAJE_API_NO_DISPONIBLE` |
| Cualquier otra cosa (500, 404, un 200 con JSON raro) | `MENSAJE_ERROR_INESPERADO` |

### Cómo se prueba sin arrancar uvicorn

Mira `tests/test_gateway.py`. `consultar_modelo(valores, cliente)` acepta un
cliente opcional, y los tests le pasan:

- el **`TestClient` de FastAPI**, que es un `httpx.Client` conectado a la API
  real en el mismo proceso;
- un `httpx.Client` con **`MockTransport`**, que simula caídas, timeouts y
  respuestas raras.

Por eso es importante que uses el cliente que te pasan y no crees otro.

## Cómo probarlo de verdad

```bash
uv run pytest
cp .env.example .env              # pon tu clave en API_KEY
```

Terminal 1 (Git Bash):

```bash
uv run uvicorn app.main:app --reload
```

Terminal 2:

```bash
uv run streamlit run frontend/app.py
```

| Caso | Qué debe ver el usuario |
|---|---|
| Valores por defecto | Probabilidad, riesgo y `Modelo 1.0.0` |
| 0 adultos | `Adultos: Input should be greater than or equal to 1` |
| 4 adultos y 4 niños | `Reserva: Una habitacion admite...` |
| Para la API (Ctrl+C en la terminal 1) y envía | `No se puede conectar con el servicio...` |
| Arranca la API con otra clave: `API_KEY=otra uv run uvicorn app.main:app` | Mensaje de no autorizado |
| Renombra `models/cancelacion` y reinicia la API | Mensaje de modelo no disponible |

Al terminar, deja `models/cancelacion` y `.env` como estaban.

## Preguntas de repaso (para el examen)

1. ¿Por qué no se ha tenido que modificar `frontend/app.py`? ¿Qué decisión de
   la práctica 5 lo ha hecho posible?
2. El frontend ya no valida con `ReservaEntrada` antes de enviar. ¿Por qué?
   ¿Qué ganarías y qué perderías validando en los dos lados?
3. ¿Qué pasa si no pones `timeout` y la API se queda colgada?
4. ¿Por qué `httpx` ha pasado de `dev` a dependencia del proyecto?
5. ¿Por qué el mensaje del 401 dice "avisa al equipo técnico" y no "introduce
   tu clave"? ¿De quién es la clave: del usuario o del frontend?
6. El frontend sigue importando `PrediccionSalida` del paquete `reservas`. Si
   frontend y API estuvieran en repositorios distintos, ¿cómo compartirías el
   contrato? (Pista: `/openapi.json`.)
7. Si dockerizas los dos servicios (semanas 11-12), ¿qué valor tendría
   `API_URL` en el contenedor del frontend?

## Entrega

`uv run pytest` en verde (129 tests) y una captura de Streamlit con una
predicción servida por la API (con la terminal de uvicorn visible, mostrando el
`POST /predict 200`).
