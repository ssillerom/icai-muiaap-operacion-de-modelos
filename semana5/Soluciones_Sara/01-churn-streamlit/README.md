# Práctica 5.1 — De una función de churn a una app Streamlit

Duración: **60 minutos**, por parejas. El objetivo es envolver una función de
inferencia ya probada con una interfaz mínima y comprobar una propiedad
operativa importante: editar un formulario no debe ejecutar el modelo.

El caso es sintético y autocontenido. `risk_score` explica una regla fija; **no
es una probabilidad calibrada ni una predicción sobre clientes reales**.

## Resultado esperado

Al terminar, `problem/starter/app.py` debe:

- recoger cuatro valores dentro de un único `st.form("churn_form")`;
- llamar cero veces a `predict()` mientras se editan los widgets;
- llamar una vez después de pulsar **Calcular riesgo**;
- mostrar `label`, `risk_score` y `explanation`;
- transformar un `ValueError` en un mensaje humano sin revelar su detalle.

No modifiques `src/churn_demo/model.py`: es el contrato de inferencia que la
interfaz debe consumir, no reimplementar.

## Material proporcionado

- `src/churn_demo/model.py` y sus seis pruebas, completos;
- `app.py`, con tres huecos observables: formulario, llamada condicionada y
  presentación/error;
- un `FakeStreamlit` que prueba la interfaz sin navegador;
- trece pruebas que actúan como especificación ejecutable;
- una solución docente separada en `../../solutions/01-churn-streamlit/`.

## Cronograma

| Minutos | Trabajo |
|---:|---|
| 0–10 | Leer el contrato y anticipar dos predicciones. |
| 10–25 | Construir el formulario y sus cuatro widgets. |
| 25–35 | Conectar el submit con una única llamada a `predict()`. |
| 35–45 | Presentar el resultado y tratar el error de forma segura. |
| 45–55 | Ejecutar los tests y corregir cada contrato incumplido. |
| 55–60 | Completar el QA manual y tender el puente hacia Wine. |

## Preparación

Desde la raíz del repositorio:

```powershell
cd semana5/modules/05-streamlit-basic-model-ui/exercises/01-churn-streamlit/problem/starter
uv sync
uv run python -m pytest -q
```

El punto de partida correcto es `5 failed, 8 passed`: los fallos corresponden
solo a los tres huecos de `app.py`. Si falla un test del modelo o del fake,
detente antes de implementar la interfaz.

## Recorrido guiado

1. Lee la firma de `predict()` y compara los perfiles `2, 95, 4, False` y
   `36, 35, 0, True`.
2. Completa `collect_profile(st)`. Usa exactamente las cuatro claves indicadas
   en los tests y coloca widgets y botón dentro del formulario.
3. Completa `run_app(st, predictor)`. Si no hay submit, informa y retorna. Si
   lo hay, usa `predictor(**values)` una sola vez.
4. Completa `render_prediction(st, result)` sin recalcular ningún campo.
5. Captura el error esperado y muestra un texto estable; nunca presentes la
   excepción original.
6. Repite tests y estilo hasta obtener trece pruebas verdes.

```powershell
uv run python -m pytest -q
uv run ruff check app.py src tests
uv run ruff format --check app.py src tests
uv run streamlit run app.py
```

## Checklist manual de cuatro casos

| Caso | Acción | Resultado esperado |
|---|---|---|
| 1. Arranque | Abrir la app. | Aparecen título, explicación y un formulario con cuatro widgets. |
| 2. Edición sin envío | Cambiar varios valores sin pulsar el botón. | No se calcula ni se presenta una predicción. |
| 3. Submit válido | Pulsar **Calcular riesgo** con un perfil válido. | Se realiza una llamada y aparecen etiqueta, score y explicación. |
| 4. Resultado actualizado | Cambiar el perfil y volver a enviar. | La salida refleja el nuevo perfil y no conserva el resultado anterior. |

## Entrega y rúbrica

Entrega `app.py`, la salida de `pytest` con trece pruebas verdes y el checklist
manual completado.

| Criterio | Puntos |
|---|---:|
| Formulario único, cuatro widgets y claves correctas | 2 |
| Submit y semántica de cero/una llamada | 2 |
| Separación entre interfaz e inferencia | 2 |
| Presentación completa y error seguro | 2 |
| Tests verdes y QA manual | 2 |
| **Total** | **10** |

La práctica siguiente conserva este patrón y sustituye los cuatro campos de
churn por el contrato Wine Quality y el gateway del bundle de S4.
