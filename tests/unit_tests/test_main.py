import json
import os
import sys
from bmi import Bmi
from main import BMICalculator, DataProcessor
from constants.bmi_units import BMIUnits, bmi_level_to_text, HealthRisk, health_risk_to_text
from unittest import TestCase


class TestBMICalculator(TestCase):

    def setUp(self) -> None:
        self.bmi_calculator = BMICalculator()

    def test_calculate_bmi_integrity(self):
        """control package rounds to 1 decimal place so the same was done here to facilitate comparison"""

        # test done for typical expected height/weight values
        for height in range(0, 251):
            height = height/100
            for mass in range(0, 635):

                try:
                    calculated_bmi_value = self.bmi_calculator.calculate(mass, height, in_cm=False, decimal_places=1)
                except ZeroDivisionError:
                    calculated_bmi_value = 0

                try:
                    control_bmi_value = Bmi.calculate_bmi(mass, height)
                except ZeroDivisionError:
                    control_bmi_value = 0
                self.assertEqual(calculated_bmi_value, control_bmi_value, msg=f'{calculated_bmi_value} != {control_bmi_value} with mass:{mass} height:{height}')

    def test_calculate_bmi_category_integrity(self):
        # test done for verify correct bmi categorisation

        expected_categories = [{'bmi': 15.0, 'category': BMIUnits.UNDERWEIGHT},
                               {'bmi': 20.0, 'category': BMIUnits.NORMAL_WEIGHT},
                               {'bmi': 25.0, 'category': BMIUnits.OVER_WEIGHT},
                               {'bmi': 30.0, 'category': BMIUnits.MODERATELY_OBESE},
                               {'bmi': 35.0, 'category': BMIUnits.SEVERELY_OBESE},
                               {'bmi': 40.0, 'category': BMIUnits.VERY_SEVERELY_OBESE},
                               {'bmi': 45.0, 'category': BMIUnits.VERY_SEVERELY_OBESE},
                               {'bmi': 50.0, 'category': BMIUnits.VERY_SEVERELY_OBESE},
                               {'bmi': 55.0, 'category': BMIUnits.VERY_SEVERELY_OBESE}]

        for expected_category_dict in expected_categories:
                input_bmi = expected_category_dict['bmi']
                expected_category = bmi_level_to_text(expected_category_dict['category'])

                calculated_category = self.bmi_calculator.category(input_bmi)

                self.assertEqual(calculated_category, expected_category, msg=f'{calculated_category} != {expected_category}')

    def test_calculate_risk_category_integrity(self):
        # test done for verify correct risk categorisation

        expected_categories = [{'bmi': 15.0, 'category': HealthRisk.MALNUTRITION},
                               {'bmi': 20.0, 'category': HealthRisk.LOW},
                               {'bmi': 25.0, 'category': HealthRisk.ENHANCED},
                               {'bmi': 30.0, 'category': HealthRisk.MEDIUM},
                               {'bmi': 35.0, 'category': HealthRisk.HIGH},
                               {'bmi': 40.0, 'category': HealthRisk.VERY_HIGH},
                               {'bmi': 45.0, 'category': HealthRisk.VERY_HIGH},
                               {'bmi': 50.0, 'category': HealthRisk.VERY_HIGH},
                               {'bmi': 55.0, 'category': HealthRisk.VERY_HIGH}]

        for expected_category_dict in expected_categories:
                input_bmi = expected_category_dict['bmi']
                expected_category = health_risk_to_text(expected_category_dict['category'])

                calculated_category = self.bmi_calculator.health_risk(input_bmi)

                self.assertEqual(calculated_category, expected_category, msg=f'{calculated_category} != {expected_category}')

    def test_calculate_bmi_negative_weight(self):
        calculated_bmi_value = self.bmi_calculator.calculate(-75, 175)
        self.assertGreaterEqual(calculated_bmi_value, 0)

    def test_calculate_bmi_negative_height(self):
        calculated_bmi_value = self.bmi_calculator.calculate(75, -175)
        self.assertGreaterEqual(calculated_bmi_value, 0)

    def test_calculate_bmi_huge_weight(self):
        calculated_bmi_value = self.bmi_calculator.calculate(sys.float_info.max*2, 175)
        self.assertEqual(calculated_bmi_value, 0)

    def test_calculate_bmi_huge_mass(self):
        calculated_bmi_value = self.bmi_calculator.calculate(75, sys.float_info.max*2)
        self.assertEqual(calculated_bmi_value, 0)

    def test_bmi_category_lower_bounds(self):
        matches = 0
        category_edge_cases = [{'bmi': 0.0, 'category': BMIUnits.UNDERWEIGHT},
                               {'bmi': 18.5, 'category': BMIUnits.NORMAL_WEIGHT},
                               {'bmi': 25.0, 'category': BMIUnits.OVER_WEIGHT},
                               {'bmi': 30.0, 'category': BMIUnits.MODERATELY_OBESE},
                               {'bmi': 35.0, 'category': BMIUnits.SEVERELY_OBESE},
                               {'bmi': 40.0, 'category': BMIUnits.VERY_SEVERELY_OBESE}]

        for category_edge_case in category_edge_cases:
            bmi_input = category_edge_case['bmi']
            expected_category = category_edge_case['category']
            bmi_category = self.bmi_calculator.category(bmi_input)
            if bmi_category == bmi_level_to_text(expected_category):
                matches += 1
        self.assertEqual(matches, len(category_edge_cases))

    def test_bmi_category_upper_bounds(self):
        matches = 0
        category_edge_cases = [{'bmi': 10.4, 'category': BMIUnits.UNDERWEIGHT},
                               {'bmi': 24.9, 'category': BMIUnits.NORMAL_WEIGHT},
                               {'bmi': 29.9, 'category': BMIUnits.OVER_WEIGHT},
                               {'bmi': 34.9, 'category': BMIUnits.MODERATELY_OBESE},
                               {'bmi': 39.9, 'category': BMIUnits.SEVERELY_OBESE},
                               {'bmi': sys.float_info.max, 'category': BMIUnits.VERY_SEVERELY_OBESE}]

        for category_edge_case in category_edge_cases:
            bmi_input = category_edge_case['bmi']
            expected_category = category_edge_case['category']
            bmi_category = self.bmi_calculator.category(bmi_input)
            if bmi_category == bmi_level_to_text(expected_category):
                matches += 1
        self.assertEqual(matches, len(category_edge_cases))

    def test_bmi_category_in_between_bounds(self):
        matches = 0
        category_edge_cases = [{'bmi': 18.39, 'category': BMIUnits.UNDERWEIGHT},
                               {'bmi': 18.45, 'category': BMIUnits.NORMAL_WEIGHT},
                               {'bmi': 29.95, 'category': BMIUnits.OVER_WEIGHT},
                               {'bmi': 34.99, 'category': BMIUnits.MODERATELY_OBESE},
                               {'bmi': 39.99, 'category': BMIUnits.SEVERELY_OBESE},
                               {'bmi': 40.01, 'category': BMIUnits.VERY_SEVERELY_OBESE}]

        for category_edge_case in category_edge_cases:
            bmi_input = category_edge_case['bmi']
            expected_category = category_edge_case['category']
            bmi_category = self.bmi_calculator.category(bmi_input)
            if bmi_category == bmi_level_to_text(expected_category):
                matches += 1
        self.assertEqual(matches, len(category_edge_cases))

    def test_risk_category_lower_bounds(self):
        matches = 0
        category_edge_cases = [{'bmi': 0.0, 'category': HealthRisk.MALNUTRITION},
                               {'bmi': 18.5, 'category': HealthRisk.LOW},
                               {'bmi': 25.0, 'category': HealthRisk.ENHANCED},
                               {'bmi': 30.0, 'category': HealthRisk.MEDIUM},
                               {'bmi': 35.0, 'category': HealthRisk.HIGH},
                               {'bmi': 40.0, 'category': HealthRisk.VERY_HIGH}]

        for category_edge_case in category_edge_cases:
            bmi_input = category_edge_case['bmi']
            expected_category = category_edge_case['category']
            health_risk_category = self.bmi_calculator.health_risk(bmi_input)
            if health_risk_category == health_risk_to_text(expected_category):
                matches += 1
        self.assertEqual(matches, len(category_edge_cases))

    def test_risk_category_upper_bounds(self):
        matches = 0
        category_edge_cases = [{'bmi': 10.4, 'category': HealthRisk.MALNUTRITION},
                               {'bmi': 24.9, 'category': HealthRisk.LOW},
                               {'bmi': 29.9, 'category': HealthRisk.ENHANCED},
                               {'bmi': 34.9, 'category': HealthRisk.MEDIUM},
                               {'bmi': 39.9, 'category': HealthRisk.HIGH},
                               {'bmi': sys.float_info.max, 'category': HealthRisk.VERY_HIGH}]

        for category_edge_case in category_edge_cases:
            bmi_input = category_edge_case['bmi']
            expected_category = category_edge_case['category']
            health_risk_category = self.bmi_calculator.health_risk(bmi_input)
            if health_risk_category == health_risk_to_text(expected_category):
                matches += 1
        self.assertEqual(matches, len(category_edge_cases))

    def test_risk_category_in_between_bounds(self):
        matches = 0
        category_edge_cases = [{'bmi': 18.39, 'category': HealthRisk.MALNUTRITION},
                               {'bmi': 18.45, 'category': HealthRisk.LOW},
                               {'bmi': 29.95, 'category': HealthRisk.ENHANCED},
                               {'bmi': 34.99, 'category': HealthRisk.MEDIUM},
                               {'bmi': 39.99, 'category': HealthRisk.HIGH},
                               {'bmi': 40.01, 'category': HealthRisk.VERY_HIGH}]

        for category_edge_case in category_edge_cases:
            bmi_input = category_edge_case['bmi']
            expected_category = category_edge_case['category']
            health_risk_category = self.bmi_calculator.health_risk(bmi_input)
            if health_risk_category == health_risk_to_text(expected_category):
                matches += 1
        self.assertEqual(matches, len(category_edge_cases))


