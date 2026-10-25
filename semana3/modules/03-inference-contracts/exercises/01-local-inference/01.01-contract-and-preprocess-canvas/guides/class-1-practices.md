# Guion docente — Clase 1: conceptos que preparan el taller

**Resultado:** al finalizar, cada pareja puede explicar el camino de una fila
de CSV hasta una predicción y ha decidido el contrato que implementará en la
clase 2. No se programa código de producción en esta sesión.

El docente puede ejecutar el [notebook guiado](../sessions/01-inferencia-contratos/notebooks/01-inferencia-y-contratos-guiada.ipynb)
como hilo conductor de la demo. Las celdas marcadas como “Práctica” se pausan
para que las parejas respondan antes de revelar el resultado.

## Preparación del docente

- Compartir el CSV de muestra y el árbol del *starter*, pero no la carpeta
  `solutions/`.
- Antes de la clase, desde la raíz del repositorio, ejecutar `uv sync` y copiar
  el modelo preentrenado del paquete docente a
  `models/wine_quality_classifier.joblib`. El artefacto no se versiona.
- Ejecutar una vez el comando de la demo con ese artefacto y
  `assets/03-wine-quality/inference_samples.csv`; comprobar que crea cinco
  predicciones antes de proyectarlo.
- Conservar una copia del mismo artefacto para distribuirla al comienzo de la
  clase 2.
- Proyectar la salida correcta de una ejecución, sin mostrar el interior de la
  solución.
- Formar parejas: quien escribe cambia cada bloque de diez minutos.

## Primera hora — Teoría intercalada con microprácticas

| Minutos | Explicación breve | Actividad de las parejas | Evidencia / pregunta de cierre |
| --- | --- | --- | --- |
| 0–10 | Qué se entrega: datos nuevos + modelo entrenado. Entrenar es distinto de inferir. | Subrayan en el CSV qué no debe conocer el modelo: `sample_id`. | “¿Qué entra al vector del modelo y qué solo viaja con la respuesta?” |
| 10–25 | Un contrato protege la frontera: nombres, tipos, rangos y campos extra. | En el [lienzo 01.01](../exercises/01-local-inference/01.01-contract-and-preprocess-canvas/problem/readme.md), completan las columnas de entrada y de salida. | Cada pareja plantea un ejemplo inválido y el error que espera. |
| 25–40 | Preprocesar no es “limpiar donde sea”: es una transformación versionada y ordenada. | Ordenan en tarjetas las 11 columnas y dibujan `CSV → solicitud → vector`. | “¿Qué pasa si `ph` pasa a ser la primera característica?” |
| 40–55 | Artefacto de modelo: estimador, orden de características y versión. | Comparan dos artefactos hipotéticos: uno con 11 campos y otro con 10. Deciden cuál cargarían y por qué. | “¿Qué se debe comprobar antes de `predict`?” |
| 55–60 | Síntesis del flujo que construirán mañana. | Cada pareja formula una regla de diseño para el taller. | Recoger una foto o enlace al lienzo. |

## Segunda hora — Demo participativa, no copia de código

| Minutos | Acción del docente | Acción del alumnado | Punto de control |
| --- | --- | --- | --- |
| 60–70 | Mostrar la estructura del *starter* y los cuatro archivos vacíos: `contracts`, `preprocess`, `inference`, `predict_file`. | Predicen la responsabilidad de cada archivo antes de abrirlo. | Nadie propone leer CSV desde `preprocess.py`. |
| 70–82 | Ejecutar el comando de referencia una vez y mostrar solo el CSV de salida. | Localizan `sample_id`, categoría, confianza y versiones. | Distinguen salida de negocio y metadatos operativos. |
| 82–97 | Trazar verbalmente `red-001`: validación, vector ordenado, modelo, predicción. | Rellenan las flechas del lienzo y señalan dónde fallaría una columna extra. | Pueden nombrar la frontera de cada paso. |
| 97–108 | Mostrar un CSV con `unexpected_field` y ejecutar para obtener el error. | Redactan el mensaje de error útil que esperan. | El error se produce antes de generar salida. |
| 108–120 | Presentar los tests del *starter* como especificación de la API local. | En parejas, leen los nombres de los cinco tests y convierten cada uno en una regla. | Ticket de salida: orden de implementación para mañana. |

## Frases y decisiones de facilitación

- Repetir: “el modelo ya existe; el trabajo es hacerlo consumible y fiable”.
- Si preguntan por exponer el modelo como servicio web, aparcarlo
  explícitamente: en semana 3 solo hay un módulo local y CLI; la exposición
  HTTP llega en la semana prevista en el temario.
- No resolver los `TODO`. La demo enseña el comportamiento y el razonamiento,
  no dicta la implementación.
- Usar el lienzo como prerequisito: una pareja que no lo complete no empieza a
  codificar hasta poder explicar su entrada, vector y salida.

## Salida de la sesión

Cada pareja entrega el lienzo 01.01 y una lista de cuatro responsabilidades:
validar, preprocesar, inferir y orquestar el fichero. Esto será su mapa para el
taller de dos horas.
