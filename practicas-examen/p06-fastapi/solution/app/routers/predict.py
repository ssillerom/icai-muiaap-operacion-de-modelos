"""POST /predict: riesgo de cancelacion de una reserva."""
from fastapi import APIRouter

from app.dependencies import ArtefactoDep
from reservas.inference import predecir
from reservas.schemas import PrediccionSalida, ReservaEntrada

router = APIRouter(tags=["prediccion"])


@router.post("/predict")
def predict(entrada: ReservaEntrada, artefacto: ArtefactoDep) -> PrediccionSalida:
    """Calcula la probabilidad de cancelacion y el nivel de riesgo de una reserva.

    FastAPI valida el cuerpo con ReservaEntrada (si no es valido responde 422
    sin llegar a esta funcion) y la respuesta con PrediccionSalida.
    """
    return predecir(entrada, artefacto)
