"""Pruebas del contrato puro y determinista de la demo."""

import unittest
from collections.abc import Callable
from typing import Any


def load_predict() -> Callable[..., dict[str, Any]]:
    """Convierte un módulo todavía ausente en un fallo RED legible."""

    try:
        from churn_demo.model import predict
    except ModuleNotFoundError as error:
        raise AssertionError("Falta implementar churn_demo.model.predict") from error
    return predict


class PredictTests(unittest.TestCase):
    def test_high_risk_profile_has_explainable_capped_score(self) -> None:
        predict = load_predict()
        result = predict(
            tenure_months=2,
            monthly_spend_eur=95.0,
            support_calls=4,
            has_annual_contract=False,
        )

        self.assertEqual(result["label"], "Baja probable")
        self.assertTrue(result["will_churn"])
        self.assertEqual(result["risk_score"], 0.95)
        self.assertIn("antigüedad inferior a 6 meses: +0,30", result["explanation"])
        self.assertIn("umbral de decisión: 0,50", result["explanation"])

    def test_low_risk_profile_has_explainable_floor_score(self) -> None:
        predict = load_predict()
        result = predict(
            tenure_months=36,
            monthly_spend_eur=35.0,
            support_calls=0,
            has_annual_contract=True,
        )

        self.assertEqual(result["label"], "Permanencia probable")
        self.assertFalse(result["will_churn"])
        self.assertEqual(result["risk_score"], 0.05)
        self.assertIn("contrato anual: -0,25", result["explanation"])

    def test_integer_valued_slider_numbers_are_accepted(self) -> None:
        predict = load_predict()
        result = predict(12.0, 60.0, 1.0, False)

        self.assertEqual(result["risk_score"], 0.45)
        self.assertEqual(
            set(result),
            {"will_churn", "label", "risk_score", "explanation"},
        )

    def test_non_integer_tenure_is_rejected(self) -> None:
        predict = load_predict()
        with self.assertRaisesRegex(ValueError, "tenure_months"):
            predict(2.5, 60.0, 1, False)

    def test_out_of_range_monthly_spend_is_rejected(self) -> None:
        predict = load_predict()
        with self.assertRaisesRegex(ValueError, "monthly_spend_eur"):
            predict(12, 301.0, 1, False)

    def test_contract_flag_must_be_boolean(self) -> None:
        predict = load_predict()
        with self.assertRaisesRegex(ValueError, "has_annual_contract"):
            predict(12, 60.0, 1, "no")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
