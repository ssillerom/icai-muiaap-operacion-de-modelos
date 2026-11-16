from fastapi import APIRouter

from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada
from app.services.modelo import predecir

router = APIRouter()


@router.post("/predict", response_model=PrediccionSalida)
def predict(entrada: PrestamoEntrada) -> PrediccionSalida:
    """Probabilidad de impago y decision para una solicitud. Datos invalidos -> 422."""
    return predecir(entrada)
