"""Tests escritos por ti (TODO 4). Este es el unico fichero de tests que debes editar.

Tienes ejemplos de todo lo que necesitas en tests/test_errores.py y
tests/test_api.py.
"""
from fastapi.testclient import TestClient

import app.dependencies as dependencias
from app.main import app
from conftest import ModeloFalso
from reservas.model.artefacto import Artefacto, Manifiesto
from reservas.schemas import EJEMPLO_RESERVA

cliente = TestClient(app)


def test_alumno_503_si_falta_el_modelo(monkeypatch):
    # TODO 4a: con monkeypatch.setattr, sustituye dependencias.cargar_modelo
    #   por una funcion que lance FileNotFoundError. Despues haz POST /predict
    #   con EJEMPLO_RESERVA y comprueba el codigo 503 y el detail.
    raise NotImplementedError("TODO 4a")


def test_alumno_el_ejemplo_de_docs_funciona():
    # TODO 4b: comprueba que el ejemplo que ve el usuario en /docs es valido.
    #   Sustituye la dependencia obtener_artefacto con app.dependency_overrides
    #   por un Artefacto con ModeloFalso(0.1) y un Manifiesto cualquiera, haz
    #   POST /predict con EJEMPLO_RESERVA y comprueba 200 y riesgo "bajo".
    #   Limpia los overrides al terminar (try/finally), aunque el test falle.
    raise NotImplementedError("TODO 4b")
