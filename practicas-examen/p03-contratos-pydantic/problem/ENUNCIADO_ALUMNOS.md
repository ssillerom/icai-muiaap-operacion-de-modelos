# Práctica 3 - Contratos de entrada y salida con Pydantic

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de la semana 4

Duración orientativa: **60-75 minutos**.

## Qué vas a construir

En la práctica 2, `validar_campos()` solo comprobaba **qué** campos llegaban.
El modelo aceptaba sin quejarse una reserva con `"adultos": -3`,
`"canal": "email"` o 9 personas en una habitación, y devolvía una probabilidad
que parecía válida pero no tenía sentido.

Ahora vas a escribir el **contrato** del modelo con Pydantic:

```
JSON  ->  ReservaEntrada  ->  preparar_fila()  ->  modelo  ->  PrediccionSalida  ->  JSON
          (valida tipos,                                        (valida la salida)
           rangos y reglas)
```

Si los datos no cumplen el contrato, **el modelo no llega a ejecutarse** y el
usuario recibe un mensaje que dice qué campo corregir.

Este contrato es el mismo que usarás después en la API FastAPI (práctica 6):
lo que escribas aquí lo vas a reutilizar tal cual.

## Material que recibes

El proyecto de la práctica 2 resuelto. `validar_campos()` ha desaparecido de
`data/features.py`: ese trabajo pasa a hacerlo Pydantic. Mira el `README.md`
para ver qué ficheros están **(HECHO)** y cuáles son **(TU)**.

## El contrato

### Entrada: `ReservaEntrada`

| Campo | Tipo | Regla |
|---|---|---|
| `antelacion_dias` | entero | de 0 a 365 |
| `noches` | entero | de 1 a 30 |
| `adultos` | entero | de 1 a 4 |
| `ninos` | entero | de 0 a 4 |
| `precio_noche` | decimal | mayor que 0 y como máximo 1000 |
| `canal` | texto | solo `web`, `agencia` o `telefono`; se aceptan mayúsculas y espacios (`" Web "` → `"web"`) |
| `cancelaciones_previas` | entero | de 0 a 10 |
| `peticiones_especiales` | entero | de 0 a 5 |

Además:

- **No se admiten campos que no estén en la tabla** (`"mascota": "perro"` es un
  error, no se ignora).
- **Regla entre campos:** `adultos + ninos` no puede superar 6 (`MAX_HUESPEDES`).

### Salida: `PrediccionSalida`

| Campo | Tipo | Regla |
|---|---|---|
| `probabilidad_cancelacion` | decimal | entre 0 y 1 |
| `riesgo` | texto | `bajo`, `medio` o `alto` |

## Qué tienes que hacer

### 0. Añadir la dependencia

El proyecto todavía no depende de Pydantic. Añádelo con `uv` (como dependencia
del proyecto, no de desarrollo) y comprueba que aparece en el `pyproject.toml`.

```bash
uv run entrenar
uv run pytest        # tras añadir pydantic: 15 tests en verde y 31 en rojo
```

### 1. `src/reservas/schemas.py` (lo más importante)

| TODO | Qué hacer | Concepto que investigar |
|---|---|---|
| 1 | Rechazar campos que no existan | `model_config = ConfigDict(extra=...)` |
| 2 | Los 8 campos con sus rangos | `Field(ge=..., gt=..., le=...)`, `Literal[...]` |
| 3 | Normalizar `canal` antes de validarlo | `@field_validator(..., mode="before")` + `@classmethod` |
| 4 | Regla de capacidad de la habitación | `@model_validator(mode="after")`, devolver `self` |
| 5 | Contrato de salida | `Field`, `Literal` |

**Checkpoint:** con `schemas.py` terminado, 41 tests en verde.

```bash
uv run pytest tests/test_schemas.py -v
```

### 2. `src/reservas/inference.py`

TODO 6: `predecir()` todavía devuelve un `dict` (versión de la práctica 2).
Haz que devuelva un `PrediccionSalida`.

**Checkpoint:** 43 tests en verde.

### 3. `src/reservas/predict.py`

TODO 7: el CLI construye `ReservaEntrada`. Si los datos no son válidos, muestra
los errores (ya tienes `formatear_errores()`) y termina con código **2**. Así
quien lo usa distingue un fichero que no se puede leer (1) de unos datos
incorrectos (2).

**Checkpoint:** los 46 tests en verde.

## Cómo probarlo

```bash
uv run pytest
uv run predecir --input ejemplos/reserva.json
uv run predecir --input ejemplos/reserva_invalida.json
echo $?              # código de salida del último comando: debe ser 2
```

Con `reserva_invalida.json` deberías ver un error por cada campo incorrecto, y
no una traza de Python.

## Preguntas de repaso (para el examen)

1. ¿Por qué el validador de `canal` tiene que ser `mode="before"`? ¿Qué
   pasaría con `" Web "` si fuera `mode="after"`?
2. ¿Por qué la regla de capacidad es un `model_validator` y no un
   `field_validator` sobre `ninos`?
3. Ejecuta `reserva_invalida.json`: tiene 4 adultos y 4 niños, pero el error de
   capacidad **no aparece**. ¿Por qué? (Pista: ¿cuándo se ejecuta un validador
   `after` si algún campo ya ha fallado?)
4. Prueba `ReservaEntrada(**{..., "noches": "3"})`. ¿Falla? Investiga el modo
   estricto (`strict=True`) y decide si lo querrías para este modelo.
5. ¿Qué ganas validando también la **salida**, si la genera tu propio código?
6. ¿Qué diferencia hay entre `model_dump()` y `model_dump_json()`?

## Entrega

`uv run pytest` en verde (46 tests) y los dos ejemplos del CLI funcionando como
se describe arriba.
