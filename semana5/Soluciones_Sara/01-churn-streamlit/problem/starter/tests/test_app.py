"""Pruebas del formulario, la semántica del submit y la presentación."""

import ast
from pathlib import Path

import pytest
from fake_streamlit import FakeStreamlit

import app

SAMPLE = {
    "tenure_months": 2,
    "monthly_spend_eur": 95.0,
    "support_calls": 4,
    "has_annual_contract": False,
}

PREDICTION = {
    "will_churn": True,
    "label": "Baja probable",
    "risk_score": 0.95,
    "explanation": "Regla docente; umbral 0,50.",
}

RETENTION_PREDICTION = {
    "will_churn": False,
    "label": "Permanencia probable",
    "risk_score": 0.05,
    "explanation": "Regla docente; umbral 0,50.",
}


class RecordingPredictor:
    """Predictor inyectable que permite contar y revisar las llamadas."""

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def __call__(self, **values: object) -> dict[str, object]:
        self.calls.append(dict(values))
        return PREDICTION


def test_collect_profile_uses_one_form_four_widgets_and_one_submit() -> None:
    st = FakeStreamlit(submitted=False)

    submitted, values = app.collect_profile(st)

    assert submitted is False
    assert st.forms == ["churn_form"]
    assert [item[0] for item in st.widgets] == [
        "slider",
        "number_input",
        "slider",
        "checkbox",
    ]
    assert [item[2]["key"] for item in st.widgets] == [
        "tenure_months",
        "monthly_spend_eur",
        "support_calls",
        "has_annual_contract",
    ]
    assert [item[2]["form_key"] for item in st.widgets] == ["churn_form"] * 4
    assert st.widgets[0][2] | {"key": "tenure_months", "form_key": "churn_form"} == {
        "min_value": 0,
        "max_value": 120,
        "value": 12,
        "key": "tenure_months",
        "form_key": "churn_form",
    }
    assert st.widgets[1][2]["min_value"] == 0.0
    assert st.widgets[1][2]["max_value"] == 300.0
    assert st.widgets[1][2]["value"] == 60.0
    assert st.widgets[2][2]["min_value"] == 0
    assert st.widgets[2][2]["max_value"] == 20
    assert st.widgets[2][2]["value"] == 1
    assert st.widgets[3][2]["value"] is False
    assert st.submit_calls == [("Calcular riesgo", "churn_form")]
    assert set(values) == {
        "tenure_months",
        "monthly_spend_eur",
        "support_calls",
        "has_annual_contract",
    }


def test_editing_without_submit_makes_zero_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    st = FakeStreamlit(submitted=False)
    predictor = RecordingPredictor()
    monkeypatch.setattr(app, "collect_profile", lambda _st: (False, SAMPLE))

    app.run_app(st, predictor)

    assert predictor.calls == []


def test_submit_makes_one_call_with_widget_values_and_renders() -> None:
    st = FakeStreamlit(submitted=True, values=SAMPLE)
    predictor = RecordingPredictor()

    app.run_app(st, predictor)

    assert predictor.calls == [SAMPLE]
    assert "Baja probable" in st.output_text()
    assert "0.95" in st.output_text()


def test_predict_error_is_human_and_hides_raw_detail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    st = FakeStreamlit(submitted=True)
    monkeypatch.setattr(app, "collect_profile", lambda _st: (True, SAMPLE))

    def failing_predictor(**_values: object) -> dict[str, object]:
        raise ValueError(r"Traceback C:\secret\customer.csv")

    app.run_app(st, failing_predictor)

    output = st.output_text()
    assert "No se pudo calcular" in output
    assert "Traceback" not in output
    assert "customer.csv" not in output


def test_render_prediction_shows_label_score_and_explanation() -> None:
    risk_st = FakeStreamlit()
    retention_st = FakeStreamlit()

    app.render_prediction(risk_st, PREDICTION)
    app.render_prediction(retention_st, RETENTION_PREDICTION)

    output = risk_st.output_text()
    assert "Baja probable" in output
    assert "0.95" in output
    assert "umbral 0,50" in output
    assert ("warning", "Baja probable") in risk_st.events
    assert ("success", "Permanencia probable") in retention_st.events


def test_fake_rejects_widgets_outside_form() -> None:
    st = FakeStreamlit()

    with pytest.raises(AssertionError, match="dentro de st.form"):
        st.slider("Antigüedad", 0, 120, 12, key="tenure_months")


def test_app_does_not_import_or_access_forbidden_framework_features() -> None:
    tree = ast.parse(Path(app.__file__).read_text(encoding="utf-8"))
    imported_roots: set[str] = set()
    imported_names: set[str] = set()
    attributes: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_roots.add(node.module.split(".")[0])
            imported_names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Attribute):
            attributes.add(node.attr)

    assert "gradio" not in imported_roots
    forbidden_attributes = {"session_state", "cache_data", "cache_resource"}
    assert forbidden_attributes.isdisjoint(imported_names | attributes)
