# UBICACION FINAL (ejercicio 1): tests/test_cli.py  (no modificar)
"""Todo junto: CSV -> validacion -> preprocess -> modelo -> CSV de salida."""

import csv
from pathlib import Path

import pytest

from claims_triage.cli import main

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "data" / "claims.csv"
WITH_ERRORS = ROOT / "data" / "claims_con_errores.csv"
MODEL = ROOT / "models" / "claims_triage_model.joblib"
EXPECTED = Path(__file__).parent / "predicciones_esperadas.csv"


def read(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)
    return rows


def run(tmp_path, input_path):
    out = tmp_path / "salida" / "predicciones.csv"
    code = main(["--input", str(input_path), "--output", str(out), "--model", str(MODEL)])
    return code, out


def test_predictions_match_expected(tmp_path):
    code, out = run(tmp_path, CLAIMS)
    assert code == 0
    got = read(out)
    expected = read(EXPECTED)
    assert len(got) == len(expected)
    for i in range(len(expected)):
        assert got[i]["claim_id"] == expected[i]["claim_id"]
        assert got[i]["decision"] == expected[i]["decision"]
        got_p = float(got[i]["risk_probability"])
        assert got_p == pytest.approx(float(expected[i]["risk_probability"]), abs=0.002)
    assert list(got[0].keys()) == ["claim_id", "decision", "risk_probability", "model_version"]


def test_invalid_row_stops_everything_and_writes_nothing(tmp_path):
    code, out = run(tmp_path, WITH_ERRORS)
    assert code == 2
    assert not out.exists()


def test_extra_column_stops_everything_and_writes_nothing(tmp_path):
    bad = tmp_path / "extra.csv"
    text = CLAIMS.read_text(encoding="utf-8")
    bad.write_text(text.replace("claim_id,", "claim_id,extra,", 1), encoding="utf-8")
    code, out = run(tmp_path, bad)
    assert code == 2
    assert not out.exists()
