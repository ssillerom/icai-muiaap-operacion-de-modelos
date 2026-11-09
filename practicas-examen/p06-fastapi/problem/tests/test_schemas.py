"""Tests de src/reservas/schemas.py (NO MODIFICAR)."""
import pytest
from pydantic import ValidationError

from reservas.schemas import PrediccionSalida, ReservaEntrada


def test_reserva_valida(caso_ok):
    entrada = ReservaEntrada(**caso_ok)
    assert entrada.model_dump() == caso_ok


@pytest.mark.parametrize(
    "campo, valor",
    [
        ("antelacion_dias", -1),
        ("antelacion_dias", 366),
        ("noches", 0),
        ("noches", 31),
        ("adultos", 0),
        ("adultos", 5),
        ("ninos", -1),
        ("precio_noche", 0),
        ("precio_noche", 1001),
        ("cancelaciones_previas", 11),
        ("peticiones_especiales", 6),
    ],
)
def test_valores_fuera_de_rango(caso_ok, campo, valor):
    caso_ok[campo] = valor
    with pytest.raises(ValidationError) as error:
        ReservaEntrada(**caso_ok)
    assert error.value.errors()[0]["loc"] == (campo,)


@pytest.mark.parametrize("limite", [{"antelacion_dias": 0}, {"antelacion_dias": 365}, {"noches": 30}])
def test_los_limites_son_validos(caso_ok, limite):
    caso_ok.update(limite)
    ReservaEntrada(**caso_ok)


def test_falta_un_campo(caso_ok):
    del caso_ok["precio_noche"]
    with pytest.raises(ValidationError, match="precio_noche"):
        ReservaEntrada(**caso_ok)


def test_campo_inventado_se_rechaza(caso_ok):
    caso_ok["mascota"] = "perro"
    with pytest.raises(ValidationError, match="mascota"):
        ReservaEntrada(**caso_ok)


def test_canal_desconocido_se_rechaza(caso_ok):
    caso_ok["canal"] = "email"
    with pytest.raises(ValidationError):
        ReservaEntrada(**caso_ok)


@pytest.mark.parametrize("canal", [" Web ", "AGENCIA", "Telefono"])
def test_canal_se_normaliza(caso_ok, canal):
    caso_ok["canal"] = canal
    assert ReservaEntrada(**caso_ok).canal == canal.strip().lower()


def test_capacidad_maxima_de_la_habitacion(caso_ok):
    caso_ok.update(adultos=4, ninos=3)
    with pytest.raises(ValidationError, match="6 huespedes"):
        ReservaEntrada(**caso_ok)


def test_capacidad_justo_en_el_limite(caso_ok):
    caso_ok.update(adultos=4, ninos=2)
    assert ReservaEntrada(**caso_ok).ninos == 2


def test_salida_valida():
    salida = PrediccionSalida(probabilidad_cancelacion=0.42, riesgo="medio", version_modelo="1.0.0")
    assert salida.model_dump() == {
        "probabilidad_cancelacion": 0.42,
        "riesgo": "medio",
        "version_modelo": "1.0.0",
    }


@pytest.mark.parametrize(
    "datos",
    [
        {"probabilidad_cancelacion": 1.5, "riesgo": "alto", "version_modelo": "1"},
        {"probabilidad_cancelacion": -0.1, "riesgo": "bajo", "version_modelo": "1"},
        {"probabilidad_cancelacion": 0.5, "riesgo": "regular", "version_modelo": "1"},
        {"probabilidad_cancelacion": 0.5, "riesgo": "medio"},
    ],
)
def test_salida_invalida(datos):
    with pytest.raises(ValidationError):
        PrediccionSalida(**datos)
