"""Dependencias de la API.

Las rutas no cargan el modelo: lo piden con `ArtefactoDep` y FastAPI llama a
`obtener_artefacto()`. En los tests se sustituye con
`app.dependency_overrides[obtener_artefacto] = ...` para usar un modelo falso.
"""
from typing import Annotated

from fastapi import Depends

from reservas.model.artefacto import Artefacto
from reservas.model.cargador import cargar_modelo


def obtener_artefacto() -> Artefacto:
    """Devuelve el artefacto del modelo (cargado una sola vez gracias a lru_cache)."""
    return cargar_modelo()


ArtefactoDep = Annotated[Artefacto, Depends(obtener_artefacto)]
