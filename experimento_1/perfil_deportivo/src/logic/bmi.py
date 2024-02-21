import os


def calculate_bmi(data):
    if os.environ.get("CORRECT_BMI"):
        weight = data.get("weight")
        height = data.get("height")
        if not weight or not height:
            return "Invalid data", 400
        return weight / (height**2)
    weight = data.get("weight")
    height = data.get("height")
    if not weight or not height:
        return "Invalid data", 400
    return weight / (height**2) * 10000
