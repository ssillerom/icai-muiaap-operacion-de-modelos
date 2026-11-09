"""Carga del artefacto del modelo, una sola vez (HECHO)."""
from functools import lru_cache
from pathlib import Path

from reservas.config import RUTA_ARTEFACTO
from reservas.model.artefacto import Artefacto, cargar_artefacto


@lru_cache(maxsize=1)
def cargar_modelo(carpeta: Path = RUTA_ARTEFACTO) -> Artefacto:
    """Carga el artefacto la primera vez y devuelve el mismo objeto en las siguientes."""
    return cargar_artefacto(carpeta)
