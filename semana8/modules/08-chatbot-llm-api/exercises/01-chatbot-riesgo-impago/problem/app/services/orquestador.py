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


def definir_tool():
    """Definicion de la tool en formato OpenAI. "parameters" es el JSON Schema de PrestamoEntrada,
    de modo que la API (/predict) y el LLM comparten un unico contrato."""
    esquema = PrestamoEntrada.model_json_schema()
    esquema.pop("title", None)
    esquema.pop("description", None)
    return {
        "type": "function",
        "function": {
            "name": NOMBRE_TOOL,
            "description": (
                "Calcula la probabilidad de impago de una solicitud de prestamo y devuelve "
                "la decision (aprobar, revisar o rechazar). Usala solo con todos los datos."
            ),
            "parameters": esquema,
        },
    }


def _formatear_errores(error):
    """Convierte un ValidationError en un texto corto que el LLM pueda entender."""
    partes = []
    for detalle in error.errors():
        campo = ".".join(str(parte) for parte in detalle["loc"]) or "entrada"
        partes.append(f"{campo}: {detalle['msg']}")
    return "Datos invalidos -> " + "; ".join(partes)


def ejecutar_tool(nombre, argumentos_json):
    """Ejecuta la tool pedida por el LLM. Nunca lanza excepcion: devuelve siempre {"ok": ...}."""
    if nombre != NOMBRE_TOOL:
        return {"ok": False, "error": f"Herramienta desconocida: {nombre}. Solo existe {NOMBRE_TOOL}."}

    try:
        datos = json.loads(argumentos_json)
    except (json.JSONDecodeError, TypeError):
        return {"ok": False, "error": "Los argumentos no son un JSON valido."}
    if not isinstance(datos, dict):
        return {"ok": False, "error": "Los argumentos deben ser un objeto JSON."}

    try:
        entrada = PrestamoEntrada.model_validate(datos)
    except ValidationError as error:
        return {"ok": False, "error": _formatear_errores(error)}

    try:
        salida = predecir(entrada)
    except Exception as error:  # el modelo no debe tumbar la conversacion
        return {"ok": False, "error": f"Error al ejecutar el modelo: {error}"}

    return {"ok": True, **salida.model_dump()}


def responder(mensajes, llm):
    """Bucle LLM -> tool -> LLM. Como mucho MAX_VUELTAS llamadas al LLM."""
    historial = [{"role": "system", "content": SISTEMA}]
    historial.extend(mensaje.model_dump() for mensaje in mensajes)
    herramientas = [definir_tool()]
    herramienta_usada = None

    for _ in range(MAX_VUELTAS):
        respuesta = llm.completar(historial, herramientas)
        llamadas = respuesta.get("tool_calls") or []

        if not llamadas:
            texto = respuesta.get("content") or "No tengo respuesta, ¿puedes reformular la pregunta?"
            return ChatSalida(respuesta=texto, herramienta=herramienta_usada)

        historial.append(respuesta)
        for llamada in llamadas:
            funcion = llamada.get("function", {})
            nombre = funcion.get("name", "")
            argumentos_json = funcion.get("arguments", "")
            resultado = ejecutar_tool(nombre, argumentos_json)
            herramienta_usada = HerramientaUsada(
                nombre=nombre, argumentos=leer_argumentos(argumentos_json), resultado=resultado
            )
            historial.append(
                {
                    "role": "tool",
                    "tool_call_id": llamada.get("id", ""),
                    "content": json.dumps(resultado),
                }
            )

    return ChatSalida(
        respuesta="No he podido completar el calculo tras varios intentos. "
        "Revisa los datos de la solicitud y vuelve a intentarlo.",
        herramienta=herramienta_usada,
    )
