import litellm

from app.services.llm import LLMLiteLLM, LLMSimulado, crear_llm


def test_cliente_litellm_texto():
    # mock_response: LiteLLM responde sin llamar a ningun servidor
    cliente = LLMLiteLLM("azure/mi-deployment", mock_response="hola")
    mensaje = cliente.completar([{"role": "user", "content": "hola"}], [])
    assert mensaje["role"] == "assistant"
    assert mensaje["content"] == "hola"
    assert "tool_calls" not in mensaje


def test_cliente_litellm_convierte_tool_calls(monkeypatch):
    llamada = litellm.types.utils.ChatCompletionMessageToolCall(
        id="call_9",
        type="function",
        function=litellm.types.utils.Function(name="calcular_riesgo_impago", arguments='{"edad": 30}'),
    )
    mensaje = litellm.types.utils.Message(content=None, role="assistant", tool_calls=[llamada])
    falsa = litellm.types.utils.ModelResponse(choices=[litellm.types.utils.Choices(message=mensaje)])
    monkeypatch.setattr(litellm, "completion", lambda **kwargs: falsa)

    resultado = LLMLiteLLM("azure/x").completar([{"role": "user", "content": "x"}], [])
    assert resultado["tool_calls"][0]["id"] == "call_9"
    assert resultado["tool_calls"][0]["function"]["name"] == "calcular_riesgo_impago"
    assert resultado["tool_calls"][0]["function"]["arguments"] == '{"edad": 30}'


def test_crear_llm_por_defecto_es_simulado(monkeypatch):
    monkeypatch.delenv("LLM_MODEL", raising=False)
    assert isinstance(crear_llm(), LLMSimulado)


def test_crear_llm_con_variable_usa_litellm(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "azure/mi-deployment")
    cliente = crear_llm()
    assert isinstance(cliente, LLMLiteLLM)
    assert cliente.modelo == "azure/mi-deployment"
