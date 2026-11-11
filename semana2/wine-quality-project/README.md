Me he hecho unos apuntes de la practica con la IA

# Wine Quality Project

Proyecto de entrenamiento de un modelo de clasificación utilizando el dataset `WineQT.csv`.

## Instalación

Desde la raíz del fork:

```bash
cd semana2/wine-quality-project
uv sync --locked
```

`uv sync --locked` crea o sincroniza el entorno `.venv` usando las versiones guardadas en `uv.lock`.

- `.venv` no se sube a GitHub.
- `uv.lock` sí se sube, porque permite reproducir el mismo entorno.

## Dependencias

Dependencias necesarias para ejecutar el proyecto:

```bash
uv add pandas scikit-learn
```

Dependencias solo de desarrollo:

```bash
uv add --dev pytest ruff
```

- `pytest`: ejecutar tests.
- `ruff`: comprobar el código.

## Estructura

```text
wine-quality-project/
├── data/
│   └── raw/
│       └── WineQT.csv
├── src/
│   └── wine_quality/
│       ├── __init__.py
│       └── train.py
├── tests/
│   └── test_train.py
├── pyproject.toml
├── uv.lock
└── README.md
```

- `data/raw/WineQT.csv`: dataset.
- `src/wine_quality/train.py`: entrenamiento del modelo.
- `tests/test_train.py`: tests.
- `pyproject.toml`: configuración y dependencias.
- `uv.lock`: versiones bloqueadas.

## Comprobaciones

Ejecutar el entrenamiento:

```bash
uv run --frozen python -m wine_quality.train
```

Ejecutar los tests:

```bash
uv run --frozen pytest
```

Comprobar el código con Ruff:

```bash
uv run --frozen ruff check .
```

`--frozen` hace que `uv` utilice el lock actual sin modificarlo.

## Git

Rama de trabajo:

```text
feature/s2-wine-project
```

Subir la rama:

```bash
git push -u origin feature/s2-wine-project
```

Después abrir un Pull Request:

```text
feature/s2-wine-project -> main
```