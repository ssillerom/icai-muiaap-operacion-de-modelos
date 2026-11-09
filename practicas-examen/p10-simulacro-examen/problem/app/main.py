"""Punto de entrada de la API (HECHO).

Arranque, desde la raiz del proyecto:  uv run uvicorn app.main:app --reload
"""
from fastapi import FastAPI

from app.routers import health, predict

app = FastAPI(
    title="API de riesgo de retraso de envios",
    description="Predice si un envio llegara tarde (datos sinteticos).",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(predict.router)
