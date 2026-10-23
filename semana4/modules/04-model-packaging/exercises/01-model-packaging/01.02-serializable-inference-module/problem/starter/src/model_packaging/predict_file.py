"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from model_inference.contracts import WineQualityRequest

from model_packaging.artifact import DEFAULT_BUNDLE_PATH, infer_wine_quality, load_model_bundle
from csv import DictReader, DictWriter

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
        x = WineQualityRequest.model_validate(row)
        prediction = infer_wine_quality(bundle, x)
        result.append(prediction)
    
    DictWriter(output_path.open(), fieldnames=WineQualityRequest.model_fields)


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
