"""Starter: conecta una función de inferencia pura con Streamlit."""

from collections.abc import Callable
from typing import Any

from churn_demo.model import ChurnPrediction, predict

Predictor = Callable[..., ChurnPrediction]


def collect_profile(st: Any) -> tuple[bool, dict[str, object]]:
    """Renderiza cuatro widgets dentro de un único formulario."""
        # TODO 1 (alumno): usa st.form("churn_form"), los cuatro widgets con las
    # claves indicadas en el README y st.form_submit_button. El formulario evita
    # inferencias durante cada edición. Compruébalo con el primer test de app
    with st.form("churn_form"):
        antiguedad=st.slider("Antigüedad", min_value=0, max_value=120, value=12, key="tenure_months")
        gasto_mensual=st.number_input("Gasto mensual", min_value=0, max_value=300, value=60, key="monthly_spend_eur")
        llamadas_sporte=st.slider("Llamadas soporte técnico", min_value=0, max_value=20, value=1, key="support_calls")
        contrato_anual=st.checkbox("Contrato anual", value=False, key="has_annual_contract")
        enviado=st.form_submit_button("Calcular riesgo")

    valores={"tenure_months":antiguedad, "monthly_spend_eur":gasto_mensual, "support_calls":llamadas_sporte, "has_annual_contract":contrato_anual}

    return enviado, valores
    


def render_prediction(st: Any, result: ChurnPrediction) -> None:
    """Muestra etiqueta, score orientativo y explicación."""
    st.write("Predicción:")
    if result["will_churn"]:
        st.warning(result["label"])
    else:
        st.success(result["label"])
    st.write(f"Score de riesgo orientativo: {result['risk_score']:.2f}")
    st.write(result["explanation"])
    
    # TODO 3 (alumno): presenta label, risk_score y explanation con componentes
    # Streamlit. No recalcules el score. Compruébalo con el test de presentación.
   


def run_app(st: Any, predictor: Predictor) -> None:
    """Conecta submit, llamada al predictor y actualización visible."""
    # TODO 2 (alumno): llama a collect_profile, ejecuta predictor(**values) solo
    # tras el submit y una única vez; convierte ValueError en un mensaje seguro.
    # Los tests de 0/1 llamadas y de error verifican este contrato.
    enviado, valores=collect_profile(st)
    if not enviado:
        return
    try:
        prediccion=predictor(**valores)
        render_prediction(st, prediccion)
    except ValueError:
        st.error("No se pudo calcular el riesgo con esos datos." \
        " Revisa los valores introducidos.")
        return
    

    


def main() -> None:
    """Configura la página real y delega el flujo comprobable en run_app."""
    import streamlit as st

    st.set_page_config(page_title="Churn sintético · S5", page_icon="📉")
    st.title("¿Qué cliente podría darse de baja?")
    st.caption("Caso docente sintético; el score no es una probabilidad calibrada.")
    run_app(st, predict)


if __name__ == "__main__":
    main()
