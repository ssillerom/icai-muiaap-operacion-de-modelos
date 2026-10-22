from typing import Literal, Optional

from pydantic import BaseModel, Field


# ---- Contrato del chat con el frontend (YA HECHO, no tocar) ----
class Mensaje(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatEntrada(BaseModel):
    mensajes: list[Mensaje] = Field(min_length=1)


class HerramientaUsada(BaseModel):
    nombre: str
    argumentos: dict
    resultado: dict


class ChatSalida(BaseModel):
    respuesta: str
    herramienta: Optional[HerramientaUsada] = None
