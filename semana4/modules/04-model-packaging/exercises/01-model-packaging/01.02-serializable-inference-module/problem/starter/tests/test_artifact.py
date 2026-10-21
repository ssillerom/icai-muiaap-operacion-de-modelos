import json
from pathlib import Path

import pytest
from sklearn.dummy import DummyClassifier

from model_packaging.artifact import (
    ArtifactManifest,
    LoadedModelBundle,
    create_manifest,
    infer_wine_quality,
    load_model_bundle,
    save_model_bundle,
)
from model_packaging.contracts import WineQualityRequest
from model_packaging.preprocess import FEATURE_NAMES

WINE_SAMPLE = {
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "ph": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4,
}


def make_estimator() -> DummyClassifier:
    """Crea un estimador pequeño para probar el contrato."""

    estimator = DummyClassifier(strategy="constant", constant="acceptable")
    estimator.fit([[0.0] * len(FEATURE_NAMES)], ["acceptable"])
    return estimator


def make_request() -> WineQualityRequest:
    """Devuelve una solicitud válida."""

    return WineQualityRequest.model_validate(WINE_SAMPLE)


def test_save_and_load_bundle_round_trip(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    estimator = make_estimator()
    manifest = create_manifest(estimator, "wine-quality-rf-v1")

    saved_manifest = save_model_bundle(bundle_path, estimator, manifest)
    loaded = load_model_bundle(bundle_path)
    prediction = infer_wine_quality(loaded, make_request())

    assert saved_manifest == manifest
    assert sorted(path.name for path in bundle_path.iterdir()) == [
        "manifest.json",
        "model.joblib",
    ]
    manifest = json.loads((bundle_path / "manifest.json").read_text())
    assert manifest["feature_names"] == list(FEATURE_NAMES)
    assert prediction.quality_band == "acceptable"
    assert prediction.confidence == 1.0


def test_load_rejects_a_reordered_feature_contract(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    estimator = make_estimator()
    save_model_bundle(
        bundle_path,
        estimator,
        create_manifest(estimator, "wine-quality-rf-v1"),
    )
    manifest_path = bundle_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["feature_names"] = list(reversed(manifest["feature_names"]))
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError):
        load_model_bundle(bundle_path)


class UnknownLabelEstimator:
    """Estimador falso para probar la validación de salida."""

    def predict(self, features: list[list[float]]) -> list[str]:
        return ["unknown"]

    def predict_proba(self, features: list[list[float]]) -> list[list[float]]:
        return [[1.0]]


def test_inference_rejects_an_unknown_model_label() -> None:
    estimator = UnknownLabelEstimator()
    bundle = LoadedModelBundle(
        estimator=estimator,
        manifest=create_manifest(estimator, "bad-output-v1"),
    )

    with pytest.raises(ValueError):
        infer_wine_quality(bundle, make_request())


def test_manifest_shape_is_strict() -> None:
    with pytest.raises(ValueError):
        ArtifactManifest.model_validate(
            {
                "schema_version": "wine-quality-bundle-v1",
                "model_version": "wine-quality-rf-v1",
                "preprocessing_version": "wine-red-features-v1",
                "feature_names": FEATURE_NAMES,
                "output_labels": ("needs_review", "acceptable", "excellent"),
                "estimator_type": "DummyClassifier",
                "unexpected": "not allowed",
            }
        )


def make_bundle(bundle_path: Path) -> None:
    """Guarda un bundle válido para romperlo después."""

    estimator = make_estimator()
    save_model_bundle(
        bundle_path,
        estimator,
        create_manifest(estimator, "wine-quality-rf-v1"),
    )


def test_load_rejects_a_corrupt_manifest(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    make_bundle(bundle_path)
    (bundle_path / "manifest.json").write_text("{esto no es json")

    with pytest.raises(ValueError, match="no es un JSON válido"):
        load_model_bundle(bundle_path)


def test_load_rejects_a_missing_manifest(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    make_bundle(bundle_path)
    (bundle_path / "manifest.json").unlink()

    with pytest.raises(FileNotFoundError, match="manifest.json"):
        load_model_bundle(bundle_path)


def test_load_rejects_another_preprocessing_version(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    make_bundle(bundle_path)
    manifest_path = bundle_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["preprocessing_version"] = "wine-red-features-v2"
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match="preprocessing_version"):
        load_model_bundle(bundle_path)


def test_load_validates_the_manifest_before_the_binary(tmp_path: Path) -> None:
    bundle_path = tmp_path / "wine_quality_bundle"
    make_bundle(bundle_path)
    (bundle_path / "model.joblib").write_bytes(b"no es un binario de joblib")
    manifest_path = bundle_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["schema_version"] = "wine-quality-bundle-v0"
    manifest_path.write_text(json.dumps(manifest))

    # Falla por el manifiesto, sin llegar a deserializar el binario.
    with pytest.raises(ValueError, match="schema_version"):
        load_model_bundle(bundle_path)


def test_save_rejects_an_estimator_without_predict_proba(tmp_path: Path) -> None:
    class OnlyPredict:
        def predict(self, features: list[list[float]]) -> list[str]:
            return ["acceptable"]

    estimator = OnlyPredict()

    with pytest.raises(ValueError, match="predict_proba"):
        save_model_bundle(
            tmp_path / "bundle", estimator, create_manifest(estimator, "demo-v1")
        )
    assert not (tmp_path / "bundle").exists()


def test_inference_message_names_the_unknown_label() -> None:
    estimator = UnknownLabelEstimator()
    bundle = LoadedModelBundle(
        estimator=estimator,
        manifest=create_manifest(estimator, "bad-output-v1"),
    )

    with pytest.raises(ValueError, match="'unknown'"):
        infer_wine_quality(bundle, make_request())
