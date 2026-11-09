"""Bloque C - API FastAPI (NO MODIFICAR)."""
import pytest
from fastapi.testclient import TestClient

import app.dependencies as dependencias
from app.main import app
from conftest import CABECERAS, modelo_falso

cliente = TestClient(app, headers=CABECERAS)
anonimo = TestClient(app)


@pytest.fixture
def con_modelo_falso():
    app.dependency_overrides[dependencias.obtener_modelo] = modelo_falso
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def modelo_prohibido():
    """Sin API key valida el modelo no debe llegar a cargarse."""

    def no_debe_llamarse():
        raise AssertionError("Sin API key no se debe cargar el modelo")

    app.dependency_overrides[dependencias.obtener_modelo] = no_debe_llamarse
    yield
    app.dependency_overrides.clear()


def test_c0_health_publico():
    assert anonimo.get("/health").json() == {"status": "ok"}


# --- C1: 503 si no hay modelo -------------------------------------------------------------


def test_c1_503_si_no_hay_modelo(monkeypatch, caso_ok):
    def sin_modelo():
        raise FileNotFoundError("C:/ruta/secreta/modelo.joblib")

    monkeypatch.setattr(dependencias, "cargar_modelo", sin_modelo)
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 503
    assert respuesta.json() == {"detail": "Modelo no disponible"}


def test_c1_obtener_modelo_real(modelo_en_disco):
    assert dependencias.obtener_modelo().version == "1.0.0"


# --- C2: API key ----------------------------------------------------------------------------


def test_c2_sin_cabecera_401(modelo_prohibido, caso_ok):
    respuesta = anonimo.post("/predict", json=caso_ok)
    assert respuesta.status_code == 401
    assert respuesta.json() == {"detail": "API key incorrecta o ausente"}


def test_c2_clave_incorrecta_401(modelo_prohibido, caso_ok):
    respuesta = anonimo.post("/predict", json=caso_ok, headers={"X-API-Key": "mala"})
    assert respuesta.status_code == 401


def test_c2_sin_api_key_configurada_401(monkeypatch, modelo_prohibido, caso_ok):
    monkeypatch.delenv("API_KEY", raising=False)
    assert cliente.post("/predict", json=caso_ok).status_code == 401


# --- C3: POST /predict ----------------------------------------------------------------------


def test_c3_predict_ok(con_modelo_falso, caso_ok):
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "probabilidad_retraso": 0.8,
        "nivel": "retraso_probable",
        "version_modelo": "test",
    }


def test_c3_predict_con_el_modelo_real(modelo_en_disco, caso_ok):
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 200
    assert respuesta.json()["version_modelo"] == "1.0.0"


@pytest.mark.parametrize("cambio, campo", [({"peso_kg": 0}, "peso_kg"), ({"fragil": True}, "fragil")])
def test_c3_422_por_campo(con_modelo_falso, caso_ok, cambio, campo):
    caso_ok.update(cambio)
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 422
    assert campo in respuesta.json()["detail"][0]["loc"]


def test_c3_422_regla_nacional(con_modelo_falso, caso_ok):
    caso_ok.update(distancia_km=2000, es_internacional=False)
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 422
    assert "1500 km" in respuesta.json()["detail"][0]["msg"]


def test_c3_openapi():
    operacion = anonimo.get("/openapi.json").json()["paths"]["/predict"]["post"]
    assert operacion["tags"] == ["prediccion"]
    assert "401" in operacion["responses"]
    assert "503" in operacion["responses"]
    esquema = operacion["requestBody"]["content"]["application/json"]["schema"]
    assert esquema["$ref"].endswith("/EnvioEntrada")
