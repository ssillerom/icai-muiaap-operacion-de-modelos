"""Fixtures comunes (NO MODIFICAR)."""
from dataclasses import dataclass

import pytest

from envios import train
from envios.config import RUTA_MODELO
from envios.model.cargador import ModeloCargado

CLAVE_TEST = "clave-de-test"
CABECERAS = {"X-API-Key": CLAVE_TEST}

CASO_OK = {
    "distancia_km": 450.0,
    "peso_kg": 2.5,
    "dias_prometidos": 3,
    "transportista": "estandar",
    "es_internacional": False,
    "envios_en_cola": 120,
}


@pytest.fixture(autouse=True)
def api_key_de_test(monkeypatch):
    """Todos los tests se ejecutan con API_KEY=clave-de-test, haya o no un .env."""
    monkeypatch.setenv("API_KEY", CLAVE_TEST)


@pytest.fixture(scope="session")
def modelo_en_disco():
    """Garantiza que existe models/modelo_envios.joblib (equivale a uv run entrenar)."""
    if not RUTA_MODELO.exists():
        modelo, _ = train.entrenar()
        train.guardar(modelo)
    return RUTA_MODELO


@pytest.fixture
def caso_ok():
    return dict(CASO_OK)


@dataclass
class ModeloFalso:
    """Doble de prueba: siempre devuelve la misma probabilidad."""

    probabilidad: float

    def predict_proba(self, fila):
        return [[1 - self.probabilidad, self.probabilidad]]


def modelo_falso(probabilidad: float = 0.8) -> ModeloCargado:
    return ModeloCargado(modelo=ModeloFalso(probabilidad), version="test")
