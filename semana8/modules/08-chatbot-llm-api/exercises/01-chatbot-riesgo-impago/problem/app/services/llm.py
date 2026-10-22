# Clientes de LLM. ESTE FICHERO VIENE HECHO: no hay que tocarlo.
#
# Todos tienen el mismo metodo:  completar(mensajes, herramientas) -> dict
# y devuelven un mensaje del asistente en formato "OpenAI":
#   {"role": "assistant", "content": "texto"}
#   {"role": "assistant", "content": None, "tool_calls": [
#        {"id": "call_1", "type": "function",
#         "function": {"name": "...", "arguments": "{\"edad\": 30}"}}]}
import json
from functools import lru_cache
import os
import re

import litellm


class LLMSimulado:
    """LLM de mentira (sin red, sin cuenta, sin coste). Sirve para desarrollar y para los tests."""

    CAMPOS = {
        "edad": r"edad\D{0,15}?(\d+)",
        "ingresos_mensuales": r"ingresos\D{0,20}?(\d+(?:[.,]\d+)?)",
        "importe_prestamo": r"importe\D{0,20}?(\d+(?:[.,]\d+)?)",
        "plazo_meses": r"plazo\D{0,15}?(\d+)",
        "antiguedad_laboral_anios": r"antig\w+\D{0,25}?(\d+)",
        "impagos_previos": r"impagos\D{0,15}?(\d+)",
    }

    def completar(self, mensajes, herramientas):
        ultimo = mensajes[-1]
        if ultimo["role"] == "tool":
            resultado = json.loads(ultimo["content"])
            if resultado.get("ok"):
                texto = "La probabilidad de impago es {:.1f}%. Decision: {}.".format(
                    resultado["probabilidad_impago"] * 100, resultado["decision"]
                )
            else:
                texto = "No he podido calcularlo: " + str(resultado.get("error"))
            return {"role": "assistant", "content": texto}

        texto_usuario = ""
        for m in mensajes:
            if m["role"] == "user":
                texto_usuario = texto_usuario + " " + m["content"].lower()

        datos = {}
        faltan = []
        for campo, patron in self.CAMPOS.items():
            encontrado = re.search(patron, texto_usuario)
            if encontrado:
                numero = float(encontrado.group(1).replace(",", "."))
                if numero == int(numero):
                    numero = int(numero)
                datos[campo] = numero
            else:
                faltan.append(campo)

        if len(datos) == 0:
            return {
                "role": "assistant",
                "content": "Hola, soy el asistente de riesgo. Dime los datos de la solicitud "
                "(edad, ingresos, importe, plazo, antiguedad e impagos previos).",
            }
        if len(faltan) > 0:
            return {
                "role": "assistant",
                "content": "Me faltan estos datos: " + ", ".join(faltan) + ".",
            }
        return {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": herramientas[0]["function"]["name"], "arguments": json.dumps(datos)},
                }
            ],
        }


class LLMGuionado:
    """Devuelve, uno a uno, los mensajes que le des. Para probar casos concretos en los tests."""

    def __init__(self, mensajes):
        self.mensajes = list(mensajes)
        self.llamadas = 0

    def completar(self, mensajes, herramientas):
        mensaje = self.mensajes[self.llamadas]
        self.llamadas = self.llamadas + 1
        return mensaje


class LLMLiteLLM:
    """Cliente basado en LiteLLM: una sola libreria para hablar con OpenAI, Azure, Ollama, etc.

    El nombre del modelo lleva el proveedor delante: "azure/<tu-deployment>", "ollama/qwen2.5:7b"...
    """

    def __init__(self, modelo, **opciones):
        self.modelo = modelo
        self.opciones = opciones

    def completar(self, mensajes, herramientas):
        respuesta = litellm.completion(
            model=self.modelo, messages=mensajes, tools=herramientas, **self.opciones
        )
        mensaje = respuesta.choices[0].message
        resultado = {"role": "assistant", "content": mensaje.content}
        if mensaje.tool_calls:
            llamadas = []
            for llamada in mensaje.tool_calls:
                llamadas.append(
                    {
                        "id": llamada.id,
                        "type": "function",
                        "function": {
                            "name": llamada.function.name,
                            "arguments": llamada.function.arguments,
                        },
                    }
                )
            resultado["tool_calls"] = llamadas
        return resultado


def crear_llm():
    """Si existe la variable LLM_MODEL usa LiteLLM con ese modelo; si no, el LLM simulado.

    Ejemplo con Azure OpenAI (LiteLLM lee estas variables solo):
        LLM_MODEL=azure/<nombre-del-deployment>
        AZURE_API_KEY, AZURE_API_BASE, AZURE_API_VERSION
    """
    modelo = os.environ.get("LLM_MODEL")
    if modelo:
        return LLMLiteLLM(modelo)
    return LLMSimulado()


@lru_cache
def get_llm():
    """Dependencia de FastAPI: devuelve el LLM (se crea una sola vez)."""
    return crear_llm()
