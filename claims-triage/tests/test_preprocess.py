# UBICACION FINAL (ejercicio 1): tests/test_preprocess.py  (no modificar)
"""Ejercicio 3: limpieza y categorizacion en una funcion preprocess."""

from claims_triage.contracts import ClaimRequest
from claims_triage.preprocess import FEATURE_NAMES, preprocess

ROW = {
    "claim_id": "X1",
    "policy_type": "terceros_ampliado",
    "driver_age": "40",
    "vehicle_age_years": "6",
    "claim_amount_eur": "1000",
    "injuries": "1",
    "police_report": "0",
}


def make(**changes):
    data = dict(ROW)
    data.update(changes)
    return ClaimRequest(**data)


def test_vector_has_one_number_per_feature():
    vector = preprocess(make())
    assert len(vector) == len(FEATURE_NAMES)


def test_vector_order_follows_feature_names():
    vector = preprocess(make())
    assert vector[FEATURE_NAMES.index("driver_age")] == 40
    assert vector[FEATURE_NAMES.index("vehicle_age_years")] == 6
    assert vector[FEATURE_NAMES.index("claim_amount_eur")] == 1000
    assert vector[FEATURE_NAMES.index("injuries")] == 1
    assert vector[FEATURE_NAMES.index("police_report")] == 0


def test_missing_vehicle_age_is_filled_with_8():
    vector = preprocess(make(vehicle_age_years=""))
    assert vector[FEATURE_NAMES.index("vehicle_age_years")] == 8.0


def test_policy_type_becomes_a_number():
    position = FEATURE_NAMES.index("policy_code")
    assert preprocess(make(policy_type="basico"))[position] == 0
    assert preprocess(make(policy_type="terceros_ampliado"))[position] == 1
    assert preprocess(make(policy_type="todo_riesgo"))[position] == 2


def test_claim_id_is_not_in_the_vector():
    assert "claim_id" not in FEATURE_NAMES
