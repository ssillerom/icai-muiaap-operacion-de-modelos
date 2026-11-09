"""Tests de src/reservas/data/features.py (NO MODIFICAR)."""
from reservas.data import features
from reservas.schemas import ReservaEntrada


def test_variables_en_el_orden_del_modelo():
    assert len(features.VARIABLES) == 8
    assert features.VARIABLES == features.NUMERICAS + features.CATEGORICAS


def test_preparar_fila_ordena_las_columnas(caso_ok):
    desordenado = dict(reversed(list(caso_ok.items())))
    fila = features.preparar_fila(ReservaEntrada(**desordenado))
    assert fila.shape == (1, 8)
    assert list(fila.columns) == features.VARIABLES
    assert fila.iloc[0]["canal"] == "web"
