"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from model_packaging.artifact import (
    DEFAULT_BUNDLE_PATH,
    infer_wine_quality,
    load_model_bundle,
)
from model_packaging.contracts import WineQualityRequest
from model_packaging.preprocess import FEATURE_NAMES

INPUT_COLUMNS = ("sample_id", *FEATURE_NAMES)
OUTPUT_COLUMNS = (
    "sample_id",
    "quality_band",
    "confidence",
    "model_version",
    "preprocessing_version",
)


def read_rows(input_path: Path) -> list[dict[str, str]]:
    """Lee el CSV completo y comprueba que la cabecera cumple el contrato."""

    with Path(input_path).open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError(f"El CSV {input_path} está vacío: falta la cabecera")
        unexpected = [name for name in reader.fieldnames if name not in INPUT_COLUMNS]
        missing = [name for name in INPUT_COLUMNS if name not in reader.fieldnames]
        if unexpected or missing:
            raise ValueError(
                f"Cabecera del CSV no válida: columnas no permitidas {unexpected}, "
                f"columnas que faltan {missing}"
            )
        return list(reader)


def write_predictions(output_path: Path, results: list[dict[str, object]]) -> None:
    """Escribe el CSV de salida en un temporal y lo publica al terminar."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f"{output_path.name}.tmp")
    try:
        with temporary.open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(results)
        temporary.replace(output_path)
    finally:
        temporary.unlink(missing_ok=True)


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """Valida todas las filas y escribe el CSV solo al final.

    Devuelve el número de predicciones escritas. Ante cualquier fila inválida
    lanza ValueError, indicando fila y sample_id, y no crea el CSV de salida.
    """

    bundle = load_model_bundle(bundle_path)
    results: list[dict[str, object]] = []
    for line, row in enumerate(read_rows(input_path), start=2):
        sample_id = row.pop("sample_id", None)
        try:
            if not sample_id:
                raise ValueError("falta sample_id")
            if None in row:
                raise ValueError("la fila tiene más valores que columnas")
            request = WineQualityRequest.model_validate(row)
            prediction = infer_wine_quality(bundle, request)
        except ValueError as error:
            raise ValueError(
                f"fila {line} (sample_id={sample_id!r}): {error}"
            ) from error
        results.append({"sample_id": sample_id, **prediction.model_dump()})

    write_predictions(output_path, results)
    return len(results)


def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


def main() -> int:
    """Ejecuta el comando: 0 si todo va bien y 2 si algo no cumple el contrato."""

    arguments = parse_args()
    try:
        count = predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print(f"{count} predicciones escritas en {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
