"""Tests de src/reservas/model/cargador.py (NO MODIFICAR)."""
import pytest

from reservas.model import cargador


def test_carga_un_modelo_que_predice_probabilidades():
    modelo = cargador.cargar_modelo()
    assert hasattr(modelo, "predict_proba")


def test_el_modelo_se_carga_una_sola_vez():
    assert cargador.cargar_modelo() is cargador.cargar_modelo()


def test_ruta_inexistente_da_un_error_claro(tmp_path):
    with pytest.raises(FileNotFoundError, match="entrenar"):
        cargador.cargar_modelo(tmp_path / "no_existe.joblib")
