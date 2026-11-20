"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.

# estimador = modelo

# En los criterios de aceptación pone: "Validar el playload del artefecto antes de invocar
# predict/predict_proba y validar la salida resultante". Por eso en infer_wine_quality()
# comprobamos que tenga esos dos métodos del estimador: predict() para obtener la categoría y predict_proba() para obtener la confianza

import joblib
from model_inference.preprocess import FEATURE_NAMES
from model_inference.preprocess import PREPROCESSING_VERSION
from model_inference.preprocess import WineFeatures
from model_inference.contracts import WineQualityPrediction

DEFAULT_MODEL_PATH = "models/wine_quality_classifier.joblib"

# model_path = DEFAULT_MODEL_PATH significa que model_path tiene un valor
# por defecto: si hacemos load_wine_quality_model(), nos va a coger DEFAULT_MODEL_PATH
# por defecto, pero si le metemos algo, cogerá ptr cosa: load_wine_quality_model("otro_modelo.joblib")
# Según lo que vemos el los test, joblib está guardando un diccionario:
#          joblib.dump(
#    {
#        "estimator": estimator,
#        "feature_names": list(EXPECTED_FEATURE_NAMES),
#        "model_version": "wine-quality-rf-v1",
#    },
#    model_path,
#)
# así que el .joblib conceptualmente contiene:
#   {
#    "estimator":       objeto modelo,
#    "feature_names":   lista,
#    "model_version":   string
#}
# por lo que artifact es un diccionario
# Dentro de artifact, la clave estimator es el objeto MODELO, por
# lo que artifact no es solo el modelo, es un diccionario que tiene dentro
# el modelo, pero también los features names y la versión del modelo
def load_wine_quality_model(model_path=DEFAULT_MODEL_PATH):
    artifact = joblib.load(model_path)

    if "estimator" not in artifact:
        raise ValueError("El artefecto no contiene un clasificador compatible")

    estimator = artifact["estimator"]

    if not hasattr(estimator, "predict") or not hasattr(estimator, "predict_proba"):
        raise ValueError("El artefecto no contiene un clasificador compatible")

    if "feature_names" not in artifact:
        raise ValueError("El artefacto no contiene feature_names")

    # comprueba que las características que espera el modelo son exactamente
    # las mismas y están en el mismo orden que las que he definido en
    # preprocess.py
    if artifact["feature_names"] != list(FEATURE_NAMES):
        raise ValueError("Los feature_names del modelo no son compatibles")

    if "model_version" not in artifact:
        raise ValueError("El artefacto no contiene model_version")

    return artifact


# Esta función pregunta al modelo "¿Qué predices para este vino?" y convierte
# su respuesta en el contrato de salida del sistema
def infer_wine_quality(artifact,
                       features: WineFeatures,
                       sample_id: str) -> WineQualityPrediction:
    estimator = artifact["estimator"] # Sacamos el modelo entrenado del artifact

    vector = features.as_vector() # este es el vector de 11 características en el orden correcto
    model_input = [vector] # model_input = [[7.4, 0.7, ..., 9.4]] Hay dos niveles de corchetes
                    # porque el modelo espera varias muestras. Aunque ahora solo vayamos a predecir
                    # un vino, hay que pasarlo como una colección de una fila.

    prediction = estimator.predict(model_input)
    quality_band = prediction[0] # El modelo devuelve una lista con las predicciones de todos los
                    # vinos. Como solo le hemos metido uno solo devuelve una predicción
    probabilities = estimator.predict_proba(model_input) # Esto podría devolver algo como [[0.77, 0.23]].
                    # Es decir, las probabilidades para las distintas categorías. Una para acceptable
                    # y otra para needs_review
    confidence = float(max(probabilities[0])) # que coja el que tenga mayor probabilidad porque es el
                    # que nos va a haber salido en prediction
    result = WineQualityPrediction(
        sample_id = sample_id,
        quality_band = quality_band,
        confidence = confidence,
        model_version = artifact["model_version"],
        preprocessing_version=PREPROCESSING_VERSION,
    )

    return result