import json

from pydantic import ValidationError

from app.schemas.chat import ChatSalida, HerramientaUsada
from app.schemas.prestamo import PrestamoEntrada
from app.services.modelo import predecir

NOMBRE_TOOL = "calcular_riesgo_impago"
MAX_VUELTAS = 4

SISTEMA = (
    "Eres un asistente de riesgo de un banco. Cuando tengas todos los datos de una solicitud de "
    "prestamo, llama a la herramienta calcular_riesgo_impago. Si falta algun dato, pidelo. "
    "Nunca inventes valores. Responde en espanol y de forma breve."
)


def leer_argumentos(texto):
    """YA HECHO: convierte el texto JSON de la tool en dict ({} si no es JSON valido)."""
    try:
        datos = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    if isinstance(datos, dict):
        return datos
    return {}


# TODO: definir_tool() -> dict con la definicion de la tool, sacando "parameters" de PrestamoEntrada
def definir_tool() -> dict:
    tool_schema = {
        "type": "function",
        "function": {
            "name": NOMBRE_TOOL,
            "description": "Calcula el riesgo de impago de un prestamo, dado un conjunto de datos del solicitante.",
            "parameters": PrestamoEntrada.model_json_schema()
        },
    }
    return tool_schema

# TODO: ejecutar_tool(nombre, argumentos_json) -> dict con "ok" True/False
#       (tool desconocida, JSON roto, datos invalidos o campos inventados -> ok False con el error)
def ejecutar_tool(nombre: str, argumentos_json:str) ->dict:
    if nombre != NOMBRE_TOOL:
        return {"ok": False, "error": "Tool desconocida"}
    argumentos = leer_argumentos(argumentos_json)
    
    try:
        entrada = PrestamoEntrada.model_validate(argumentos)
    except ValidationError as e:
        return {"ok": False, "error": f"Datos invalidos: {e}"}
    
    resultado = predecir(entrada)
    
    return {"ok": True, **resultado.model_dump()}
# TODO: responder(mensajes, llm) -> ChatSalida, con el bucle LLM -> tool -> LLM (maximo MAX_VUELTAS)
def responder(mensajes, llm) -> ChatSalida:
    historial = [{"role": "system", "content": SISTEMA}] 
    for mensaje in mensajes:
        historial.append({"role": mensaje.role, "content": mensaje.content})
    herramienta_usada = None
    for _ in range(MAX_VUELTAS):
        respuesta = llm.completar(historial, [definir_tool()])
        if "tool_calls" not in respuesta:
            return ChatSalida(respuesta=respuesta.get("content") or "", herramienta=herramienta_usada)
        llamada = respuesta["tool_calls"][0]
        nombre = llamada["function"]["name"]
        argumentos_json = llamada["function"]["arguments"]
        argumentos = leer_argumentos(argumentos_json)
        resultado = ejecutar_tool(nombre, argumentos_json)
        herramienta_usada = HerramientaUsada(
            nombre=nombre,
            argumentos=argumentos,
            resultado=resultado,
        )
        historial.extend(
            [
                respuesta,
                {
                    "role": "tool",
                    "tool_call_id": llamada["id"],
                    "content": json.dumps(resultado),
                },
            ]
        )

    return ChatSalida(respuesta="No he podido completar la solicitud.", herramienta=herramienta_usada)
