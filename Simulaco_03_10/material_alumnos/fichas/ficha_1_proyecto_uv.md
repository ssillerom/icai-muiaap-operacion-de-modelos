# Ejercicio 1 · Crear el entorno y montar el proyecto (30 min, en parejas)

**Caso:** una aseguradora recibe un CSV de siniestros de coche y un modelo ya entrenado decide si cada uno va a **revision manual** (posible fraude) o a **tramitacion normal**. Vais a construir un programa que lo haga. No se entrena nada.

Os damos los ficheros **sueltos en una carpeta** (`material_alumnos/`). Vuestro trabajo aqui es crear el proyecto y dejar cada fichero en su sitio.

## Pasos
1. Crear el proyecto y fijar Python (fuera de la carpeta del material):
   ```bash
   uv init --lib --name claims-triage claims-triage
   cd claims-triage
   uv python pin 3.12      # o la version que tengais
   ```
   `--lib` ya crea `src/claims_triage/` con un `__init__.py` de ejemplo. Mirad que ha creado (`ls -a`, `ls src/claims_triage`).
2. Instalar dependencias:
   ```bash
   uv add pydantic scikit-learn==1.7.2 joblib
   uv add --dev pytest ruff
   ```
   scikit-learn debe ser **exactamente** esa version: el modelo se guardo con ella.
3. Abrid `pyproject.toml` y añadid al final estas lineas (limitan los avisos de estilo a los basicos):
   ```toml
   [tool.ruff]
   line-length = 100

   [tool.ruff.lint]
   select = ["E", "F", "I"]
   ```
4. Crear las carpetas que faltan: `data/`, `models/` y `tests/`.
5. Colocar los ficheros del material:
   - `claims.csv` y `claims_con_errores.csv` -> `data/`
   - `claims_triage_model.joblib` -> `models/`
   - `__init__.py` (sustituye al de ejemplo), `contracts.py`, `preprocess.py`, `inference.py` y `cli.py` -> `src/claims_triage/`
   - los cinco `test_*.py` y `predicciones_esperadas.csv` -> `tests/`
6. Comparad vuestra estructura con la del enunciado (`ls -R`, sin `.venv`).
7. `uv sync` y `uv run pytest`.
8. `git init` y primer commit con `pyproject.toml`, `uv.lock`, el codigo y los tests (`.venv` fuera: ya viene en el `.gitignore`).

## Checkpoint
- `uv run pytest tests/test_smoke.py` en verde (si falla, algun fichero no esta donde debe).
- El resto de tests en **rojo**: es lo esperado, los vais a poner en verde.
- `uv.lock` en el repositorio y `.venv` fuera.

## Pistas
- Si `uv sync` o pytest no encuentran `claims_triage`: comprobad que `src/claims_triage/__init__.py` existe y que los `.py` estan dentro de esa carpeta.
- Los tests buscan `data/` y `models/` en la raiz del proyecto, al lado de `pyproject.toml`.
- Cada fichero del material empieza con un comentario `UBICACION FINAL` que dice donde va.
- Para pensar: ¿que pasa si alguien clona el repo sin `uv.lock`?
