"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida. -> Esto
# quiere decir que no podemos ir escribiendo el CSV fila a fila mientras
# procesamos. Primero tenemos que guardar todas las predicciones en memoria
# y, solo si todas han salido bien, crea el fichero final.


# parser es una herramienta para leer lo que escribes en la terminal. Si
# ejecuto: python -m model_inference.predict_file --input datos.csv --output salida.csv,
# Python recibe eso como texto. argparse sirva para interpretar ese texto.

# Cuando hago: parser.add_argument("--input", required=True)
            #  parser.add_argument("--output", required=True)
# Estoy diciendo que mi programa acepta un argumento llamado --input y otro
# llamado --output. Luego, si yo hago: python -m model_inference.predict_file --input datos.csv --output salida.csv
# Entonces, después de ejecutar args = parser.parse_args(), estoy diciendo que args.input es datos.csv y
# que args.output es salida.csv, por lo que ya puedo usar cómodamente args.input y args.output

import argparse
import csv
import sys
from pathlib import Path

from pydantic import ValidationError

from model_inference.contracts import WineQualityRequest
from model_inference.inference import (DEFAULT_MODEL_PATH, infer_wine_quality, load_wine_quality_model)
from model_inference.preprocess import preprocess_wine_request

# python -m model_inference.predict_file \ --input assets/inference_samples.csv \ -- output predictions.csv

# DictReader produce algo conceptualmente como:
    #{
    #"sample_id": "red-001",
    #"fixed_acidity": "7.4",
    #"volatile_acidity": "0.7",
    #"alcohol": "9.4"
    #}


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH)

    args = parser.parse_args()

    artifact = load_wine_quality_model(args.model)

    predictions = []

    # Definir las columnas del CSV de salida:
    output_fields = [
        "sample_id",
        "quality_band",
        "confidence",
        "model_version",
        "preprocessing_version",
    ]

    # abre el csv y a partir de ahora al archivo abierto lo vamos a llamar source
    with open(args.input, newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source) # DictReader lee cada línea del CSV y la transforma en un diccionario

        # Recorremos las filas. Cada row es un diccionario, y cada diccionario tiene las variables de un vino (las 11 variables + el id)
        for row in reader:
            # Como WineQualityRequest tiene solo las 11 características, tenemos que separar el id
            sample_id = row.pop("sample_id", None) # pop hace dos cosas: guarda el valor en la variable sample_id y además lo quita del diccionario. El None es para que si no existe, devuelve None en vez de error
            if not sample_id:
                raise ValueError("sample_id no puede estar vacío")

            try:
                request = WineQualityRequest(**row) # ** desempaqueta el diccionario.
                # si tenemos que row es: row = {
                #    "fixed_acidity": "7.4",
                #    "volatile_acidity": "0.7",
                #    "citric_acid": "0.0",
                #}
                ## Si hacemos **row, lo que va a hacer es:
                #WineQualityRequest(
                #    fixed_acidity="7.4",
                #    volatile_acidity="0.7",
                #    citric_acid="0.0",
                #)

            except ValidationError as error:
                raise ValueError(f"Error en la muestra {sample_id}: {error}") from error

            features = preprocess_wine_request(request)

            prediction = infer_wine_quality(artifact, features, sample_id)

            predictions.append(prediction)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", newline="", encoding="utf-8") as destination:
            writer = csv.DictWriter(destination, fieldnames=output_fields)
            writer.writeheader()

            for prediction in predictions:
                writer.writerow(prediction.model_dump())


if __name__ == "__main__":
    try:
        main()
    except (ValueError, ValidationError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)