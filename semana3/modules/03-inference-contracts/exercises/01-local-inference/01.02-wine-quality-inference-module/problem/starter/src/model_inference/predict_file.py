"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.

import argparse
import sys
from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from model_inference.contracts import WineQualityPrediction, WineQualityRequest
from model_inference.inference import DEFAULT_MODEL_PATH, infer_wine_quality,load_wine_quality_model



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=str(DEFAULT_MODEL_PATH))
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        predicts = predict_file(args.input, args.model)
        df_predicts = pd.DataFrame(predicts)
        df_predicts.to_csv(args.output, index=False)
    except (ValidationError, ValueError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(2)


def predict_file(path: str, model_path: str = str(DEFAULT_MODEL_PATH)) -> list:
    file_path = Path(path)
    data = pd.read_csv(file_path)
    model = load_wine_quality_model(model_path)
    results = []
    for index, row in data.iterrows():
        row = row.to_dict()
        sample_id = row.pop("sample_id")
        try:
            request = WineQualityRequest.model_validate(row)
            predict, probabilities = infer_wine_quality(model=model, row=request)
            result = {
                "sample_id": sample_id,
                "quality_band": predict[0],
                "confidence": probabilities,
                "model_version": "wine-quality-rf-v1",
                "preprocessing_version": "wine-red-features-v1",
            }
            results.append(WineQualityPrediction.model_validate(result).model_dump())
        except ValidationError as error:
            raise ValueError(f"Fila inválida para sample_id={sample_id}: {error}")

    return results

if __name__ == "__main__":
    main()
