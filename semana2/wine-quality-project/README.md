# wine-quality

Entrenamiento reproducible del caso Wine (S1) como proyecto uv.

## Estructura

- `data/raw/WineQT.csv`: dataset original (no se modifica)
- `src/wine_quality/train.py`: entrenamiento y evaluación
- `tests/test_train.py`: test de datos y reproducibilidad

## Instalación (desde la raíz del fork)

```bash
cd semana2/wine-quality-project
uv sync --locked
```

## Ejecución

```bash
uv run --frozen python -m wine_quality.train
```

## Comprobaciones

```bash
uv run --frozen pytest
uv run --frozen ruff check .
```