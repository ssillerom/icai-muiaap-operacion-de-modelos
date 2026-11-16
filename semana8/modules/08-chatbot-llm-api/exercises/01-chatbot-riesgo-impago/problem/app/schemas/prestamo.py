from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator


class PrestamoEntrada(BaseModel):
    """Contrato de entrada del modelo de impago (y de la tool del LLM).

    Es el unico contrato: /predict lo usa como body y el orquestador genera
    con el el JSON Schema de la tool que se envia al LLM.
    """

    # extra="forbid": un campo inventado (por el LLM o por un cliente) es un error, no se ignora
    model_config = ConfigDict(extra="forbid")

    edad: int = Field(ge=18, le=75, description="Edad del solicitante en anios (18 a 75)")
    ingresos_mensuales: float = Field(gt=0, description="Ingresos netos mensuales en euros")
    importe_prestamo: float = Field(gt=0, description="Importe solicitado en euros")
    plazo_meses: int = Field(ge=6, le=84, description="Plazo de devolucion en meses (6 a 84)")
    antiguedad_laboral_anios: int = Field(
        ge=0, le=50, description="Anios en el empleo actual (0 a 50, como mucho edad - 16)"
    )
    impagos_previos: int = Field(ge=0, le=20, description="Numero de impagos previos (0 a 20)")

    @field_validator("antiguedad_laboral_anios")
    @classmethod
    def antiguedad_coherente_con_edad(cls, valor: int, info: ValidationInfo) -> int:
        # edad se declara antes, asi que ya esta validada en info.data (si era valida)
        edad = info.data.get("edad")
        if edad is not None and valor > edad - 16:
            raise ValueError(
                f"antiguedad_laboral_anios ({valor}) no puede ser mayor que edad - 16 ({edad - 16})"
            )
        return valor


class PrediccionSalida(BaseModel):
    """Contrato de salida: probabilidad de impago y decision derivada."""

    probabilidad_impago: float = Field(ge=0, le=1)
    decision: Literal["aprobar", "revisar", "rechazar"]
