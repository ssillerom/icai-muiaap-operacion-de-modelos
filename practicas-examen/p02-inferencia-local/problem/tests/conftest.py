"""Fixtures comunes (NO MODIFICAR)."""
import pytest

from reservas import train
from reservas.config import RUTA_MODELO

CASO_OK = {
    "antelacion_dias": 30,
    "noches": 3,
    "adultos": 2,
    "ninos": 0,
    "precio_noche": 120.0,
    "canal": "web",
    "cancelaciones_previas": 0,
    "peticiones_especiales": 1,
}


@pytest.fixture(scope="session", autouse=True)
def modelo_entrenado():
    """Entrena y guarda el modelo si todavia no existe (equivale a uv run entrenar)."""
    if not RUTA_MODELO.exists():
        modelo, _ = train.entrenar()
        train.guardar_modelo(modelo)
    return RUTA_MODELO


@pytest.fixture
def caso_ok():
    return dict(CASO_OK)
