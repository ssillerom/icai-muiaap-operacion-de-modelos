# Explicación — Una interfaz fina sobre una función pura

La solución separa tres responsabilidades que cambian por motivos distintos:

```text
widgets dentro de st.form
          ↓ submit
run_app → predict(**values) → ChurnPrediction
          ↓
etiqueta + score + explicación, o error seguro
```

## Por qué `model.py` no vive en `app.py`git ls-tree -r --name-only main -- ':(top)semana4/Soluciones_Sara/'

`predict()` valida entradas, calcula el score y redacta la explicación. Esa
regla ya tiene seis pruebas y puede ser consumida por cualquier interfaz. Si
se copiara dentro de `app.py`, cada cambio tendría que sincronizarse en dos
sitios y dos interfaces podrían responder de forma distinta al mismo perfil.

`app.py` solo traduce interacción humana a argumentos y el resultado a
componentes visuales. `run_app(st, predictor)` recibe ambas dependencias paragit ls-tree -r --name-only main -- ':(top)semana4/Soluciones_Sara/'
que los tests cuenten llamadas reales al predictor sin iniciar un servidor ni
un navegador.

## Por qué usar un formulario

Streamlit vuelve a ejecutar el script cuando cambia un widget. Dentro de
`st.form`, los cambios se agrupan hasta pulsar el botón. Aun así, el código
debe comprobar `submitted`: el formulario agrupa la entrada y el `if` decide
si procede inferir. Juntos garantizan cero llamadas durante la edición y una
llamada por envío.

## Por qué ocultar el detalle del error

Un `ValueError` puede contener nombres de archivos, rutas o información que no
ayuda al usuario. La interfaz muestra un mensaje estable y recuperable; el
detalle técnico no se concatena ni se imprime. En semanas posteriores se podrá
registrar ese detalle en un canal operativo separado.

## Límite deliberado de S5

Esta primera app no conserva resultados entre reruns ni reutiliza recursos.
Tampoco necesita una máquina de estados. Estado de sesión, caché, latencia,
telemetría y una UX de errores más rica pertenecen a S6. Mantener fuera esas
responsabilidades permite ver y probar el contrato esencial:

```text
sin submit → 0 llamadas
con submit → 1 llamada → resultado o mensaje seguro
```

Usa el [cronograma, checklist y rúbrica](../README.md) para completar la
práctica en 60 minutos y preparar la transferencia del mismo patrón a Wine.
