"""TODO: transformación de una muestra validada en el vector del modelo."""

# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.
# FEATURE_NAMES contiene los nombre de las 11 variables en el orden exacto
# en el que las espera el modelo
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

from model_inference.contracts import WineQualityRequest


# __init__ es una función especial de las clases de Python. Se ejecuta
# automáticamente cuando creas un objeto.
# Para crear un objeto haríamos: features = WineFeatures(
#    fixed_acidity=7.4,
#    volatile_acidity=0.7,
#    ...
#)
# self representa el objeto concreto que estamos creando
class WineFeatures:
    def __init__(
        self,
        fixed_acidity,
        volatile_acidity,
        citric_acid,
        residual_sugar,
        chlorides,
        free_sulfur_dioxide,
        total_sulfur_dioxide,
        density,
        ph,
        sulphates,
        alcohol,
    ):
        self.fixed_acidity = fixed_acidity
        self.volatile_acidity = volatile_acidity
        self.citric_acid = citric_acid
        self.residual_sugar = residual_sugar
        self.chlorides = chlorides
        self.free_sulfur_dioxide = free_sulfur_dioxide
        self.total_sulfur_dioxide = total_sulfur_dioxide
        self.density = density
        self.ph = ph
        self.sulphates = sulphates
        self.alcohol = alcohol

    # as_vector coge los 11 valores guardados dentro de un objeto WineFeatures
    # y devuelve una lista con ellos en el orden correcto. Este vector no está
    # definido como una variable, el método simplemente devuelve el vector.
    def as_vector(self):
        return [
            self.fixed_acidity,
            self.volatile_acidity,
            self.citric_acid,
            self.residual_sugar,
            self.chlorides,
            self.free_sulfur_dioxide,
            self.total_sulfur_dioxide,
            self.density,
            self.ph,
            self.sulphates,
            self.alcohol,
        ]


# request es el parámetro que recibe la función
# Al hacer request: WineQualityRequest estamos diciendo que esperamos que request
# sea un objeto de tipo WineQualityRequest
# Al hacer fixed_acidity = request.fixed_acidity, lo que estamos haciendo es que para
# el fixed_acidity del nievo WineFeatures, utiliza el fixed_acidity que había en request
def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    features = WineFeatures(
        fixed_acidity=request.fixed_acidity,
        volatile_acidity=request.volatile_acidity,
        citric_acid=request.citric_acid,
        residual_sugar=request.residual_sugar,
        chlorides=request.chlorides,
        free_sulfur_dioxide=request.free_sulfur_dioxide,
        total_sulfur_dioxide=request.total_sulfur_dioxide,
        density=request.density,
        ph=request.ph,
        sulphates=request.sulphates,
        alcohol=request.alcohol,
    )

    return features


# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.