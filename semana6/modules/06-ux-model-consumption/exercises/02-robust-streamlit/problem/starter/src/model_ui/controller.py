"""TODOs del controlador de estados independiente de Streamlit."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from time import perf_counter
from uuid import uuid4

from model_ui.contracts import UiState
from model_ui.gateway import InferenceGateway
from model_ui.presentation import build_prediction_view, to_user_facing_error
from model_ui.telemetry import Telemetry

StateEmitter = Callable[[UiState], None]
Clock = Callable[[], float]
RequestIdFactory = Callable[[], str]


class PredictionController:
    """Orquesta loading, gateway, errores y telemetría."""

    def __init__(
        self,
        gateway: InferenceGateway,
        *,
        telemetry: Telemetry | None = None,
        clock: Clock = perf_counter,
        request_id_factory: RequestIdFactory | None = None,
    ) -> None:
        self.gateway = gateway
        self.telemetry = telemetry or Telemetry()
        self._clock = clock
        self._request_id_factory = request_id_factory or (lambda: uuid4().hex[:10])

    def submit(
        self,
        values: Mapping[str, object],
        *,
        emit: StateEmitter | None = None,
    ) -> UiState:
        """TODO: emite loading, mide, valida la salida y devuelve success/error."""
        request_id = self._request_id_factory()

        if emit is not None:
            emit(UiState(phase="loading", request_id=request_id))

        start_time = self._clock()

        try:
            prediction = self.gateway.predict(values)
            latency_ms = round((self._clock() - start_time) * 1000, 3)
            view = build_prediction_view(prediction, latency_ms)
            state = UiState(phase="success", request_id=request_id, view=view)
            self.telemetry.record_success(
                latency_ms,
                model_version=prediction.model_version,
                preprocessing_version=prediction.preprocessing_version,
            )
        except Exception as error:
            latency_ms = round((self._clock() - start_time) * 1000, 3)
            user_error = to_user_facing_error(error, request_id)
            state = UiState(phase="error", request_id=request_id, error=user_error)
            self.telemetry.record_error(
                latency_ms=latency_ms,
                code=user_error.code,
            )

        if emit is not None:
            emit(state)

        return state