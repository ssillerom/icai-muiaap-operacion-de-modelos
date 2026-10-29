"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
from csv import DictReader, DictWriter
from pathlib import Path

from model_packaging.artifact import (
    DEFAULT_BUNDLE_PATH,
    infer_wine_quality,
    load_model_bundle,
)
from model_packaging.contracts import WineQualityRequest


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """TODO: valida todas las filas y escribe el CSV solo al final."""
    csv_reader = DictReader(input_path.open())
    bundle = load_model_bundle(bundle_path)
    result = []
    for row in csv_reader:
        prep_row = {key: value for key, value in row.items() if key != "sample_id"}
        x = WineQualityRequest.model_validate(prep_row)
        prediction = infer_wine_quality(bundle, x)
        result.append(prediction)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = DictWriter(
            f,
            fieldnames=[
                "quality_band",
                "confidence",
                "model_version",
                "preprocessing_version",
            ],
        )
        writer.writeheader()
        writer.writerows(prediction.model_dump() for prediction in result)
    return len(result)


def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(
        predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    )
