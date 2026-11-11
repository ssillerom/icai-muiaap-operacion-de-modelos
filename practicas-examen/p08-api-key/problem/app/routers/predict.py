"""POST /predict: riesgo de cancelacion de una reserva (requiere API key)."""
from fastapi import APIRouter, Depends

from app.dependencies import ArtefactoDep
from app.security import verificar_api_key
from reservas.inference import predecir
from reservas.schemas import PrediccionSalida, ReservaEntrada

# TODO 3a: protege TODAS las rutas de este router con verificar_api_key.
#   Investiga el parametro `dependencies=[Depends(...)]` de APIRouter.
#   /health esta en otro router y debe seguir siendo publico.
router = APIRouter(tags=["prediccion"])


# TODO 3b: documenta el 401 en `responses` ("API key incorrecta o ausente") y
#   anade al docstring que la ruta requiere la cabecera X-API-Key.
#   Comprobacion: tests/test_seguridad.py::test_openapi_documenta_el_401
@router.post(
    "/predict",
    summary="Predecir riesgo de cancelacion",
    responses={503: {"description": "Modelo no disponible"}},
)
def predict(entrada: ReservaEntrada, artefacto: ArtefactoDep) -> PrediccionSalida:
    """Calcula la probabilidad de cancelacion y el nivel de riesgo de una reserva.

    - **200**: prediccion con probabilidad, riesgo (bajo, medio o alto) y version del modelo.
    - **422**: la reserva no cumple el contrato (rangos, canal, campos o capacidad).
    - **503**: el modelo no esta disponible; la peticion puede repetirse mas tarde.
    """
    return predecir(entrada, artefacto)
