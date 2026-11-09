"""Tests de src/reservas/model/cargador.py (NO MODIFICAR)."""
import pytest

from reservas.config import VERSION_MODELO
from reservas.model import cargador
from reservas.model.artefacto import Artefacto


@pytest.fixture(autouse=True)
def _artefacto(artefacto_en_disco):
    return artefacto_en_disco


def test_carga_el_artefacto_por_defecto():
    artefacto = cargador.cargar_modelo()
    assert isinstance(artefacto, Artefacto)
    assert hasattr(artefacto.modelo, "predict_proba")
    assert artefacto.manifiesto.version_modelo == VERSION_MODELO


def test_el_artefacto_se_carga_una_sola_vez():
    assert cargador.cargar_modelo() is cargador.cargar_modelo()
