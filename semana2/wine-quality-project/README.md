# Wine Quality

Este modelo está oensado para entrenar un modelo basado en la base de datos WineQT.csv
En esta práctoca solo se tendrá en cuenta la capacidad de crear un proyecto con con el gestor uv para conseguir un repositorio reproducible en cualquier equipo


## Requisitos
- uv instalado
- Git y terminal Bash

## Instalación

El proceso se basó en los siguientes pasos:
1. Crear una rama dentro de mi repositorio de Git: git switch -c feature/s2-wine-project
2.Crear el nuevo proyecto y añade dependencias para crear la carpeta .venv: uv init --package --vcs none --name wine-quality semana2/wine-quality-project
3.Migrar los files desde la carpeta starter inicial de mi fork a carpetas dentro de mi proyecto.
4.Ajustar las rutas e import tras esta migración de files.
5.Cerra la reproducibilidad
Desde la raíz del fork:



## Estructura

    wine-quality-project/
    ├── data/raw/WineQT.csv        # datos originales, no se modifican
    ├── src/wine_quality/train.py  # entrenamiento
    ├── tests/test_train.py        # prueba del entrenamiento
    ├── pyproject.toml             # dependencias y configuración
    └── uv.lock                    # versiones bloqueadas


## Comprobaciones
    uv run --frozen pytest ##Comprueba que el código funciona (en este caso el entrenamiento)
    uv run --frozen ruff check .##Comprueba que el código está limpio 

Qué valida cada una y qué resultado indica que todo está bien.