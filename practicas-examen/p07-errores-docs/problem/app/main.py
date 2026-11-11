"""Punto de entrada de la API.

Arranque, desde la raiz del proyecto:  uv run uvicorn app.main:app --reload
Documentacion interactiva:            http://localhost:8000/docs
"""
from fastapi import FastAPI

from app.routers import health, predict

app = FastAPI(
    title="API de riesgo de cancelacion",
    description="Predice el riesgo de que se cancele una reserva de hotel (datos sinteticos).",
    version="0.7.0",
)

app.include_router(health.router)
app.include_router(predict.router)
