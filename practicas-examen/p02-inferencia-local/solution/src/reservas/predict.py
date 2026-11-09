"""CLI de inferencia. Uso: uv run predecir --input ejemplos/reserva.json"""
import argparse
import json
import sys

from reservas.inference import predecir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Riesgo de cancelacion de una reserva")
    parser.add_argument("--input", required=True, help="Fichero JSON con la reserva")
    args = parser.parse_args(argv)

    try:
        with open(args.input, encoding="utf-8") as fichero:
            datos = json.load(fichero)
        resultado = predecir(datos)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(json.dumps(resultado, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
