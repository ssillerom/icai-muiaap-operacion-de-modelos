"""POST /predict: riesgo de cancelacion de una reserva."""
from fastapi import APIRouter

from app.dependencies import ArtefactoDep
from reservas.inference import predecir
from reservas.schemas import PrediccionSalida, ReservaEntrada

router = APIRouter(tags=["prediccion"])


# TODO 2: documenta la ruta para quien la consuma desde /docs:
#   - summary="Predecir riesgo de cancelacion" en el decorador;
#   - responses={503: {"description": "Modelo no disponible"}} en el decorador
#     (el 422 lo documenta FastAPI solo);
#   - amplia el docstring con una linea por codigo de respuesta: 200, 422 y 503.
#   Comprobacion: tests/test_documentacion.py::test_predict_*
@router.post("/predict")
def predict(entrada: ReservaEntrada, artefacto: ArtefactoDep) -> PrediccionSalida:
    """Calcula la probabilidad de cancelacion y el nivel de riesgo de una reserva."""
    return predecir(entrada, artefacto)
