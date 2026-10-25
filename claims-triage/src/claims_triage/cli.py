# UBICACION FINAL (ejercicio 1): src/claims_triage/cli.py
"""Programa principal: CSV -> validacion -> preprocess -> modelo -> CSV de salida.

Se ejecuta asi (desde la raiz del proyecto):
    uv run python -m claims_triage.cli --input data/claims.csv --output .tmp/predicciones.csv

Pasos del programa:
  1. read_claims : lee el CSV y valida cada fila con ClaimRequest    (ejercicio 2)
  2. load_model  : carga el modelo                                    (ejercicio 4)
  3. predict     : predice cada siniestro                             (ejercicios 3 y 4)
  4. escribe el CSV de salida                                         (ejercicio 4)
"""

import argparse
import csv  # noqa: F401
import os  # noqa: F401
import sys  # noqa: F401

from pydantic import ValidationError  # noqa: F401

from claims_triage.contracts import ClaimRequest  # noqa: F401
from claims_triage.inference import load_model, predict  # noqa: F401

# Columnas del CSV de salida, en este orden.
OUTPUT_COLUMNS = ["claim_id", "decision", "risk_probability", "model_version"]


def read_claims(path):
    """EJERCICIO 2: leer el CSV y devolver la lista de siniestros validados."""
    # TODO 2.8: leer el fichero CSV indicado, cuyas filas tienen las columnas
    #   de ClaimRequest.

    # TODO 2.9: validar cada fila con ClaimRequest. Si alguna fila no es valida,
    #   hay que parar con un ValueError cuyo mensaje diga en que LINEA del
    #   fichero esta el problema y cual es (la cabecera es la linea 1).

    # TODO 2.10: devolver la lista con todos los siniestros validados.
    raise NotImplementedError("TODO: ejercicio 2 (read_claims)")


def main(argv=None):
    # Ya hecho: lee los argumentos --input, --output y --model.
    parser = argparse.ArgumentParser(description="Triaje de siniestros")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="models/claims_triage_model.joblib")
    args = parser.parse_args(argv)  # noqa: F841

    # TODO 4.12: leer y validar los siniestros y cargar el modelo. Si algo de
    #   eso falla (ValueError), mostrar el error por la salida de errores y
    #   terminar con codigo de salida 2, SIN escribir ningun fichero.

    # TODO 4.13: obtener la prediccion de cada siniestro.

    # TODO 4.14: escribir el CSV de salida (con las columnas de OUTPUT_COLUMNS)
    #   en la ruta --output, creando la carpeta si no existe. Solo se escribe
    #   cuando todo lo anterior ha ido bien: si algo falla, no debe quedar un
    #   fichero a medias.

    # TODO 4.15: mostrar cuantos siniestros se han predicho y terminar con
    #   codigo de salida 0.
    raise NotImplementedError("TODO: ejercicio 4 (main)")


if __name__ == "__main__":
    raise SystemExit(main())
