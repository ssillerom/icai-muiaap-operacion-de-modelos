"""Tests de src/reservas/inference.py (NO MODIFICAR)."""
import pytest

from reservas import inference

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


def test_predecir_devuelve_probabilidad_y_riesgo(caso_ok):
    resultado = inference.predecir(caso_ok)
    assert set(resultado) == {"probabilidad_cancelacion", "riesgo"}
    assert isinstance(resultado["probabilidad_cancelacion"], float)
    assert 0.0 <= resultado["probabilidad_cancelacion"] <= 1.0
    assert resultado["riesgo"] == inference.clasificar_riesgo(
        resultado["probabilidad_cancelacion"]
    )


def test_el_modelo_distingue_reservas_arriesgadas(caso_ok):
    segura = inference.predecir(caso_ok)["probabilidad_cancelacion"]
    arriesgada = inference.predecir(RESERVA_ARRIESGADA)["probabilidad_cancelacion"]
    assert arriesgada > segura


def test_predecir_con_campos_incorrectos_da_value_error(caso_ok):
    caso_ok["mascota"] = "perro"
    with pytest.raises(ValueError):
        inference.predecir(caso_ok)
