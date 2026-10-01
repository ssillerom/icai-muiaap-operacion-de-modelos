"""TODO: carga del .joblib e inferencia sobre características preparadas."""

from pathlib import Path

import joblib

from model_inference.preprocess import FEATURE_NAMES, WineFeatures

DEFAULT_MODEL_PATH = Path("models/wine_quality_classifier.joblib")


class ModelArtifactError(ValueError):
    """El artefacto cargado no cumple la interfaz mínima esperada."""


def load_wine_quality_model(model_path: Path = DEFAULT_MODEL_PATH) -> dict:
    """Carga el bundle .joblib y valida su estructura antes de devolverlo."""
    bundle = joblib.load(model_path)

    required_keys = {"estimator", "feature_names", "model_version"}
    missing = required_keys - bundle.keys()
    if missing:
        raise ModelArtifactError(f"Faltan claves en el artefacto: {missing}")

    if tuple(bundle["feature_names"]) != FEATURE_NAMES:
        raise ModelArtifactError(
            "feature_names del artefacto no coincide con el orden esperado "
            f"({bundle['feature_names']} != {FEATURE_NAMES})"
        )

    estimator = bundle["estimator"]
    if not hasattr(estimator, "predict") or not hasattr(estimator, "predict_proba"):
        raise ModelArtifactError(
            "El estimador no implementa predict/predict_proba"
        )

    return bundle


def infer_wine_quality(bundle: dict, features: WineFeatures) -> tuple[str, float]:
    """Ejecuta predict/predict_proba sobre un vector ya preprocesado."""
    estimator = bundle["estimator"]
    vector = features.vector.reshape(1, -1)

    quality_band = estimator.predict(vector)[0]
    probabilities = estimator.predict_proba(vector)[0]
    confidence = float(max(probabilities))

    return str(quality_band), confidence
# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.
