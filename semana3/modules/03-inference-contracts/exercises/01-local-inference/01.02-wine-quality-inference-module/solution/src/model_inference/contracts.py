"""TODO: contratos de entrada y salida de la inferencia."""

# Implementa WineQualityRequest y WineQualityPrediction con Pydantic.
# Revisa los campos de assets/inference_samples.csv y prohíbe columnas extra.

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


# Hay que hacer una función que valide el csv. A la función se le pasa
# el csv como parámetro

# Otra función que recive el csv validado de la función anterior
# y esa función convierte las variables en un vector con las 11 caracterñisticas
# para que el modelo las pueda aceptar.

# Ejecuto la predicción (.joblib). La salida de este modelo tiene otro pydantic
# con


# Cuando se define un contrato con Pydantic, los campos que se escriben dentro de la
# clase son los datos que tendrá que recibir ese objeto cuando se crea, salvo
# que alguno tenga un valor por defecto o sea opcional.


class WineQualityRequest(BaseModel):
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
    model_config = ConfigDict(extra="forbid")

    sample_id: str = Field(min_length=1)
    quality_band: Literal["acceptable", "needs_review"]
    confidence: float = Field(ge=0, le=1)
    model_version: str
    preprocessing_version: str


# Hacer una función dentro de esta clase en la que
# se devuelva un

# repo extrucrura de carpetas, entorno virtual, pydantic (todo lo de esta práctica)

# WineQualityPrediction es un contrato que va a ser solo un valor que va a ser un valor de predicción


# Función de preprocesado