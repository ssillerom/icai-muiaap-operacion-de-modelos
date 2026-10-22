# Módulo 08 - Chatbot con LLM, FastAPI y un modelo

Ejercicio: `exercises/01-chatbot-riesgo-impago/problem/`

Punto de partida del alumnado: proyecto con la estructura estándar de una app
FastAPI (`app/` con `routers`, `schemas`, `services`; `frontend/`; `models/`;
`scripts/`; `tests/`; `pyproject.toml`). Los `TODO` están en cinco ficheros:

- `app/schemas/prestamo.py`
- `app/services/modelo.py`
- `app/services/orquestador.py`
- `app/routers/predict.py`
- `app/routers/chat.py`

El enunciado completo está en
`exercises/01-chatbot-riesgo-impago/problem/ENUNCIADO_ALUMNOS.md` y en el
handout [Assignment 8.2](../../../assignments/semana08_clase02_assignment.pdf).

Comprobación: `uv sync` y `uv run pytest` (con la solución completa, todos los
tests pasan).
