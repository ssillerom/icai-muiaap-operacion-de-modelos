"""Comprobaciones automáticas del material del miércoles. Ejecutar: python -m pytest -q"""
import sys
from pathlib import Path
from streamlit.testing.v1 import AppTest

S = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(S))


def test_contador_roto_no_recuerda():
    at = AppTest.from_file(str(S / "01_contador_roto.py")).run()
    for _ in range(3):
        at.button[0].click().run()
    assert at.metric[0].value == "1"


def test_contador_con_estado_y_callback():
    for name, n in (("02_contador_estado.py", 3), ("03_contador_callback.py", 3)):
        at = AppTest.from_file(str(S / name)).run()
        for _ in range(n):
            at.button[0].click().run()
        assert at.metric[0].value == str(n)


def test_app_ejemplo_historial():
    at = AppTest.from_file(str(S / "04_app_ejemplo.py")).run()
    assert not at.exception and len(at.session_state.history) == 0
    sub = next(b for b in at.button if b.label == "Predecir y guardar")
    for _ in range(3):
        sub.click().run()
    at.checkbox[0].check().run()
    assert len(at.session_state.history) == 3 and at.metric[0].value == "3"
    next(b for b in at.button if b.label == "Vaciar historial").click().run()
    assert at.metric[0].value == "0"


def test_starter_arranca_y_esta_incompleto():
    at = AppTest.from_file(str(S / "05_practica_starter.py"))
    at.run()
    assert not at.exception
    assert not hasattr(at.session_state, "history") or "history" not in at.session_state


def test_starter_con_huecos_resueltos_funciona():
    """Aplica la solución A-C al starter y comprueba el comportamiento pedido."""
    code = (S / "05_practica_starter.py").read_text()
    code = code.replace("    pass  # TODO A: asignar [] a st.session_state.history",
                        "    st.session_state.history = []")
    code = code.replace("    pass  # TODO B: añadir {**inputs, **result} a history",
                        "    st.session_state.history.append({**inputs, **result})")
    code = code.replace('st.info("TODO C: dibuja aquí el historial y su contador.")',
                        'h = st.session_state.get("history", [])\n'
                        'st.metric("Predicciones guardadas", len(h))\n'
                        'if h:\n    st.dataframe(h, hide_index=True)')
    assert "TODO" not in code
    at = AppTest.from_string(code).run()
    assert not at.exception
    sub = next(b for b in at.button if b.label == "Predecir y guardar")
    for _ in range(3):
        sub.click().run()
    assert len(at.session_state.history) == 3 and at.metric[0].value == "3"
