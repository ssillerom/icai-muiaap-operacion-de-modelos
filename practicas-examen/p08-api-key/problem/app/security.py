"""Autenticacion con API key en la cabecera X-API-Key (TU)."""
import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status

from app.config import obtener_api_key

MENSAJE_NO_AUTORIZADO = "API key incorrecta o ausente"


def verificar_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    """Deja pasar la peticion solo si la cabecera X-API-Key coincide con API_KEY.

    FastAPI convierte el parametro x_api_key en la cabecera "x-api-key" (los
    nombres de cabecera no distinguen mayusculas).
    """
    # TODO 2: lanza HTTPException con status 401 (status.HTTP_401_UNAUTHORIZED)
    #   y detail=MENSAJE_NO_AUTORIZADO si:
    #     - no hay API_KEY configurada (cerrado por defecto: sin clave, nadie entra);
    #     - no llega la cabecera;
    #     - la cabecera no coincide con la clave.
    #   Compara con secrets.compare_digest sobre bytes (.encode()), no con ==.
    #   Si todo es correcto, no devuelvas nada: la peticion sigue su camino.
    #   Comprobacion: tests/test_seguridad.py (bloque TODO 2 y 3)
    raise NotImplementedError("TODO 2: verificar_api_key")
