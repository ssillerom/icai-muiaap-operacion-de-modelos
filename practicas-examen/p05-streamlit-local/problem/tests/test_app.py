"""Tests de la app Streamlit completa con AppTest (NO MODIFICAR).

AppTest ejecuta frontend/app.py sin navegador y permite pulsar botones y
cambiar widgets desde el test.
"""
import pytest
from streamlit.testing.v1 import AppTest

from reservas.config import RAIZ

APP = str(RAIZ / "frontend" / "app.py")


@pytest.fixture
def app(artefacto_en_disco):
    prueba = AppTest.from_file(APP, default_timeout=30)
    prueba.run()
    assert not prueba.exception
    return prueba


def test_la_app_arranca_sin_resultado(app):
    assert len(app.metric) == 0
    assert len(app.error) == 0


def test_enviar_muestra_la_prediccion(app):
    app.button[0].click().run()
    assert not app.exception
    assert len(app.metric) == 1
    assert app.metric[0].value.endswith("%")
    assert any("Modelo 1.0.0" in c.value for c in app.caption)


def test_datos_invalidos_muestran_el_error(app):
    entradas = {n.label: n for n in app.number_input}
    entradas["Adultos"].set_value(4)
    entradas["Niños"].set_value(4)
    app.button[0].click().run()
    assert not app.exception
    assert len(app.metric) == 0
    assert len(app.error) == 1
    assert any("6 huespedes" in m.value for m in app.markdown)
