from pathlib import Path

import pytest

from wine_quality.train import FEATURES, load_dataset, train_and_evaluate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "WineQT.csv"


def test_training_pipeline() -> None:
    dataset = load_dataset(DATASET_PATH)

    assert dataset.shape == (1143, 13)
    assert sorted(dataset["quality"].unique().tolist()) == [3, 4, 5, 6, 7, 8]
    assert "Id" not in FEATURES
    assert len(FEATURES) == 11

    metrics = train_and_evaluate(DATASET_PATH)
    repeated_metrics = train_and_evaluate(DATASET_PATH)

    assert metrics["rows"] == 1143
    assert metrics["features"] == 11
    assert metrics["classes"] == [3, 4, 5, 6, 7, 8]
    assert 0.0 <= metrics["validation_f1_macro"] <= 1.0
    assert repeated_metrics["validation_f1_macro"] == pytest.approx(
        metrics["validation_f1_macro"]
    )
