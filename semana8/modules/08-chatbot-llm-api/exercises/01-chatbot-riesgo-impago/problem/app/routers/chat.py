from fastapi import APIRouter, Depends

from app.schemas.chat import ChatEntrada, ChatSalida
from app.services.llm import get_llm
from app.services.orquestador import responder

router = APIRouter()


@router.post("/chat", response_model=ChatSalida)
def chat(entrada: ChatEntrada, llm=Depends(get_llm)) -> ChatSalida:
    """Recibe la conversacion y devuelve la respuesta del asistente (y la tool usada, si la hubo).

    El LLM llega por Depends(get_llm) para que los tests puedan sustituirlo con dependency_overrides.
    """
    return responder(entrada.mensajes, llm)
