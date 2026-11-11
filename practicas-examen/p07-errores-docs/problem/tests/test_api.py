"""Tests de la API FastAPI (NO MODIFICAR)."""
import pytest
from fastapi.testclient import TestClient

from app.dependencies import obtener_artefacto
from app.main import app
from conftest import ModeloFalso
from reservas.config import VERSION_MODELO
from reservas.model.artefacto import Artefacto, Manifiesto

cliente = TestClient(app)


def artefacto_falso(probabilidad=0.8):
    manifiesto = Manifiesto(
        version_modelo="test",
        fecha_entrenamiento="2026-01-01T00:00:00Z",
        variables=[],
        metricas={},
        version_sklearn="-",
    )
    return Artefacto(modelo=ModeloFalso(probabilidad), manifiesto=manifiesto)


@pytest.fixture
def modelo_falso():
    """Sustituye la dependencia del modelo por un doble que siempre devuelve 0.8."""
    app.dependency_overrides[obtener_artefacto] = artefacto_falso
    yield
    app.dependency_overrides.clear()


# --- TODO 1 y 2: routers registrados y GET /health ------------------------------


def test_health():
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok"}


# --- TODO 3 y 4: dependencia y POST /predict -------------------------------------


def test_obtener_artefacto_devuelve_el_artefacto_real(artefacto_en_disco):
    artefacto = obtener_artefacto()
    assert isinstance(artefacto, Artefacto)
    assert artefacto.manifiesto.version_modelo == VERSION_MODELO


def test_predict_con_modelo_falso(modelo_falso, caso_ok):
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "probabilidad_cancelacion": 0.8,
        "riesgo": "alto",
        "version_modelo": "test",
    }


def test_predict_con_el_modelo_real(artefacto_en_disco, caso_ok):
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert 0 <= datos["probabilidad_cancelacion"] <= 1
    assert datos["riesgo"] in ("bajo", "medio", "alto")
    assert datos["version_modelo"] == VERSION_MODELO


def test_predict_normaliza_el_canal(modelo_falso, caso_ok):
    caso_ok["canal"] = "  WEB "
    assert cliente.post("/predict", json=caso_ok).status_code == 200


@pytest.mark.parametrize(
    "cambio, campo",
    [
        ({"adultos": 0}, "adultos"),
        ({"precio_noche": -10}, "precio_noche"),
        ({"canal": "email"}, "canal"),
        ({"mascota": "perro"}, "mascota"),
    ],
)
def test_predict_datos_invalidos_da_422(modelo_falso, caso_ok, cambio, campo):
    caso_ok.update(cambio)
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 422
    assert campo in respuesta.json()["detail"][0]["loc"]


def test_predict_falta_un_campo_da_422(modelo_falso, caso_ok):
    del caso_ok["noches"]
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 422
    assert "noches" in respuesta.json()["detail"][0]["loc"]


def test_predict_regla_de_capacidad_da_422(modelo_falso, caso_ok):
    caso_ok.update(adultos=4, ninos=4)
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 422
    assert "6 huespedes" in respuesta.json()["detail"][0]["msg"]


def test_predict_sin_cuerpo_da_422(modelo_falso):
    assert cliente.post("/predict").status_code == 422


def test_predict_solo_admite_post():
    assert cliente.get("/predict").status_code == 405


# --- Documentacion OpenAPI (sale sola si los TODOs 1-4 estan bien) --------------


def test_openapi_documenta_las_rutas():
    esquema = cliente.get("/openapi.json").json()
    assert "get" in esquema["paths"]["/health"]
    operacion = esquema["paths"]["/predict"]["post"]
    cuerpo = operacion["requestBody"]["content"]["application/json"]["schema"]
    respuesta = operacion["responses"]["200"]["content"]["application/json"]["schema"]
    assert cuerpo["$ref"].endswith("/ReservaEntrada")
    assert respuesta["$ref"].endswith("/PrediccionSalida")
    assert operacion["tags"] == ["prediccion"]


def test_docs_disponible():
    assert cliente.get("/docs").status_code == 200
