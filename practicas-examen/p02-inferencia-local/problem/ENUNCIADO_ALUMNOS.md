# Práctica 2 - Inferencia local separada del entrenamiento

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de la semana 3

Duración orientativa: **60 minutos**.

## Qué vas a construir

En la práctica 1 dejaste un proyecto que **entrena** y guarda el modelo. Ahora
falta **usarlo**: dada una reserva nueva, devolver la probabilidad de
cancelación y un nivel de riesgo, sin volver a entrenar.

```
ejemplos/reserva.json  ->  preparar_fila()  ->  modelo.joblib  ->  {"probabilidad_cancelacion": 0.12, "riesgo": "bajo"}
                         (data/features.py)   (model/cargador.py)       (inference.py)
```

La idea clave es la **separación de responsabilidades**:

| Pieza | Responsabilidad | No debe saber nada de... |
|---|---|---|
| `data/features.py` | qué variables usa el modelo y en qué orden | cómo se carga el modelo |
| `model/cargador.py` | dónde está el artefacto y cargarlo una vez | qué datos llegan |
| `inference.py` | unir las piezas y traducir la probabilidad a riesgo | ficheros, terminal |
| `predict.py` | leer un JSON de la terminal y mostrar el resultado | sklearn |

## Material que recibes

El proyecto de la práctica 1 ya resuelto, con la nueva estructura. Mira el
`README.md` para ver qué ficheros están **(HECHO)** y cuáles son **(TU)**.

```bash
uv sync
uv run entrenar          # crea models/modelo.joblib
uv run pytest            # al empezar: 1 test en verde y 20 en rojo
```

> Si no ejecutas `uv run entrenar`, los tests entrenan el modelo
> automáticamente la primera vez (mira `tests/conftest.py`).

## El modelo

Recibe 8 variables, **en este orden** (están en `VARIABLES`):

| Variable | Tipo | Ejemplo |
|---|---|---|
| `antelacion_dias` | entero | 30 |
| `noches` | entero | 3 |
| `adultos` | entero | 2 |
| `ninos` | entero | 0 |
| `precio_noche` | decimal | 120.0 |
| `cancelaciones_previas` | entero | 0 |
| `peticiones_especiales` | entero | 1 |
| `canal` | texto: `web`, `agencia` o `telefono` | `"web"` |

El modelo es un `Pipeline` de sklearn que recibe un `DataFrame` con esas
columnas. `modelo.predict_proba(fila)[0][1]` es la probabilidad de cancelación.

Riesgo según la probabilidad: menor de 0,3 → `bajo`; menor de 0,6 → `medio`;
resto → `alto`.

## Qué tienes que hacer

Sigue este orden; cada paso tiene sus tests.

| Paso | Fichero | Qué hacer | Tests |
|---|---|---|---|
| 1 | `data/features.py` | `validar_campos()` y `preparar_fila()` | `test_features.py` (5) |
| 2 | `model/cargador.py` | `cargar_modelo()` con `lru_cache` y error claro si falta el fichero | `test_cargador.py` (3) |
| 3 | `inference.py` | `clasificar_riesgo()` y `predecir()` | `test_inference.py` (9) |
| 4 | `predict.py` | CLI que lee un JSON y devuelve 0 o 1 | `test_cli.py` (3) |
| 5 | `pyproject.toml` | script `predecir` | `test_cli.py::test_comando_predecir_en_pyproject` |

Puedes lanzar solo los tests de un paso:

```bash
uv run pytest tests/test_features.py -v
```

## Cómo probarlo

```bash
uv run pytest
uv sync                                          # tras tocar [project.scripts]
uv run predecir --input ejemplos/reserva.json
```

Prueba también a romper `ejemplos/reserva.json` (borra un campo, añade otro
inventado, deja una coma de más) y comprueba que el CLI muestra un mensaje
claro y no una traza de Python.

## Preguntas de repaso (para el examen)

1. ¿Qué pasaría si `preparar_fila()` construyera el DataFrame con
   `list(datos.values())` en vez de recorrer `VARIABLES`?
2. ¿Por qué `train.py` importa `VARIABLES` desde `data/features.py` en lugar
   de definir su propia lista?
3. ¿Qué ventaja tiene `lru_cache` frente a cargar el joblib en cada llamada?
   ¿Y frente a cargarlo como variable global al importar el módulo?
4. `validar_campos()` detecta campos que faltan o sobran. ¿Qué errores **no**
   detecta? (Piensa en `"adultos": -3` o `"canal": "email"`.) Esto lo resuelve
   la práctica 3 con Pydantic.

## Entrega

`uv run pytest` en verde (21 tests) y `uv run predecir --input ejemplos/reserva.json`
funcionando.
