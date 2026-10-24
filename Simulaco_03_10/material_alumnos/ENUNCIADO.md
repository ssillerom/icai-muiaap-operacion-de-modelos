# Practica: triaje de siniestros de coche

## Contexto
Una aseguradora recibe un fichero CSV con siniestros de coche. Un modelo de machine learning **ya entrenado** (no lo entrenais) estima la probabilidad de que cada siniestro sea sospechoso. Vuestro programa debe leer el CSV, comprobar que los datos son correctos, prepararlos, ejecutar el modelo y escribir una decision para cada siniestro:

- `revision_manual`: la probabilidad de riesgo es 0.5 o mas.
- `tramitacion_normal`: en caso contrario.

Los datos son inventados y el modelo no sirve para nada real.

## Que teneis que conseguir
Un proyecto que otra persona pueda clonar y ejecutar con este comando:

```bash
uv run python -m claims_triage.cli --input data/claims.csv --output .tmp/predicciones.csv
```

y que genere un CSV con `claim_id, decision, risk_probability, model_version`.

## Que se os da
Todos los ficheros llegan **sueltos, en una sola carpeta**. Montar la estructura del proyecto forma parte del ejercicio 1.

| Fichero | Para que sirve | Va en |
|---|---|---|
| `claims.csv` | 12 siniestros validos | `data/` |
| `claims_con_errores.csv` | filas con errores, para probar la validacion | `data/` |
| `claims_triage_model.joblib` | el modelo ya entrenado | `models/` |
| `__init__.py`, `contracts.py`, `preprocess.py`, `inference.py`, `cli.py` | codigo de partida con `TODO` numerados | `src/claims_triage/` |
| `test_*.py` (5 ficheros) y `predicciones_esperadas.csv` | las pruebas y la salida esperada | `tests/` |

Estructura final que debeis conseguir:

```text
claims-triage/
  pyproject.toml
  uv.lock
  data/
    claims.csv
    claims_con_errores.csv
  models/
    claims_triage_model.joblib
  src/claims_triage/
    __init__.py  contracts.py  preprocess.py  inference.py  cli.py
  tests/
    test_smoke.py  test_contracts.py  test_preprocess.py
    test_inference.py  test_cli.py  predicciones_esperadas.csv
```

Al principio **la mayoria de las pruebas fallan: es normal**. Vuestro objetivo es ponerlas todas en verde.

## Ejercicios
| # | Que hacer | Ficheros | Prueba |
|---|---|---|---|
| 1 | Crear el entorno y el proyecto con `uv` y **montar la estructura de carpetas** colocando cada fichero donde corresponde | `pyproject.toml`, carpetas | `tests/test_smoke.py` |
| 2 | Leer el CSV y validar cada fila con un modelo Pydantic (`ClaimRequest`) | `contracts.py`, `cli.py` | `tests/test_contracts.py` |
| 3 | Escribir `preprocess`: una limpieza y una categorizacion | `preprocess.py` | `tests/test_preprocess.py` |
| 4 | Cargar el modelo, predecir y validar la salida con otro modelo Pydantic (`ClaimPrediction`) | `inference.py`, `contracts.py`, `cli.py` | `tests/test_inference.py`, `tests/test_cli.py` |

Orden de trabajo: seguid los `TODO 2.1`, `2.2`... en orden. Despues de cada ejercicio, ejecutad su prueba y haced un commit.

## Comandos utiles
```bash
uv sync                                  # instala las dependencias
uv run pytest                            # todas las pruebas
uv run pytest tests/test_contracts.py    # solo las de un fichero
uv run ruff check .                      # revisa el estilo
```

## Reglas
- Codigo **simple y legible**, del nivel que hemos visto en clase. Nada de trucos.
- No cambieis `FEATURE_NAMES` ni los tests.
- Trabajad en parejas. Cuando acabeis, ejecutad el programa de otra pareja y comparad su salida con `tests/predicciones_esperadas.csv`.

## Entrega / comprobacion final
1. `uv run pytest` sin ningun fallo.
2. `uv run ruff check .` sin avisos.
3. El comando de arriba genera el CSV de salida.
4. Repositorio con `pyproject.toml`, `uv.lock`, el codigo y los tests (opcional: rama + push + pull request a `main` de **vuestro fork**).

## Preguntas para pensar (no se entregan)
1. ¿Que pasa si el CSV trae una columna que no esta en el contrato? ¿Y una edad de 16 anos?
2. ¿Por que `claim_id` no entra en el vector del modelo?
3. ¿Que pasaria si cambiais el orden de dos elementos en `preprocess`?
4. Un siniestro con probabilidad 0.51: ¿quien deberia decidir el umbral?
