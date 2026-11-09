"""Cliente HTTP que conecta el frontend con la API.

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
    return httpx.Client(base_url=API_URL, headers={"X-API-Key": API_KEY}, timeout=TIMEOUT_SEGUNDOS)


def consultar(valores: dict, cliente: httpx.Client | None = None) -> Respuesta:
    """POST /predict y traduccion del resultado a una Respuesta."""
    propio = cliente is None
    if propio:
        cliente = crear_cliente()
    try:
        respuesta = cliente.post("/predict", json=valores)
    except httpx.RequestError:
        return Respuesta(ok=False, errores=[MENSAJE_API_NO_DISPONIBLE])
    finally:
        if propio:
            cliente.close()

    if respuesta.status_code == 200:
        try:
            return Respuesta(ok=True, prediccion=PrediccionSalida.model_validate(respuesta.json()))
        except (ValueError, ValidationError):
            return Respuesta(ok=False, errores=[MENSAJE_ERROR_INESPERADO])
    if respuesta.status_code == 422:
        return Respuesta(ok=False, errores=traducir_errores(respuesta.json()["detail"]))
    if respuesta.status_code == 401:
        return Respuesta(ok=False, errores=[MENSAJE_NO_AUTORIZADO])
    if respuesta.status_code == 503:
        return Respuesta(ok=False, errores=[MENSAJE_MODELO_NO_DISPONIBLE])
    return Respuesta(ok=False, errores=[MENSAJE_ERROR_INESPERADO])
