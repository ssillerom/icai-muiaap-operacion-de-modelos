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
    # TODO 3: devuelve el artefacto usando la funcion del backend que ya lo
    #   carga una sola vez. No vuelvas a leer el joblib aqui.
    #   Comprobacion: tests/test_api.py::test_obtener_artefacto_devuelve_el_artefacto_real
    raise NotImplementedError("TODO 3: obtener_artefacto")


# (HECHO) Tipo para declarar en una ruta "necesito el artefacto". Ejemplo:
#     def mi_ruta(artefacto: ArtefactoDep): ...
ArtefactoDep = Annotated[Artefacto, Depends(obtener_artefacto)]
