"""Tests de la documentacion OpenAPI (NO MODIFICAR)."""
from fastapi.testclient import TestClient

from app.main import app
from reservas.schemas import ReservaEntrada

cliente = TestClient(app)


def esquema():
    return cliente.get("/openapi.json").json()


def operacion_predict():
    return esquema()["paths"]["/predict"]["post"]


def test_predict_tiene_summary():
    assert operacion_predict()["summary"] == "Predecir riesgo de cancelacion"


def test_predict_documenta_el_503():
    respuestas = operacion_predict()["responses"]
    assert respuestas["503"]["description"] == "Modelo no disponible"
    assert "422" in respuestas


def test_predict_describe_los_codigos_en_el_docstring():
    descripcion = operacion_predict()["description"]
    for codigo in ["200", "422", "503"]:
        assert codigo in descripcion


def test_reserva_entrada_tiene_un_ejemplo_valido():
    componente = esquema()["components"]["schemas"]["ReservaEntrada"]
    ejemplos = componente["examples"]
    assert len(ejemplos) >= 1
    ReservaEntrada(**ejemplos[0])
