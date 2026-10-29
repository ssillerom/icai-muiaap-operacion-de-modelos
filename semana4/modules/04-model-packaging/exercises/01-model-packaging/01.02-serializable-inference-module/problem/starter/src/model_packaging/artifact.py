"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import field_validator

from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)
from model_packaging.preprocess import (
    FEATURE_NAMES,
    PREPROCESSING_VERSION,
    preprocess_wine_request,
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
        if v != ARTIFACT_SCHEMA_VERSION:
            message = (
                f"Versión de esquema inválida: {v}. "
                f"Debería ser: {ARTIFACT_SCHEMA_VERSION}"
            )
            raise ValueError(message)
        return v

    @field_validator("model_version")
    @classmethod
    def validate_model_version(cls, v: str) -> str:
        """Valida que la versión del modelo no esté vacía."""
        if not v:
            raise ValueError("La versión del modelo no puede estar vacía.")
        return v.strip()

    @field_validator("preprocessing_version")
    @classmethod
    def validate_preprocessing_version(cls, v: str) -> str:
        """Valida que la versión de preprocesamiento sea la esperada."""
        if v != PREPROCESSING_VERSION:
            message = (
                f"Versión de preprocesamiento inválida: {v}. "
                f"Debería ser: {PREPROCESSING_VERSION}"
            )
            raise ValueError(message)
        return v

    @field_validator("feature_names")
    @classmethod
    def validate_feature_names(cls, v: tuple[str, ...]) -> tuple[str, ...]:
        """Valida que los nombres de las características sean los esperados."""
        if v != FEATURE_NAMES:
            message = (
                f"Nombres de características inválidos: {v}. "
                f"Deberían ser: {FEATURE_NAMES}"
            )
            raise ValueError(message)
        return v

    @field_validator("output_labels")
    @classmethod
    def validate_output_labels(
        cls, v: tuple[QualityBand, ...]
    ) -> tuple[QualityBand, ...]:
        """Valida que las etiquetas de salida sean las esperadas."""
        if v != OUTPUT_LABELS:
            message = (
                f"Etiquetas de salida inválidas: {v}. Deberían ser: {OUTPUT_LABELS}"
            )
            raise ValueError(message)
        return v


@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest


def validate_estimator(estimator) -> WineQualityEstimator:
    """Valida que el estimador cumpla con la interfaz requerida."""
    if not hasattr(estimator, "predict") or not hasattr(estimator, "predict_proba"):
        raise ValueError("El estimador no es compatible.")

    return estimator


def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """TODO: devuelve un manifiesto compatible con el contrato."""
    return ArtifactManifest(
        schema_version=ARTIFACT_SCHEMA_VERSION,
        model_version=model_version,
        preprocessing_version=PREPROCESSING_VERSION,
        feature_names=FEATURE_NAMES,
        output_labels=OUTPUT_LABELS,
        estimator_type=type(estimator).__name__,
    )


def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,
    manifest: ArtifactManifest | None = None,
) -> ArtifactManifest:
    """TODO: escribe manifest.json y model.joblib de forma segura."""

    estimator = validate_estimator(estimator)

    if manifest is None:
        manifest = create_manifest(estimator, model_version="wine-qual")

    bundle_path.mkdir(parents=True, exist_ok=True)

    with open(bundle_path / MANIFEST_FILENAME, "w", encoding="utf-8") as f:
        json.dump(manifest.model_dump(mode="json"), f, indent=2)

    model_data = {
        "estimator": estimator,
        "feature_names": list(manifest.feature_names),
        "model_version": manifest.model_version,
    }

    joblib.dump(model_data, bundle_path / MODEL_FILENAME)

    return manifest


def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """TODO: valida el manifiesto antes de cargar el estimador."""
    with open(bundle_path / MANIFEST_FILENAME) as f:
        manifest = ArtifactManifest.model_validate_json(f.read())

    model = joblib.load(bundle_path / MODEL_FILENAME)
    if not isinstance(model, dict):
        raise ValueError("El artefacto debe ser un diccionario.")

    estimator = model.get("estimator")

    if estimator is None:
        raise ValueError("El estimador no se encuentra en el bundle.")

    estimator = validate_estimator(estimator)
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
        preprocessing_version=bundle.manifest.preprocessing_version,
    )
