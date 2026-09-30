"""TODO: transformación de una muestra validada en el vector del modelo."""

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

class WineFeatures:
    def __init__(self, vector: list[float]):
        self._vector=vector
        
    def as_vector(self)->list[float]:
        return self._vector
    
def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    # Extrae los valores en el orden matemático exacto dictado por FEATURE_NAMES
    vector = [getattr(request, name) for name in FEATURE_NAMES]
    return WineFeatures(vector)