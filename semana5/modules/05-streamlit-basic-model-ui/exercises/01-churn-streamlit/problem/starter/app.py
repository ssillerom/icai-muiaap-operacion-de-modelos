"""Starter: conecta una función de inferencia pura con Streamlit."""

from collections.abc import Callable
from typing import Any

from churn_demo.model import ChurnPrediction, predict

Predictor = Callable[..., ChurnPrediction]


def collect_profile(st: Any) -> tuple[bool, dict[str, object]]:
    """Renderiza cuatro widgets dentro de un único formulario."""
    # TODO 1 (alumno): usa st.form("churn_form"), los cuatro widgets con las
    # claves indicadas en el README y st.form_submit_button. El formulario evita
    # inferencias durante cada edición. Compruébalo con el primer test de app.
    with st.form("churn_form"):
        ant = st.slider(
            "Antigüedad",
            min_value=0,
            max_value=120,
            value=12,
            key="tenure_months",
        )
        gasto = st.number_input(
            "Gasto Mensual",
            min_value=0,
            max_value=300,
            value=60,
            key="monthly_spend_eur",
        )
        llamadas = st.slider(
            "Llamadas al soporte",
            min_value=0,
            max_value=20,
            value=1,
            key="support_calls",
        )
        contrato = st.checkbox("Contrato anual", value=False, key="has_annual_contract")
        submit_button = st.form_submit_button("Calcular riesgo")
    values = {
        "tenure_months": ant,
        "monthly_spend_eur": gasto,
        "support_calls": llamadas,
        "has_annual_contract": contrato,
    }
    if not submit_button:
        return False, values
    return True, values


def render_prediction(st: Any, result: ChurnPrediction) -> None:
    """Muestra etiqueta, score orientativo y explicación."""
    # TODO 3 (alumno): presenta label, risk_score y explanation con componentes
    # Streamlit. No recalcules el score. Compruébalo con el test de presentación.
    if result["will_churn"]:
        st.warning(result["label"])
    else:
        st.success(result["label"])
    st.write(f"Score de riesgo: {result['risk_score']:.2f}")
    st.write(f"Explicación: {result['explanation']}")


def run_app(st: Any, predictor: Predictor) -> None:
    """Conecta submit, llamada al predictor y actualización visible."""
    # TODO 2 (alumno): llama a collect_profile, ejecuta predictor(**values) solo
    # tras el submit y una única vez; convierte ValueError en un mensaje seguro.
    # Los tests de 0/1 llamadas y de error verifican este contrato.
    submitted, values = collect_profile(st)
    if submitted:
        try:
            result = predictor(**values)
        except ValueError:
            st.error("No se pudo calcular la predicción")
            return
        render_prediction(st, result)
    else:
        st.info("Por favor, completa el formulario'.")


def main() -> None:
    """Configura la página real y delega el flujo comprobable en run_app."""
    import streamlit as st

    st.set_page_config(page_title="Churn sintético · S5", page_icon="📉")
    st.title("¿Qué cliente podría darse de baja?")
    st.caption("Caso docente sintético; el score no es una probabilidad calibrada.")
    run_app(st, predict)


if __name__ == "__main__":
    main()
