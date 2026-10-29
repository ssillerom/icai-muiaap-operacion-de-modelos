"""Cliente HTTP que adapta la API Wine al contrato de inferencia de la UI."""

from __future__ import annotations

from collections.abc import Mapping
from threading import local
from typing import Any

import requests
from pydantic import ValidationError  # noqa: F401 - pista para el TODO S7.4

from model_ui.contracts import PredictionPayload
from model_ui.errors import (  # noqa: F401 - pistas para el TODO S7.2
    ArtifactUnavailableError,
    BackendInferenceError,
    InferenceTimeoutError,
    InputContractError,
)


class HttpInferenceGateway:
    """Implementa la frontera de inferencia mediante una llamada HTTP REST."""

    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 5.0,
        session: Any | None = None,
    ) -> None:
        normalized = base_url.strip().rstrip("/")
        if not normalized:
            raise ValueError("base_url no puede estar vacia")
        if timeout <= 0:
            raise ValueError("timeout debe ser positivo")

        self._prediction_url = f"{normalized}/v1/predictions"
        self._timeout = float(timeout)
        self._session = session if session is not None else requests.Session()
        self._request_context = local()
        self.last_request_id: str | None = None

    @property
    def last_request_id(self) -> str | None:
        """Devuelve el identificador de la ultima llamada en el contexto actual."""

        return getattr(self._request_context, "request_id", None)

    @last_request_id.setter
    def last_request_id(self, value: str | None) -> None:
        self._request_context.request_id = value

    def predict(self, values: Mapping[str, object]) -> PredictionPayload:
        """Envia la muestra por HTTP y devuelve el contrato interno de S6."""

        self.last_request_id = None
        # TODO S7.1: envia POST a self._prediction_url con json={"features": ...},
        # Accept application/json y self._timeout. Compruebalo con el test de llamada.
        try:
            response = self._session.post(
                self._prediction_url,
                json={"features": values},
                headers={"Accept": "application/json"},
                timeout=self._timeout,
            )
        # TODO S7.2: traduce Timeout, ConnectionError y RequestException a los
        # errores de dominio que ya entiende PredictionController.
        except requests.Timeout as e:
            raise InferenceTimeoutError(
                "La inferencia superó el tiempo permitido"
            ) from e
        except requests.ConnectionError as e:
            raise ArtifactUnavailableError("El backend no está disponible") from e
        except requests.RequestException as e:
            raise BackendInferenceError(
                "Error en la comunicación con el backend"
            ) from e
        # TODO S7.3: lee un objeto JSON, conserva request_id y diferencia 422/503
        # del resto de errores HTTP.
        self.last_request_id = self._header_request_id(response)
        if response.status_code == 422:
            raise InputContractError(
                "La petición no cumple el contrato de entrada del modelo"
            )
        if response.status_code == 503:
            raise ArtifactUnavailableError(
                "El bundle o el backend necesario no está disponible"
            )
        if not 200 <= response.status_code < 300:
            raise BackendInferenceError(f"Error HTTP {response.status_code}")

        # TODO S7.4: valida body["prediction"] como PredictionPayload; un dict sin
        # validar no satisface el contrato de salida.
        body = self._read_object(response)
        prediction_data = body.get("prediction")
        self.last_request_id = self._request_id(response, body)
        try:
            return PredictionPayload.model_validate(prediction_data)
        except ValidationError as e:
            raise BackendInferenceError(
                "El backend no pudo producir una salida compatible"
            ) from e

    @staticmethod
    def _read_object(response: Any) -> dict[str, Any]:
        """Lee una respuesta JSON que debe representar un objeto."""
        # TODO S7.3: usa response.json(), traduce ValueError y rechaza listas u
        # otros valores que no sean un objeto JSON.
        try:
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("La respuesta JSON no es un objeto")
            return data
        except ValueError as e:
            raise BackendInferenceError(
                "La respuesta del backend no es un objeto JSON válido"
            ) from e

    @staticmethod
    def _request_id(response: Any, body: dict[str, Any]) -> str | None:
        """Obtiene request_id del cuerpo y usa la cabecera como alternativa."""
        # TODO S7.3: prioriza body["request_id"] y usa X-Request-Id como fallback.
        request_id = body.get("request_id")
        if request_id is not None:
            return request_id
        return HttpInferenceGateway._header_request_id(response)

    @staticmethod
    def _header_request_id(response: Any) -> str | None:
        headers = getattr(response, "headers", {})
        return headers.get("X-Request-Id")
