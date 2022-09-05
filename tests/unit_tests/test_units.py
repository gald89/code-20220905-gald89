from unittest import TestCase
from constants.bmi_units import BMIUnits, bmi_level_to_text, HealthRisk, health_risk_to_text


class TestBMIUnits(TestCase):

    def test_invalid_bmi_text(self):
        with self.assertRaises(ValueError) as context:
            bmi_level_to_text(BMIUnits(6))

    def test_invalid_risk_text(self):
        with self.assertRaises(ValueError) as context:
            health_risk_to_text(HealthRisk(6))