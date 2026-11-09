"""Tests de src/reservas/predict.py (NO MODIFICAR)."""
import json

import pytest

from reservas import predict


@pytest.fixture(autouse=True)
def _artefacto(artefacto_en_disco):
    return artefacto_en_disco


def escribir_json(ruta, datos):
    ruta.write_text(json.dumps(datos), encoding="utf-8")
    return str(ruta)


def test_cli_imprime_la_prediccion_en_json(tmp_path, capsys, caso_ok):
    fichero = escribir_json(tmp_path / "reserva.json", caso_ok)
    assert predict.main(["--input", fichero]) == 0
    salida = json.loads(capsys.readouterr().out)
    assert set(salida) == {"probabilidad_cancelacion", "riesgo", "version_modelo"}


def test_cli_fichero_inexistente_devuelve_1(tmp_path, capsys):
    assert predict.main(["--input", str(tmp_path / "no_existe.json")]) == 1
    assert capsys.readouterr().err


def test_cli_json_roto_devuelve_1(tmp_path, capsys):
    fichero = tmp_path / "roto.json"
    fichero.write_text('{"noches": 3,', encoding="utf-8")
    assert predict.main(["--input", str(fichero)]) == 1


def test_cli_datos_invalidos_devuelve_2_y_explica_el_campo(tmp_path, capsys, caso_ok):
    caso_ok["adultos"] = 0
    fichero = escribir_json(tmp_path / "reserva.json", caso_ok)
    assert predict.main(["--input", fichero]) == 2
    salida = capsys.readouterr()
    assert "adultos" in salida.err
    assert "Traceback" not in salida.err
    assert salida.out == ""


def test_cli_error_entre_campos_devuelve_2(tmp_path, capsys, caso_ok):
    caso_ok.update(adultos=4, ninos=4)
    fichero = escribir_json(tmp_path / "reserva.json", caso_ok)
    assert predict.main(["--input", fichero]) == 2
    assert "huespedes" in capsys.readouterr().err


def test_cli_modelo_no_disponible_devuelve_1(tmp_path, capsys, caso_ok, monkeypatch):
    def sin_modelo(entrada):
        raise FileNotFoundError("No se encuentra manifest.json. Generalo con: uv run entrenar")

    monkeypatch.setattr(predict, "predecir", sin_modelo)
    fichero = escribir_json(tmp_path / "reserva.json", caso_ok)
    assert predict.main(["--input", fichero]) == 1
    assert "entrenar" in capsys.readouterr().err
