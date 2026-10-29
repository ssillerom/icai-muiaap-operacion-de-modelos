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
    session = session if session is not None else requests
    try:
        response = session.post(f"{base_url}/v1/predictions", json=payload, headers={"Accept": "application/json"}, timeout=timeout)
    # TODO 4: llama a `raise_for_status()` y conserva el status de HTTPError.
        response.raise_for_status()
    except requests.HTTPError as e:
        raise PredictionClientError(str(e), status_code=e.response.status_code) from e
    # TODO 5: traduce Timeout y ConnectionError a PredictionClientError.
    except requests.Timeout as e:
        raise PredictionClientError("Timeout", status_code=None) from e
    except requests.ConnectionError as e:
        raise PredictionClientError("Error de conexión. Intenta conectar de nuevo", status_code=None) from e

    # TODO 6: convierte la respuesta con `.json()` y exige un diccionario.
    data = response.json()
    if not isinstance(data, dict):
        raise PredictionClientError("Response.json() no es un objeto dict", status_code=response.status_code)
    
    return data