"""Bloque C - Integracion del frontend con la API (NO MODIFICAR)."""
import httpx
import pytest
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

import app.dependencies as dependencias
import cliente_api
from app.main import app as api
from conftest import CABECERAS, modelo_falso
from envios.config import RAIZ

RESPUESTA_OK = {"probabilidad_retraso": 0.1, "nivel": "a_tiempo", "version_modelo": "x"}


@pytest.fixture
def con_api():
    """TestClient autorizado contra la API real, con un modelo falso."""
    api.dependency_overrides[dependencias.obtener_modelo] = modelo_falso
    yield TestClient(api, headers=CABECERAS)
    api.dependency_overrides.clear()


def simulado(manejador):
    return httpx.Client(base_url="http://api", transport=httpx.MockTransport(manejador))


# --- C4: crear_cliente ---------------------------------------------------------------------


def test_c4_crear_cliente(monkeypatch):
    monkeypatch.setattr(cliente_api, "API_URL", "http://api.ejemplo:9000")
    monkeypatch.setattr(cliente_api, "API_KEY", "clave-front")
    with cliente_api.crear_cliente() as cliente:
        assert str(cliente.base_url).rstrip("/") == "http://api.ejemplo:9000"
        assert cliente.headers["x-api-key"] == "clave-front"
        assert cliente.timeout.read == cliente_api.TIMEOUT_SEGUNDOS


# --- C4: consultar -------------------------------------------------------------------------


def test_c4_prediccion(con_api, caso_ok):
    respuesta = cliente_api.consultar(caso_ok, con_api)
    assert respuesta.ok is True
    assert respuesta.prediccion.nivel == "retraso_probable"


def test_c4_422_con_etiqueta(con_api, caso_ok):
    caso_ok["peso_kg"] = 0
    respuesta = cliente_api.consultar(caso_ok, con_api)
    assert respuesta.ok is False
    assert respuesta.errores == ["Peso (kg): Input should be greater than 0"]


def test_c4_422_regla_nacional(con_api, caso_ok):
    caso_ok.update(distancia_km=2000, es_internacional=False)
    respuesta = cliente_api.consultar(caso_ok, con_api)
    assert respuesta.errores == ["Envío: Un envio nacional no puede superar 1500 km"]


def test_c4_401(caso_ok):
    respuesta = cliente_api.consultar(caso_ok, TestClient(api))
    assert respuesta.errores == [cliente_api.MENSAJE_NO_AUTORIZADO]


def test_c4_503(caso_ok, monkeypatch):
    def sin_modelo():
        raise FileNotFoundError("no hay modelo")

    monkeypatch.setattr(dependencias, "cargar_modelo", sin_modelo)
    respuesta = cliente_api.consultar(caso_ok, TestClient(api, headers=CABECERAS))
    assert respuesta.errores == [cliente_api.MENSAJE_MODELO_NO_DISPONIBLE]


@pytest.mark.parametrize("fallo", [httpx.ConnectError, httpx.ReadTimeout])
def test_c4_api_caida(caso_ok, fallo):
    def manejador(peticion):
        raise fallo("sin respuesta", request=peticion)

    respuesta = cliente_api.consultar(caso_ok, simulado(manejador))
    assert respuesta.errores == [cliente_api.MENSAJE_API_NO_DISPONIBLE]


@pytest.mark.parametrize("estado, cuerpo", [(500, {}), (200, {"raro": 1})])
def test_c4_respuesta_inesperada(caso_ok, estado, cuerpo):
    respuesta = cliente_api.consultar(caso_ok, simulado(lambda p: httpx.Response(estado, json=cuerpo)))
    assert respuesta.errores == [cliente_api.MENSAJE_ERROR_INESPERADO]


def test_c4_sin_cliente_crea_uno_y_lo_cierra(caso_ok, monkeypatch):
    creados = []

    def crear():
        creados.append(simulado(lambda p: httpx.Response(200, json=RESPUESTA_OK)))
        return creados[-1]

    monkeypatch.setattr(cliente_api, "crear_cliente", crear)
    assert cliente_api.consultar(caso_ok).ok is True
    assert creados[0].is_closed


# --- Todo junto: la app Streamlit contra la API ------------------------------------------------


def test_c4_app_streamlit_contra_la_api(modelo_en_disco, monkeypatch):
    monkeypatch.setattr(cliente_api, "crear_cliente", lambda: TestClient(api, headers=CABECERAS))
    pagina = AppTest.from_file(str(RAIZ / "frontend" / "app.py"), default_timeout=30)
    pagina.run()
    pagina.button[0].click().run()
    assert not pagina.exception
    assert len(pagina.metric) == 1
    assert any("Modelo 1.0.0" in c.value for c in pagina.caption)
