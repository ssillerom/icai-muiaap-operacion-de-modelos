# Wine Quality Project

Pipeline modular para el entrenamiento y evaluación de un clasificador de calidad de vino (`ExtraTreesClassifier`), empaquetado bajo estándares de reproducibilidad estricta con `uv`.

## Estructura del Proyecto

```text
semana2/wine-quality-project/
├── data/
│   └── raw/
│       └── WineQT.csv          # Dataset de entrada inmutable
├── src/
│   └── wine_quality/
│       ├── __init__.py         # Módulo raíz del paquete
│       └── train.py            # Lógica modular de entrenamiento y métricas
├── tests/
│   └── test_train.py           # Suite de pruebas automatizadas
├── pyproject.toml              # Definición declarativa del paquete y dependencias
├── uv.lock                     # Bloqueo criptográfico determinista del entorno
└── README.md                   # Manual operativo de ejecución