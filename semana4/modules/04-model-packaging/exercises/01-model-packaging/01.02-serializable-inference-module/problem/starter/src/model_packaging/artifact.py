"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

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
    """Metadatos legibles del bundle; se validan antes de cargar el binario."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str
    model_version: str = Field(min_length=1)
    preprocessing_version: str
    feature_names: tuple[str, ...]
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)

    @field_validator("schema_version")
    @classmethod
    def _check_schema_version(cls, value: str) -> str:
        if value != ARTIFACT_SCHEMA_VERSION:
            raise ValueError(
                f"schema_version {value!r} no es compatible; "
                f"se espera {ARTIFACT_SCHEMA_VERSION!r}"
            )
        return value

    @field_validator("preprocessing_version")
    @classmethod
    def _check_preprocessing_version(cls, value: str) -> str:
        if value != PREPROCESSING_VERSION:
            raise ValueError(
                f"preprocessing_version {value!r} no coincide con el preprocesado "
                f"del código ({PREPROCESSING_VERSION!r})"
            )
        return value

    @field_validator("feature_names")
    @classmethod
    def _check_feature_names(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if value != FEATURE_NAMES:
            raise ValueError(
                "feature_names no coincide con FEATURE_NAMES: los nombres y el "
                f"orden deben ser exactamente {list(FEATURE_NAMES)}"
            )
        return value

    @field_validator("output_labels")
    @classmethod
    def _check_output_labels(
        cls, value: tuple[QualityBand, ...]
    ) -> tuple[QualityBand, ...]:
        if value != OUTPUT_LABELS:
            raise ValueError(
                f"output_labels {list(value)} no coincide con {list(OUTPUT_LABELS)}"
            )
        return value

    @model_validator(mode="after")
    def _check_versions_are_different(self) -> ArtifactManifest:
        if self.model_version == self.preprocessing_version:
            raise ValueError(
                "model_version y preprocessing_version son versiones distintas "
                "y no pueden tener el mismo valor"
            )
        return self


@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest


def _require_estimator_interface(estimator: object) -> None:
    """Comprueba que el estimador ofrece predict() y predict_proba()."""

    missing = [
        name
        for name in ("predict", "predict_proba")
        if not callable(getattr(estimator, name, None))
    ]
    if missing:
        raise ValueError(
            "El estimador no es compatible: le falta "
            + " y ".join(f"{name}()" for name in missing)
        )


def _write_atomically(path: Path, write: Callable[[Path], object]) -> None:
    """Escribe en un fichero temporal y lo mueve al destino al terminar."""

    temporary = path.with_name(f"{path.name}.tmp")
    try:
        write(temporary)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """Devuelve un manifiesto compatible con el contrato de la semana 3."""

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
    """Escribe manifest.json y model.joblib de forma segura."""

    if manifest is None:
        raise ValueError(
            "save_model_bundle necesita un manifiesto: créalo con create_manifest()."
        )
    _require_estimator_interface(estimator)
    # Se vuelve a validar por si el objeto se construyó sin pasar por Pydantic.
    manifest = ArtifactManifest.model_validate(manifest.model_dump())
    if manifest.estimator_type != type(estimator).__name__:
        raise ValueError(
            f"estimator_type {manifest.estimator_type!r} no coincide con el "
            f"estimador que se guarda ({type(estimator).__name__!r})"
        )

    bundle_path = Path(bundle_path)
    bundle_path.mkdir(parents=True, exist_ok=True)
    # El manifiesto se escribe el último: si existe, el binario ya está completo.
    _write_atomically(
        bundle_path / MODEL_FILENAME,
        lambda target: joblib.dump(estimator, target),
    )
    manifest_text = json.dumps(manifest.model_dump(mode="json"), indent=2)
    _write_atomically(
        bundle_path / MANIFEST_FILENAME,
        lambda target: target.write_text(manifest_text + "\n", encoding="utf-8"),
    )
    return manifest


def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """Valida el manifiesto antes de cargar el estimador.

    joblib deserializa con pickle: solo debe cargarse un bundle de una fuente de
    confianza. El manifiesto describe el binario, pero no lo hace seguro.
    """

    bundle_path = Path(bundle_path)
    manifest_path = bundle_path / MANIFEST_FILENAME
    model_path = bundle_path / MODEL_FILENAME
    for required in (manifest_path, model_path):
        if not required.is_file():
            raise FileNotFoundError(f"No existe {required.name} en {bundle_path}")

    try:
        raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(
            f"{MANIFEST_FILENAME} no es un JSON válido: {error}"
        ) from error
    manifest = ArtifactManifest.model_validate(raw_manifest)

    try:
        estimator = joblib.load(model_path)
    except Exception as error:
        raise ValueError(
            f"No se pudo deserializar {MODEL_FILENAME}: {error}"
        ) from error
    _require_estimator_interface(estimator)
    if manifest.estimator_type != type(estimator).__name__:
        raise ValueError(
            f"estimator_type {manifest.estimator_type!r} no coincide con el "
            f"estimador cargado ({type(estimator).__name__!r})"
        )
    return LoadedModelBundle(estimator=estimator, manifest=manifest)


def infer_wine_quality(
    bundle: LoadedModelBundle,
    request: WineQualityRequest,
) -> WineQualityPrediction:
    """Preprocesa, invoca el estimador y valida la respuesta."""

    vector = [preprocess_wine_request(request).as_vector()]
    labels = bundle.estimator.predict(vector)
    probabilities = bundle.estimator.predict_proba(vector)
    if len(labels) != 1 or len(probabilities) != 1:
        raise ValueError("El estimador debe devolver una predicción por fila")

    label = str(labels[0])
    if label not in bundle.manifest.output_labels:
        raise ValueError(
            f"El modelo devolvió la etiqueta {label!r}, que no está permitida; "
            f"etiquetas válidas: {list(bundle.manifest.output_labels)}"
        )
    return WineQualityPrediction(
        quality_band=label,
        confidence=float(max(probabilities[0])),
        model_version=bundle.manifest.model_version,
        preprocessing_version=bundle.manifest.preprocessing_version,
    )
