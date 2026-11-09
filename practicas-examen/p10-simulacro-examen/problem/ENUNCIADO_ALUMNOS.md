# Práctica 10 - Simulacro de examen: ¿llegará tarde este envío?

Operación de Modelos (MUIAAp) · Comillas ICAI

Duración: **2 horas**, individual. Puedes consultar la documentación oficial
(uv, Pydantic, FastAPI, httpx, Streamlit) y tus prácticas anteriores.

## Contexto

Una empresa de logística quiere avisar a sus clientes cuando un paquete tiene
muchas probabilidades de llegar tarde. El equipo de datos ha entrenado un
modelo (con datos **sintéticos**) y otro equipo ha hecho la interfaz en
Streamlit. A ti te toca dejar el proyecto bien configurado, escribir el
contrato y la carga del modelo, exponerlo como API protegida y conectar la
interfaz.

```
Streamlit (HECHO)  ->  cliente_api.py (C4)  ->  POST /predict  ->  FastAPI (C1-C3)
                                                X-API-Key            |
                                                                     v
                                     EnvioEntrada (B1) -> cargar_modelo (B3) -> predecir (B4) -> PrediccionSalida (B2)
```

Es un dominio **nuevo**, pero todo lo que necesitas lo has practicado en las
prácticas 1-9. Los comentarios `TODO` de este proyecto son más escuetos que en
las prácticas: el detalle está en este enunciado.

## Arranque

```bash
uv sync
uv run python -m envios.train     # entrena y guarda models/modelo_envios.joblib
uv run pytest                     # al empezar: casi todo en rojo
uv run python scripts/nota.py     # nota orientativa por bloques
```

`models/` no está en el repositorio: los tests generan el modelo si falta.

## Bloque A - Proyecto y entorno (2 puntos)

**A1. `pyproject.toml`** tiene tres problemas. Arréglalos con comandos de `uv`
siempre que sea posible:

- falta el servidor ASGI para poder arrancar la API con `uv run uvicorn ...`;
- `pytest` está declarado como dependencia del proyecto, pero solo se usa para
  desarrollar;
- no existe el comando `uv run entrenar`, que debe ejecutar `envios.train:main`.

**A2. Qué se versiona y qué no:**

- `.gitignore` debe excluir también los modelos generados (`models/`) y el
  fichero de secretos (`.env`);
- crea `.env.example` con las dos variables que usa el proyecto, `API_KEY` y
  `API_URL`, con valores de ejemplo (nunca una clave real).

Tests: `tests/test_a_proyecto.py`.

## Bloque B - Contrato y modelo (4 puntos)

### B1. `EnvioEntrada` (`src/envios/schemas.py`)

| Campo | Tipo | Regla |
|---|---|---|
| `distancia_km` | decimal | mayor que 0 y como máximo 5000 |
| `peso_kg` | decimal | mayor que 0 y como máximo 70 |
| `dias_prometidos` | entero | de 1 a 15 |
| `transportista` | texto | `rapido`, `estandar` o `economico`; se aceptan mayúsculas y espacios (`" RAPIDO "` → `"rapido"`) |
| `es_internacional` | booleano | |
| `envios_en_cola` | entero | de 0 a 1000 |

- No se admiten campos que no estén en la tabla.
- **Regla entre campos:** un envío **no** internacional no puede superar 1500 km
  (`MAX_KM_NACIONAL`). Mensaje: `Un envio nacional no puede superar 1500 km`.

### B2. `PrediccionSalida`

| Campo | Tipo | Regla |
|---|---|---|
| `probabilidad_retraso` | decimal | entre 0 y 1 |
| `nivel` | texto | `a_tiempo`, `riesgo` o `retraso_probable` |
| `version_modelo` | texto | |

### B3. `cargar_modelo()` (`src/envios/model/cargador.py`)

El modelo se guarda como **un solo `joblib` con un diccionario**:

```python
{"modelo": <Pipeline de sklearn>, "variables": [...], "version": "1.0.0"}
```

- Se carga **una sola vez** y se reutiliza.
- Si el fichero no existe: `FileNotFoundError` con un mensaje que diga cómo
  generarlo (`uv run entrenar`).
