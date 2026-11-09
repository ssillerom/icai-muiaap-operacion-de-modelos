"""Tests de la API key (NO MODIFICAR)."""
import pytest
from fastapi.testclient import TestClient

from app.config import obtener_api_key
from app.dependencies import obtener_artefacto
from app.main import app
from conftest import CLAVE_TEST
from reservas.config import RAIZ

cliente_anonimo = TestClient(app)
NO_AUTORIZADO = {"detail": "API key incorrecta o ausente"}


@pytest.fixture
def modelo_que_no_debe_usarse():
    """Si la peticion no esta autorizada, el modelo no debe llegar a cargarse."""

    def no_debe_llamarse():
        raise AssertionError("Sin API key valida no se debe cargar el modelo")

    app.dependency_overrides[obtener_artefacto] = no_debe_llamarse
    yield
    app.dependency_overrides.clear()


# --- TODO 1: configuracion ----------------------------------------------------------


def test_la_clave_se_lee_del_entorno(monkeypatch):
    monkeypatch.setenv("API_KEY", "otra-clave")
    assert obtener_api_key() == "otra-clave"


def test_sin_clave_configurada_devuelve_none(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    assert obtener_api_key() is None


def test_clave_vacia_cuenta_como_no_configurada(monkeypatch):
    monkeypatch.setenv("API_KEY", "")
    assert obtener_api_key() is None


# --- TODO 2 y 3: verificar la cabecera en /predict ---------------------------------


def test_sin_cabecera_da_401(modelo_que_no_debe_usarse, caso_ok):
    respuesta = cliente_anonimo.post("/predict", json=caso_ok)
    assert respuesta.status_code == 401
    assert respuesta.json() == NO_AUTORIZADO


def test_clave_incorrecta_da_401(modelo_que_no_debe_usarse, caso_ok):
    respuesta = cliente_anonimo.post("/predict", json=caso_ok, headers={"X-API-Key": "mala"})
    assert respuesta.status_code == 401
    assert respuesta.json() == NO_AUTORIZADO


def test_clave_con_caracteres_no_ascii_da_401(modelo_que_no_debe_usarse, caso_ok):
    respuesta = cliente_anonimo.post(
        "/predict", json=caso_ok, headers={"X-API-Key": "contraseña".encode()}
    )
    assert respuesta.status_code == 401


def test_clave_correcta_da_200(artefacto_en_disco, caso_ok):
    respuesta = cliente_anonimo.post("/predict", json=caso_ok, headers={"X-API-Key": CLAVE_TEST})
    assert respuesta.status_code == 200


def test_el_nombre_de_la_cabecera_no_distingue_mayusculas(artefacto_en_disco, caso_ok):
    respuesta = cliente_anonimo.post("/predict", json=caso_ok, headers={"x-api-key": CLAVE_TEST})
    assert respuesta.status_code == 200


def test_sin_api_key_configurada_se_rechaza_todo(monkeypatch, modelo_que_no_debe_usarse, caso_ok):
    monkeypatch.delenv("API_KEY", raising=False)
    respuesta = cliente_anonimo.post("/predict", json=caso_ok, headers={"X-API-Key": ""})
    assert respuesta.status_code == 401


def test_la_autenticacion_va_antes_que_la_validacion(modelo_que_no_debe_usarse):
    """Sin clave no se revela nada del contrato: 401 aunque el cuerpo sea invalido."""
    respuesta = cliente_anonimo.post("/predict", json={"adultos": 0})
    assert respuesta.status_code == 401


def test_health_sigue_siendo_publico():
    assert cliente_anonimo.get("/health").status_code == 200


def test_openapi_documenta_el_401():
    operacion = cliente_anonimo.get("/openapi.json").json()["paths"]["/predict"]["post"]
    assert operacion["responses"]["401"]["description"] == "API key incorrecta o ausente"
    nombres = [p["name"].lower() for p in operacion.get("parameters", [])]
    assert "x-api-key" in nombres


# --- TODO 4: secretos fuera del repositorio ------------------------------------------


def test_existe_env_example_sin_clave_real():
    contenido = (RAIZ / ".env.example").read_text(encoding="utf-8")
    assert "API_KEY=" in contenido
    assert CLAVE_TEST not in contenido


def test_env_esta_en_gitignore():
    lineas = (RAIZ / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".env" in [linea.strip() for linea in lineas]
