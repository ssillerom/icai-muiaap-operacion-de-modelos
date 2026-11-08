"""TODOs del controlador de estados independiente de Streamlit."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from time import perf_counter
from uuid import uuid4

from model_ui.contracts import PredictionPayload, UiState
from model_ui.gateway import InferenceGateway
from model_ui.telemetry import Telemetry
from model_ui.presentation import build_prediction_view, to_user_facing_error

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
        """Emite loading, mide, valida la salida y devuelve success/error."""
        request_id = self._request_id_factory()

        if emit is not None:
            emit(UiState(phase="loading", request_id=request_id))

        start = self._clock()
        error: Exception | None = None
        try:
            raw = self.gateway.predict(values)
        except Exception as exc:
            error = exc
        latency_ms = self._elapsed_ms(start)  # el reloj se llama exactamente 2 veces

        if error is None:
            try:
                # Valida la salida del backend contra el contrato.
                prediction = PredictionPayload.model_validate(raw)
            except Exception as exc:
                error = exc

        if error is not None:
            user_error = to_user_facing_error(error, request_id=request_id)
            # Solo código y latencia: nunca values ni payload.
            self.telemetry.record_error(user_error.code, latency_ms)
            final_state = UiState(phase="error", request_id=request_id, error=user_error)
        else:
            view = build_prediction_view(prediction, latency_ms)
            self.telemetry.record_success(
                latency_ms,
                model_version=view.model_version,
                preprocessing_version=view.preprocessing_version,
            )
            final_state = UiState(phase="success", request_id=request_id, view=view)

        if emit is not None:
            emit(final_state)
        return final_state

    def _elapsed_ms(self, start: float) -> float:
        """Milisegundos desde start, redondeados para evitar ruido de float."""
        return round((self._clock() - start) * 1000, 3)
