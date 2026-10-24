"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.
"""Carga del .joblib e inferencia."""

from pathlib import Path

import joblib

from model_inference.contracts import WineQualityPrediction
from model_inference.preprocess import (
    FEATURE_NAMES,
    PREPROCESSING_VERSION,
    WineFeatures,
)

DEFAULT_MODEL_PATH = Path("models/wine_quality_classifier.joblib")


def load_wine_quality_model(path: Path = DEFAULT_MODEL_PATH) -> dict:
    """Carga el artefacto y comprueba que es compatible."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el modelo: {path}")

    bundle = joblib.load(path)

    if not isinstance(bundle, dict):
        raise ValueError("El artefacto debe ser un diccionario")
    for key in ("estimator", "feature_names", "model_version"):
        if key not in bundle:
            raise ValueError(f"Falta la clave '{key}' en el artefacto")

    estimator = bundle["estimator"]
    if not (hasattr(estimator, "predict") and hasattr(estimator, "predict_proba")):
        raise ValueError("El estimador debe tener predict y predict_proba")
    if tuple(bundle["feature_names"]) != FEATURE_NAMES:
        raise ValueError("feature_names del modelo no coincide con FEATURE_NAMES")
    if not bundle["model_version"]:
        raise ValueError("model_version no puede estar vacío")

    return bundle


def infer_wine_quality(bundle: dict, features: WineFeatures) -> WineQualityPrediction:
    """Predice la banda de calidad de una muestra."""
    estimator = bundle["estimator"]
    x = [features.as_vector()]  # matriz 2D: una fila

    label = str(estimator.predict(x)[0])
    confidence = float(max(estimator.predict_proba(x)[0]))

    return WineQualityPrediction(
        quality_band=label,
        confidence=confidence,
        model_version=bundle["model_version"],
        preprocessing_version=PREPROCESSING_VERSION,
    )