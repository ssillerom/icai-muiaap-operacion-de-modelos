"""CLI de inferencia. Uso: uv run predecir --input ejemplos/reserva.json

Codigos de salida: 0 correcto, 1 fichero o modelo no disponible, 2 datos invalidos.
"""
import argparse
import json
import sys

from pydantic import ValidationError

from reservas.inference import predecir
from reservas.model.artefacto import ArtefactoIncompatible
from reservas.schemas import ReservaEntrada


def formatear_errores(error: ValidationError) -> str:
    """Una linea por error: campo y motivo. Los errores entre campos no tienen campo."""
    lineas = []
    for detalle in error.errors():
        campo = ".".join(str(parte) for parte in detalle["loc"]) or "reserva"
        lineas.append(f"- {campo}: {detalle['msg']}")
    return "\n".join(lineas)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Riesgo de cancelacion de una reserva")
    parser.add_argument("--input", required=True, help="Fichero JSON con la reserva")
    args = parser.parse_args(argv)

    try:
        with open(args.input, encoding="utf-8") as fichero:
            datos = json.load(fichero)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Error: no se puede leer {args.input}: {error}", file=sys.stderr)
        return 1

    try:
        entrada = ReservaEntrada(**datos)
    except ValidationError as error:
        print("Error: datos de la reserva no validos", file=sys.stderr)
        print(formatear_errores(error), file=sys.stderr)
        return 2

    try:
        resultado = predecir(entrada)
    except (FileNotFoundError, ArtefactoIncompatible, ValidationError) as error:
        # ValidationError aqui significa un manifest.json que no cumple el contrato
        print(f"Error: modelo no disponible: {error}", file=sys.stderr)
        return 1

    print(resultado.model_dump_json())
    return 0


if __name__ == "__main__":
    sys.exit(main())
