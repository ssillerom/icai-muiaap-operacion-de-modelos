"""Carga del modelo entrenado."""
from functools import lru_cache
from pathlib import Path

import joblib

from reservas.config import RUTA_MODELO


@lru_cache(maxsize=1)
def cargar_modelo(ruta: Path = RUTA_MODELO):
    """Carga el joblib una sola vez y reutiliza el mismo objeto en las siguientes llamadas."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encuentra el modelo en {ruta}. Generalo con: uv run entrenar"
        )
    return joblib.load(ruta)
