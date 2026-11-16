"""TODO: transformación de una muestra validada en el vector del modelo."""

from model_inference.contracts import WineQualityRequest
from pydantic import BaseModel
# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.
FEATURE_NAMES = (
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
)

PREPROCESSING_VERSION = "wine-red-features-v1"

class WineFeatures(BaseModel):
    values: list[float]

    def as_vector(self) -> list[float]:
        return self.values

def preprocess_wine_request(request: WineQualityRequest)->WineFeatures:
    return WineFeatures(values=[
        request.fixed_acidity,
        request.volatile_acidity,
        request.citric_acid,
        request.residual_sugar,
        request.chlorides,
        request.free_sulfur_dioxide,
        request.total_sulfur_dioxide,
        request.density,
        request.ph,
        request.sulphates,
        request.alcohol,
    ]
    )

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.
