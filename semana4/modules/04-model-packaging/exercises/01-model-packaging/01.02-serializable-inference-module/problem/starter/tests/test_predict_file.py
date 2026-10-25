import csv
from pathlib import Path

import pytest
from test_artifact import WINE_SAMPLE, make_estimator

from model_packaging.artifact import create_manifest, save_model_bundle
from model_packaging.predict_file import predict_file
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



# Comprobar 5 predicciones y la ejecución del CLI
def test_cli_generates_five_predictions(tmp_path: Path) -> None:
    import os
    import subprocess
    import sys

    bundle_path = tmp_path / "bundle"
    input_path = tmp_path / "five_wines.csv"
    output_path = tmp_path / "predictions.csv"

    write_bundle(bundle_path)

    rows = [
        {
            "sample_id": f"red-{i:03d}",
            **{key: str(value) for key, value in WINE_SAMPLE.items()},
        }
        for i in range(1, 6)
    ]

    write_input(input_path, rows=rows)

    project_path = Path(__file__).resolve().parents[1]

    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(project_path / "src")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "model_packaging.predict_file",
            "--bundle",
            str(bundle_path),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=project_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 5, result.stderr

    with output_path.open(newline="", encoding="utf-8") as source:
        predictions = list(csv.DictReader(source))

    assert len(predictions) == 5

    assert all(
        row["model_version"] == "wine-quality-rf-v1"
        for row in predictions
    )