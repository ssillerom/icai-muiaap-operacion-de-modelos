"""Contrato de inferencia consumido por la interfaz Streamlit de la práctica."""

from math import isfinite
from typing import Literal, TypedDict

ChurnLabel = Literal["Baja probable", "Permanencia probable"]


class ChurnPrediction(TypedDict):
    """Salida pequeña, serializable y comprensible por cualquier interfaz."""

    will_churn: bool
    label: ChurnLabel
    risk_score: float
    explanation: str


def _whole_number(name: str, value: int | float, upper: int) -> int:
    """Normaliza los enteros que un slider puede entregar como `float`."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} debe ser un número entero")
    number = float(value)
    if not isfinite(number) or not number.is_integer():
        raise ValueError(f"{name} debe ser un número entero")
    normalized = int(number)
    if not 0 <= normalized <= upper:
        raise ValueError(f"{name} debe estar entre 0 y {upper}")
    return normalized


def _bounded_number(name: str, value: int | float, upper: float) -> float:
    """Valida un número real finito dentro del rango didáctico."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} debe ser un número")
    normalized = float(value)
    if not isfinite(normalized) or not 0 <= normalized <= upper:
        raise ValueError(f"{name} debe estar entre 0 y {upper:g}")
    return normalized


def predict(
    tenure_months: int | float,
    monthly_spend_eur: int | float,
    support_calls: int | float,
    has_annual_contract: bool,
) -> ChurnPrediction:
    """Aplica una regla sintética reproducible; no es un modelo entrenado."""

    tenure = _whole_number("tenure_months", tenure_months, 120)
    monthly_spend = _bounded_number("monthly_spend_eur", monthly_spend_eur, 300)
    calls = _whole_number("support_calls", support_calls, 20)
    if not isinstance(has_annual_contract, bool):
        raise ValueError("has_annual_contract debe ser booleano")

    score = 0.25
    factors = ["base: +0,25"]

    if tenure < 6:
        score += 0.30
        factors.append("antigüedad inferior a 6 meses: +0,30")
    elif tenure >= 24:
        score -= 0.15
        factors.append("antigüedad de al menos 24 meses: -0,15")
    else:
        factors.append("antigüedad entre 6 y 23 meses: +0,00")

    if monthly_spend >= 80:
        score += 0.20
        factors.append("gasto mensual de al menos 80 €: +0,20")
    elif monthly_spend < 40:
        score -= 0.05
        factors.append("gasto mensual inferior a 40 €: -0,05")
    else:
        factors.append("gasto mensual entre 40 y 79,99 €: +0,00")

    if calls >= 3:
        score += 0.25
        factors.append("tres o más llamadas de soporte: +0,25")
    elif calls >= 1:
        score += 0.10
        factors.append("una o dos llamadas de soporte: +0,10")
    else:
        factors.append("sin llamadas de soporte: +0,00")

    if has_annual_contract:
        score -= 0.25
        factors.append("contrato anual: -0,25")
    else:
        score += 0.10
        factors.append("sin contrato anual: +0,10")

    risk_score = round(min(0.95, max(0.05, score)), 2)
    will_churn = risk_score >= 0.50
    label: ChurnLabel = "Baja probable" if will_churn else "Permanencia probable"
    score_text = f"{risk_score:.2f}".replace(".", ",")
    explanation = (
        "Regla docente: "
        + "; ".join(factors)
        + f". Score acotado: {score_text}; umbral de decisión: 0,50. "
        "No es una probabilidad calibrada."
    )

    return {
        "will_churn": will_churn,
        "label": label,
        "risk_score": risk_score,
        "explanation": explanation,
    }
