"""Errores personalizados y su conversión para la capa de UX."""

from __future__ import annotations

from model_ui.contracts import UserFacingError


class InputContractError(ValueError):
    """La petición no cumple el contrato de entrada."""


class ArtifactUnavailableError(FileNotFoundError):
    """El bundle o backend no está disponible."""


class InferenceTimeoutError(TimeoutError):
    """La inferencia tardó más de lo permitido."""


class BackendInferenceError(RuntimeError):
    """El backend no produjo una salida compatible."""

