"""Puente entre el frontend y la API REST (practica 9).

app.py NO cambia respecto a la practica 5: sigue llamando a consultar_modelo()
y recibiendo una Respuesta. Lo unico que cambia es como se obtiene la
prediccion: antes llamando a predecir() en el mismo proceso; ahora con un
POST /predict a la API.

Configuracion (variables de entorno o fichero .env):
    API_URL   URL base de la API (por defecto http://localhost:8000)
    API_KEY   clave que se envia en la cabecera X-API-Key
"""
import os
from dataclasses import dataclass, field

import httpx
from dotenv import load_dotenv
from pydantic import ValidationError

from reservas.schemas import PrediccionSalida

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "")
TIMEOUT_SEGUNDOS = 10.0

# Nombres que ve el usuario en el formulario
ETIQUETAS = {
    "antelacion_dias": "Antelación (días)",
    "noches": "Noches",
    "adultos": "Adultos",
    "ninos": "Niños",
    "precio_noche": "Precio por noche (€)",
    "canal": "Canal de reserva",
    "cancelaciones_previas": "Cancelaciones previas",
    "peticiones_especiales": "Peticiones especiales",
}
MENSAJE_MODELO_NO_DISPONIBLE = (
    "El modelo no está disponible en este momento. Inténtalo más tarde o avisa al equipo técnico."
)
MENSAJE_API_NO_DISPONIBLE = (
    "No se puede conectar con el servicio de predicción. Inténtalo más tarde."
)
MENSAJE_NO_AUTORIZADO = (
    "El frontend no está autorizado a usar la API. Avisa al equipo técnico (revisar API_KEY)."
)
MENSAJE_ERROR_INESPERADO = "Ha ocurrido un error inesperado. Inténtalo más tarde."


@dataclass
class Respuesta:
    """Lo que recibe app.py: o una prediccion, o una lista de mensajes para el usuario."""

    ok: bool
    prediccion: PrediccionSalida | None = None
    errores: list[str] = field(default_factory=list)


def crear_cliente() -> httpx.Client:
    """Cliente HTTP con la URL base, la cabecera X-API-Key y un timeout."""
    return httpx.Client(
        base_url=API_URL,
        headers={"X-API-Key": API_KEY},
        timeout=TIMEOUT_SEGUNDOS,
    )


def traducir_errores_api(detalle: list[dict]) -> list[str]:
    """Convierte el `detail` de un 422 de FastAPI en frases con la etiqueta del formulario.

    En FastAPI, loc empieza por "body": ["body", "adultos"]. Los errores del
    model_validator no tienen campo: loc == ["body"].
    """
    mensajes = []
    for error in detalle:
        loc = error.get("loc", [])
        campo = loc[1] if len(loc) > 1 else None
        etiqueta = ETIQUETAS.get(campo, "Reserva")
        texto = error.get("msg", "").removeprefix("Value error, ")
        mensajes.append(f"{etiqueta}: {texto}")
    return mensajes


def consultar_modelo(valores: dict, cliente: httpx.Client | None = None) -> Respuesta:
    """Envia la reserva a POST /predict y traduce la respuesta HTTP a una Respuesta.

    `cliente` permite inyectar otro cliente en los tests (por ejemplo, el
    TestClient de FastAPI). Si no se pasa, se crea uno y se cierra al terminar.
    """
    propio = cliente is None
    if propio:
        cliente = crear_cliente()
    try:
        respuesta = cliente.post("/predict", json=valores)
    except httpx.RequestError:
        # Servidor apagado, URL incorrecta, timeout...
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
        return Respuesta(ok=False, errores=traducir_errores_api(respuesta.json()["detail"]))
    if respuesta.status_code == 401:
        return Respuesta(ok=False, errores=[MENSAJE_NO_AUTORIZADO])
    if respuesta.status_code == 503:
        return Respuesta(ok=False, errores=[MENSAJE_MODELO_NO_DISPONIBLE])
    return Respuesta(ok=False, errores=[MENSAJE_ERROR_INESPERADO])
