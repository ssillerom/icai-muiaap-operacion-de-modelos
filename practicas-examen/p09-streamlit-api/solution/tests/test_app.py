"""Tests de la app Streamlit completa contra la API, con AppTest (NO MODIFICAR).

AppTest ejecuta frontend/app.py sin navegador. En lugar de arrancar uvicorn,
se sustituye gateway.crear_cliente por el TestClient de FastAPI, de modo que
la app habla con la API real en el mismo proceso.
"""
import pytest
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

import app.dependencies as dependencias
import gateway
from app.main import app as api
from conftest import CABECERAS
from reservas.config import RAIZ, VERSION_MODELO

APP = str(RAIZ / "frontend" / "app.py")


@pytest.fixture
def pagina(artefacto_en_disco, monkeypatch):
    monkeypatch.setattr(gateway, "crear_cliente", lambda: TestClient(api, headers=CABECERAS))
    prueba = AppTest.from_file(APP, default_timeout=30)
    prueba.run()
    assert not prueba.exception
    return prueba


def test_la_app_arranca_sin_resultado(pagina):
    assert len(pagina.metric) == 0
    assert len(pagina.error) == 0


def test_enviar_muestra_la_prediccion_de_la_api(pagina):
    pagina.button[0].click().run()
    assert not pagina.exception
    assert len(pagina.metric) == 1
    assert any(f"Modelo {VERSION_MODELO}" in c.value for c in pagina.caption)


def test_datos_invalidos_muestran_el_error_de_la_api(pagina):
    entradas = {n.label: n for n in pagina.number_input}
    entradas["Adultos"].set_value(4)
    entradas["Niños"].set_value(4)
    pagina.button[0].click().run()
    assert len(pagina.metric) == 0
    assert len(pagina.error) == 1
    assert any("6 huespedes" in m.value for m in pagina.markdown)


def test_modelo_no_disponible_en_la_api(pagina, monkeypatch):
    def sin_modelo():
        raise FileNotFoundError("no hay modelo")

    monkeypatch.setattr(dependencias, "cargar_modelo", sin_modelo)
    pagina.button[0].click().run()
    assert len(pagina.error) == 1
    assert any("no está disponible" in m.value for m in pagina.markdown)
