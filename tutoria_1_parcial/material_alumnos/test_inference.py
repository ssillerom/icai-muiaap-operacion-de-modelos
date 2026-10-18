# UBICACION FINAL (ejercicio 1): tests/test_inference.py  (no modificar)
"""Ejercicio 4: cargar el modelo, predecir y validar la salida."""

from pathlib import Path

import joblib
import pytest
from pydantic import ValidationError

from claims_triage.contracts import ClaimPrediction, ClaimRequest
from claims_triage.inference import load_model, predict

MODEL = Path(__file__).resolve().parents[1] / "models" / "claims_triage_model.joblib"


def make(**changes):
    data = {
        "claim_id": "X1",
        "policy_type": "todo_riesgo",
        "driver_age": "23",
        "vehicle_age_years": "1",
        "claim_amount_eur": "18500.75",
        "injuries": "1",
        "police_report": "0",
    }
    data.update(changes)
    return ClaimRequest(**data)


def test_model_loads():
    model = load_model(MODEL)
    assert model["model_version"] != ""


def test_risky_claim_goes_to_manual_review():
    prediction = predict(load_model(MODEL), make())
    assert isinstance(prediction, ClaimPrediction)
    assert prediction.claim_id == "X1"
    assert prediction.decision == "revision_manual"
    assert 0 <= prediction.risk_probability <= 1
    assert prediction.model_version == load_model(MODEL)["model_version"]


def test_safe_claim_goes_to_normal_processing():
    claim = make(
        policy_type="basico",
        driver_age="50",
        claim_amount_eur="150",
        injuries="0",
        police_report="1",
    )
    prediction = predict(load_model(MODEL), claim)
    assert prediction.decision == "tramitacion_normal"


def test_model_with_other_features_is_rejected(tmp_path):
    data = joblib.load(MODEL)
    data["feature_names"] = ["otra", "cosa"]
    bad = tmp_path / "bad.joblib"
    joblib.dump(data, bad)
    with pytest.raises(ValueError):
        load_model(bad)


def test_output_model_rejects_invalid_values():
    with pytest.raises(ValidationError):
        ClaimPrediction(claim_id="X1", decision="quizas", risk_probability=0.5, model_version="v")
    with pytest.raises(ValidationError):
        ClaimPrediction(
            claim_id="X1", decision="revision_manual", risk_probability=1.5, model_version="v"
        )
