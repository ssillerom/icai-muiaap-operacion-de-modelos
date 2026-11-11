"""Starter del cliente HTTP. Completa los TODO sin modificar la API."""

from __future__ import annotations

from typing import Any

# El TODO de la práctica usará este cliente para realizar la petición HTTP.
import requests  # noqa: F401


class PredictionClientError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


def request_prediction(
    payload: dict[str, Any],
    *,
    base_url: str = "http://127.0.0.1:8000",
    timeout: float = 5.0,
    session: Any | None = None,
) -> dict[str, Any]:
    """Envía una predicción y devuelve un objeto JSON de respuesta."""
    # TODO 3: selecciona `session` o `requests` y envía POST con `json=`,
    # `Accept` y `timeout`. Comprueba los argumentos con test_client.py.
    try:
        cliente = session or requests  # NUEVO método aprendido, si arg1 es None coge el siguiente si no coge el arg1
        response =  cliente.post(base_url+"/v1/predictions", json = payload, headers= {"Accept":"application/json"}, timeout= timeout) #el url lo he forzado para el test pero no entiendo por que
        # TODO 4: llama a `raise_for_status()` y conserva el status de HTTPError.
        response.raise_for_status()
    except requests.HTTPError as error:
        raise PredictionClientError("se ha rechazado la request", status_code= error.response.status_code ) from error
        # TODO 5: traduce Timeout y ConnectionError a PredictionClientError.
    except requests.Timeout as error:
        raise PredictionClientError("timeout") from error
    except requests.ConnectionError as error:
        raise PredictionClientError("error al conectar") from error  
    # TODO 6: convierte la respuesta con `.json()` y exige un diccionario.
    respuesta = response.json()
    es_dict = isinstance(respuesta, dict)
    if not es_dict:
        raise PredictionClientError("el objeto de respuesta no es un diccionario")
    return respuesta
