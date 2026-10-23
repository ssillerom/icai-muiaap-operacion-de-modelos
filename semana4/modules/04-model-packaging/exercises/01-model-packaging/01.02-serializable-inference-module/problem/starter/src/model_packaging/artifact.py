"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Protocol

import joblib
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import field_validator
from model_packaging.preprocess import WineFeatures, preprocess_wine_request
from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)

ARTIFACT_SCHEMA_VERSION = "wine-quality-bundle-v1"
DEFAULT_BUNDLE_PATH = Path("models/wine_quality_bundle")
MANIFEST_FILENAME = "manifest.json"
MODEL_FILENAME = "model.joblib"
OUTPUT_LABELS: tuple[QualityBand, ...] = (
    "needs_review",
    "acceptable",
    "excellent",
)


class WineQualityEstimator(Protocol):
    """Interfaz mínima que debe cumplir el estimador cargado."""

    def predict(self, features: list[list[float]]) -> Sequence[str]:
        """Devuelve una etiqueta por fila."""

    def predict_proba(self, features: list[list[float]]) -> Sequence[Sequence[float]]:
        """Devuelve probabilidades por fila."""


class ArtifactManifest(BaseModel):
    """TODO: declara y valida los metadatos del bundle."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str
    model_version: str = Field(min_length=1)
    preprocessing_version: str
    feature_names: tuple[str, ...]
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)
    
    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, v: str) -> str:
        """Valida que la versión del esquema sea la esperada."""
        print(f"Validando schema_version: {v}")
        return v

@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest


def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """TODO: devuelve un manifiesto compatible con el contrato."""
    return ArtifactManifest(
        schema_version=ARTIFACT_SCHEMA_VERSION,
        model_version=model_version,
        preprocessing_version="wine-red-features-v1",
        feature_names=(
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
        ),
        output_labels=OUTPUT_LABELS,
        estimator_type=type(estimator).__name__
    )
    


def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,
    manifest: ArtifactManifest | None = None,
) -> ArtifactManifest:
    """TODO: escribe manifest.json y model.joblib de forma segura."""
    if manifest is not None:
        with open(bundle_path / MANIFEST_FILENAME, "w") as f:
            json.dump(manifest, f, indent=2)
    
    with open(bundle_path / MODEL_FILENAME, "wb") as f:
        joblib.dump(estimator, f)

    return manifest
    


def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """TODO: valida el manifiesto antes de cargar el estimador."""
    with open(bundle_path / MANIFEST_FILENAME, "r") as f:
        manifest = ArtifactManifest.model_validate_json(f.read())
    
    estimator = joblib.load(bundle_path / MODEL_FILENAME)
    
    return LoadedModelBundle(estimator=estimator, manifest=manifest)



def infer_wine_quality(
    bundle: LoadedModelBundle,
    request: WineQualityRequest,
) -> WineQualityPrediction:
    """TODO: preprocesa, invoca el estimador y valida la respuesta."""
    X = preprocess_wine_request(request)
   
    prediction = bundle.estimator.predict([X.as_vector()])
    probs = bundle.estimator.predict_proba([X.as_vector()])
    probability = max(probs[0])
    return WineQualityPrediction(
        quality_band=prediction[0],
        confidence=probability,
        model_version=bundle.manifest.model_version,
        preprocessing_version=bundle.manifest.preprocessing_version
    )
