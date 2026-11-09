"""Tests de src/reservas/data/features.py (NO MODIFICAR)."""
import pytest

from reservas.data import features


def test_variables_en_el_orden_del_modelo():
    assert len(features.VARIABLES) == 8
    assert features.VARIABLES == features.NUMERICAS + features.CATEGORICAS


def test_preparar_fila_ordena_las_columnas(caso_ok):
    desordenado = dict(reversed(list(caso_ok.items())))
    fila = features.preparar_fila(desordenado)
    assert fila.shape == (1, 8)
    assert list(fila.columns) == features.VARIABLES
    assert fila.iloc[0]["canal"] == "web"


def test_validar_campos_detecta_variable_que_falta(caso_ok):
    del caso_ok["noches"]
    with pytest.raises(ValueError, match="noches"):
        features.validar_campos(caso_ok)


def test_validar_campos_detecta_campo_que_sobra(caso_ok):
    caso_ok["mascota"] = "perro"
    with pytest.raises(ValueError, match="mascota"):
        features.validar_campos(caso_ok)


def test_preparar_fila_valida_los_campos(caso_ok):
    del caso_ok["canal"]
    with pytest.raises(ValueError):
        features.preparar_fila(caso_ok)
