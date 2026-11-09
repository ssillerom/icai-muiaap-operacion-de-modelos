"""Tests de src/reservas/inference.py (NO MODIFICAR)."""
import pytest

from reservas import inference
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


@pytest.mark.parametrize(
    "probabilidad, riesgo",
    [(0.0, "bajo"), (0.29, "bajo"), (0.3, "medio"), (0.59, "medio"), (0.6, "alto"), (1.0, "alto")],
)
def test_clasificar_riesgo(probabilidad, riesgo):
    assert inference.clasificar_riesgo(probabilidad) == riesgo


def test_predecir_devuelve_una_prediccion_salida(caso_ok):
    resultado = inference.predecir(ReservaEntrada(**caso_ok))
    assert isinstance(resultado, PrediccionSalida)
    assert 0.0 <= resultado.probabilidad_cancelacion <= 1.0
    assert resultado.riesgo == inference.clasificar_riesgo(resultado.probabilidad_cancelacion)


def test_el_modelo_distingue_reservas_arriesgadas(caso_ok):
    segura = inference.predecir(ReservaEntrada(**caso_ok))
    arriesgada = inference.predecir(ReservaEntrada(**RESERVA_ARRIESGADA))
    assert arriesgada.probabilidad_cancelacion > segura.probabilidad_cancelacion


def test_canal_en_mayusculas_da_la_misma_prediccion(caso_ok):
    normal = inference.predecir(ReservaEntrada(**caso_ok))
    caso_ok["canal"] = "  WEB "
    mayusculas = inference.predecir(ReservaEntrada(**caso_ok))
    assert mayusculas == normal
