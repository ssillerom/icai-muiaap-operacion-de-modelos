"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""
import pandas as pd
from src.model_inference.contracts import WineQualityRequest
from src.model_inference.inference import DEFAULT_MODEL_PATH, load_wine_quality_model, infer_wine_quality
from src.model_inference.preprocess import preprocess_wine_request
import argparse
from pathlib import Path
import csv
import sys
# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.



def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--model", default=DEFAULT_MODEL_PATH)
        parser.add_argument("--input", required=True, type=Path)
        parser.add_argument("--output", required=True, type=Path)
        args = parser.parse_args()
        print(args.model, args.input, args.output)

        with open(args.input, newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            lista = []
            for fila in lector:
                sample_id = fila["sample_id"]
                fila.pop("sample_id")
                if not sample_id.strip():
                    raise ValueError("sample_id vacío: cada fila necesita un identificador")
                try:
                    request= WineQualityRequest(**fila) #los ** traducen a clave = valor para la request
                    vector = preprocess_wine_request(request)
                    artefacto = load_wine_quality_model(args.model)
                    prediction = infer_wine_quality(artefacto, vector)
                except ValueError as error:
                    raise ValueError(f"Fila {sample_id} inválida: {error}")
                lista.append([sample_id, prediction])

        with open(args.output, "w", newline="", encoding="utf-8") as e:
            writer = csv.DictWriter(e, fieldnames=["sample_id", "quality_band", "confidence", "model_version", "preprocessing_version"])
            writer.writeheader() 
            for i in range(len(lista)):
                dicc = {"sample_id" :lista[i][0]}
                dicc.update(lista[i][1].model_dump())
                writer.writerow(dicc)
    except ValueError as error:
        print(f"ha habido un error: {error}", file=sys.stderr)
        sys.exit(2)
            

if __name__ == "__main__":
    main()