"""Contratos de entrada y salida del modelo (B1 y B2). Reglas en el enunciado."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MAX_KM_NACIONAL = 1500


class EnvioEntrada(BaseModel):
    """Datos de un envio."""

    # TODO B1: contrato de entrada (tabla del enunciado):
    #   - rechazar campos desconocidos;
    #   - los 6 campos con su tipo y sus rangos;
    #   - `transportista` normalizado (espacios y mayusculas) antes de validarlo;
    #   - regla entre campos: un envio NO internacional no puede superar
    #     MAX_KM_NACIONAL km. Mensaje: "Un envio nacional no puede superar 1500 km".
    pass


class PrediccionSalida(BaseModel):
    """Respuesta del modelo."""

    # TODO B2: probabilidad_retraso (0 a 1), nivel ("a_tiempo", "riesgo" o
    #   "retraso_probable") y version_modelo (texto).
    pass
