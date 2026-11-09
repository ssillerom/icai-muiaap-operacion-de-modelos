"""Contratos de entrada y salida del modelo."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MAX_KM_NACIONAL = 1500


class EnvioEntrada(BaseModel):
    """Datos de un envio."""

    model_config = ConfigDict(extra="forbid")

    distancia_km: float = Field(gt=0, le=5000)
    peso_kg: float = Field(gt=0, le=70)
    dias_prometidos: int = Field(ge=1, le=15)
    transportista: Literal["rapido", "estandar", "economico"]
    es_internacional: bool
    envios_en_cola: int = Field(ge=0, le=1000)

    @field_validator("transportista", mode="before")
    @classmethod
    def normalizar_transportista(cls, valor):
        if isinstance(valor, str):
            return valor.strip().lower()
        return valor

    @model_validator(mode="after")
    def comprobar_distancia_nacional(self):
        if not self.es_internacional and self.distancia_km > MAX_KM_NACIONAL:
            raise ValueError(
                f"Un envio nacional no puede superar {MAX_KM_NACIONAL} km"
            )
        return self


class PrediccionSalida(BaseModel):
    """Respuesta del modelo."""

    probabilidad_retraso: float = Field(ge=0, le=1)
    nivel: Literal["a_tiempo", "riesgo", "retraso_probable"]
    version_modelo: str
