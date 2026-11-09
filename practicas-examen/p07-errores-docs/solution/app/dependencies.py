"""Dependencias de la API.

Las rutas no cargan el modelo: lo piden con `ArtefactoDep` y FastAPI llama a
`obtener_artefacto()`. En los tests se sustituye con
`app.dependency_overrides[obtener_artefacto] = ...` para usar un modelo falso.
"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from reservas.model.artefacto import Artefacto, ArtefactoIncompatible
from reservas.model.cargador import cargar_modelo

MENSAJE_MODELO_NO_DISPONIBLE = "Modelo no disponible"


def obtener_artefacto() -> Artefacto:
    """Devuelve el artefacto del modelo o responde 503 si no se puede cargar.

    503 (Service Unavailable) indica que el fallo es del servicio y temporal:
    la peticion era correcta y puede repetirse cuando el modelo este disponible.
    El detalle nunca incluye el texto de la excepcion (puede contener rutas).
    """
    try:
        return cargar_modelo()
    except (FileNotFoundError, ArtefactoIncompatible, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=MENSAJE_MODELO_NO_DISPONIBLE,
        )


ArtefactoDep = Annotated[Artefacto, Depends(obtener_artefacto)]
