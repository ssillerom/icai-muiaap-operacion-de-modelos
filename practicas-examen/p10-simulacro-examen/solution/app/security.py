"""Autenticacion con la cabecera X-API-Key."""
import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status

from app.config import obtener_api_key

MENSAJE_NO_AUTORIZADO = "API key incorrecta o ausente"


def verificar_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    """401 si no hay clave configurada, si falta la cabecera o si no coincide."""
    esperada = obtener_api_key()
    if (
        esperada is None
        or x_api_key is None
        or not secrets.compare_digest(x_api_key.encode(), esperada.encode())
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=MENSAJE_NO_AUTORIZADO)
