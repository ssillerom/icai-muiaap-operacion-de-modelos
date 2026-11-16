import csv
import subprocess
import sys
from pathlib import Path

import joblib
from sklearn.dummy import DummyClassifier

# La expectativa vive deliberadamente fuera del starter: cambiar su contrato
# no debe modificar el artefacto contra el que se prueba el CLI.
EXPECTED_FEATURE_NAMES = (
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
)

WINE_SAMPLE = {
    "fixed_acidity": "7.4",
    "volatile_acidity": "0.7",
    "citric_acid": "0.0",
    "residual_sugar": "1.9",
    "chlorides": "0.076",
    "free_sulfur_dioxide": "11.0",
    "total_sulfur_dioxide": "34.0",
    "density": "0.9978",
    "ph": "3.51",
    "sulphates": "0.56",
    "alcohol": "9.4",
}


def write_instructor_model(
    model_path: Path,
    quality_band: str = "acceptable",
) -> None:
    """Crea un artefacto estable para probar el comando público de inferencia."""

    estimator = DummyClassifier(strategy="constant", constant=quality_band)
    estimator.fit([[0.0] * len(EXPECTED_FEATURE_NAMES)], [quality_band])
    joblib.dump(
        {
            "estimator": estimator,
            "feature_names": list(EXPECTED_FEATURE_NAMES),
            "model_version": "wine-quality-rf-v1",
        },
        model_path,
    )


def write_input_csv(
    input_path: Path,
    extra_field: bool = False,
    sample_id: str = "red-001",
    second_invalid_row: bool = False,
    sample_ids: tuple[str, ...] | None = None,
    invalid_ph: bool = False,
    missing_field: str | None = None,
) -> None:
    """Escribe filas de Kaggle para comprobar contratos del comando local."""

    ids = sample_ids or (sample_id,)
    rows = []
    for index, current_sample_id in enumerate(ids):
        row = {"sample_id": current_sample_id, **WINE_SAMPLE}
        if invalid_ph and index == 0:
            row["ph"] = "99"
        if missing_field is not None:
            row.pop(missing_field, None)
        if extra_field:
            row["unexpected_field"] = "not allowed"
        rows.append(row)

    if second_invalid_row:
        invalid_row = {
            "sample_id": "red-002",
            **WINE_SAMPLE,
            "alcohol": "invalid",
        }
        if missing_field is not None:
            invalid_row.pop(missing_field, None)
        rows.append(invalid_row)

    with input_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_predict_file(
    model_path: Path,
    input_path: Path,
    output_path: Path,
) -> subprocess.CompletedProcess[str]:
    """Invoca el mismo comando que ejecutará el alumnado durante el taller."""

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "model_inference.predict_file",
            "--model",
            str(model_path),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_predict_file_writes_predictions_for_kaggle_rows(tmp_path: Path) -> None:
    model_path = tmp_path / "wine_quality_classifier.joblib"
    input_path = tmp_path / "inference_samples.csv"
    output_path = tmp_path / "predictions.csv"
    write_instructor_model(model_path)
    write_input_csv(input_path)

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 0
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


def test_predict_file_writes_all_requested_rows(tmp_path: Path) -> None:
    model_path = tmp_path / "wine_quality_classifier.joblib"
    input_path = tmp_path / "five_samples.csv"
    output_path = tmp_path / "predictions.csv"
    sample_ids = tuple(f"red-00{number}" for number in range(1, 6))
    write_instructor_model(model_path)
    write_input_csv(input_path, sample_ids=sample_ids)

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 0
    with output_path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    assert [row["sample_id"] for row in rows] == list(sample_ids)
    assert list(rows[0]) == [
        "sample_id",
        "quality_band",
        "confidence",
        "model_version",
        "preprocessing_version",
    ]


