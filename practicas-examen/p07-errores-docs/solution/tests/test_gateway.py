"""Tests de frontend/gateway.py (NO MODIFICAR)."""
import pytest
from pydantic import ValidationError

import gateway
from reservas.model.artefacto import ArtefactoIncompatible
from reservas.schemas import PrediccionSalida, ReservaEntrada


def error_de(valores):
    with pytest.raises(ValidationError) as info:
        ReservaEntrada(**valores)
    return info.value


# --- TODO 1: traducir_errores ---------------------------------------------------


def test_traducir_usa_la_etiqueta_del_formulario(caso_ok):
    caso_ok["adultos"] = 0
    mensajes = gateway.traducir_errores(error_de(caso_ok))
    assert len(mensajes) == 1
    assert mensajes[0].startswith("Adultos: ")


def test_traducir_un_mensaje_por_error(caso_ok):
    caso_ok.update(adultos=0, noches=0, canal="email")
    mensajes = gateway.traducir_errores(error_de(caso_ok))
    assert len(mensajes) == 3
    assert any(m.startswith("Noches: ") for m in mensajes)
    assert any(m.startswith("Canal de reserva: ") for m in mensajes)


def test_traducir_error_entre_campos(caso_ok):
    caso_ok.update(adultos=4, ninos=4)
    mensajes = gateway.traducir_errores(error_de(caso_ok))
    assert mensajes == ["Reserva: Una habitacion admite como maximo 6 huespedes (adultos + ninos = 8)"]


# --- TODO 2: consultar_modelo ---------------------------------------------------


def test_consulta_correcta(artefacto_en_disco, caso_ok):
    respuesta = gateway.consultar_modelo(caso_ok)
    assert respuesta.ok is True
    assert isinstance(respuesta.prediccion, PrediccionSalida)
    assert respuesta.errores == []


def test_consulta_con_datos_invalidos_no_llama_al_modelo(caso_ok, monkeypatch):
    def no_debe_llamarse(entrada):
        raise AssertionError("Con datos invalidos no se debe llamar al modelo")

    monkeypatch.setattr(gateway, "predecir", no_debe_llamarse)
    caso_ok["ninos"] = -1
    respuesta = gateway.consultar_modelo(caso_ok)
    assert respuesta.ok is False
    assert respuesta.prediccion is None
    assert respuesta.errores[0].startswith("Niños: ")


@pytest.mark.parametrize(
    "excepcion",
    [
        FileNotFoundError("C:/ruta/secreta/models/cancelacion/manifest.json"),
        ArtefactoIncompatible("variables distintas: C:/ruta/secreta"),
    ],
)
def test_modelo_no_disponible_da_un_mensaje_generico(caso_ok, monkeypatch, excepcion):
    def falla(entrada):
        raise excepcion

    monkeypatch.setattr(gateway, "predecir", falla)
    respuesta = gateway.consultar_modelo(caso_ok)
    assert respuesta.ok is False
    assert respuesta.errores == [gateway.MENSAJE_MODELO_NO_DISPONIBLE]
    assert "secreta" not in " ".join(respuesta.errores)
