from enum import Enum
from constants.exceptions import BMIValueError, HealthRiskValueError
from typing import Type, Union


class BMIUnits(Enum):
    UNDERWEIGHT = 0
    NORMAL_WEIGHT = 1
    OVER_WEIGHT = 2
    MODERATELY_OBESE = 3
    SEVERELY_OBESE = 4
    VERY_SEVERELY_OBESE = 5


class HealthRisk(Enum):
    MALNUTRITION = 0
    LOW = 1
    ENHANCED = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


def bmi_level_to_text(units: BMIUnits) -> str:

    if units == BMIUnits.UNDERWEIGHT:
        return 'Underweight'
    elif units == BMIUnits.NORMAL_WEIGHT:
        return 'Normal weight'
    elif units == BMIUnits.OVER_WEIGHT:
        return 'Overweight'
    elif units == BMIUnits.MODERATELY_OBESE:
        return 'Moderately obese'
    elif units == BMIUnits.SEVERELY_OBESE:
        return 'Severely obese'
    elif units == BMIUnits.VERY_SEVERELY_OBESE:
        return 'Very severely obese'
    else:
        raise BMIValueError('Unknown units: ', units)


def health_risk_to_text(units: HealthRisk) -> str:

    if units == HealthRisk.MALNUTRITION:
        return 'Malnutrition risk'
    elif units == HealthRisk.LOW:
        return 'Low risk'
    elif units == HealthRisk.ENHANCED:
        return 'Enhanced risk'
    elif units == HealthRisk.MEDIUM:
        return 'Medium risk'
    elif units == HealthRisk.HIGH:
        return 'High risk'
    elif units == HealthRisk.VERY_HIGH:
        return 'Very high risk'
    else:
        raise HealthRiskValueError('Unknown risk: ', units)


def bmi_category_or_risk(bmi_value: float, units: Type[Union[BMIUnits, HealthRisk]]) -> Union[BMIUnits, HealthRisk]:
    """Slightly adjusted ranges in order to avoid having ambiguous in-between category values"""

    if bmi_value < 18.4:
        return units(0)
    elif 18.4 <= bmi_value < 25.0:
        return units(1)
    elif 25.0 <= bmi_value < 30.0:
        return units(2)
    elif 30.0 <= bmi_value < 35.0:
        return units(3)
    elif 35.0 <= bmi_value < 40.0:
        return units(4)
    elif bmi_value >= 40.0:
        return units(5)


def bmi_category(bmi_value: float) -> BMIUnits:
    return bmi_category_or_risk(bmi_value, BMIUnits)


def risk_category(bmi_value: float) -> HealthRisk:
    return bmi_category_or_risk(bmi_value, HealthRisk)