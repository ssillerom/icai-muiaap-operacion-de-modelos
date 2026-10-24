# Ejercicio 2 · Leer el CSV y validarlo con Pydantic (35 min)

Abrid `data/claims.csv` y mirad las columnas. Vais a escribir un modelo Pydantic que describa **una fila**. Tests: `tests/test_contracts.py`.

## Parte A · `ClaimRequest` en `contracts.py`
Un campo por columna:

| Columna | Tipo y limites |
|---|---|
| `claim_id` | texto, no vacio |
| `policy_type` | solo `basico`, `terceros_ampliado` o `todo_riesgo` (`Literal`) |
| `driver_age` | entero entre 18 y 90 |
| `vehicle_age_years` | numero entre 0 y 30, **opcional** (puede venir vacio) |
| `claim_amount_eur` | numero mayor que 0 y hasta 100000 |
| `injuries` | 0 o 1 |
| `police_report` | 0 o 1 |

Y no se admiten columnas que no esten en la lista (`extra="forbid"`).

## Parte B · Leer el CSV y validar, en `cli.py`
Leed el CSV de forma que cada fila llegue como datos de **texto** y validad cada una con `ClaimRequest`. Si una fila no es valida, el programa debe parar diciendo en que linea esta el problema (la cabecera es la 1) y cual es, y terminar con codigo de salida 2. Probad con `data/claims_con_errores.csv`.

## Checkpoint
`uv run pytest tests/test_contracts.py` en verde. Commit.

## Pistas
- Pydantic convierte los textos al tipo que declareis, y falla si no se puede.
- Una celda vacia llega como `""`, que no es un numero. Para ese caso (y solo ese) tenemos una plantilla de validador en `contracts.py` (TODO 2.7): es `@field_validator("vehicle_age_years", mode="before")` sobre un `@classmethod`; `mode="before"` recibe el valor antes de la conversion.
- Cada `ValidationError` indica el campo y el motivo del fallo.
- Para pensar: ¿que pasaria si el modelo recibiera una edad de conductor de 16 y no la hubierais validado?
