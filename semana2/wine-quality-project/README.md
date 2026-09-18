# Wine Quality Project

Proyecto Python para entrenar y evaluar un modelo de clasificación utilizando el dataset `WineQT.csv`.

El proyecto está gestionado con `uv` y organizado como un paquete Python.

## Instalación

Desde la raíz del fork, entrar en el proyecto:

```bash
cd semana2/wine-quality-project
```

Instalar las dependencias utilizando las versiones definidas en `uv.lock`:

```bash
uv sync --locked
```

## Estructura

La estructura principal del proyecto es:

```text
semana2/wine-quality-project/
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

## Comprobaciones

### Ejecutar el entrenamiento

El entrenamiento se ejecuta con:

```bash
uv run --frozen python -m wine_quality.train
```

### Ejecutar los tests

Para ejecutar las pruebas:

```bash
uv run --frozen pytest
```

### Comprobar el código con Ruff

Para comprobar el código con Ruff:

```bash
uv run --frozen ruff check .
```