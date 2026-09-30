# Solución docente — Lienzo de contrato y preprocesado

La respuesta esperada distingue tres piezas: el CSV histórico se usó para
entrenar, el `.joblib` es el artefacto entregado y
`inference_samples.csv` contiene datos nuevos. El contrato de entrada tiene 11
variables numéricas y prohíbe columnas adicionales. El vector conserva este
orden: acidez fija, acidez volátil, ácido cítrico, azúcar residual, cloruros,
SO₂ libre, SO₂ total, densidad, pH, sulfatos y alcohol.

Los criterios mínimos son: una fila válida genera predicción; una columna extra
detiene el script; y toda salida conserva las versiones de modelo y
preprocesado.
