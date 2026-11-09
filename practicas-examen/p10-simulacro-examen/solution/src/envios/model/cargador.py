"""Carga del modelo: un joblib con el payload {"modelo", "variables", "version"}."""
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib

from envios.config import RUTA_MODELO
from envios.data.features import VARIABLES

CLAVES_PAYLOAD = {"modelo", "variables", "version"}


class ModeloIncompatible(ValueError):
    """El fichero existe pero no corresponde con el codigo actual (HECHO)."""


@dataclass(frozen=True)
class ModeloCargado:
    """Modelo listo para predecir (HECHO)."""

    modelo: Any
    version: str


@lru_cache(maxsize=1)
def cargar_modelo(ruta: Path = RUTA_MODELO) -> ModeloCargado:
    """Carga el payload una sola vez y comprueba que es compatible."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encuentra el modelo en {ruta}. Generalo con: uv run entrenar")
    payload = joblib.load(ruta)
    if not isinstance(payload, dict) or not CLAVES_PAYLOAD <= payload.keys():
        raise ModeloIncompatible(f"El payload debe ser un dict con las claves {sorted(CLAVES_PAYLOAD)}")
    if payload["variables"] != VARIABLES:
        raise ModeloIncompatible(
            f"El modelo usa {payload['variables']} y el codigo {VARIABLES}"
        )
    return ModeloCargado(modelo=payload["modelo"], version=payload["version"])
