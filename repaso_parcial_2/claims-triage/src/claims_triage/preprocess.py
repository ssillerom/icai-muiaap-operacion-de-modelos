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
    if request.vehicle_age_years is None:
        request.vehicle_age_years = DEFAULT_VEHICLE_AGE

    if request.policy_type == "basico":
        policy_code = 0
    elif request.policy_type == "terceros_ampliado":
        policy_code = 1
    elif request.policy_type == "todo_riesgo":
        policy_code = 2

    return [
        request.driver_age,
        request.vehicle_age_years,
        request.claim_amount_eur,
        request.injuries,
        request.police_report,
        policy_code
    ]
