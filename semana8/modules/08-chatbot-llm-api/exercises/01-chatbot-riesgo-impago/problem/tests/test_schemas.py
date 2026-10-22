import pytest
from pydantic import ValidationError

from conftest import CASO_OK
from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada


def test_entrada_valida():
    entrada = PrestamoEntrada(**CASO_OK)
    assert entrada.edad == 30
    assert entrada.plazo_meses == 36


def test_edad_fuera_de_rango():
    caso = dict(CASO_OK)
    caso["edad"] = 15
    with pytest.raises(ValidationError):
        PrestamoEntrada(**caso)


def test_ingresos_deben_ser_positivos():
    caso = dict(CASO_OK)
    caso["ingresos_mensuales"] = 0
    with pytest.raises(ValidationError):
        PrestamoEntrada(**caso)


def test_falta_un_campo():
    caso = dict(CASO_OK)
    del caso["plazo_meses"]
    with pytest.raises(ValidationError):
        PrestamoEntrada(**caso)


def test_campo_inventado_se_rechaza():
    caso = dict(CASO_OK)
    caso["color_favorito"] = "azul"
    with pytest.raises(ValidationError):
        PrestamoEntrada(**caso)


def test_antiguedad_incoherente_con_la_edad():
    caso = dict(CASO_OK)
    caso["edad"] = 20
    caso["antiguedad_laboral_anios"] = 15
    with pytest.raises(ValidationError):
        PrestamoEntrada(**caso)


def test_salida_valida_y_decision_limitada():
    salida = PrediccionSalida(probabilidad_impago=0.1, decision="aprobar")
    assert salida.decision == "aprobar"
    with pytest.raises(ValidationError):
        PrediccionSalida(probabilidad_impago=1.5, decision="aprobar")
    with pytest.raises(ValidationError):
        PrediccionSalida(probabilidad_impago=0.5, decision="quiza")
