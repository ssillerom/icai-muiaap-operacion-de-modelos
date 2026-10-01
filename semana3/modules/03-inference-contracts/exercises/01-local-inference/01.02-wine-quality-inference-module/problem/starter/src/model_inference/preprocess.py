"""TODO: transformación de una muestra validada en el vector del modelo."""

# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.


from dataclasses import dataclass

import numpy as np

from model_inference.contracts import WineQualityRequest

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

PREPROCESSING_VERSION = "1.0.0"


@dataclass(frozen=True)
class WineFeatures:
    """Vector de características listo para el modelo, sin sample_id mezclado."""

    sample_id: str
    vector: np.ndarray
    preprocessing_version: str = PREPROCESSING_VERSION


def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    """Convierte una WineQualityRequest validada en un WineFeatures ordenado."""
    values = [getattr(request, name) for name in FEATURE_NAMES]
    vector = np.array(values, dtype=float)
    return WineFeatures(sample_id=request.sample_id, vector=vector)

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.
