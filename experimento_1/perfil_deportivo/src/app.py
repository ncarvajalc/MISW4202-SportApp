from flask import Flask
from flask_restful import Api

from routes.bmi import BMIResource


app = Flask(__name__)
Api = Api(app)


# Routes
Api.add_resource(BMIResource, "/calculate_bmi")
