"""Fixtures comunes (NO MODIFICAR)."""
from dataclasses import dataclass

import pytest

from reservas import train
from reservas.config import RUTA_ARTEFACTO
from reservas.model.artefacto import NOMBRE_MANIFIESTO, guardar_artefacto

# Clave que usan los tests. La fija el fixture api_key_de_test en el entorno.
CLAVE_TEST = "clave-de-test"
CABECERAS = {"X-API-Key": CLAVE_TEST}

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


@pytest.fixture(scope="session")
def modelo_y_metricas():
    """Modelo recien entrenado, sin guardar."""
    return train.entrenar()


@pytest.fixture(scope="session")
def artefacto_en_disco(modelo_y_metricas):
    """Garantiza que existe el artefacto por defecto (equivale a uv run entrenar)."""
    if not (RUTA_ARTEFACTO / NOMBRE_MANIFIESTO).exists():
        guardar_artefacto(*modelo_y_metricas)
    return RUTA_ARTEFACTO


@pytest.fixture(autouse=True)
def api_key_de_test(monkeypatch):
    """Todos los tests se ejecutan con API_KEY=clave-de-test, haya o no un .env."""
    monkeypatch.setenv("API_KEY", CLAVE_TEST)


@pytest.fixture
def caso_ok():
    return dict(CASO_OK)


@dataclass
class ModeloFalso:
    """Doble de prueba: siempre devuelve la misma probabilidad."""

    probabilidad: float

    def predict_proba(self, fila):
        return [[1 - self.probabilidad, self.probabilidad]]
