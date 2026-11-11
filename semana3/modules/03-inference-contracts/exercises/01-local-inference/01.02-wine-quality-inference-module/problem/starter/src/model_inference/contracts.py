"""TODO: contratos de entrada y salida de la inferencia."""

# Implementa WineQualityRequest y WineQualityPrediction con Pydantic.
# Revisa los campos de assets/inference_samples.csv y prohíbe columnas extra.
from pydantic import BaseModel, Field, ConfigDict 
from typing import Literal
 
class WineQualityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fixed_acidity:          float = Field(ge=0, le=20)
    volatile_acidity:       float = Field(ge=0, le=2)
    citric_acid:            float = Field(ge=0, le=1)
    residual_sugar:         float = Field(ge=0, le=20)
    chlorides:              float = Field(ge=0, le=1)
    free_sulfur_dioxide:    float = Field(ge=0, le=100)
    total_sulfur_dioxide:   float = Field(ge=0, le=350)
    density:                float = Field(ge=0, le=1.1)
    ph:                     float = Field(ge=0, le=4.5)
    sulphates:              float = Field(ge=0, le=3)
    alcohol:                float = Field(ge=5, le=20)


class WineQualityPrediction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quality_band:           Literal["needs_review", "acceptable", "excellent"]#lo saco del test del assert
    confidence:             float = Field(ge=0, le=1)
    model_version:          str = Field(min_length=1)
    preprocessing_version:  str = Field(min_length=1)  
