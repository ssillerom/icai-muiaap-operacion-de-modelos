"""Artefacto del modelo: una carpeta con model.joblib + manifest.json.

El manifiesto describe el modelo (version, variables, metricas, version de
sklearn) para poder comprobar, ANTES de predecir, que el artefacto corresponde
con el codigo que lo va a usar.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import sklearn
from pydantic import BaseModel

from reservas.config import RUTA_ARTEFACTO, VERSION_MODELO
from reservas.data.features import VARIABLES

NOMBRE_MODELO = "model.joblib"
NOMBRE_MANIFIESTO = "manifest.json"


class ArtefactoIncompatible(ValueError):
    """El artefacto existe pero no corresponde con el codigo actual."""


class Manifiesto(BaseModel):
    """Contenido de manifest.json."""

    version_modelo: str
    fecha_entrenamiento: datetime
    variables: list[str]
    metricas: dict[str, float]
    version_sklearn: str


@dataclass(frozen=True)
class Artefacto:
    """Modelo cargado junto con su manifiesto."""

    modelo: Any
    manifiesto: Manifiesto


def guardar_artefacto(
    modelo, metricas: dict, carpeta: Path = RUTA_ARTEFACTO, version: str = VERSION_MODELO
) -> Path:
    """Guarda model.joblib y manifest.json en `carpeta` y devuelve la carpeta."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, carpeta / NOMBRE_MODELO)
    manifiesto = Manifiesto(
        version_modelo=version,
        fecha_entrenamiento=datetime.now(timezone.utc),
        variables=VARIABLES,
        metricas=metricas,
        version_sklearn=sklearn.__version__,
    )
    (carpeta / NOMBRE_MANIFIESTO).write_text(manifiesto.model_dump_json(indent=2), encoding="utf-8")
    return carpeta


def leer_manifiesto(carpeta: Path = RUTA_ARTEFACTO) -> Manifiesto:
    """Lee y valida manifest.json."""
    ruta = Path(carpeta) / NOMBRE_MANIFIESTO
    if not ruta.exists():
        raise FileNotFoundError(f"No se encuentra {ruta}. Generalo con: uv run entrenar")
    return Manifiesto.model_validate_json(ruta.read_text(encoding="utf-8"))


def cargar_artefacto(carpeta: Path = RUTA_ARTEFACTO) -> Artefacto:
    """Lee el manifiesto, comprueba que es compatible y carga el modelo."""
    carpeta = Path(carpeta)
    manifiesto = leer_manifiesto(carpeta)
    if manifiesto.variables != VARIABLES:
        raise ArtefactoIncompatible(
            f"El modelo se entreno con {manifiesto.variables} y el codigo usa {VARIABLES}"
        )
    ruta_modelo = carpeta / NOMBRE_MODELO
    if not ruta_modelo.exists():
        raise FileNotFoundError(f"No se encuentra {ruta_modelo}. Generalo con: uv run entrenar")
    return Artefacto(modelo=joblib.load(ruta_modelo), manifiesto=manifiesto)
