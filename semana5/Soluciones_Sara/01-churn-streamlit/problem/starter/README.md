# Starter — Práctica 5.1 Churn con Streamlit

Este proyecto contiene una regla de churn completa y probada. Tu trabajo está
limitado a los tres `TODO` de `app.py`:

1. `collect_profile(st)`: un formulario `churn_form` con cuatro widgets y el
   botón **Calcular riesgo**;
2. `run_app(st, predictor)`: cero llamadas sin submit, una llamada con los
   cuatro valores al enviar y un error seguro si la inferencia los rechaza;
3. `render_prediction(st, result)`: etiqueta, score y explicación.

No edites `model.py` ni copies su regla dentro de `app.py`. La inyección de
`predictor` existe para comprobar el número de llamadas sin levantar Streamlit.

## Arranque

```powershell
uv sync
uv run python -m pytest -q
```

Antes de resolver los huecos debes ver exactamente:

```text
5 failed, 8 passed
```

Después de completarlos:

```powershell
uv run python -m pytest -q
uv run ruff check app.py src tests
uv run ruff format --check app.py src tests
uv run streamlit run app.py
```

La meta es `13 passed` y dos comprobaciones de Ruff sin errores.

## Contrato de widgets

| Valor | Componente | Rango e inicial | `key` |
|---|---|---|---|
| Antigüedad | `st.slider` | 0–120; inicial 12 | `tenure_months` |
| Gasto mensual | `st.number_input` | 0–300; inicial 60 | `monthly_spend_eur` |
| Llamadas a soporte | `st.slider` | 0–20; inicial 1 | `support_calls` |
| Contrato anual | `st.checkbox` | inicial desactivado | `has_annual_contract` |

Hints:

- crea el diccionario dentro de `with st.form("churn_form"):`;
- guarda el booleano que devuelve `st.form_submit_button`;
- retorna pronto cuando ese booleano sea falso;
- llama `predictor(**values)`, no a una copia de la regla;
- ante `ValueError`, muestra un mensaje fijo y no `str(error)`.

No añadas Gradio, estado de sesión ni caché. Esas decisiones se estudiarán en
S6; aquí interesa observar con claridad el rerun, el formulario y la frontera
de inferencia.

El enunciado completo, el cronograma, el checklist de cuatro casos y la rúbrica
están en [`../../README.md`](../../README.md).
