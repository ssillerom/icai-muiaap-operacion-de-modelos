# Práctica 02 — Evolucionar la app Streamlit de S5

Esta práctica recibe la primera interfaz de S5 y la refactoriza para soportar
el modelo de ejecución avanzado de Streamlit. El formulario básico no es el
trabajo nuevo: ya está implementado en el snapshot del starter.

## Objetivo

Implementar:

- `st.session_state` inicializado de forma idempotente;
- `st.cache_resource` para el gateway/bundle;
- máquina de estados `idle/loading/success/error`;
- presentación de confianza y latencia;
- errores con código, recuperación y `request_id`;
- retry y clear;
- telemetría sin payloads.

## Punto de partida

El starter conserva de S5:

- `FEATURE_FIELDS`;
- `collect_values()`;
- el `DemoGateway`;
- el adaptador del bundle de S4;
- la presentación mínima del formulario.

El alumno implementa los componentes avVanzados de `session.py`,
`policies.py`, `presentation.py`, `controller.py` y el cableado avanzado de
`app.py`.

## Orden recomendado

1. `session.py`: inicialización y limpieza sin perder telemetría;
2. `policies.py`: límites de confianza y latencia;
3. `presentation.py`: view model y errores accionables;
4. `controller.py`: emitir, medir, validar y registrar;
5. `app.py`: caché, session state, render, retry y clear.

## Comandos

```bash
cd problem/starter
uv sync
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

## Evidencia

- diff que muestre qué código de S5 se conserva;
- resultado que sobrevive a un rerun;
- gateway cargado con `st.cache_resource`;
- estados de carga, éxito y error visibles;
- reintento y limpieza funcionando;
- confianza baja y latencia alta comunicadas correctamente;
- snapshot de telemetría sin valores de las features.
