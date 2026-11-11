# Práctica 1 - Del script al proyecto con uv

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de la semana 2

Duración orientativa: **45-60 minutos**.

## Qué vas a construir

Un hotel quiere estimar el **riesgo de que una reserva se cancele**. Un
compañero ha dejado un prototipo que funciona en su portátil, pero no es un
proyecto:

```
train.py              entrenamiento sacado de un notebook
reservas_hotel.csv    datos (sintéticos) de 2000 reservas
test_train.py         tests que tu proyecto tiene que pasar (NO MODIFICAR)
```

Problemas del prototipo:

- no declara dependencias ni tiene entorno virtual;
- las rutas dependen de la carpeta desde la que lo ejecutes;
- cada entrenamiento da una métrica distinta (no hay semilla);
- no hay una forma estándar de lanzarlo.

Al terminar tendrás esta estructura, que es la base de todas las prácticas
siguientes:

```
reservas/
  .gitignore
  .python-version
  pyproject.toml
  uv.lock
  README.md
  data/raw/reservas_hotel.csv
  models/                     (lo genera el entrenamiento, no se versiona)
  src/reservas/__init__.py
  src/reservas/train.py
  tests/test_train.py
```

## Pasos

### 1. Crear el proyecto

Desde la carpeta donde quieras crear el proyecto (en Git Bash):

```bash
uv init --package reservas
cd reservas
```

Mira qué ha creado. `--package` genera el layout `src/reservas/` y un
`[build-system]`, de modo que el proyecto se instala en su entorno y puedes
hacer `from reservas import train` desde cualquier sitio (también desde los
tests).

> `uv init` añade en `src/reservas/__init__.py` una función `main()` de ejemplo
> y el script `reservas = "reservas:main"` en el `pyproject.toml`. Puedes
> borrar los dos.

### 2. Declarar dependencias

El prototipo usa `pandas`, `scikit-learn` y `joblib`. `pytest` solo hace falta
para desarrollar, no para ejecutar el modelo.

- Añade las dependencias del proyecto con `uv add`.
- Añade `pytest` como dependencia **de desarrollo** (investiga la opción
  `--dev` de `uv add`).

Comprueba que el `pyproject.toml` tiene `dependencies` y un
`[dependency-groups]` con `dev`, y que se han creado `uv.lock` y `.venv/`.

### 3. Ordenar los ficheros

| Fichero del prototipo | Destino |
|---|---|
| `reservas_hotel.csv` | `data/raw/reservas_hotel.csv` |
| `train.py` | `src/reservas/train.py` |
| `test_train.py` | `tests/test_train.py` |

### 4. Completar los TODOs de `src/reservas/train.py`

| TODO | Qué hay que hacer | Test que lo comprueba |
|---|---|---|
| 1 | Rutas a partir de la raíz del proyecto con `pathlib` (`RAIZ`, `RUTA_DATOS`, `RUTA_MODELO`) | `test_rutas_relativas_a_la_raiz` |
| 2 | Semilla fija usada en `train_test_split` | `test_entrenamiento_reproducible` |
| 3 | `guardar_modelo` crea la carpeta de destino si no existe | `test_guardar_modelo` |

Pista para el TODO 1: el fichero está en `src/reservas/train.py`. ¿Cuántos
niveles hay que subir desde él para llegar a la raíz?

### 5. Un comando para entrenar

Añade al `pyproject.toml` un script de proyecto llamado `entrenar` que ejecute
la función `main` de `reservas.train` (investiga `[project.scripts]`). Después:

```bash
uv sync
uv run entrenar
```

Debe imprimir las métricas y crear `models/modelo.joblib`. Ejecútalo dos veces:
las métricas tienen que ser idénticas.

### 6. Qué no se versiona

Añade al `.gitignore` la carpeta `models/`. El modelo es un **artefacto
generado**: se reconstruye con `uv run entrenar` a partir del código, los datos
y `uv.lock`. Comprueba que `.venv` también está ignorado.

> Si creaste el proyecto dentro de una carpeta que ya era un repositorio git,
> `uv init` **no** genera `.gitignore` (ni ejecuta `git init`). En ese caso
> créalo tú con, al menos, `.venv`, `models/` y `__pycache__/`.

### 7. Comprobar

```bash
uv run pytest
```

Cuando los 8 tests estén en verde, la práctica está terminada.

## Preguntas de repaso (para el examen)

1. ¿Qué diferencia hay entre `dependencies` y el grupo `dev`? ¿Qué instala
   `uv sync --no-dev`?
2. ¿Por qué `uv.lock` **sí** se sube al repositorio y `.venv/` **no**?
3. Un compañero clona tu repositorio. ¿Qué dos comandos necesita para tener el
   modelo entrenado?
4. ¿Qué pasaría con `RUTA_DATOS = "reservas_hotel.csv"` si ejecutas los tests
   desde otra carpeta?
5. ¿Para qué sirve `.python-version`? ¿Y `requires-python`?

## Entrega

Repositorio con el proyecto y `uv run pytest` en verde. **No** subas `.venv/`
ni `models/`.
