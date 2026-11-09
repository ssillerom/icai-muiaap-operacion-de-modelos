"""Contratos de entrada y salida del modelo."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MAX_HUESPEDES = 6

# Ejemplo que aparece en /docs al pulsar "Try it out"
EJEMPLO_RESERVA = {
    "antelacion_dias": 30,
    "noches": 3,
    "adultos": 2,
    "ninos": 0,
    "precio_noche": 120.0,
    "canal": "web",
    "cancelaciones_previas": 0,
    "peticiones_especiales": 1,
}


class ReservaEntrada(BaseModel):
    """Datos de una reserva que recibe el modelo."""

    model_config = ConfigDict(extra="forbid", json_schema_extra={"examples": [EJEMPLO_RESERVA]})

    antelacion_dias: int = Field(ge=0, le=365, description="Dias entre la reserva y la llegada")
    noches: int = Field(ge=1, le=30)
    adultos: int = Field(ge=1, le=4)
    ninos: int = Field(ge=0, le=4)
    precio_noche: float = Field(gt=0, le=1000, description="Precio por noche en euros")
    canal: Literal["web", "agencia", "telefono"]
    cancelaciones_previas: int = Field(ge=0, le=10)
    peticiones_especiales: int = Field(ge=0, le=5)

    @field_validator("canal", mode="before")
    @classmethod
    def normalizar_canal(cls, valor):
        """Acepta " Web " o "AGENCIA": quita espacios y pasa a minusculas antes de validar."""
        if isinstance(valor, str):
            return valor.strip().lower()
        return valor

    @model_validator(mode="after")
    def comprobar_capacidad(self):
        """Regla entre campos: una habitacion admite como maximo MAX_HUESPEDES personas."""
        if self.adultos + self.ninos > MAX_HUESPEDES:
            raise ValueError(
                f"Una habitacion admite como maximo {MAX_HUESPEDES} huespedes "
                f"(adultos + ninos = {self.adultos + self.ninos})"
            )
        return self


class PrediccionSalida(BaseModel):
    """Respuesta del modelo."""

    probabilidad_cancelacion: float = Field(ge=0, le=1)
    riesgo: Literal["bajo", "medio", "alto"]
    version_modelo: str = Field(description="Version del modelo que ha hecho la prediccion")
