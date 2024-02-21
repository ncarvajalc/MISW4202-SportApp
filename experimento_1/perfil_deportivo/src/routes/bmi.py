from flask import request
from flask_restful import Resource
from logic.bmi import calculate_bmi


class BMIResource(Resource):
    def post(self):
        return calculate_bmi(request.json)
