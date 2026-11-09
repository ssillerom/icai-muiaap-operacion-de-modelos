"""Cliente HTTP que conecta el frontend con la API (C4).

Configuracion (entorno o .env): API_URL y API_KEY.
"""
import os
from dataclasses import dataclass, field

import httpx
from dotenv import load_dotenv
from pydantic import ValidationError

from envios.schemas import PrediccionSalida

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "")
TIMEOUT_SEGUNDOS = 10.0

# (HECHO)
ETIQUETAS = {
    "distancia_km": "Distancia (km)",
    "peso_kg": "Peso (kg)",
    "dias_prometidos": "Días prometidos",
    "transportista": "Transportista",
    "es_internacional": "Envío internacional",
    "envios_en_cola": "Envíos en cola",
}
MENSAJE_API_NO_DISPONIBLE = "No se puede conectar con el servicio de predicción."
MENSAJE_NO_AUTORIZADO = "El frontend no está autorizado a usar la API (revisar API_KEY)."
MENSAJE_MODELO_NO_DISPONIBLE = "El modelo no está disponible en este momento."
MENSAJE_ERROR_INESPERADO = "Ha ocurrido un error inesperado."


@dataclass
class Respuesta:
    """Lo que recibe app.py (HECHO)."""

    ok: bool
    prediccion: PrediccionSalida | None = None
    errores: list[str] = field(default_factory=list)


def traducir_errores(detalle: list[dict]) -> list[str]:
    """`detail` de un 422 de FastAPI -> frases con la etiqueta del formulario (HECHO)."""
    mensajes = []
    for error in detalle:
        loc = error.get("loc", [])
        etiqueta = ETIQUETAS.get(loc[1] if len(loc) > 1 else None, "Envío")
        mensajes.append(f"{etiqueta}: {error.get('msg', '').removeprefix('Value error, ')}")
    return mensajes


def crear_cliente() -> httpx.Client:
    """Cliente con URL base, cabecera X-API-Key y timeout."""
    # TODO C4a
    raise NotImplementedError("TODO C4a: crear_cliente")


def consultar(valores: dict, cliente: httpx.Client | None = None) -> Respuesta:
    """POST /predict y traduccion del resultado a una Respuesta."""
    # TODO C4b: usa el cliente que te pasen o crea uno (y cierralo tu solo
    #   si lo has creado tu). Traduce el resultado:
    #     200 -> prediccion | 422 -> traducir_errores | 401 | 503 |
    #     API que no responde | cualquier otra cosa
    #   con los mensajes definidos arriba.
    raise NotImplementedError("TODO C4b: consultar")
