"""CLI: python -m model_inference.predict_file --input <csv> --output <csv>"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from model_inference.contracts import WineQualityRequest
from model_inference.inference import (
    DEFAULT_MODEL_PATH,
    infer_wine_quality,
    load_wine_quality_model,
)
from model_inference.preprocess import preprocess_wine_request

OUTPUT_COLUMNS = [
    "sample_id",
    "quality_band",
    "confidence",
    "model_version",
    "preprocessing_version",
]


def read_rows(input_path: Path) -> list[dict]:
    with Path(input_path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def predict_file(
    input_path: Path,
    output_path: Path,
    model_path: Path = DEFAULT_MODEL_PATH,
) -> int:
    """Valida todo primero y escribe el CSV solo al final."""
    try:
        bundle = load_wine_quality_model(model_path)
        results = []
        for line, row in enumerate(read_rows(input_path), start=2):
            sample_id = row.pop("sample_id", None)
            try:
                if not sample_id:
                    raise ValueError("falta sample_id")
                request = WineQualityRequest.model_validate(row)
                features = preprocess_wine_request(request)
                prediction = infer_wine_quality(bundle, features)
            except ValueError as error:
                raise ValueError(
                    f"fila {line} (sample_id={sample_id!r}): {error}"
                ) from error
            results.append({"sample_id": sample_id, **prediction.model_dump()})
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(results)

    print(f"{len(results)} predicciones escritas en {output_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(predict_file(arguments.input, arguments.output, arguments.model))
