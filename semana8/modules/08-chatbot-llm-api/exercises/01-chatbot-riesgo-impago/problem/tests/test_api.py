import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.llm import LLMSimulado, get_llm
from conftest import CASO_OK

cliente = TestClient(app)


@pytest.fixture
def llm_simulado():
    app.dependency_overrides[get_llm] = lambda: LLMSimulado()
    yield
    app.dependency_overrides.clear()


def test_health():
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok"}


def test_predict_ok():
    respuesta = cliente.post("/predict", json=CASO_OK)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert 0 <= datos["probabilidad_impago"] <= 1
    assert datos["decision"] in ("aprobar", "revisar", "rechazar")


def test_predict_datos_invalidos_da_422():
    caso = dict(CASO_OK)
    caso["edad"] = 200
    assert cliente.post("/predict", json=caso).status_code == 422


def test_predict_campo_inventado_da_422():
    caso = dict(CASO_OK)
    caso["pelo"] = "castano"
    assert cliente.post("/predict", json=caso).status_code == 422


def test_chat_flujo_completo_con_tool(llm_simulado):
    pregunta = (
        "Quiero la probabilidad para edad 30, ingresos 2500, importe 12000, "
        "plazo 36, antiguedad 5, impagos 0"
    )
    respuesta = cliente.post("/chat", json={"mensajes": [{"role": "user", "content": pregunta}]})
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["herramienta"]["argumentos"]["edad"] == 30
    assert datos["herramienta"]["resultado"]["ok"] is True
    assert "probabilidad de impago" in datos["respuesta"]


def test_chat_faltan_datos_pide_el_dato(llm_simulado):
    respuesta = cliente.post(
        "/chat", json={"mensajes": [{"role": "user", "content": "edad 30 e ingresos 2500"}]}
    )
    datos = respuesta.json()
    assert datos["herramienta"] is None
    assert "faltan" in datos["respuesta"].lower()


def test_chat_valida_la_entrada():
    assert cliente.post("/chat", json={"mensajes": []}).status_code == 422
    assert cliente.post("/chat", json={"mensajes": [{"role": "robot", "content": "x"}]}).status_code == 422
