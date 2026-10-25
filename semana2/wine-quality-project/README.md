# Wine Quality Project

Proyecto de entrenamiento de un modelo de clasificación sobre el dataset WineQT.

## Instalación

Desde la raíz del repositorio:

```bash
cd semana2/wine-quality-project
uv sync --locked
```

Este comando sincroniza el entorno virtual utilizando las dependencias fijadas en `uv.lock`.

## Estructura del proyecto

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

- `data/raw/WineQT.csv`: dataset utilizado para el entrenamiento.
- `src/wine_quality/train.py`: código de carga de datos, entrenamiento y evaluación del modelo.
- `tests/test_train.py`: pruebas del pipeline de entrenamiento.
- `pyproject.toml`: configuración del proyecto y sus dependencias.
- `uv.lock`: versiones bloqueadas de las dependencias para garantizar la reproducibilidad.
