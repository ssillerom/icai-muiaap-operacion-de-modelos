import csv
import sys
from pathlib import Path

import pytest
from test_artifact import WINE_SAMPLE, make_estimator

from model_packaging.artifact import create_manifest, save_model_bundle
from model_packaging.predict_file import main, predict_file
from model_packaging.preprocess import FEATURE_NAMES


def write_input(
    input_path: Path,
    rows: list[dict[str, str]] | None = None,
    extra_field: bool = False,
) -> None:
    """Escribe un CSV que sigue o rompe la cabecera del contrato."""

    source_rows = rows or [
        {
            "sample_id": "red-001",
            **{key: str(value) for key, value in WINE_SAMPLE.items()},
        }
    ]
    fieldnames = ["sample_id", *FEATURE_NAMES]
    if extra_field:
        fieldnames.append("unexpected_field")
    with input_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(source_rows)


def write_bundle(bundle_path: Path) -> None:
    """Prepara el bundle temporal que usará el CLI."""

    estimator = make_estimator()
    save_model_bundle(
        bundle_path,
        estimator,
        create_manifest(estimator, "wine-quality-rf-v1"),
    )


def test_predict_file_writes_a_validated_csv(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle"
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "predictions.csv"
    write_bundle(bundle_path)
    write_input(input_path)

    count = predict_file(input_path, output_path, bundle_path)

    assert count == 1
    assert output_path.exists()


def test_predict_file_rejects_an_unknown_column(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle"
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "predictions.csv"
    write_bundle(bundle_path)
    write_input(input_path, extra_field=True)

    with pytest.raises(ValueError):
        predict_file(input_path, output_path, bundle_path)

    assert not output_path.exists()


def test_predict_file_writes_nothing_when_a_later_row_is_invalid(
    tmp_path: Path,
) -> None:
    bundle_path = tmp_path / "bundle"
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "predictions.csv"
    write_bundle(bundle_path)
    valid_row = {
        "sample_id": "red-001",
        **{key: str(value) for key, value in WINE_SAMPLE.items()},
    }
    invalid_row = {**valid_row, "sample_id": "red-002", "alcohol": "not-a-number"}
    write_input(input_path, rows=[valid_row, invalid_row])

    with pytest.raises(ValueError):
        predict_file(input_path, output_path, bundle_path)

    assert not output_path.exists()


def test_predict_file_names_the_row_and_field_out_of_range(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle"
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "predictions.csv"
    write_bundle(bundle_path)
    valid_row = {
        "sample_id": "red-001",
        **{key: str(value) for key, value in WINE_SAMPLE.items()},
    }
    out_of_range_row = {**valid_row, "sample_id": "red-002", "ph": "99"}
    write_input(input_path, rows=[valid_row, out_of_range_row])

    with pytest.raises(ValueError, match=r"(?s)fila 3 \(sample_id='red-002'\).*ph"):
        predict_file(input_path, output_path, bundle_path)

    assert not output_path.exists()


def test_predict_file_writes_the_stable_output_schema(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle"
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "predictions.csv"
    write_bundle(bundle_path)
    write_input(input_path)

    predict_file(input_path, output_path, bundle_path)

    with output_path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    assert rows == [
        {
            "sample_id": "red-001",
            "quality_band": "acceptable",
            "confidence": "1.0",
            "model_version": "wine-quality-rf-v1",
            "preprocessing_version": "wine-red-features-v1",
        }
    ]
    assert not list(tmp_path.glob("*.tmp"))


def test_cli_returns_2_and_prints_the_error_for_an_invalid_row(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    bundle_path = tmp_path / "bundle"
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "predictions.csv"
    write_bundle(bundle_path)
    row = {
        "sample_id": "red-001",
        **{key: str(value) for key, value in WINE_SAMPLE.items()},
        "alcohol": "",
    }
    write_input(input_path, rows=[row])
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "predict_file",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--bundle",
            str(bundle_path),
        ],
    )

    assert main() == 2
    assert "fila 2 (sample_id='red-001')" in capsys.readouterr().err
    assert not output_path.exists()
