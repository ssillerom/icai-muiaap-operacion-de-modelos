from fastapi import APIRouter, Depends

from app.schemas.chat import ChatEntrada, ChatSalida
from app.services.llm import get_llm
from app.services.orquestador import responder

router = APIRouter()


# TODO: POST /chat (entrada ChatEntrada, salida ChatSalida). Recibe el LLM con Depends(get_llm)
@router.post("/chat", response_model=ChatSalida)
def chat(chat_entrada: ChatEntrada, llm=Depends(get_llm)):
    """Recibe un chat de entrada y devuelve la respuesta del LLM, usando la herramienta si es necesario."""
    return responder(chat_entrada.mensajes, llm)
