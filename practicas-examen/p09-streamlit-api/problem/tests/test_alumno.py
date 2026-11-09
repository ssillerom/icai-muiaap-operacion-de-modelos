"""Tests propios de la practica 7 (ya resueltos)."""
from fastapi.testclient import TestClient

import app.dependencies as dependencias
from app.main import app
from conftest import CABECERAS, ModeloFalso
from reservas.model.artefacto import Artefacto, Manifiesto
from reservas.schemas import EJEMPLO_RESERVA

cliente = TestClient(app, headers=CABECERAS)


def test_alumno_503_si_falta_el_modelo(monkeypatch):
    def sin_modelo():
        raise FileNotFoundError("no hay modelo")

    monkeypatch.setattr(dependencias, "cargar_modelo", sin_modelo)
    respuesta = cliente.post("/predict", json=EJEMPLO_RESERVA)
    assert respuesta.status_code == 503
    assert respuesta.json()["detail"] == "Modelo no disponible"


def test_alumno_el_ejemplo_de_docs_funciona():
    manifiesto = Manifiesto(
        version_modelo="test",
        fecha_entrenamiento="2026-01-01T00:00:00Z",
        variables=[],
        metricas={},
        version_sklearn="-",
    )
    app.dependency_overrides[dependencias.obtener_artefacto] = lambda: Artefacto(
        modelo=ModeloFalso(0.1), manifiesto=manifiesto
    )
    try:
        respuesta = cliente.post("/predict", json=EJEMPLO_RESERVA)
    finally:
        app.dependency_overrides.clear()
    assert respuesta.status_code == 200
    assert respuesta.json()["riesgo"] == "bajo"
