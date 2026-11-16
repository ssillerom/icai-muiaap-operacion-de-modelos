
 
import argparse
import csv
import sys
from pathlib import Path
 
from pydantic import ValidationError
 
from model_inference.contracts import WineQualityRequest
from model_inference.inference import (
    DEFAULT_MODEL_PATH,
    infer_wine_quality,
    load_wine_quality_model,
)
 

OUTPUT_COLUMNS = [
    "sample_id",
    "quality_band",
    "confidence",
    "model_version",
    "preprocessing_version",
]
 
 
def read_samples(path):

    lista_limpia = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, fila in enumerate(reader, start=2):
            try:
                request = WineQualityRequest.model_validate(fila)
                lista_limpia.append(request)
            except ValidationError as error:
                sample_id = fila.get("sample_id")
                raise ValueError(
                    f"Error en la linea {i} (sample_id={sample_id}): {error}"
                ) from error
 
    return lista_limpia
 
 
def main(argv=None):
    parser = argparse.ArgumentParser(description="Inferencia de calidad de vino")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH)
    args = parser.parse_args(argv)
 

    try:
        requests = read_samples(args.input)
        model = load_wine_quality_model(args.model)
 
        predicciones = []
        for muestra in requests:
            prediccion = infer_wine_quality(model, muestra)
            predicciones.append(prediccion)
    except (ValueError, TypeError) as e:
        print(e, file=sys.stderr)
        return 2
 

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for p in predicciones:
            writer.writerow(p.model_dump())
 
    print(f"Se han predicho {len(predicciones)} muestras")
    return 0
 
 
if __name__ == "__main__":
    raise SystemExit(main())
    sys.exit(main())