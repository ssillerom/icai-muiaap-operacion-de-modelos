"""Autenticacion con API key en la cabecera X-API-Key."""
import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status

from app.config import obtener_api_key

MENSAJE_NO_AUTORIZADO = "API key incorrecta o ausente"


def verificar_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    """Deja pasar la peticion solo si la cabecera X-API-Key coincide con API_KEY.

    - FastAPI convierte el parametro x_api_key en la cabecera "x-api-key".
    - Si API_KEY no esta configurada, se rechaza todo (cerrado por defecto).
    - secrets.compare_digest compara en tiempo constante para no dar pistas
      sobre la clave midiendo cuanto tarda la respuesta.
    """
    esperada = obtener_api_key()
    if (
        esperada is None
        or x_api_key is None
        or not secrets.compare_digest(x_api_key.encode(), esperada.encode())
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MENSAJE_NO_AUTORIZADO,
        )
