from fastapi import APIRouter

from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada
from app.services.modelo import predecir

router = APIRouter()


# TODO: POST /predict (entrada PrestamoEntrada, salida PrediccionSalida)
@router.post("/predict", response_model=PrediccionSalida)
def predict(prestamo: PrestamoEntrada):
    """Predice el riesgo de impago de un prestamo."""
    return predecir(prestamo)
