"""Dependencia que entrega el modelo a las rutas."""
from typing import Annotated

from fastapi import Depends, HTTPException, status

from envios.model.cargador import ModeloCargado, ModeloIncompatible, cargar_modelo

MENSAJE_MODELO_NO_DISPONIBLE = "Modelo no disponible"


def obtener_modelo() -> ModeloCargado:
    """Modelo cargado, o 503 si no se puede cargar."""
    try:
        return cargar_modelo()
    except (FileNotFoundError, ModeloIncompatible):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=MENSAJE_MODELO_NO_DISPONIBLE,
        )


ModeloDep = Annotated[ModeloCargado, Depends(obtener_modelo)]
