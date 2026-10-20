"""Script CLI que encadena contratos, preprocesado e inferencia."""

import argparse
import csv
import os
import sys

from pydantic import ValidationError

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


def read_samples(path):
    samples = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample_id = row.pop("sample_id", "")
            try:
                request = WineQualityRequest(**row)
            except ValidationError as error:
                raise ValueError(f"Muestra {sample_id}: {error}") from error
            samples.append((sample_id, request))
    return samples


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inferencia local de calidad de vino")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default=str(DEFAULT_MODEL_PATH))
    args = parser.parse_args(argv)

    try:
        samples = read_samples(args.input)
        model = load_wine_quality_model(args.model)
        predictions = []
        for sample_id, request in samples:
            features = preprocess_wine_request(request)
            prediction = infer_wine_quality(model, sample_id, features)
            predictions.append(prediction)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2

    folder = os.path.dirname(args.output)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for prediction in predictions:
            writer.writerow(prediction.model_dump())

    print(f"{len(predictions)} predicciones escritas en {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
