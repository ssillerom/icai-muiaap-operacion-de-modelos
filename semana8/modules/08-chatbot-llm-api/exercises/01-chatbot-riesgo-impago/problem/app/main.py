"""Punto de entrada de la API (YA HECHO). Arranque: uvicorn app.main:app --port 8000"""
from fastapi import FastAPI

from app.routers import chat, health, predict

app = FastAPI(title="Practica 8 - Chatbot de riesgo")

app.include_router(health.router)
app.include_router(predict.router)
app.include_router(chat.router)
