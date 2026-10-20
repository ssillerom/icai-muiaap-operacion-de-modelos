"""Transformación de una muestra validada en el vector del modelo."""

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
    """Los 11 valores ya validados, en el orden de FEATURE_NAMES."""

    values: tuple[float, ...]

    def as_vector(self) -> list[float]:
        return list(self.values)


def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    values = []
    for name in FEATURE_NAMES:
        values.append(getattr(request, name))
    return WineFeatures(values=tuple(values))
