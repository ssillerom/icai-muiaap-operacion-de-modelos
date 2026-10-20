"""Contratos de entrada y salida de la inferencia."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WineQualityRequest(BaseModel):
    """Las 11 características de una muestra de vino (sin sample_id)."""

    model_config = ConfigDict(extra="forbid")

    fixed_acidity: float = Field(ge=0, le=20)
    volatile_acidity: float = Field(ge=0, le=2)
    citric_acid: float = Field(ge=0, le=2)
    residual_sugar: float = Field(ge=0, le=20)
    chlorides: float = Field(ge=0, le=1)
    free_sulfur_dioxide: float = Field(ge=0, le=100)
    total_sulfur_dioxide: float = Field(ge=0, le=300)
    density: float = Field(ge=0.98, le=1.01)
    ph: float = Field(ge=2.5, le=4.5)
    sulphates: float = Field(ge=0, le=3)
    alcohol: float = Field(ge=5, le=20)


class WineQualityPrediction(BaseModel):
    """Una fila del CSV de salida."""

    model_config = ConfigDict(extra="forbid")

    sample_id: str = Field(min_length=1)
    quality_band: Literal["needs_review", "acceptable", "excellent"]
    confidence: float = Field(ge=0, le=1)
    model_version: str = Field(min_length=1)
    preprocessing_version: str = Field(min_length=1)
