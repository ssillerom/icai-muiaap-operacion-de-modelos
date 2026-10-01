"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""
"""Script CLI que encadena contratos, preprocesado e inferencia."""

import argparse
import csv
import sys
from pathlib import Path

from pydantic import ValidationError

from model_inference.contracts import WineQualityPrediction, WineQualityRequest
from model_inference.inference import (
    DEFAULT_MODEL_PATH,
    infer_wine_quality,
    load_wine_quality_model,
)
from model_inference.preprocess import preprocess_wine_request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inferencia local de calidad de vino")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH, type=Path)
    return parser.parse_args()


def read_requests(input_path: Path) -> list[WineQualityRequest]:
    """Lee y valida todas las filas del CSV. Falla entero si una fila es inválida."""
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    requests: list[WineQualityRequest] = []
    for i, row in enumerate(rows, start=1):
        try:
            requests.append(WineQualityRequest(**row))
        except ValidationError as exc:
            raise ValueError(f"Fila {i} inválida en {input_path}: {exc}") from exc

    return requests


def write_predictions(output_path: Path, predictions: list[WineQualityPrediction]) -> None:
    """Escribe el CSV de salida solo cuando ya tenemos TODAS las predicciones."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(WineQualityPrediction.model_fields.keys())
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for prediction in predictions:
            writer.writerow(prediction.model_dump())


def main() -> None:
    args = parse_args()

    try:
        requests = read_requests(args.input)
        bundle = load_wine_quality_model(args.model)

        predictions: list[WineQualityPrediction] = []
        for request in requests:
            features = preprocess_wine_request(request)
            quality_band, confidence = infer_wine_quality(bundle, features)
            predictions.append(
                WineQualityPrediction(
                    sample_id=request.sample_id,
                    quality_band=quality_band,
                    confidence=confidence,
                    model_version=bundle["model_version"],
                    preprocessing_version=features.preprocessing_version,
                )
            )

        write_predictions(args.output, predictions)

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.
