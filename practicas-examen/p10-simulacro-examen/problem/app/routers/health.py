"""GET /health (HECHO, publico)."""
from fastapi import APIRouter

router = APIRouter(tags=["salud"])


@router.get("/health")
def health() -> dict[str, str]:
    """Responde {"status": "ok"} si la API esta en marcha."""
    return {"status": "ok"}
