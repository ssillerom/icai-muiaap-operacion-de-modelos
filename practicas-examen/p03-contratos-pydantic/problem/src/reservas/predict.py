"""CLI de inferencia (TU). Uso: uv run predecir --input ejemplos/reserva.json

Codigos de salida: 0 correcto, 1 fichero no legible, 2 datos invalidos.
"""
import argparse
import json
import sys

from pydantic import ValidationError

from reservas.inference import predecir
from reservas.schemas import ReservaEntrada


def formatear_errores(error: ValidationError) -> str:
    """Una linea por error: campo y motivo (HECHO)."""
    lineas = []
    for detalle in error.errors():
        # Los errores del model_validator no son de un campo concreto: loc == ()
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

    # TODO 7: construye ReservaEntrada a partir de `datos`. Si Pydantic lanza
    #   ValidationError, escribe en sys.stderr "Error: datos de la reserva no
    #   validos" seguido de formatear_errores(error) y devuelve 2 (no imprimas
    #   nada en stdout). Si es valida, llama a predecir() e imprime el
    #   resultado en JSON (investiga model_dump_json) y devuelve 0.
    #   Comprobacion: tests/test_cli.py
    raise NotImplementedError("TODO 7: validar la entrada y predecir")


if __name__ == "__main__":
    sys.exit(main())
