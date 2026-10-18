Responsabilidad de cada módulo

-contracts.py: aquí están los dos contratos, hechos con Pydantic. El de entrada (WineQualityRequest) comprueba que cada vino tiene las 11 características, que son números y que están dentro de un rango posible. Si llega un campo de más, lo rechaza. El de salida (WineQualityPrediction) comprueba que la categoría es una de las tres permitidas (acceptable, excellent o needs_review), que la confianza está entre 0 y 1 y que el sample_id y las versiones no están vacías

-preprocess.py: coge un vino que ya está validado y lo convierte en una lista con los 11 números, en el mismo orden con el que se entrenó el modelo (FEATURE_NAMES). También guarda el nombre de la versión del preprocesado. No lee ningún CSV, solo recibe un vino.

-inference.py: carga el archivo .joblib y comprueba que sirve antes de usarlo: que trae el modelo, los nombres de las columnas y la versión, que el modelo tiene predict y predict_proba, y que las columnas son las mismas que las nuestras y en el mismo orden. Después hace la predicción de un vino y devuelve el resultado ya comprobado con el contrato de salida

-predict_file.py: es el comando que se ejecuta. Lee el CSV fila a fila, pasa cada fila por contracts, preprocess e inference, y escribe el CSV de salida. No carga el modelo por su cuenta,lo que hace es usar inference.py. Si algo falla muestra el error y termina con código 2.

Dos decisiones de diseño

1.- Escribir el CSV solo al final: Primero se leen y se predicen todas las filas, y solo cuando todas son válidas se escribe el archivo de salida. Así, si una fila falla, no queda un archivo a medias que parezca bueno

2.- Comprobar el modelo al cargarlo: Antes de predecir se comprueba que las columnas del modelo son las mias y en el mismo orden. Si no lo fueran, el modelo predeciría mal sin avisar, y así falla antes con un mensaje que lo explica
