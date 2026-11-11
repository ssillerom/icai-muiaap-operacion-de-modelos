"""Tests de frontend/gateway.py contra la API (NO MODIFICAR).

La mayoria usan el TestClient de FastAPI como cliente HTTP: es un httpx.Client
que habla con la API en el mismo proceso, sin arrancar uvicorn.
"""
import tomllib

import httpx
import pytest
from fastapi.testclient import TestClient

import app.dependencies as dependencias
import gateway
from app.main import app
from conftest import CABECERAS, ModeloFalso
from reservas.config import RAIZ
from reservas.model.artefacto import Artefacto, Manifiesto
from reservas.schemas import PrediccionSalida


def artefacto_falso():
    manifiesto = Manifiesto(
        version_modelo="test",
        fecha_entrenamiento="2026-01-01T00:00:00Z",
        variables=[],
        metricas={},
        version_sklearn="-",
    )
    return Artefacto(modelo=ModeloFalso(0.8), manifiesto=manifiesto)


@pytest.fixture
def api():
    """Cliente HTTP autorizado contra la API, con un modelo falso."""
    app.dependency_overrides[dependencias.obtener_artefacto] = artefacto_falso
    yield TestClient(app, headers=CABECERAS)
    app.dependency_overrides.clear()


def cliente_simulado(manejador):
    """Cliente httpx cuyas respuestas (o fallos) decide `manejador`."""
    return httpx.Client(base_url="http://api", transport=httpx.MockTransport(manejador))


# --- Paso 0: httpx pasa a ser dependencia del proyecto --------------------------------


def test_httpx_es_dependencia_del_proyecto():
    with open(RAIZ / "pyproject.toml", "rb") as fichero:
        pyproject = tomllib.load(fichero)
    assert "httpx" in " ".join(pyproject["project"]["dependencies"])
    assert "httpx" not in " ".join(pyproject["dependency-groups"]["dev"])


# --- TODO 1: crear_cliente ---------------------------------------------------------------


def test_crear_cliente_usa_la_configuracion(monkeypatch):
    monkeypatch.setattr(gateway, "API_URL", "http://api.ejemplo:9000")
    monkeypatch.setattr(gateway, "API_KEY", "clave-del-front")
    with gateway.crear_cliente() as cliente:
        assert str(cliente.base_url).rstrip("/") == "http://api.ejemplo:9000"
        assert cliente.headers["x-api-key"] == "clave-del-front"
        assert cliente.timeout.read == gateway.TIMEOUT_SEGUNDOS


# --- TODO 2: traducir_errores_api --------------------------------------------------------


def test_traducir_error_de_un_campo():
    detalle = [{"loc": ["body", "adultos"], "msg": "Input should be greater than or equal to 1"}]
    assert gateway.traducir_errores_api(detalle) == [
        "Adultos: Input should be greater than or equal to 1"
    ]


def test_traducir_error_entre_campos():
    detalle = [{"loc": ["body"], "msg": "Value error, Una habitacion admite como maximo 6 huespedes"}]
    assert gateway.traducir_errores_api(detalle) == [
        "Reserva: Una habitacion admite como maximo 6 huespedes"
    ]


# --- TODO 3: consultar_modelo contra la API real ------------------------------------------


def test_prediccion_correcta(api, caso_ok):
    respuesta = gateway.consultar_modelo(caso_ok, api)
    assert respuesta.ok is True
    assert isinstance(respuesta.prediccion, PrediccionSalida)
    assert respuesta.prediccion.riesgo == "alto"
    assert respuesta.prediccion.version_modelo == "test"


def test_422_con_la_etiqueta_del_formulario(api, caso_ok):
    caso_ok["adultos"] = 0
    respuesta = gateway.consultar_modelo(caso_ok, api)
    assert respuesta.ok is False
    assert respuesta.errores == ["Adultos: Input should be greater than or equal to 1"]


def test_422_regla_de_capacidad(api, caso_ok):
    caso_ok.update(adultos=4, ninos=4)
    respuesta = gateway.consultar_modelo(caso_ok, api)
    assert respuesta.errores[0].startswith("Reserva: Una habitacion admite")


def test_401_sin_clave(caso_ok):
    respuesta = gateway.consultar_modelo(caso_ok, TestClient(app))
    assert respuesta.ok is False
    assert respuesta.errores == [gateway.MENSAJE_NO_AUTORIZADO]


def test_503_sin_modelo(caso_ok, monkeypatch):
    def sin_modelo():
        raise FileNotFoundError("no hay modelo")

    monkeypatch.setattr(dependencias, "cargar_modelo", sin_modelo)
    respuesta = gateway.consultar_modelo(caso_ok, TestClient(app, headers=CABECERAS))
    assert respuesta.errores == [gateway.MENSAJE_MODELO_NO_DISPONIBLE]


# --- TODO 3: fallos de red y respuestas inesperadas ---------------------------------------


@pytest.mark.parametrize("fallo", [httpx.ConnectError, httpx.ReadTimeout])
def test_api_caida_o_lenta(caso_ok, fallo):
    def manejador(peticion):
        raise fallo("sin respuesta", request=peticion)

    respuesta = gateway.consultar_modelo(caso_ok, cliente_simulado(manejador))
    assert respuesta.ok is False
    assert respuesta.errores == [gateway.MENSAJE_API_NO_DISPONIBLE]


@pytest.mark.parametrize(
    "estado, cuerpo",
    [(500, {"detail": "Internal Server Error"}), (200, {"inesperado": True}), (404, {})],
)
def test_respuesta_inesperada(caso_ok, estado, cuerpo):
    respuesta = gateway.consultar_modelo(
        caso_ok, cliente_simulado(lambda peticion: httpx.Response(estado, json=cuerpo))
    )
    assert respuesta.ok is False
    assert respuesta.errores == [gateway.MENSAJE_ERROR_INESPERADO]


def test_envia_post_a_predict_con_el_json(caso_ok):
    recibidas = []

    def manejador(peticion):
        recibidas.append(peticion)
        return httpx.Response(
            200, json={"probabilidad_cancelacion": 0.1, "riesgo": "bajo", "version_modelo": "x"}
        )

    gateway.consultar_modelo(caso_ok, cliente_simulado(manejador))
    assert recibidas[0].method == "POST"
    assert recibidas[0].url.path == "/predict"
    assert recibidas[0].read() == httpx.Request("POST", "/", json=caso_ok).read()


def test_sin_cliente_usa_crear_cliente_y_lo_cierra(caso_ok, monkeypatch):
    creados = []

    def crear():
        cliente = cliente_simulado(
            lambda peticion: httpx.Response(
                200, json={"probabilidad_cancelacion": 0.1, "riesgo": "bajo", "version_modelo": "x"}
            )
        )
        creados.append(cliente)
        return cliente

    monkeypatch.setattr(gateway, "crear_cliente", crear)
    assert gateway.consultar_modelo(caso_ok).ok is True
    assert len(creados) == 1
    assert creados[0].is_closed
