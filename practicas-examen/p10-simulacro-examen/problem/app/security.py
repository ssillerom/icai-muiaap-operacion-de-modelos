"""Autenticacion con la cabecera X-API-Key (C2)."""
import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status

from app.config import obtener_api_key

MENSAJE_NO_AUTORIZADO = "API key incorrecta o ausente"


def verificar_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    """401 si no hay clave configurada, si falta la cabecera o si no coincide."""
    # TODO C2: 401 con detail=MENSAJE_NO_AUTORIZADO en los tres casos.
    #   Compara de forma segura.
    raise NotImplementedError("TODO C2: verificar_api_key")
