"""TODO: contratos de entrada y salida de la inferencia."""
"""Contratos de entrada y salida de la inferencia."""

from pydantic import BaseModel, ConfigDict, Field


class WineQualityRequest(BaseModel):
    """Una fila de entrada validada, tal como llega del CSV."""

    model_config = ConfigDict(extra="forbid")

    sample_id: str

    fixed_acidity: float = Field(ge=0)
    volatile_acidity: float = Field(ge=0)
    citric_acid: float = Field(ge=0)
    residual_sugar: float = Field(ge=0)
    chlorides: float = Field(ge=0)
    free_sulfur_dioxide: float = Field(ge=0)
    total_sulfur_dioxide: float = Field(ge=0)
    density: float = Field(gt=0)
    ph: float = Field(ge=0, le=14)
    sulphates: float = Field(ge=0)
    alcohol: float = Field(ge=0, le=100)


class WineQualityPrediction(BaseModel):
    """El resultado que se escribe en el CSV de salida."""

    model_config = ConfigDict(extra="forbid")

    sample_id: str
    quality_band: str
    confidence: float = Field(ge=0, le=1)
    model_version: str
    preprocessing_version: str
# Implementa WineQualityRequest y WineQualityPrediction con Pydantic.
# Revisa los campos de assets/inference_samples.csv y prohíbe columnas extra.
