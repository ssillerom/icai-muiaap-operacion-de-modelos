"""Carga del modelo: un joblib con el payload {"modelo", "variables", "version"} (B3)."""
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


def cargar_modelo(ruta: Path = RUTA_MODELO) -> ModeloCargado:
    """Carga el payload una sola vez y comprueba que es compatible."""
    # TODO B3:
    #   - el modelo se carga una sola vez y se reutiliza;
    #   - si el fichero no existe: FileNotFoundError que diga como generarlo
    #     ("uv run entrenar");
    #   - si el payload no es un dict con CLAVES_PAYLOAD, o sus variables no son
    #     exactamente VARIABLES: ModeloIncompatible;
    #   - devuelve ModeloCargado(modelo=..., version=...).
    raise NotImplementedError("TODO B3: cargar_modelo")
