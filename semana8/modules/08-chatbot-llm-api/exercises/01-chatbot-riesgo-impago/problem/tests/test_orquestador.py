import json

from conftest import CASO_OK
from app.services.llm import LLMGuionado
from app.services.orquestador import NOMBRE_TOOL, definir_tool, ejecutar_tool, responder
from app.schemas.chat import Mensaje
from app.schemas.prestamo import PrestamoEntrada


def llamada(argumentos):
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "id": "call_1",
                "type": "function",
                "function": {"name": NOMBRE_TOOL, "arguments": json.dumps(argumentos)},
            }
        ],
    }


def texto(contenido):
    return {"role": "assistant", "content": contenido}


def test_definir_tool_sale_del_modelo_pydantic():
    tool = definir_tool()
    assert tool["type"] == "function"
    assert tool["function"]["name"] == NOMBRE_TOOL
    propiedades = tool["function"]["parameters"]["properties"]
    assert set(propiedades) == set(PrestamoEntrada.model_fields)


def test_ejecutar_tool_ok():
    resultado = ejecutar_tool(NOMBRE_TOOL, json.dumps(CASO_OK))
    assert resultado["ok"] is True
    assert 0 <= resultado["probabilidad_impago"] <= 1
    assert resultado["decision"] in ("aprobar", "revisar", "rechazar")


def test_ejecutar_tool_datos_invalidos():
    caso = dict(CASO_OK)
    caso["edad"] = 5
    resultado = ejecutar_tool(NOMBRE_TOOL, json.dumps(caso))
    assert resultado["ok"] is False
    assert "edad" in resultado["error"]


def test_ejecutar_tool_campo_inventado():
    caso = dict(CASO_OK)
    caso["saldo_cuenta"] = 100
    resultado = ejecutar_tool(NOMBRE_TOOL, json.dumps(caso))
    assert resultado["ok"] is False
    assert "saldo_cuenta" in resultado["error"]


def test_ejecutar_tool_json_roto_o_tool_desconocida():
    assert ejecutar_tool(NOMBRE_TOOL, "esto no es json")["ok"] is False
    assert ejecutar_tool("borrar_base_de_datos", "{}")["ok"] is False


def test_responder_sin_tool():
    llm = LLMGuionado([texto("Hola, dime los datos.")])
    salida = responder([Mensaje(role="user", content="hola")], llm)
    assert salida.respuesta == "Hola, dime los datos."
    assert salida.herramienta is None


def test_responder_con_tool_pasa_los_argumentos_correctos():
    llm = LLMGuionado([llamada(CASO_OK), texto("Riesgo bajo.")])
    salida = responder([Mensaje(role="user", content="calcula")], llm)
    assert salida.respuesta == "Riesgo bajo."
    assert salida.herramienta.nombre == NOMBRE_TOOL
    assert salida.herramienta.argumentos == CASO_OK
    assert salida.herramienta.resultado["ok"] is True


def test_responder_el_llm_recibe_el_resultado_de_la_tool():
    llm = LLMGuionado([llamada(CASO_OK), texto("ok")])
    visto = []
    original = llm.completar

    def espia(mensajes, herramientas):
        visto.append([m["role"] for m in mensajes])
        return original(mensajes, herramientas)

    llm.completar = espia
    responder([Mensaje(role="user", content="calcula")], llm)
    assert visto[0] == ["system", "user"]
    assert visto[1] == ["system", "user", "assistant", "tool"]


def test_responder_el_llm_inventa_un_campo_y_se_recupera():
    malo = dict(CASO_OK)
    malo["color_favorito"] = "azul"
    llm = LLMGuionado([llamada(malo), llamada(CASO_OK), texto("Ya esta.")])
    salida = responder([Mensaje(role="user", content="calcula")], llm)
    assert salida.respuesta == "Ya esta."
    assert salida.herramienta.resultado["ok"] is True


def test_responder_no_entra_en_bucle_infinito():
    malo = dict(CASO_OK)
    malo["edad"] = 1
    llm = LLMGuionado([llamada(malo)] * 20)
    salida = responder([Mensaje(role="user", content="calcula")], llm)
    assert llm.llamadas <= 10
    assert salida.respuesta != ""
