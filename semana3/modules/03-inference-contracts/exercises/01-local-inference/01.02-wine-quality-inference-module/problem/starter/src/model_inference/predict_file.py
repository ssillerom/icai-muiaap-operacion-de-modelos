"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.

import csv
import argparse
from pathlib import Path
from .contracts import WineQualityRequest
from .preprocess import preprocess_wine_request
from .inference import WineModel

def main():
    parser = argparse.ArgumentParser(description="Inferencia local de calidad de vino")
    parser.add_argument("--input", required=True, type=Path, help="Ruta al CSV de entrada")
    parser.add_argument("--output", required=True, type=Path, help="Ruta al CSV de salida")
    parser.add_argument("--model", default=Path("models/wine_quality_classifier.joblib"), type=Path)
    args = parser.parse_args()

    # 1. Carga del modelo (falla rápido si el binario es incompatible)
    model = WineModel(args.model)
    
    # 2. Lectura y procesamiento en memoria
    predictions = []
    with args.input.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_number, row in enumerate(reader, start=1):
            sample_id = row.pop("sample_id", None)
            if not sample_id:
                raise ValueError(f"Fila {row_number}: Falta sample_id")
            
            # Si una sola fila es inválida, Pydantic lanzará ValidationError y el script morirá aquí
            request = WineQualityRequest.model_validate(row)
            features = preprocess_wine_request(request)
            
            prediction = model.predict(sample_id=sample_id, vector=features.as_vector())
            predictions.append(prediction)

    # 3. Escritura atómica (solo llegamos aquí si el 100% de las filas pasaron)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(WineQualityPrediction.model_fields.keys()))
        writer.writeheader()
        for pred in predictions:
            writer.writerow(pred.model_dump())

if __name__ == "__main__":
    main()