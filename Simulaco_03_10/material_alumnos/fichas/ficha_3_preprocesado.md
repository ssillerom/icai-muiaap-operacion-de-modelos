# Ejercicio 3 · Limpiar y categorizar: la funcion `preprocess` (25 min)

El modelo solo entiende **numeros, en un orden concreto**. En `preprocess.py` escribid `preprocess(request)`, que recibe un `ClaimRequest` ya validado y devuelve una lista de 6 numeros en el orden de `FEATURE_NAMES`. Tests: `tests/test_preprocess.py`.

## Dos pasos, nada mas
1. **Limpieza:** si `vehicle_age_years` es `None`, usar `DEFAULT_VEHICLE_AGE` (8.0).
2. **Categorizacion:** `policy_type` pasa a un numero (`policy_code`): `basico` = 0, `terceros_ampliado` = 1, `todo_riesgo` = 2 (columna `policy_code`).

El resto de datos pasan tal cual. `claim_id` **no** entra en la lista.

## Checkpoint
`uv run pytest tests/test_preprocess.py` en verde. Commit.

## Pistas
- El orden importa: el modelo no sabe como se llaman las columnas, solo mira la posicion.
- Para pensar: ¿que pasaria si cambiais el orden de dos elementos de la lista? ¿Dara error?
