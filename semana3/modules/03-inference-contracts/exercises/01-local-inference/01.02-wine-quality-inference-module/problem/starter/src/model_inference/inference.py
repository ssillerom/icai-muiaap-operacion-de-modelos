"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.

from pathlib import Path
from model_inference.preprocess import FEATURE_NAMES, PREPROCESSING_VERSION
from model_inference.contracts import WineQualityPrediction
import joblib


DEFAULT_MODEL_PATH = Path("models/wine_quality_classifier.joblib")

def load_wine_quality_model(ruta = DEFAULT_MODEL_PATH): #se queda como default, si no meto ninguna ruta usa esa
    artefacto = joblib.load(ruta)
    estimador = artefacto.get("estimator")
    if not hasattr(estimador, "predict_proba"):   ### PREGUNTA: no entiendo por que tengo que comprobar predict_proba
        raise ValueError("El artefacto no tiene las un clasificador compatible" # debe tener tambien las palabras clasificador compatible
        "")
    elif artefacto["feature_names"]!=list(FEATURE_NAMES):
        raise ValueError("feature_names no son los mismos")  #al parecer el test usa completed.stderr, fuerza que este
                                                              #mal y mira a ver si esta feature_names en el error tal cual
    return artefacto


def infer_wine_quality(artefacto, features):
    probs = artefacto["estimator"].predict_proba([features.as_vector()])
    posicion = probs[0].argmax()
    quality = artefacto["estimator"].classes_[posicion]
    confidence = max(probs[0])
    return WineQualityPrediction(
        quality_band =          quality,
        confidence =            confidence,
        model_version =         artefacto["model_version"],
        preprocessing_version = PREPROCESSING_VERSION
    )
