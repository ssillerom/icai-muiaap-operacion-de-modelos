"""TODO: transformación de una muestra validada en el vector del modelo."""

from dataclasses import dataclass

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
# Nombre de esta forma de preparar los datos. Irá en el CSV de salida.
PREPROCESSING_VERSION = "wine-red-features-v1"

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.


@dataclass(frozen=True, slots=True)
# frozen=True: una vez creado el objeto, no se puede cambiar ningún valor.
# Si se intenta, Python da un error (FrozenInstanceError).
# slots=True: el objeto guarda solo los campos declarados, de forma más compacta.
class WineFeatures:  # porque no WineQualityDataclass?
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
        # Devuelve la lista de valores en el orden de FEATURE_NAME
        vector = []
        for name in FEATURE_NAMES:
            vector.append(getattr(self, name))
        return vector


# Nota: self es el propio objeto sobre el que llamas al método:
# features = WineFeatures(fixed_acidity=1.0, ..., alcohol=11.0)
# features.as_vector()


# no entiendo muy bien esta funcion preguntar en clase
def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    # Convierte la request ya validada en un WineFeatures
    return WineFeatures(**request.model_dump())
