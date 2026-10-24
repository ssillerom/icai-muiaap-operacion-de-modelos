"""TODO: transformación de una muestra validada en el vector del modelo."""
from dataclasses import dataclass

from model_inference.contracts import WineQualityRequest

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
@dataclass(frozen=True)
class WineFeatures:
    """Las once medidas, ya preparadas."""

    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    ph: float
    sulphates: float
    alcohol: float

    def as_vector(self) -> list[float]:
        """Devuelve los valores en el orden de FEATURE_NAMES."""
        return [getattr(self, name) for name in FEATURE_NAMES]


def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    """Convierte la petición validada en características (sin sample_id)."""
    values = {name: getattr(request, name) for name in FEATURE_NAMES}
    return WineFeatures(**values)
# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.
