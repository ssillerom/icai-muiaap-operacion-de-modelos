def predict_toy(tenure_months, monthly_spend_eur, contract, support_calls):
    """Regla inventada para practicar interfaces. NO es un modelo validado."""
    score = 0.15
    score += 0.25 if tenure_months < 12 else 0.0
    score += 0.20 if monthly_spend_eur > 70 else 0.0
    score += 0.20 if contract == "Mensual" else 0.0
    score += min(support_calls * 0.05, 0.20)
    probability = round(min(score, 0.95), 2)
    return {"probability": probability,
            "risk": "Alto" if probability >= 0.5 else "Bajo"}
