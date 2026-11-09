"""Tests de src/reservas/inference.py (NO MODIFICAR)."""
import pytest

from conftest import ModeloFalso
from reservas import inference
from reservas.config import VERSION_MODELO
from reservas.model.artefacto import Artefacto, Manifiesto
from reservas.schemas import PrediccionSalida, ReservaEntrada

RESERVA_ARRIESGADA = {
    "antelacion_dias": 300,
    "noches": 2,
    "adultos": 2,
    "ninos": 2,
    "precio_noche": 380.0,
    "canal": "agencia",
    "cancelaciones_previas": 3,
    "peticiones_especiales": 0,
}


def artefacto_falso(probabilidad):
    manifiesto = Manifiesto(
        version_modelo="test",
        fecha_entrenamiento="2026-01-01T00:00:00Z",
        variables=[],
        metricas={},
        version_sklearn="-",
    )
    return Artefacto(modelo=ModeloFalso(probabilidad), manifiesto=manifiesto)


@pytest.mark.parametrize(
    "probabilidad, riesgo",
    [(0.0, "bajo"), (0.29, "bajo"), (0.3, "medio"), (0.59, "medio"), (0.6, "alto"), (1.0, "alto")],
)
def test_clasificar_riesgo(probabilidad, riesgo):
    assert inference.clasificar_riesgo(probabilidad) == riesgo


def test_predecir_con_el_artefacto_real(artefacto_en_disco, caso_ok):
    resultado = inference.predecir(ReservaEntrada(**caso_ok))
    assert isinstance(resultado, PrediccionSalida)
    assert 0.0 <= resultado.probabilidad_cancelacion <= 1.0
    assert resultado.version_modelo == VERSION_MODELO


def test_el_modelo_distingue_reservas_arriesgadas(artefacto_en_disco, caso_ok):
    segura = inference.predecir(ReservaEntrada(**caso_ok))
    arriesgada = inference.predecir(ReservaEntrada(**RESERVA_ARRIESGADA))
    assert arriesgada.probabilidad_cancelacion > segura.probabilidad_cancelacion


def test_predecir_con_un_artefacto_inyectado(caso_ok):
    resultado = inference.predecir(ReservaEntrada(**caso_ok), artefacto_falso(0.8))
    assert resultado.model_dump() == {
        "probabilidad_cancelacion": 0.8,
        "riesgo": "alto",
        "version_modelo": "test",
    }
