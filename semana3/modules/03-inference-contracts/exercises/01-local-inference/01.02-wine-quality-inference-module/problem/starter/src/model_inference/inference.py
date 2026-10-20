"""Carga del .joblib e inferencia sobre características preparadas."""

from pathlib import Path

import joblib

from model_inference.contracts import WineQualityPrediction
from model_inference.preprocess import (
    FEATURE_NAMES,
    PREPROCESSING_VERSION,
    WineFeatures,
)

DEFAULT_MODEL_PATH = Path("models/wine_quality_classifier.joblib")


def load_wine_quality_model(path):
    model = joblib.load(path)

    if not isinstance(model, dict) or "estimator" not in model:
        raise ValueError("El artefacto no contiene un clasificador compatible.")

    estimator = model["estimator"]
    if not hasattr(estimator, "predict") or not hasattr(estimator, "predict_proba"):
        raise ValueError("El artefacto no contiene un clasificador compatible.")

    if list(model["feature_names"]) != list(FEATURE_NAMES):
        raise ValueError("feature_names del modelo no coincide con FEATURE_NAMES.")

    return model


def infer_wine_quality(model, sample_id: str, features: WineFeatures):
    vector = features.as_vector()
    estimator = model["estimator"]

    label = estimator.predict([vector])[0]
    probabilities = estimator.predict_proba([vector])[0]
    confidence = float(max(probabilities))

    return WineQualityPrediction(
        sample_id=sample_id,
        quality_band=str(label),
        confidence=confidence,
        model_version=model["model_version"],
        preprocessing_version=PREPROCESSING_VERSION,
    )
