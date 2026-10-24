"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

from pydantic import ValidationError

from model_packaging.artifact import (
    DEFAULT_BUNDLE_PATH,
    infer_wine_quality,
    load_model_bundle,
)
from model_packaging.contracts import WineQualityRequest

OUTPUT_COLUMNS = [
    "sample_id",
    "quality_band",
    "confidence",
    "model_version",
    "preprocessing_version",
]


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """Valida todas las filas y escribe el CSV solo al final."""

    bundle = load_model_bundle(bundle_path)
    rows = []

    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample_id = row.pop("sample_id", "")
            if sample_id == "":
                raise ValueError("Hay una fila con sample_id vacío.")
            try:
                request = WineQualityRequest.model_validate(row)
            except ValidationError as error:
                raise ValueError(f"Muestra {sample_id}: {error}") from error

            prediction = infer_wine_quality(bundle, request)
            output_row = prediction.model_dump()
            output_row["sample_id"] = sample_id
            rows.append(output_row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".tmp")
    with temporary_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary_path, output_path)
    return len(rows)


def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    try:
        count = predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    except (FileNotFoundError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"Predicciones escritas: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
