"""Bloque B - Contratos Pydantic (NO MODIFICAR)."""
import pytest
from pydantic import ValidationError

from envios.schemas import EnvioEntrada, PrediccionSalida

# --- B1: EnvioEntrada -----------------------------------------------------------------


def test_b1_envio_valido(caso_ok):
    assert EnvioEntrada(**caso_ok).model_dump() == caso_ok


@pytest.mark.parametrize(
    "campo, valor",
    [
        ("distancia_km", 0),
        ("distancia_km", 5001),
        ("peso_kg", 0),
        ("peso_kg", 70.5),
        ("dias_prometidos", 0),
        ("dias_prometidos", 16),
        ("envios_en_cola", -1),
        ("envios_en_cola", 1001),
    ],
)
def test_b1_fuera_de_rango(caso_ok, campo, valor):
    caso_ok[campo] = valor
    with pytest.raises(ValidationError) as error:
        EnvioEntrada(**caso_ok)
    assert error.value.errors()[0]["loc"] == (campo,)


@pytest.mark.parametrize("limite", [{"peso_kg": 70}, {"dias_prometidos": 15}, {"envios_en_cola": 0}])
def test_b1_limites_validos(caso_ok, limite):
    caso_ok.update(limite)
    EnvioEntrada(**caso_ok)


def test_b1_campo_inventado(caso_ok):
    caso_ok["fragil"] = True
    with pytest.raises(ValidationError, match="fragil"):
        EnvioEntrada(**caso_ok)


def test_b1_falta_un_campo(caso_ok):
    del caso_ok["transportista"]
    with pytest.raises(ValidationError, match="transportista"):
        EnvioEntrada(**caso_ok)


@pytest.mark.parametrize("texto", [" RAPIDO ", "Economico", "estandar"])
def test_b1_transportista_normalizado(caso_ok, texto):
    caso_ok["transportista"] = texto
    assert EnvioEntrada(**caso_ok).transportista == texto.strip().lower()


def test_b1_transportista_desconocido(caso_ok):
    caso_ok["transportista"] = "dron"
    with pytest.raises(ValidationError):
        EnvioEntrada(**caso_ok)


def test_b1_nacional_de_mas_de_1500_km(caso_ok):
    caso_ok.update(distancia_km=1600, es_internacional=False)
    with pytest.raises(ValidationError, match="1500 km"):
        EnvioEntrada(**caso_ok)


def test_b1_nacional_justo_1500_km(caso_ok):
    caso_ok.update(distancia_km=1500, es_internacional=False)
    EnvioEntrada(**caso_ok)


def test_b1_internacional_de_mas_de_1500_km(caso_ok):
    caso_ok.update(distancia_km=1600, es_internacional=True)
    EnvioEntrada(**caso_ok)


# --- B2: PrediccionSalida ---------------------------------------------------------------


def test_b2_salida_valida():
    salida = PrediccionSalida(probabilidad_retraso=0.5, nivel="riesgo", version_modelo="1.0.0")
    assert salida.model_dump() == {
        "probabilidad_retraso": 0.5,
        "nivel": "riesgo",
        "version_modelo": "1.0.0",
    }


@pytest.mark.parametrize(
    "datos",
    [
        {"probabilidad_retraso": 1.2, "nivel": "riesgo", "version_modelo": "1"},
        {"probabilidad_retraso": 0.5, "nivel": "tarde", "version_modelo": "1"},
        {"probabilidad_retraso": 0.5, "nivel": "riesgo"},
    ],
)
def test_b2_salida_invalida(datos):
    with pytest.raises(ValidationError):
        PrediccionSalida(**datos)
