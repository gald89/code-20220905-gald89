import os
import json
import sys

from constants.bmi_units import BMIUnits
from constants.bmi_units import bmi_category, risk_category, bmi_level_to_text, health_risk_to_text
from typing import Callable


class BMICalculator(object):
    def __init__(self):
        self.min_height_m = 0
        self.min_weight_kg = 0

        self.max_height_m = sys.float_info.max
        self.max_weight_kg = sys.float_info.max

    @staticmethod
    def _bmi_formula() -> Callable[[float, float], float]:
        fn = lambda mass_kg, height_m: mass_kg/height_m**2
        return fn

    def calculate(self, mass_kg: float, height: float, in_cm=True, decimal_places=2) -> float:
        if in_cm:
            height_m = height / 100
        else:
            height_m = height

        if height < self.min_height_m:
            return 0
        if mass_kg < self.min_weight_kg:
            return 0

        if height > self.max_height_m:
            return 0
        if mass_kg > self.max_weight_kg:
            return 0

        bmi_index = self._bmi_formula()(mass_kg, height_m)
        bmi_index_rounded = round(bmi_index, decimal_places)
        return bmi_index_rounded

    @staticmethod
    def category(bmi: float) -> str:
        estimated_bmi_category = bmi_category(bmi)
        friendly_bmi_category = bmi_level_to_text(estimated_bmi_category)
        return friendly_bmi_category

    @staticmethod
    def health_risk(bmi: float) -> str:
        estimated_risk_category = risk_category(bmi)
        friendly_risk_category = health_risk_to_text(estimated_risk_category)
        return friendly_risk_category


class DataProcessor(object):

    @staticmethod
    def process_data(data_file_src) -> list:
        """Accepts the path to a json file as input and return an updated list with added bmi, category and risk"""
        updated_json_file_data = []
        bmi_calculator = BMICalculator()

        if os.path.exists(data_file_src):
            try:
                with open(data_file_src, 'r') as file:
                    raw_file_data = file.read()
            except FileNotFoundError:
                print(f'Failed to find test data at {data_file_src}')
            else:
                try:
                    json_file_data = json.loads(raw_file_data)
                except json.JSONDecodeError as e:
                    print(f'Failed to decode JSON data in {data_file_src} - {e}')
                except TypeError:
                    print(f'Incorrect JSON file data found in {data_file_src}')
                else:
                    for person_data in json_file_data:
                        if all([key in person_data for key in ['Gender', 'HeightCm', 'WeightKg']]):
                            gender = person_data['Gender']
                            height = person_data['HeightCm']
                            if not type(height) == int:
                                print(f'Warning - unexpected type {type(height)} found for height, should be int')
                                continue
                            weight = person_data['WeightKg']
                            if not type(weight) == int:
                                print(f'Warning - unexpected type {type(height)} found for weight, should be int')
                                continue

                            try:
                                bmi_value = bmi_calculator.calculate(weight, height)
                            except ZeroDivisionError:
                                print(f'Incomplete data found for weight or height.. skipping - {weight} {height}')
                            else:
                                bmi_category = bmi_calculator.category(bmi_value)
                                health_risk = bmi_calculator.health_risk(bmi_value)

                                person_data['BMI'] = bmi_value
                                person_data['BMICategory'] = bmi_category
                                person_data['HealthRisk'] = health_risk
                                updated_json_file_data.append(person_data)
                        else:
                            print(f'Incomplete data found for current record.. skipping - {person_data}')
                            continue

        return updated_json_file_data


if __name__ == '__main__':
    data_file_src = 'data/data.json'
    target_group = BMIUnits.OVER_WEIGHT

    processed_data = DataProcessor.process_data(data_file_src)
    overweight_data = [data for data in processed_data if data['BMICategory'] == bmi_level_to_text(target_group)]
    print(f'{len(overweight_data)} person(s) are classified as being {bmi_level_to_text(target_group)}')