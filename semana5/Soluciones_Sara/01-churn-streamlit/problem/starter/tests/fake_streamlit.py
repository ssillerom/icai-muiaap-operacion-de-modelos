"""Doble mínimo de Streamlit para comprobar el contrato de la práctica."""

from collections.abc import Mapping


class FormContext:
    """Contexto que registra qué formulario contiene cada widget."""

    def __init__(self, owner: "FakeStreamlit", key: str) -> None:
        self.owner = owner
        self.key = key

    def __enter__(self) -> "FormContext":
        if self.owner.active_form is not None:
            raise AssertionError("Solo puede haber un formulario activo")
        self.owner.active_form = self.key
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.owner.active_form = None


class FakeStreamlit:
    """Registra widgets, envíos y salidas sin abrir un navegador."""

    def __init__(
        self,
        *,
        submitted: bool = False,
        values: Mapping[str, object] | None = None,
    ) -> None:
        self.submitted = submitted
        self.values = dict(values or {})
        self.active_form: str | None = None
        self.forms: list[str] = []
        self.widgets: list[tuple[str, str, dict[str, object]]] = []
        self.submit_calls: list[tuple[str, str]] = []
        self.events: list[tuple[object, ...]] = []

    def form(self, key: str) -> FormContext:
        self.forms.append(key)
        return FormContext(self, key)

    def slider(
        self,
        label: str,
        min_value: int,
        max_value: int,
        value: int,
        *,
        key: str,
    ) -> object:
        form_key = self.require_form("slider")
        self.widgets.append(
            (
                "slider",
                label,
                {
                    "min_value": min_value,
                    "max_value": max_value,
                    "value": value,
                    "key": key,
                    "form_key": form_key,
                },
            )
        )
        return self.values.get(key, value)

    def number_input(self, label: str, **kwargs: object) -> object:
        form_key = self.require_form("number_input")
        self.widgets.append(("number_input", label, {**kwargs, "form_key": form_key}))
        key = kwargs["key"]
        if not isinstance(key, str):
            raise AssertionError("number_input necesita una key de texto")
        return self.values.get(key, kwargs["value"])

    def checkbox(self, label: str, *, value: bool, key: str) -> object:
        form_key = self.require_form("checkbox")
        self.widgets.append(
            (
                "checkbox",
                label,
                {"value": value, "key": key, "form_key": form_key},
            )
        )
        return self.values.get(key, value)

    def form_submit_button(self, label: str) -> bool:
        form_key = self.require_form("form_submit_button")
        self.submit_calls.append((label, form_key))
        return self.submitted

    def info(self, value: object) -> None:
        self.events.append(("info", value))

    def error(self, value: object) -> None:
        self.events.append(("error", value))

    def warning(self, value: object) -> None:
        self.events.append(("warning", value))

    def success(self, value: object) -> None:
        self.events.append(("success", value))

    def metric(self, label: str, value: object) -> None:
        self.events.append(("metric", label, value))

    def write(self, value: object) -> None:
        self.events.append(("write", value))

    def require_form(self, component: str) -> str:
        if self.active_form is None:
            raise AssertionError(f"{component} debe estar dentro de st.form")
        return self.active_form

    def output_text(self) -> str:
        return repr(self.events)
