from conftest import CASO_OK
from app.services.modelo import decidir, predecir
from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada


def test_predecir_devuelve_salida_valida():
    salida = predecir(PrestamoEntrada(**CASO_OK))
    assert isinstance(salida, PrediccionSalida)
    assert 0 <= salida.probabilidad_impago <= 1


def test_mas_impagos_mas_riesgo():
    bueno = dict(CASO_OK)
    malo = dict(CASO_OK)
    malo["impagos_previos"] = 3
    p_bueno = predecir(PrestamoEntrada(**bueno)).probabilidad_impago
    p_malo = predecir(PrestamoEntrada(**malo)).probabilidad_impago
    assert p_malo > p_bueno


def test_decidir_umbrales():
    assert decidir(0.05) == "aprobar"
    assert decidir(0.3) == "revisar"
    assert decidir(0.8) == "rechazar"
