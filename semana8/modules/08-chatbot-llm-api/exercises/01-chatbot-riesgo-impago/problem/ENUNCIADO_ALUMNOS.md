# Práctica 8 - Chatbot de riesgo con LLM, FastAPI y un modelo

Operación de Modelos (MUIAAP) · Comillas ICAI

## Qué vas a construir

Un chatbot de solicitudes de préstamo. El usuario escribe en lenguaje natural
("calcula el riesgo para 30 años, ingresos 2500...") y por detrás:

1. El **frontend Streamlit** (ya hecho, con el logo de Comillas) envía la conversación a tu API.
2. Tu **API FastAPI** (`POST /chat`) pasa la conversación a un **LLM**.
3. El LLM decide llamar a una **tool** con los datos del préstamo.
4. Tu código valida esos datos con **Pydantic**, llama al **modelo joblib** y devuelve el resultado al LLM.
5. El LLM redacta la respuesta final.

```
Streamlit  ->  POST /chat  ->  orquestador  <->  LLM
                                   |
                                   v  (tool: calcular_riesgo_impago)
                              Pydantic -> modelo.joblib
```

**Tú haces solo el backend.** El frontend, el cliente del LLM y los tests ya vienen hechos.
Usas lo aprendido en las semanas 1 a 5: contratos con Pydantic (entrada y salida), cargar y
usar un modelo joblib, tests y la demo en Streamlit.

## Material que recibes

Recibes el proyecto ya montado con la estructura estándar de una app FastAPI (ver `README.md`):

```
practica8/
  pyproject.toml          dependencias (sin versiones) y configuración de pytest
  app/
    main.py               API y routers                           (hecho)
    config.py             ajustes                                 (hecho)
    routers/health.py     GET /health                             (hecho)
    routers/predict.py    POST /predict                           (TÚ)
    routers/chat.py       POST /chat                              (TÚ)
    schemas/prestamo.py   Pydantic de entrada y salida            (TÚ)
    schemas/chat.py       contrato del chat con el frontend       (hecho)
    services/modelo.py    cargar joblib y predecir                (TÚ)
    services/orquestador.py  tool + bucle LLM                     (TÚ)
    services/llm.py       cliente LiteLLM + LLM simulado          (hecho, no tocar)
  frontend/app.py         chat en Streamlit con logo              (hecho, no tocar)
  models/modelo_impago.joblib
  scripts/entrenar_modelo.py   solo si el joblib da error de versión
  tests/                  tests completos
```

Instala las dependencias con `uv sync` (sin fijar versión de Python). Incluye **LiteLLM**,
la librería con la que el proyecto habla con el LLM.

## El modelo

Recibe 6 variables, **en este orden** (está en `VARIABLES`):

| Variable | Tipo | Regla |
|---|---|---|
| `edad` | entero | de 18 a 75 |
| `ingresos_mensuales` | decimal | mayor que 0 |
| `importe_prestamo` | decimal | mayor que 0 |
| `plazo_meses` | entero | de 6 a 84 |
| `antiguedad_laboral_anios` | entero | de 0 a 50, y no puede ser mayor que `edad - 16` |
| `impagos_previos` | entero | de 0 a 20 |

`modelo.predict_proba([[...seis valores...]])[0][1]` es la probabilidad de impago.

Decisión según la probabilidad: menor de 0,2 → `aprobar`; menor de 0,5 → `revisar`; resto → `rechazar`.

## Qué tienes que hacer

### 1. `app/schemas/prestamo.py` (Pydantic)
- `PrestamoEntrada`: las 6 variables con sus reglas. Tiene que **rechazar campos que no existan**
  (el LLM a veces se inventa alguno) y validar la regla de antigüedad con un `field_validator`.
- `PrediccionSalida`: `probabilidad_impago` (entre 0 y 1) y `decision`.
- Las clases del chat (`app/schemas/chat.py`) ya están hechas: son el contrato con el frontend.

### 2. `app/services/modelo.py`
Cargar el joblib **una sola vez**, `decidir()` y `predecir()`.

### 3. `app/services/orquestador.py` (lo más importante)
- `definir_tool()`: la definición de la tool para el LLM. Su `parameters` **sale de `PrestamoEntrada`**
  (no escribas los campos a mano: así el contrato es uno solo).
- `ejecutar_tool(nombre, argumentos_json)`: valida los argumentos con Pydantic y llama al modelo.
  Devuelve siempre un diccionario con `"ok"`. Si algo falla (tool desconocida, JSON roto, dato inválido,
  campo inventado) devuelve `{"ok": False, "error": "..."}` en vez de lanzar una excepción,
  para que el LLM pueda corregirse o pedir el dato al usuario.
- `responder(mensajes, llm)`: el bucle. Prepara el historial con el mensaje `system`, pregunta al LLM;
  si pide una tool la ejecuta y le devuelve el resultado como mensaje `tool`; repite hasta que conteste con texto.
  Nunca más de `MAX_VUELTAS` vueltas.

### 4. `app/routers/predict.py` y `app/routers/chat.py`
`POST /predict` y `POST /chat`. `/chat` recibe el LLM con `Depends(get_llm)` (así los tests pueden sustituirlo por uno falso).

## Cómo probarlo

**Tests** (sin LLM, sin red): `uv run pytest`. Cuando todos pasen, tu backend cumple el contrato.

**Con el chatbot completo:**
```
uv run uvicorn app.main:app --port 8000
uv run streamlit run frontend/app.py      (en otra terminal de Git Bash)
```

Por defecto usa un **LLM simulado** (sin cuenta ni coste) que entiende frases como
"edad 30, ingresos 2500, importe 12000, plazo 36, antigüedad 5, impagos 0".

Para usar un LLM real basta con definir `LLM_MODEL` antes de arrancar la API. El cliente usa
[LiteLLM](https://docs.litellm.ai), así que el nombre del modelo lleva delante el proveedor
(`azure/<deployment>`, `ollama/<modelo>`...) y las claves van en las variables de entorno que
pide cada proveedor. Los datos para el LLM real los dará el profesor en clase.

## Entrega

Repositorio en GitHub con el proyecto y `uv run pytest` en verde. Entrega el enlace a la rama o PR final.

## Extra opcional (para la parte de Docker)

Un `Dockerfile` para la API y un `docker-compose.yml` que levante `api` y `streamlit`
(el frontend lee la variable `API_URL`).
