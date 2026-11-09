"""Puente entre el frontend y la API REST (TU, practica 9).

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

# Nombres que ve el usuario en el formulario (HECHO)
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
    """Lo que recibe app.py: o una prediccion, o una lista de mensajes para el usuario (HECHO)."""

    ok: bool
    prediccion: PrediccionSalida | None = None
    errores: list[str] = field(default_factory=list)


def crear_cliente() -> httpx.Client:
    """Cliente HTTP con la URL base, la cabecera X-API-Key y un timeout."""
    # TODO 1: crea y devuelve un httpx.Client con:
    #   - base_url = API_URL (asi luego basta con post("/predict", ...));
    #   - la cabecera "X-API-Key" con API_KEY en headers;
    #   - timeout = TIMEOUT_SEGUNDOS. Sin timeout, si la API se cuelga, la
    #     interfaz se queda esperando para siempre.
    #   Comprobacion: tests/test_gateway.py::test_crear_cliente_usa_la_configuracion
    raise NotImplementedError("TODO 1: crear_cliente")


def traducir_errores_api(detalle: list[dict]) -> list[str]:
    """Convierte el `detail` de un 422 de FastAPI en frases con la etiqueta del formulario."""
    # TODO 2: es lo mismo que traducir_errores() de la practica 5, pero ahora
    #   los errores llegan como JSON de la API. Diferencia: en FastAPI `loc`
    #   empieza por "body", p. ej. ["body", "adultos"]; el campo es loc[1].
    #   Los errores del model_validator traen loc == ["body"]: usa "Reserva".
    #   Quita el prefijo "Value error, " del mensaje.
    #   Comprobacion: tests/test_gateway.py::test_traducir_*
    raise NotImplementedError("TODO 2: traducir_errores_api")


def consultar_modelo(valores: dict, cliente: httpx.Client | None = None) -> Respuesta:
    """Envia la reserva a POST /predict y traduce la respuesta HTTP a una Respuesta.

    `cliente` permite inyectar otro cliente en los tests (por ejemplo, el
    TestClient de FastAPI). Si no se pasa, se crea uno y se cierra al terminar.
    """
    # TODO 3:
    #   1) si no te pasan cliente, crealo con crear_cliente() y cierralo al
    #      terminar (try/finally o with); si te lo pasan, NO lo cierres;
    #   2) haz POST "/predict" con los valores como JSON. No valides aqui con
    #      ReservaEntrada: la API ya valida (un solo contrato);
    #   3) si httpx lanza httpx.RequestError (API apagada, URL mal, timeout)
    #      -> MENSAJE_API_NO_DISPONIBLE;
    #   4) traduce el codigo de estado:
    #        200 -> Respuesta(ok=True, prediccion=PrediccionSalida.model_validate(json))
    #               (si el JSON no cumple el contrato -> MENSAJE_ERROR_INESPERADO)
    #        422 -> traducir_errores_api(json["detail"])
    #        401 -> MENSAJE_NO_AUTORIZADO
    #        503 -> MENSAJE_MODELO_NO_DISPONIBLE
    #        otro -> MENSAJE_ERROR_INESPERADO
    #   Comprobacion: tests/test_gateway.py (bloques TODO 3) y tests/test_app.py
    raise NotImplementedError("TODO 3: consultar_modelo")
