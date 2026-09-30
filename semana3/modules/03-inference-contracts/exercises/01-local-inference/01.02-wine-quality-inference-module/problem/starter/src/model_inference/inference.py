"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.

import joblib
from pathlib import Path
from typing import Any
from .contracts import WineQualityPrediction
from .preprocess import PREPROCESSING_VERSION, FEATURE_NAMES

class WineModel:
    def __init__(self, model_path: str | Path):
        self.model_path = Path(model_path)
        self.estimator = self._load_and_validate_model()
        self.model_version = getattr(self.estimator, "model_version", "unknown")

    def _load_and_validate_model(self) -> Any:
        if not self.model_path.exists():
            raise FileNotFoundError(f"No se encuentra el modelo en {self.model_path}")
        
        model = joblib.load(self.model_path)
        
        # Validación crítica: ¿El modelo entrenado espera las mismas variables que nuestro sistema?
        expected_features = tuple(model.feature_names_in_)
        if expected_features != FEATURE_NAMES:
            raise ValueError(
                f"Incompatibilidad de características. "
                f"El modelo espera {expected_features}, pero el preprocesado usa {FEATURE_NAMES}"
            )
        return model

    def predict(self, sample_id: str, vector: list[float]) -> WineQualityPrediction:
        # scikit-learn espera matrices 2D, por eso pasamos [vector]
        prediction = self.estimator.predict([vector])[0]
        probabilities = self.estimator.predict_proba([vector])[0]
        confidence = max(probabilities)

        return WineQualityPrediction(
            sample_id=sample_id,
            quality_band=str(prediction),
            confidence=float(confidence),
            model_version=self.model_version,
            preprocessing_version=PREPROCESSING_VERSION
        )