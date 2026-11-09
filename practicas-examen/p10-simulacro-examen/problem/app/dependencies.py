"""Dependencia que entrega el modelo a las rutas (C1)."""
from typing import Annotated

from fastapi import Depends, HTTPException, status

from envios.model.cargador import ModeloCargado, ModeloIncompatible, cargar_modelo

MENSAJE_MODELO_NO_DISPONIBLE = "Modelo no disponible"


def obtener_modelo() -> ModeloCargado:
    """Modelo cargado, o 503 si no se puede cargar."""
    # TODO C1: si el modelo no esta disponible, responde 503 con
    #   {"detail": "Modelo no disponible"} sin filtrar detalles internos.
    raise NotImplementedError("TODO C1: obtener_modelo")


# (HECHO) Tipo para pedir el modelo en una ruta: def ruta(modelo: ModeloDep)
ModeloDep = Annotated[ModeloCargado, Depends(obtener_modelo)]
