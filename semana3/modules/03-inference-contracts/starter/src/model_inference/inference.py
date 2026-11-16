"""TODO: carga del .joblib e inferencia sobre características preparadas."""
import joblib
from model_inference.preprocess import FEATURE_NAMES
from model_inference.contracts import WineQualityRequest, WineQualityPrediction
from model_inference.preprocess import preprocess_wine_request, PREPROCESSING_VERSION

DEFAULT_MODEL_PATH = "model/wine_quality_classifier.joblib"

def load_wine_quality_model(path=DEFAULT_MODEL_PATH):
    model=joblib.load(path)
    if not isinstance(model, dict):
        raise TypeError(f"Se esperaba un dict, llegó {type(model).__name__}")
    estimator=model.get("feature_names")
    ##hecho con ia
    if not (callable(getattr(estimator, "predict", None))
            and callable(getattr(estimator, "predict_proba", None))):
        raise TypeError("El artefacto no contiene un clasificador compatible")
    #hecho con ia

    if list(FEATURE_NAMES) != list(model.get("feature_names", [])):
        raise ValueError ("feature_names no coincide con el contrato")
    return model

def infer_wine_quality(model:dict, request:WineQualityRequest):
    pedido_precesado=preprocess_wine_request(request).as_vector()
    target=model["estimator"].predict([pedido_precesado])[0]
    confidence=float(max(model["estimator"].predict_proba([pedido_precesado])[0]))

    return WineQualityPrediction(
        sample_id=request.sample_id,
        quality_band=str(target),
        confidence=confidence,
        model_version=model["model_version"],
        preprocessing_version=PREPROCESSING_VERSION
    )


# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.
