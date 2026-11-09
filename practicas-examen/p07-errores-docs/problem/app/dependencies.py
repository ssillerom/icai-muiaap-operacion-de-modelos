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
    """Devuelve el artefacto del modelo o responde 503 si no se puede cargar."""
    # TODO 1: ahora mismo, si el modelo no se puede cargar, la excepcion sube
    #   hasta FastAPI y el cliente recibe un 500 (error interno). Captura los
    #   tres fallos de "modelo no disponible" que ya conoces de P4/P5
    #   (FileNotFoundError, ArtefactoIncompatible y ValidationError del
    #   manifiesto) y lanza HTTPException con:
    #     status_code = 503 (usa status.HTTP_503_SERVICE_UNAVAILABLE)
    #     detail      = MENSAJE_MODELO_NO_DISPONIBLE
    #   No pongas en detail el texto de la excepcion. Y no captures Exception:
    #   un bug nuestro debe seguir siendo un 500.
    #   Comprobacion: tests/test_errores.py
    return cargar_modelo()


ArtefactoDep = Annotated[Artefacto, Depends(obtener_artefacto)]
