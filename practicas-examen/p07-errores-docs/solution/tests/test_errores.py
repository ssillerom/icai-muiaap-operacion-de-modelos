"""Tests del error 503 cuando el modelo no esta disponible (NO MODIFICAR)."""
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

import app.dependencies as dependencias
from app.main import app
from reservas.model.artefacto import ArtefactoIncompatible, Manifiesto

cliente = TestClient(app)


def manifiesto_corrupto():
    try:
        Manifiesto.model_validate({})
    except ValidationError as error:
        return error


@pytest.fixture(params=["sin_fichero", "incompatible", "manifiesto_corrupto"])
def modelo_roto(request, monkeypatch):
    """Simula que cargar_modelo() falla de tres formas distintas."""
    errores = {
        "sin_fichero": FileNotFoundError("C:/ruta/secreta/models/cancelacion/manifest.json"),
        "incompatible": ArtefactoIncompatible("variables distintas en C:/ruta/secreta"),
        "manifiesto_corrupto": manifiesto_corrupto(),
    }

    def falla():
        raise errores[request.param]

    monkeypatch.setattr(dependencias, "cargar_modelo", falla)


def test_predict_sin_modelo_da_503(modelo_roto, caso_ok):
    respuesta = cliente.post("/predict", json=caso_ok)
    assert respuesta.status_code == 503
    assert respuesta.json() == {"detail": "Modelo no disponible"}


def test_el_error_no_filtra_detalles_internos(modelo_roto, caso_ok):
    respuesta = cliente.post("/predict", json=caso_ok)
    assert "secreta" not in respuesta.text
    assert "Traceback" not in respuesta.text


def test_health_sigue_respondiendo_sin_modelo(modelo_roto):
    assert cliente.get("/health").status_code == 200


def test_otros_errores_no_se_ocultan_como_503(monkeypatch, caso_ok):
    """Un bug nuestro (p. ej. un TypeError) no es 'modelo no disponible'."""

    def bug():
        raise TypeError("bug en el codigo")

    monkeypatch.setattr(dependencias, "cargar_modelo", bug)
    cliente_sin_excepciones = TestClient(app, raise_server_exceptions=False)
    assert cliente_sin_excepciones.post("/predict", json=caso_ok).status_code == 500
