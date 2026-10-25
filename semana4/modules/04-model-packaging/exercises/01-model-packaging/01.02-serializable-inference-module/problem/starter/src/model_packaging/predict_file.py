"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
import csv
import os
import tempfile
from pathlib import Path

from pydantic import ValidationError

from model_packaging.artifact import (
    DEFAULT_BUNDLE_PATH,
    infer_wine_quality,
    load_model_bundle,
)

from model_packaging.contracts import WineQualityRequest


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """TODO: valida todas las filas y escribe el CSV solo al final."""

    # Cargar el modelo y su manifiesto
    bundle = load_model_bundle(bundle_path)

    # Definir las columnas que esperamos
    expected_columns = [
        "sample_id",
        *bundle.manifest.feature_names, # * es para desempaquetar los elementos de la tupla e introducirlos individualmente en la lista
    ]

    # Lista para guardar las predicciones
    results = []

    # Leer el CSV
    with input_path.open(newline="", encoding="utf-8") as source:

        reader = csv.DictReader(source)

        # Comprobar las columnas
        if reader.fieldnames != expected_columns:
            raise ValueError(
                f"Columnas incompatibles. Esperadas: {expected_columns}"
            )

        # Recorrer todas las filas
        for line_number, row in enumerate(reader, start=2):

            try:
                if not row["sample_id"]:
                    raise ValueError("sample_id no puede estar vacío")

                # Validar los datos del vino
                request = WineQualityRequest.model_validate(
                    {
                        feature: row[feature]
                        for feature in bundle.manifest.feature_names
                    }
                )

                # Realizar la predicción
                prediction = infer_wine_quality(bundle, request)

            except (ValidationError, ValueError, KeyError) as error:
                raise ValueError(
                    f"Error en la fila {line_number}: {error}"
                ) from error

            # Guardar la predicción en memoria
            results.append({
                "sample_id": row["sample_id"],
                **prediction.model_dump(),
            })

    # Definir las columnas de salida
    fieldnames = [
        "sample_id",
        "quality_band",
        "confidence",
        "model_version",
        "preprocessing_version",
    ]

    # Preparar la carpeta de salida
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Escribir primero en un archivo temporal
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8",
            delete=False,
            dir=output_path.parent,
            suffix=".tmp",
        ) as target:

            temporary_path = Path(target.name)

            writer = csv.DictWriter(
                target,
                fieldnames=fieldnames,
            )

            writer.writeheader()
            writer.writerows(results)

        # Publicar el CSV final
        os.replace(temporary_path, output_path)

    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    # Devolver el número de predicciones
    return len(results)




def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path) # qué CSV contiene los vinos
    parser.add_argument("--output", required=True, type=Path) # dónde queremos guardar las predicciones
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path) # dónde está el modelo empaquetado
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(
        predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    )
