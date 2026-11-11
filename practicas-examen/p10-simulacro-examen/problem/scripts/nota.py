"""Nota orientativa del simulacro (HECHO). Uso: uv run python scripts/nota.py

Los argumentos extra se pasan a pytest (p. ej. -x o --basetemp=...).

Ejecuta los tests y calcula la nota por bloques en proporcion a los tests
superados: A (proyecto) 2 puntos, B (contrato y modelo) 4, C (API e
integracion) 4.
"""
import sys
from collections import defaultdict

import pytest

PESOS = {"a": ("A - Proyecto y entorno", 2), "b": ("B - Contrato y modelo", 4), "c": ("C - API e integracion", 4)}


class Contador:
    def __init__(self):
        self.total = defaultdict(int)
        self.superados = defaultdict(int)

    def pytest_runtest_logreport(self, report):
        fichero = report.nodeid.split("::")[0].rsplit("/", 1)[-1]  # test_b_modelo.py
        bloque = fichero.removeprefix("test_")[:1]
        if bloque not in PESOS:
            return
        # Un test cuenta una vez: en "call", o en "setup" si fallo antes de ejecutarse
        if report.when == "call" or (report.when == "setup" and not report.passed):
            self.total[bloque] += 1
            self.superados[bloque] += report.passed


def main() -> int:
    contador = Contador()
    argumentos = ["-q", "-p", "no:cacheprovider", "--no-header", "-rN", "--tb=no", *sys.argv[1:]]
    pytest.main(argumentos, plugins=[contador])
    nota = 0.0
    print("\nBloque                        Tests        Puntos")
    for clave, (nombre, peso) in PESOS.items():
        total, ok = contador.total[clave], contador.superados[clave]
        puntos = peso * ok / total if total else 0.0
        nota += puntos
        print(f"{nombre:<28} {ok:>3}/{total:<3}    {puntos:4.2f} / {peso}")
    print(f"{'NOTA':<28} {'':>7}    {nota:4.2f} / 10")
    return 0


if __name__ == "__main__":
    sys.exit(main())
