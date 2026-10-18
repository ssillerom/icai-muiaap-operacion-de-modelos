"""Comando que lee un CSV de vinos, predice cada uno y escribe otro CSV."""
import argparse
import csv
import sys
from pathlib import Path

from model_inference.contracts import WineQualityPrediction, WineQualityRequest

from model_inference.contracts import WineQualityPrediction, WineQualityRequest
from model_inference.inference import (
    DEFAULT_MODEL_PATH,
    infer_wine_quality,
    load_wine_quality_model,
)
from model_inference.preprocess import preprocess_wine_request

# columnas del csv de salida, en este orden
COLUMNAS_SALIDA = [
    "sample_id",
    "quality_band",
    "confidence",
    "model_version",
    "preprocessing_version",
]

def leer_y_predecir(ruta: Path, contenido: dict) -> list[WineQualityPrediction]:

    resultados = []

    with open(ruta, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            # fila es un diccionario, por ejemplo:
            # {"sample_id": "red-001", "ph": "3.51", ...}
            # pop saca sample_id de la fila y nos da su valor. Lo quitamos
            # porque no es una característica del vino y el contrato no admite
            # campos de más. El "" es lo que devuelve si no existe sample_id
            sample_id = fila.pop("sample_id", "")
            try:
                #los ** pasan cada clave de la fila como argumento,deshacen el diccionario
                peticion = WineQualityRequest(**fila)
                caracteristicas = preprocess_wine_request(peticion)
                resultado = infer_wine_quality(sample_id, caracteristicas, contenido)
                resultados.append(resultado)
            except ValueError as error:
                # el error de pydantic es un tipo de ValueError, por eso lo
                # cogemos aquí. Lo lanzamos otra vez añadiendo qué vino y qué
                # línea del csv ha fallado. El from error guarda el error original 
                raise ValueError(
                    f"Fila inválida (sample_id={sample_id}, "
                    f"línea {reader.line_num}): {error}"
                ) from error
    if not resultados:
        raise ValueError("El CSV no tiene filas.")
    return resultados


def guardar_csv(resultados: list[WineQualityPrediction], ruta: Path) -> None:
    # crea la carpeta de salida si no existe, como el os.makedirs de la tutoría,pero
    #usando otro metodo(es el que habia q haber usado en el examen)
    # parents=True crea también las carpetas de arriba y exist_ok=True no da error
    # si la carpeta ya existe.
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS_SALIDA)
        writer.writeheader()
        for resultado in resultados:
            # model_dump convierte la predicción en un diccionario, que es lo que
            # necesita writerow
            writer.writerow(resultado.model_dump())

def main(argv: list[str] | None = None) -> int:
    # estos son los argumentos que acepta el comando
    parser = argparse.ArgumentParser(description="Predice la calidad de vinos.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default=str(DEFAULT_MODEL_PATH))
    args = parser.parse_args(argv)

    # cogemos dos tipos de error: ValueError (modelo o fila mal) y
    # FileNotFoundError (el archivo no existe)
    try:
        contenido = load_wine_quality_model(Path(args.model))
        resultados = leer_y_predecir(Path(args.input), contenido)
    except (ValueError, FileNotFoundError) as error:
        # mostramos el error y salimos con 2 sin haber escrito ningún archivo
        print(error, file=sys.stderr)
        return 2

    # solo escribimos el csv si todas las filas han ido bien
    guardar_csv(resultados, Path(args.output))
    print(f"Se han predicho {len(resultados)} filas en {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())