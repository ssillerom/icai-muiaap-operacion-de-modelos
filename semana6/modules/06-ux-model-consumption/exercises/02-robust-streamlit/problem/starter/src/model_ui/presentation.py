"""TODOs de la vista UX: copy de salida y traducción de errores."""

from __future__ import annotations
from model_ui.policies import classify_confidence, classify_latency
from model_ui.errors import InputContractError, ArtifactUnavailableError, InferenceTimeoutError, BackendInferenceError

from model_ui.contracts import PredictionPayload, PredictionView, UserFacingError
from model_ui.policies import (
    DEFAULT_CONFIDENCE_POLICY,
    DEFAULT_LATENCY_POLICY,
    ConfidencePolicy,
    LatencyPolicy,
)

QUALITY_LABELS = {
    "needs_review": "Requiere revisión",
    "acceptable": "Resultado aceptable",
    "excellent": "Resultado excelente",
}

CONFIDENCE_COPY = {
    "low": (
        "Confianza baja",
        "El resultado es orientativo y requiere revisión; "
        "la confianza no es una garantía.",
    ),
    "medium": (
        "Confianza intermedia",
        "Usa el resultado como señal orientativa y revisa su contexto antes de actuar.",
    ),
    "high": (
        "Confianza alta",
        "La confianza es alta para este modelo, pero no garantiza "
        "que la decisión sea correcta.",
    ),
}

LATENCY_COPY = {
    "within_target": (
        "Dentro del objetivo",
        "La respuesta quedó dentro del objetivo de la demo.",
    ),
    "above_target": (
        "Por encima del objetivo",
        "La respuesta llegó, pero la latencia supera el objetivo técnico de la demo.",
    ),
}


def build_prediction_view(
    prediction: PredictionPayload,
    latency_ms: float,
    *,
    confidence_policy: ConfidencePolicy = DEFAULT_CONFIDENCE_POLICY,
    latency_policy: LatencyPolicy = DEFAULT_LATENCY_POLICY,
) -> PredictionView:
    """TODO: construye la vista con etiquetas, confianza, latencia y versiones."""
    quality_l=QUALITY_LABELS[prediction.quality_band]
    confidence_le=classify_confidence(prediction.confidence, confidence_policy)
    confidence_la=CONFIDENCE_COPY[confidence_le][0]
    confidence_m=CONFIDENCE_COPY[confidence_le][1]
    latency_s=classify_latency(latency_ms, latency_policy)
    latency_la=LATENCY_COPY[latency_s][0]
    latency_m=LATENCY_COPY[latency_s][1]
    return PredictionView(
       quality_band=prediction.quality_band,
       quality_label=quality_l,
       confidence=prediction.confidence,
       confidence_level=confidence_le,
       confidence_label=confidence_la,
       confidence_message=confidence_m,
       latency_ms=latency_ms,
       latency_status=latency_s,
       latency_label=latency_la,
       latency_message=latency_m,
       model_version=prediction.model_version,
       preprocessing_version=prediction.preprocessing_version,
    )


def to_user_facing_error(error: Exception, request_id: str) -> UserFacingError:
    """Convierte excepciones internas del sistema en objetos UserFacingError seguros para la UX."""
    if isinstance(error, InputContractError):
        code = "invalid_input"
        title = "Entrada no válida"
        message = "La petición no cumple el contrato de entrada."
        recovery = "Revisa los campos requeridos y vuelve a intentarlo."
        
    elif isinstance(error, ArtifactUnavailableError):
        code = "artifact_unavailable"
        title = "Recurso no disponible"
        message = "El bundle o backend no está disponible."
        recovery = "Verifica los identificadores o inténtalo más tarde."
        
    elif isinstance(error, InferenceTimeoutError):
        code = "timeout"
        title = "Tiempo de espera agotado"
        message = "La inferencia tardó más de lo permitido."
        recovery = "Vuelve a enviar la solicitud en unos momentos."
        
    elif isinstance(error, BackendInferenceError):
        code = "prediction_error"
        title = "Error de procesamiento"
        message = "El backend no produjo una salida compatible."
        recovery = "Inténtalo de nuevo o contacta a soporte si persiste."
        
    else:
        code = "prediction_error"
        title = "Error de Procesamiento"
        message = "No se pudo generar una prediccion válida"
        recovery = "Inténtalo de nuevo o contacta a soporte a ver si persiste."

    return UserFacingError(
        code=code,
        title=title,
        message=message,
        recovery=recovery,
        request_id=request_id,
    )


