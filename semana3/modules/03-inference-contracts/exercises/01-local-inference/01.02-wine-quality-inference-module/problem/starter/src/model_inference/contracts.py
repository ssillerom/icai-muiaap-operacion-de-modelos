"""Contratos de entrada y salida de la inferencia."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

QualityBand = Literal["needs_review", "acceptable", "excellent"]


class WineQualityRequest(BaseModel):
    """Mediciones de una muestra de vino tinto."""

    model_config = ConfigDict(extra="forbid")

    fixed_acidity: float = Field(ge=0, le=20, allow_inf_nan=False)
    volatile_acidity: float = Field(ge=0, le=2, allow_inf_nan=False)
    citric_acid: float = Field(ge=0, le=2, allow_inf_nan=False)
    residual_sugar: float = Field(ge=0, le=20, allow_inf_nan=False)
    chlorides: float = Field(ge=0, le=1, allow_inf_nan=False)
    free_sulfur_dioxide: float = Field(ge=0, le=100, allow_inf_nan=False)
    total_sulfur_dioxide: float = Field(ge=0, le=300, allow_inf_nan=False)
    density: float = Field(ge=0.98, le=1.01, allow_inf_nan=False)
    ph: float = Field(ge=2.5, le=4.5, allow_inf_nan=False)
    sulphates: float = Field(ge=0, le=3, allow_inf_nan=False)
    alcohol: float = Field(ge=5, le=20, allow_inf_nan=False)


class WineQualityPrediction(BaseModel):
    """Resultado de una predicción con las versiones usadas."""

    model_config = ConfigDict(extra="forbid")

    quality_band: QualityBand
    confidence: float = Field(ge=0, le=1, allow_inf_nan=False)
    model_version: str = Field(min_length=1)
    preprocessing_version: str = Field(min_length=1)