def test_predict_file_rejects_an_unknown_csv_column(tmp_path: Path) -> None:
    model_path = tmp_path / "wine_quality_classifier.joblib"
    input_path = tmp_path / "invalid_inference_samples.csv"
    output_path = tmp_path / "predictions.csv"
    write_instructor_model(model_path)
    write_input_csv(input_path, extra_field=True)

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 2
    assert "unexpected_field" in completed.stderr
    assert not output_path.exists()


def test_predict_file_rejects_a_missing_required_field(tmp_path: Path) -> None:
    model_path = tmp_path / "wine_quality_classifier.joblib"
    input_path = tmp_path / "missing_alcohol.csv"
    output_path = tmp_path / "predictions.csv"
    write_instructor_model(model_path)
    write_input_csv(input_path, missing_field="alcohol")

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 2
    assert "alcohol" in completed.stderr
    assert not output_path.exists()


def test_predict_file_rejects_an_out_of_range_field(tmp_path: Path) -> None:
    model_path = tmp_path / "wine_quality_classifier.joblib"
    input_path = tmp_path / "invalid_ph.csv"
    output_path = tmp_path / "predictions.csv"
    write_instructor_model(model_path)
    write_input_csv(input_path, invalid_ph=True)

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 2
    assert "ph" in completed.stderr
    assert not output_path.exists()


def test_predict_file_leaves_no_output_when_a_later_row_is_invalid(
    tmp_path: Path,
) -> None:
    model_path = tmp_path / "wine_quality_classifier.joblib"
    input_path = tmp_path / "partially_invalid_inference_samples.csv"
    output_path = tmp_path / "predictions.csv"
    write_instructor_model(model_path)
    write_input_csv(input_path, second_invalid_row=True)

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 2
    assert "red-002" in completed.stderr
    assert not output_path.exists()


def test_predict_file_rejects_an_invalid_prediction_category(tmp_path: Path) -> None:
    model_path = tmp_path / "invalid_category.joblib"
    input_path = tmp_path / "inference_samples.csv"
    output_path = tmp_path / "predictions.csv"
    write_instructor_model(model_path, quality_band="unknown")
    write_input_csv(input_path)

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 2
    assert "quality_band" in completed.stderr
    assert not output_path.exists()


def test_predict_file_rejects_an_incomplete_model_artifact(tmp_path: Path) -> None:
    model_path = tmp_path / "incomplete_model.joblib"
    input_path = tmp_path / "inference_samples.csv"
    output_path = tmp_path / "predictions.csv"
    joblib.dump(
        {
            "feature_names": list(EXPECTED_FEATURE_NAMES),
            "model_version": "wine-quality-rf-v1",
        },
        model_path,
    )
    write_input_csv(input_path)

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 2
    assert "clasificador compatible" in completed.stderr
    assert not output_path.exists()


def test_predict_file_rejects_an_empty_sample_id(tmp_path: Path) -> None:
    model_path = tmp_path / "wine_quality_classifier.joblib"
    input_path = tmp_path / "empty_sample_id.csv"
    output_path = tmp_path / "predictions.csv"
    write_instructor_model(model_path)
    write_input_csv(input_path, sample_id="")

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 2
    assert "sample_id" in completed.stderr
    assert not output_path.exists()


def test_predict_file_rejects_an_incompatible_model_artifact(tmp_path: Path) -> None:
    model_path = tmp_path / "incompatible_wine_model.joblib"
    input_path = tmp_path / "inference_samples.csv"
    output_path = tmp_path / "predictions.csv"
    estimator = DummyClassifier(strategy="constant", constant="acceptable")
    estimator.fit([[0.0] * len(EXPECTED_FEATURE_NAMES)], ["acceptable"])
    joblib.dump(
        {
            "estimator": estimator,
            "feature_names": list(reversed(EXPECTED_FEATURE_NAMES)),
            "model_version": "wine-quality-rf-v1",
        },
        model_path,
    )
    write_input_csv(input_path)

    completed = run_predict_file(model_path, input_path, output_path)

    assert completed.returncode == 2
    assert "feature_names" in completed.stderr
    assert not output_path.exists()
