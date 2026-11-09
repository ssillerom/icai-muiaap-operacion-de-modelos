"""Tests de src/reservas/predict.py y del comando predecir (NO MODIFICAR)."""
import json
import tomllib

from reservas import predict
from reservas.config import RAIZ


def escribir_json(ruta, datos):
    ruta.write_text(json.dumps(datos), encoding="utf-8")
    return str(ruta)


def test_cli_imprime_la_prediccion_en_json(tmp_path, capsys, caso_ok):
    fichero = escribir_json(tmp_path / "reserva.json", caso_ok)
    assert predict.main(["--input", fichero]) == 0
    salida = json.loads(capsys.readouterr().out)
    assert set(salida) == {"probabilidad_cancelacion", "riesgo"}


def test_cli_fichero_inexistente_devuelve_1(tmp_path, capsys):
    assert predict.main(["--input", str(tmp_path / "no_existe.json")]) == 1
    assert capsys.readouterr().err


def test_cli_campos_incorrectos_devuelve_1(tmp_path, capsys, caso_ok):
    del caso_ok["adultos"]
    fichero = escribir_json(tmp_path / "reserva.json", caso_ok)
    assert predict.main(["--input", fichero]) == 1
    assert "adultos" in capsys.readouterr().err


def test_comando_predecir_en_pyproject():
    with open(RAIZ / "pyproject.toml", "rb") as fichero:
        scripts = tomllib.load(fichero)["project"]["scripts"]
    assert scripts.get("predecir") == "reservas.predict:main"
