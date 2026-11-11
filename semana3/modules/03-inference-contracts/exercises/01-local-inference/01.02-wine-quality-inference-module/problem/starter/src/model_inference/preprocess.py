"""TODO: transformación de una muestra validada en el vector del modelo."""
from pydantic import BaseModel
from model_inference.contracts import WineQualityRequest
import numpy as np

PREPROCESSING_VERSION = "wine-red-features-v1"

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

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.
class WineFeatures(BaseModel): #hay que definirlo para el test 
    lista : list[float]
    def as_vector(self):
        return self.lista
    
def preprocess_wine_request(WineQualityRequest):
    vector = WineFeatures(lista = [getattr(WineQualityRequest, nombres) for nombres in FEATURE_NAMES])
    return vector

