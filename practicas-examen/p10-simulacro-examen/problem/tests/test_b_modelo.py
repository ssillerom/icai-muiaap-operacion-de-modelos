"""Bloque B - Carga del modelo e inferencia (NO MODIFICAR)."""
import joblib
import pytest

from conftest import modelo_falso
from envios import inference
from envios.config import VERSION_MODELO
from envios.data.features import VARIABLES
from envios.model import cargador
from envios.schemas import EnvioEntrada, PrediccionSalida

ENVIO_ARRIESGADO = {
    "distancia_km": 4800.0,
    "peso_kg": 60.0,
    "dias_prometidos": 1,
    "transportista": "economico",
    "es_internacional": True,
    "envios_en_cola": 950,
}

# --- B3: cargar_modelo --------------------------------------------------------------------


def test_b3_carga_el_modelo_de_disco(modelo_en_disco):
    cargado = cargador.cargar_modelo()
    assert isinstance(cargado, cargador.ModeloCargado)
    assert hasattr(cargado.modelo, "predict_proba")
    assert cargado.version == VERSION_MODELO


def test_b3_se_carga_una_sola_vez(modelo_en_disco):
    assert cargador.cargar_modelo() is cargador.cargar_modelo()


def test_b3_fichero_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError, match="entrenar"):
        cargador.cargar_modelo(tmp_path / "no_existe.joblib")


@pytest.mark.parametrize(
    "payload",
    [
        ["no", "es", "un", "dict"],
        {"modelo": object(), "version": "1.0.0"},
        {"modelo": object(), "variables": list(reversed(VARIABLES)), "version": "1.0.0"},
    ],
    ids=["no_es_dict", "falta_variables", "variables_distintas"],
)
def test_b3_payload_incompatible(tmp_path, payload):
    ruta = tmp_path / "modelo.joblib"
    joblib.dump(payload, ruta)
    with pytest.raises(cargador.ModeloIncompatible):
        cargador.cargar_modelo(ruta)


def test_b3_modelo_incompatible_es_value_error():
    assert issubclass(cargador.ModeloIncompatible, ValueError)


# --- B4: inferencia -------------------------------------------------------------------------


@pytest.mark.parametrize(
    "probabilidad, nivel",
    [
        (0.0, "a_tiempo"),
        (0.34, "a_tiempo"),
        (0.35, "riesgo"),
        (0.64, "riesgo"),
        (0.65, "retraso_probable"),
        (1.0, "retraso_probable"),
    ],
)
def test_b4_clasificar_nivel(probabilidad, nivel):
    assert inference.clasificar_nivel(probabilidad) == nivel


def test_b4_predecir_con_modelo_inyectado(caso_ok):
    resultado = inference.predecir(EnvioEntrada(**caso_ok), modelo_falso(0.8))
    assert isinstance(resultado, PrediccionSalida)
    assert resultado.model_dump() == {
        "probabilidad_retraso": 0.8,
        "nivel": "retraso_probable",
        "version_modelo": "test",
    }


def test_b4_predecir_con_el_modelo_real(modelo_en_disco, caso_ok):
    seguro = inference.predecir(EnvioEntrada(**caso_ok))
    arriesgado = inference.predecir(EnvioEntrada(**ENVIO_ARRIESGADO))
    assert seguro.version_modelo == VERSION_MODELO
    assert arriesgado.probabilidad_retraso > seguro.probabilidad_retraso
