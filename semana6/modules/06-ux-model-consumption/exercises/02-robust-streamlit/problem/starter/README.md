# Taller S6 — Interfaz Streamlit operable

Este starter es un snapshot de la primera interfaz de S5. El formulario y el
gateway básico ya están preparados: **no los vuelvas a implementar**. Tu
trabajo es convertir la pantalla que diseñaste en Clase 1 en una app que
mantiene estado, comunica su actividad y responde a fallos sin ocultarlos.

## Arranque

```bash
uv sync --extra app
uv run pytest -q
```

Los tests empiezan en rojo: describen el comportamiento que debes conseguir.
Trabaja en el orden indicado abajo y ejecuta `uv run pytest -q` con frecuencia.
Cuando la lógica esté verde, abre la app:

```bash
uv run streamlit run app.py
```

Los `TODO` del trabajo avanzado están en:

- `src/model_ui/session.py`;
- `src/model_ui/policies.py`;
- `src/model_ui/presentation.py`;
- `src/model_ui/controller.py`;
- `app.py`, para caché y renderizado de estados.

Las pruebas describen las transiciones y los contratos públicos. La app debe
conservar el comportamiento de S5 y añadir estado, reintento, limpieza y
telemetría.

## Orden de implementación

1. **`session.py`** — inicializa con `setdefault`; limpiar vuelve a `idle` y
   borra los valores del último envío, pero no la telemetría.
2. **`policies.py`** — clasifica confianza y latencia con los umbrales del
   diseño. La confianza es una señal de comunicación, no una garantía.
3. **`presentation.py`** — crea un `PredictionView` y traduce excepciones a
   mensajes seguros, con recuperación y `request_id`.
4. **`controller.py`** — emite `loading`, mide latencia, registra solo
   agregados y termina en `success` o `error`.
5. **`app.py`** — cachea el gateway con `st.cache_resource`, guarda el último
   estado y conecta el formulario heredado con el renderizado.

No cambies el contrato de S4, los nombres de las 11 features, `collect_values()`
ni los tests para hacerlos pasar.

## Revisión visual obligatoria

La app no está terminada solo porque los tests estén verdes. En parejas,
comprobad y capturad estos recorridos:

| Recorrido | Debe observarse |
| --- | --- |
| Inicio | Instrucción clara; no hay resultado vacío ni detalle técnico dominante. |
| Éxito | Categoría, confianza y latencia se leen de un vistazo. |
| Rerun | El último resultado sigue visible tras interactuar de nuevo. |
| Error | No aparece traceback; hay explicación, recuperación y `request_id`. |
| Limpiar / reintentar | Limpiar vuelve a `idle` sin borrar telemetría; reintentar reutiliza solo el último envío. |

En `render_state()` utiliza los componentes acordados en Clase 1:

- `st.empty` o un contenedor estable para el estado que cambia;
- `st.status` para el ciclo de la operación;
- tres `st.metric` para categoría, confianza y latencia;
- `st.warning` o `st.info` para interpretar confianza y lentitud;
- `st.expander` para versiones y `request_id`.

No representes confianza con `st.progress`: expresa avance de una tarea, no
certeza del modelo. Tampoco anides columnas o expanders.

## Evidencia de entrega

- `uv run pytest -q` y `uv run ruff check .` verdes;
- captura de `loading`, éxito, error y reintento;
- una frase que explique qué objeto se cachea y por qué no contiene datos de
  una petición;
- una captura o nota que demuestre que la telemetría no incluye las features;
- lista breve de las decisiones que se conservan para sustituir el gateway por
  HTTP en S7.

- Se cachea el modelo y no contiene datos de una petición porque el modelo es un objeto pesado que no cambia entre peticiones, mientras que los datos de una petición son específicos de cada solicitud y no deben ser almacenados en caché.

- Se conservaran las decisiones de la interfaz de usuario, la gestión de estado, la presentación de resultados y la telemetría. Esto permitirá mantener la consistencia en la experiencia del usuario y asegurar que los datos relevantes se recopilen y presenten adecuadamente, incluso cuando se cambie el método de comunicación con el modelo.
