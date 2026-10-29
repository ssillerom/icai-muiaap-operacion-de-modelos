"""TODOs de la vista UX: copy de salida y traducción de errores."""

from __future__ import annotations

from model_ui.contracts import PredictionPayload, PredictionView, UserFacingError
from model_ui.errors import (
    ArtifactUnavailableError,
    InferenceTimeoutError,
    InputContractError,
)
from model_ui.policies import (
    DEFAULT_CONFIDENCE_POLICY,
    DEFAULT_LATENCY_POLICY,
    ConfidencePolicy,
    LatencyPolicy,
    classify_confidence,
    classify_latency,
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
    confidence_level = classify_confidence(prediction.confidence, confidence_policy)
    latency_status = classify_latency(latency_ms, latency_policy)

    return PredictionView(
        quality_band=prediction.quality_band,
        quality_label=QUALITY_LABELS[prediction.quality_band],
        confidence=prediction.confidence,
        confidence_level=confidence_level,
        confidence_label=CONFIDENCE_COPY[confidence_level][0],
        confidence_message=CONFIDENCE_COPY[confidence_level][1],
        latency_ms=latency_ms,
        latency_status=latency_status,
        latency_label=LATENCY_COPY[latency_status][0],
        latency_message=LATENCY_COPY[latency_status][1],
        model_version=prediction.model_version,
        preprocessing_version=prediction.preprocessing_version,
    )


def to_user_facing_error(error: Exception, request_id: str) -> UserFacingError:
    """TODO: asigna código estable, mensaje accionable y recuperación."""
    if isinstance(error, InputContractError):
        code = "invalid_input"
        title = "Datos de entrada no válidos"
        message = "Los datos introducidos no cumplen los requisitos del modelo."
        recovery = (
            "Revisa los campos del formulario y asegúrate de que cumplen "
            "los rangos exigidos."
        )
    elif isinstance(error, ArtifactUnavailableError):
        code = "artifact_unavailable"
        title = "Modelo no disponible"
        message = (
            "El servicio o artefacto del modelo no se encuentra disponible "
            "actualmente."
        )
        recovery = (
            "Vuelve a intentarlo pasados unos minutos o contacta con soporte "
            "si persiste."
        )
    elif isinstance(error, InferenceTimeoutError):
        code = "timeout"
        title = "Tiempo de espera superado"
        message = "La inferencia tardó más tiempo del límite permitido para la demo."
        recovery = (
            "Prueba a reintentar la solicitud para comprobar si el servicio "
            "responde."
        )
    else:
        code = "prediction_error"
        title = "Error de inferencia"
        message = "No fue posible procesar la predicción con el backend de inferencia."
        recovery = "Revisa los valores introducidos o intenta de nuevo más tarde."

    return UserFacingError(
        code=code,
        title=title,
        message=message,
        recovery=recovery,
        request_id=request_id,
    )