- Si el contenido no es un diccionario con las tres claves, o sus `variables`
  no son exactamente `VARIABLES` (mismo orden): `ModeloIncompatible`.
- Devuelve un `ModeloCargado` (ya definido).

### B4. Inferencia (`src/envios/inference.py`)

- `clasificar_nivel(p)`: `a_tiempo` si p < 0,35; `riesgo` si p < 0,65;
  `retraso_probable` en el resto. Usa las constantes.
- `predecir(entrada, modelo=None)`: si no recibe `modelo`, usa
  `cargar_modelo()`. La probabilidad de retraso es
  `predict_proba(fila)[0][1]`, redondeada a 4 decimales. La fila se construye
  con `preparar_fila()` (ya hecha).

Tests: `tests/test_b_contrato.py` y `tests/test_b_modelo.py`.

## Bloque C - API e integración (4 puntos)

### C1. `obtener_modelo()` (`app/dependencies.py`)

Si el modelo no se puede cargar (no existe o es incompatible), responde
**503** con `{"detail": "Modelo no disponible"}`. Nunca incluyas el texto de
la excepción.

### C2. `verificar_api_key()` (`app/security.py`)

La cabecera `X-API-Key` debe coincidir con `API_KEY` (la lee
`app/config.obtener_api_key()`, ya hecha). Si no hay clave configurada, si
falta la cabecera o si no coincide: **401** con
`{"detail": "API key incorrecta o ausente"}`. Usa una comparación segura.

### C3. `POST /predict` (`app/routers/predict.py`)

- Todas las rutas del router exigen la API key; `/health` (ya hecho) sigue
  siendo público.
- Cuerpo `EnvioEntrada`, respuesta `PrediccionSalida` y modelo recibido con
  `ModeloDep`.
- Documenta los códigos 401 y 503 en `responses`.
- Sin una clave válida, el modelo **no** debe llegar a cargarse.

### C4. Cliente del frontend (`frontend/cliente_api.py`)

`frontend/app.py` está hecho y **no se toca**: llama a
`cliente_api.consultar(valores)` y espera una `Respuesta`.

- `crear_cliente()`: `httpx.Client` con `base_url=API_URL`, la cabecera
  `X-API-Key` con `API_KEY` y `timeout=TIMEOUT_SEGUNDOS`.
- `consultar(valores, cliente=None)`: `POST /predict` con los valores en JSON.
  Si no recibe cliente, crea uno y lo cierra al terminar.

| Resultado | `Respuesta` |
|---|---|
| `200` | `ok=True`, `prediccion` validada con `PrediccionSalida` |
| `422` | `traducir_errores(json["detail"])` (ya hecha) |
| `401` | `MENSAJE_NO_AUTORIZADO` |
| `503` | `MENSAJE_MODELO_NO_DISPONIBLE` |
| La API no responde (`httpx.RequestError`) | `MENSAJE_API_NO_DISPONIBLE` |
| Cualquier otra cosa (500, un 200 con JSON inválido...) | `MENSAJE_ERROR_INESPERADO` |

Tests: `tests/test_c_api.py` y `tests/test_c_frontend.py`.

## Comprobación final

```bash
uv run python scripts/nota.py
cp .env.example .env
uv run uvicorn app.main:app --reload       # terminal 1
uv run streamlit run frontend/app.py       # terminal 2
```

Prueba en el navegador un envío normal, uno nacional de 2000 km y uno con la
API apagada.

## Normas

- No modifiques los tests, `frontend/app.py` ni los ficheros marcados como
  **HECHO**.
- La nota de `scripts/nota.py` es **orientativa**: en el examen real también
  se valorará la claridad del código y que la aplicación funcione arrancada.
- Entrega: repositorio con el proyecto, sin `.venv/`, `models/` ni `.env`.

## Orden recomendado

A (15 min) → B1-B2 (25 min) → B3-B4 (25 min) → C1-C3 (30 min) → C4 (20 min) →
comprobación final (5 min).

El bloque A es independiente. El C **usa** lo que hagas en el B (los schemas
y `predecir()`), así que conviene terminar B1, B2 y B4 antes de ponerte con la
API. Si te atascas en B3, puedes seguir: los tests de la API inyectan un
modelo falso.
