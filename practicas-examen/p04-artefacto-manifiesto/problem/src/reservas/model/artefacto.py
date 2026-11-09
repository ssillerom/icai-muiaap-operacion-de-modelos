"""Artefacto del modelo: una carpeta con model.joblib + manifest.json (TU).

El manifiesto describe el modelo (version, variables, metricas, version de
sklearn) para poder comprobar, ANTES de predecir, que el artefacto corresponde
con el codigo que lo va a usar.

    models/cancelacion/
      model.joblib
      manifest.json
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
    """El artefacto existe pero no corresponde con el codigo actual (HECHO)."""


class Manifiesto(BaseModel):
    """Contenido de manifest.json."""

    # TODO 1: los 5 campos del manifiesto (ver tabla del enunciado) con su tipo:
    #   version_modelo, fecha_entrenamiento (datetime), variables (lista de str),
    #   metricas (diccionario de str a float) y version_sklearn.
    #   Pydantic convertira la fecha ISO del JSON en datetime al leerlo.
    #   Comprobacion: tests/test_artefacto.py::test_manifiesto_*
    pass


@dataclass(frozen=True)
class Artefacto:
    """Modelo cargado junto con su manifiesto (HECHO)."""

    modelo: Any
    manifiesto: Manifiesto


def guardar_artefacto(
    modelo, metricas: dict, carpeta: Path = RUTA_ARTEFACTO, version: str = VERSION_MODELO
) -> Path:
    """Guarda model.joblib y manifest.json en `carpeta` y devuelve la carpeta."""
    # TODO 2: crea la carpeta (con sus padres), guarda el modelo con joblib y
    #   escribe el manifiesto. La fecha es datetime.now(timezone.utc), las
    #   variables son VARIABLES y la version de sklearn es sklearn.__version__.
    #   Construye un Manifiesto y escribelo con model_dump_json(indent=2):
    #   asi el fichero siempre cumple el contrato.
    #   Comprobacion: tests/test_artefacto.py::test_guardar_* y test_contenido_del_manifiesto
    raise NotImplementedError("TODO 2: guardar_artefacto")


def leer_manifiesto(carpeta: Path = RUTA_ARTEFACTO) -> Manifiesto:
    """Lee y valida manifest.json."""
    # TODO 3: si el fichero no existe, FileNotFoundError con un mensaje que diga
    #   como generarlo ("uv run entrenar"). Si existe, validalo con
    #   Manifiesto.model_validate_json (un manifiesto incompleto debe fallar
    #   con ValidationError, no mas tarde con un KeyError).
    #   Comprobacion: tests/test_artefacto.py::test_leer_manifiesto_*
    raise NotImplementedError("TODO 3: leer_manifiesto")


def cargar_artefacto(carpeta: Path = RUTA_ARTEFACTO) -> Artefacto:
    """Lee el manifiesto, comprueba que es compatible y carga el modelo."""
    # TODO 4: en este orden:
    #   1) lee el manifiesto;
    #   2) si sus variables no son exactamente VARIABLES (mismo orden), lanza
    #      ArtefactoIncompatible explicando la diferencia;
    #   3) si falta model.joblib, FileNotFoundError ("uv run entrenar");
    #   4) devuelve Artefacto(modelo=..., manifiesto=...).
    #   Comprobacion: tests/test_artefacto.py::test_ida_y_vuelta_* y test_cargar_*
    raise NotImplementedError("TODO 4: cargar_artefacto")
