# Práctica 5 - Conectar un frontend Streamlit con el backend

Operación de Modelos (MUIAAp) · Comillas ICAI · Repaso de las semanas 4 y 5

Duración orientativa: **45 minutos**.

## Qué vas a construir

El equipo de recepción del hotel quiere usar el modelo sin abrir una terminal.
Ya tienen una interfaz en Streamlit (`frontend/app.py`) hecha por otro equipo.
**No la tienes que programar ni modificar**: tu trabajo es conectarla con el
backend que construiste en las prácticas 1-4.

```
frontend/app.py  ──valores del formulario──>  frontend/gateway.py  ──>  ReservaEntrada  ──>  predecir()
  (HECHO)        <──────── Respuesta ────────       (TU)              (Pydantic, P3)      (artefacto, P4)
```

La pieza que escribes, el **gateway**, decide tres cosas:

1. Si los datos del formulario no cumplen el contrato, **no se llama al modelo**
   y el usuario ve qué campo corregir, con el nombre que aparece en pantalla.
2. Si el modelo no está disponible, el usuario ve un mensaje comprensible,
   **nunca** una traza ni una ruta interna del servidor.
3. Si todo va bien, la interfaz recibe la predicción.

Fíjate en que los widgets de `app.py` permiten valores fuera de rango (por
ejemplo, 0 adultos o 10 niños). Está hecho a propósito: las reglas están en
**un único sitio**, el contrato Pydantic del backend, y la interfaz no las
duplica.

## Material que recibes

El proyecto de la práctica 4 resuelto, más:

```
frontend/app.py        interfaz Streamlit                       (HECHO, no tocar)
frontend/gateway.py    puente con el backend                    (TU)
tests/test_gateway.py  tests del gateway                        (HECHO)
tests/test_app.py      tests de la app completa con AppTest     (HECHO)
```

`streamlit` ya está en las dependencias y `pyproject.toml` añade `frontend/` al
`pythonpath` de pytest para que los tests puedan hacer `import gateway`.

```bash
uv sync
uv run entrenar
uv run pytest        # al empezar: 65 tests en verde y 9 en rojo
```

Lee `frontend/app.py` antes de empezar. Fíjate en qué espera recibir de
`gateway.consultar_modelo()`: un objeto `Respuesta` con `ok`, `prediccion` y
`errores`.

## Qué tienes que hacer

Todo está en `frontend/gateway.py`.

| TODO | Qué hacer | Tests |
|---|---|---|
| 1 | `traducir_errores()`: de `ValidationError` a frases del tipo `"Adultos: Input should be greater than or equal to 1"` | `test_traducir_*` |
| 2 | `consultar_modelo()`: validar → predecir → `Respuesta` | `test_consulta_*`, `test_modelo_no_disponible_*`, `test_app.py` |

Ejemplos de lo que debe devolver `traducir_errores()`:

| Datos | Mensajes |
|---|---|
| `adultos=0` | `["Adultos: Input should be greater than or equal to 1"]` |
| `adultos=4, ninos=4` | `["Reserva: Una habitacion admite como maximo 6 huespedes (adultos + ninos = 8)"]` |

## Cómo probarlo

```bash
uv run pytest
uv run streamlit run frontend/app.py
```

Se abrirá el navegador en `http://localhost:8501`. Prueba estos casos y
comprueba lo que ves:

| Caso | Qué debe aparecer |
|---|---|
| Valores por defecto | Probabilidad, riesgo en color y `Modelo 1.0.0` |
| 0 adultos | Error con la etiqueta `Adultos` |
| 4 adultos y 4 niños | Error `Reserva: Una habitacion admite...` |
| Renombra `models/cancelacion` y vuelve a enviar | Mensaje de modelo no disponible, sin rutas |

> En el último caso tendrás que **reiniciar Streamlit**: el artefacto se
> carga una sola vez (`lru_cache`) y sigue en memoria. Después deja la carpeta
> como estaba.

## Preguntas de repaso (para el examen)

1. ¿Por qué `app.py` no importa nada de `reservas` y solo habla con `gateway`?
   ¿Qué fichero cambiarás cuando el modelo esté detrás de una API?
2. ¿Por qué no se muestra al usuario el texto de la excepción cuando falta el
   modelo? ¿Dónde lo registrarías para poder investigar el fallo?
3. ¿Qué ganas y qué pierdes si repites en los widgets los mismos límites que
   en `ReservaEntrada`?
4. Streamlit vuelve a ejecutar `app.py` entero en cada interacción. ¿Por qué no
   se recarga el modelo cada vez? ¿Qué haría `st.cache_resource` en su lugar?
5. ¿Para qué sirve `st.form`? ¿Qué pasaría sin él cada vez que cambias un
   número?

## Entrega

`uv run pytest` en verde (74 tests) y una captura de la app con una predicción
y otra con un error de validación.