class TestDataProcessor(TestCase):
    # test various types of json files to ensure program does not crash

    def test_invalid_json(self):
        data_file_src = '../test_data/corrupted.json'
        try:
            DataProcessor.process_data(data_file_src)
        except json.JSONDecodeError:
            self.fail("process_data() raised JSONDecodeError unexpectedly!")
        except TypeError:
            self.fail("process_data() raised TypeError unexpectedly!")

    def test_missing_json(self):
        data_file_src = '../test_data/does_not_exist.json'
        try:
            DataProcessor.process_data(data_file_src)
        except FileNotFoundError:
            self.fail("process_data() raised FileNotFoundError unexpectedly!")

    def test_incomplete_json(self):
        """Program should ignore entries with missing attributes"""
        data_file_src = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'incomplete.json')
        expected_number_of_records = 3
        processed_data = DataProcessor.process_data(data_file_src)
        self.assertEqual(len(processed_data), 3,
                         msg=f'{len(processed_data)} processed records found instead of expected {expected_number_of_records}')

    def test_process_data(self):
        expected_list = [
            {'Gender': 'Male', 'HeightCm': 178, 'WeightKg': 75, 'BMI': 23.67, 'BMICategory': 'Normal weight',
             'HealthRisk': 'Low risk'},
            {'Gender': 'Female', 'HeightCm': 152, 'WeightKg': 55, 'BMI': 23.81, 'BMICategory': 'Normal weight',
             'HealthRisk': 'Low risk'},
            {'Gender': 'Male', 'HeightCm': 196, 'WeightKg': 125, 'BMI': 32.54, 'BMICategory': 'Moderately obese',
             'HealthRisk': 'Medium risk'},
            {'Gender': 'Female', 'HeightCm': 180, 'WeightKg': 62, 'BMI': 19.14, 'BMICategory': 'Normal weight',
             'HealthRisk': 'Low risk'},
            {'Gender': 'Female', 'HeightCm': 158, 'WeightKg': 55, 'BMI': 22.03, 'BMICategory': 'Normal weight',
             'HealthRisk': 'Low risk'},
            {'Gender': 'Female', 'HeightCm': 160, 'WeightKg': 90, 'BMI': 35.16, 'BMICategory': 'Severely obese',
             'HealthRisk': 'High risk'}]

        data_file_src = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'data2.json')
        data_list = DataProcessor.process_data(data_file_src)
        self.assertListEqual(data_list, expected_list)