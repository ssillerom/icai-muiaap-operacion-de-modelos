# UBICACION FINAL (ejercicio 1): src/claims_triage/preprocess.py
"""EJERCICIO 3: preprocesado.

El modelo solo entiende NUMEROS y en un ORDEN concreto. Esta funcion convierte
un siniestro ya validado (un ClaimRequest) en la lista de numeros que espera.
"""

# Orden exacto en el que se entreno el modelo. NO LO CAMBIEIS.
# El modelo no sabe como se llaman las columnas: solo mira la posicion.
FEATURE_NAMES = [
    "driver_age",
    "vehicle_age_years",
    "claim_amount_eur",
    "injuries",
    "police_report",
    "policy_code",
]

# Valor que usamos cuando no se conoce la edad del vehiculo.
DEFAULT_VEHICLE_AGE = 8.0


def preprocess(request):
    """Recibe un ClaimRequest y devuelve la lista de numeros para el modelo.

    Los datos del siniestro estan en sus atributos: request.driver_age,
    request.policy_type, etc.
    """
    # TODO 3.1 (LIMPIEZA): si la edad del vehiculo no esta informada, el modelo
    #   debe recibir DEFAULT_VEHICLE_AGE en su lugar.

    # TODO 3.2 (CATEGORIZACION): el modelo no entiende texto, asi que el tipo
    #   de poliza debe convertirse en un codigo numerico (policy_code):
    #       basico -> 0     terceros_ampliado -> 1     todo_riesgo -> 2

    # TODO 3.3: devolver los valores del siniestro, ya limpios, en el orden
    #   exacto de FEATURE_NAMES. El identificador (claim_id) no es un dato para
    #   el modelo y no debe incluirse.
    raise NotImplementedError("TODO: ejercicio 3")
