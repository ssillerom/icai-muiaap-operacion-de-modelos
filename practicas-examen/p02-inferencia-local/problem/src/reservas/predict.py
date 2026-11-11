"""CLI de inferencia (TU). Uso: uv run predecir --input ejemplos/reserva.json"""
import argparse
import json
import sys

from reservas.inference import predecir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Riesgo de cancelacion de una reserva")
    parser.add_argument("--input", required=True, help="Fichero JSON con la reserva")
    args = parser.parse_args(argv)

    # TODO: lee el JSON de args.input, llama a predecir() e imprime el
    #   resultado con json.dumps. Devuelve 0 si todo va bien.
    #   Si el fichero no existe (OSError), el JSON esta roto
    #   (json.JSONDecodeError) o los campos son incorrectos (ValueError),
    #   escribe "Error: ..." en sys.stderr y devuelve 1. Un CLI no debe
    #   terminar con una traza de Python.
    #   Comprobacion: tests/test_cli.py
    raise NotImplementedError("TODO: main")


if __name__ == "__main__":
    sys.exit(main())
