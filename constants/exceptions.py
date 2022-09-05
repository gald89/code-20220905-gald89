class BMIValueError(ValueError):
    """Raise when an unknown BMI unit value is encountered"""
    def __init__(self, message, input_bmi, *args):
        self.message = message
        self.input_bmi = input_bmi
        super(BMIValueError, self).__init__(message, input_bmi, *args)


class HealthRiskValueError(ValueError):
    """Raise when an unknown Risk value is encountered"""
    def __init__(self, message, input_risk, *args):
        self.message = message
        self.input_risk = input_risk
        super(BMIValueError, self).__init__(message, input_risk, *args)