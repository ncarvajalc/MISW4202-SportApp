from flask import Flask
from flask_restful import Api

from routes.private_data import PrivateDataResource


app = Flask(__name__)
Api = Api(app)


# Routes
Api.add_resource(PrivateDataResource, "/private_data/<string:username>")
