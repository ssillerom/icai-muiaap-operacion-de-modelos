# Práctica 4 - Artefacto del modelo con manifiesto

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de la semana 4

Duración orientativa: **45-60 minutos**.

## Qué vas a construir

Hasta ahora el modelo era un `modelo.joblib` suelto. Si alguien te pasa ese
fichero no sabes qué versión es, con qué variables se entrenó, qué métricas
tenía ni con qué versión de scikit-learn se guardó. Si el código cambia el
orden de `VARIABLES`, el modelo seguirá prediciendo... con las columnas
cambiadas y sin dar ningún error.

Ahora el modelo se guarda como un **artefacto**: una carpeta con el modelo y un
manifiesto que lo describe.

```
models/cancelacion/
  model.joblib       el Pipeline de sklearn
  manifest.json      qué es este modelo
```

```json
{
  "version_modelo": "1.0.0",
  "fecha_entrenamiento": "2026-11-09T10:52:27.427482Z",
  "variables": ["antelacion_dias", "noches", "...", "canal"],
  "metricas": {"filas": 2000.0, "accuracy": 0.7575, "f1": 0.7557},
  "version_sklearn": "1.7.2"
}
```

Al cargar el artefacto se **comprueba el manifiesto antes de usar el modelo**.
Además, cada predicción incluye `version_modelo`, así puedes saber qué modelo
generó cada respuesta.

## Material que recibes

El proyecto de la práctica 3 resuelto, con los cambios ya hechos fuera de
`model/artefacto.py`:

- `config.py`: `RUTA_ARTEFACTO` (carpeta, configurable con `MODEL_DIR`) y
  `VERSION_MODELO`.
- `schemas.py`: `PrediccionSalida` incluye `version_modelo`.
- `cargador.py`: `cargar_modelo()` devuelve un `Artefacto` (modelo + manifiesto).
- `inference.py`: `predecir(entrada, artefacto=None)`. Si le pasas un artefacto
  lo usa; si no, carga el de disco. Esto te servirá en la API para inyectar un
  modelo falso en los tests.
- `train.py`: `main()` llama a `guardar_artefacto()`.

```bash
uv sync
uv run pytest        # al empezar: 37 tests en verde
```

Los 37 tests en verde son la regresión de la práctica 3 y **no deben ponerse en
rojo**. Los demás fallan hasta que completes `model/artefacto.py`.

## El manifiesto

| Campo | Tipo | Valor al guardar |
|---|---|---|
| `version_modelo` | `str` | el parámetro `version` (por defecto `VERSION_MODELO`) |
| `fecha_entrenamiento` | `datetime` | `datetime.now(timezone.utc)` |
| `variables` | `list[str]` | `VARIABLES` |
| `metricas` | `dict[str, float]` | las métricas que devuelve `entrenar()` |
| `version_sklearn` | `str` | `sklearn.__version__` |

## Qué tienes que hacer

Todo está en `src/reservas/model/artefacto.py`.

| TODO | Qué hacer | Tests | Checkpoint |
|---|---|---|---|
| 1 | `Manifiesto` (Pydantic) con los 5 campos | `test_manifiesto_*` | 45 en verde |
| 2 | `guardar_artefacto()` | `test_guardar_*`, `test_contenido_del_manifiesto` | |
| 3 | `leer_manifiesto()` con `model_validate_json` | `test_leer_manifiesto_*` | |
| 4 | `cargar_artefacto()`: manifiesto → compatibilidad → modelo | `test_ida_y_vuelta_*`, `test_cargar_*` | 64 en verde |

```bash
uv run pytest tests/test_artefacto.py -v
```

Cuando termines el TODO 2 ya puedes ejecutar `uv run entrenar` y abrir
`models/cancelacion/manifest.json`.

## Cómo probarlo

```bash
uv run pytest
uv run entrenar
uv run predecir --input ejemplos/reserva.json     # ahora incluye version_modelo
```

Haz también estas pruebas a mano:

1. Edita `manifest.json` y cambia el orden de dos variables. ¿Qué dice
   `uv run predecir`?
2. Borra `model.joblib` y vuelve a predecir.
3. Borra el campo `version_sklearn` del manifiesto. ¿En qué momento falla y con
   qué error?

Después vuelve a ejecutar `uv run entrenar` para dejarlo bien.

## Preguntas de repaso (para el examen)

1. ¿Por qué se comprueba el manifiesto **antes** de cargar el `joblib`?
2. ¿Por qué escribir el manifiesto con `Manifiesto(...).model_dump_json()` y no
   con `json.dump` de un diccionario hecho a mano?
3. `ArtefactoIncompatible` hereda de `ValueError`. ¿Qué ventaja tiene crear una
   excepción propia en vez de lanzar `ValueError` directamente?
4. El manifiesto guarda `version_sklearn` pero no se comprueba al cargar. ¿Qué
   harías si la versión instalada no coincide? ¿Error, aviso o nada?
5. ¿Por qué el artefacto **no** se sube al repositorio, si es tan importante?
   ¿Dónde lo guardarías en un proyecto real? (Piensa en MLflow, semana 1.)

## Entrega

`uv run pytest` en verde (64 tests) y un `manifest.json` generado con
`uv run entrenar`.
