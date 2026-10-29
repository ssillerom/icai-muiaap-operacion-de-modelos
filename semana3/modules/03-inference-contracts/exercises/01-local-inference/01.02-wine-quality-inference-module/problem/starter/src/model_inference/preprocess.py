"""TODO: transformación de una muestra validada en el vector del modelo."""

# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.
import numpy as np

from model_inference.contracts import WineQualityRequest

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

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.
class WineFeatures:
    def __init__(self, request: WineQualityRequest):
        self.request = request
    
    def as_vector(self):
        row = self.request
        return np.array([
            row.fixed_acidity,
            row.volatile_acidity,
            row.citric_acid,
            row.residual_sugar,
            row.chlorides,
            row.free_sulfur_dioxide,
            row.total_sulfur_dioxide,
            row.density,
            row.ph,
            row.sulphates,
            row.alcohol
        ]).tolist()
        



def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    return WineFeatures(request)