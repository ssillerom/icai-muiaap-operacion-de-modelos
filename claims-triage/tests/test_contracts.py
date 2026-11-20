# UBICACION FINAL (ejercicio 1): tests/test_contracts.py  (no modificar)
"""Ejercicio 2: validar con Pydantic las filas del CSV."""

import pytest
from pydantic import ValidationError

from claims_triage.contracts import ClaimRequest

# Una fila tal y como la lee csv.DictReader: todo es texto
ROW = {
    "claim_id": "X1",
    "policy_type": "todo_riesgo",
    "driver_age": "29",
    "vehicle_age_years": "3.5",
    "claim_amount_eur": "1250.50",
    "injuries": "1",
    "police_report": "0",
}


def make(**changes):
    data = dict(ROW)
    data.update(changes)
    return ClaimRequest(**data)


def test_valid_row_is_converted_to_the_right_types():
    claim = make()
    assert claim.claim_id == "X1"
    assert claim.driver_age == 29
    assert claim.vehicle_age_years == 3.5
    assert claim.claim_amount_eur == 1250.50
    assert claim.injuries == 1
    assert claim.police_report == 0


def test_empty_vehicle_age_is_none():
    assert make(vehicle_age_years="").vehicle_age_years is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("policy_type", "premium"),
        ("driver_age", "16"),
        ("driver_age", "abc"),
        ("claim_amount_eur", "-350"),
        ("claim_amount_eur", "0"),
        ("injuries", "2"),
        ("police_report", "-1"),
        ("vehicle_age_years", "99"),
        ("claim_id", ""),
    ],
)
def test_invalid_values_are_rejected(field, value):
    with pytest.raises(ValidationError) as info:
        make(**{field: value})
    assert info.value.errors()[0]["loc"] == (field,)


def test_extra_column_is_rejected():
    data = dict(ROW)
    data["unexpected_field"] = "x"
    with pytest.raises(ValidationError):
        ClaimRequest(**data)


def test_missing_column_is_rejected():
    data = dict(ROW)
    del data["driver_age"]
    with pytest.raises(ValidationError):
        ClaimRequest(**data)
