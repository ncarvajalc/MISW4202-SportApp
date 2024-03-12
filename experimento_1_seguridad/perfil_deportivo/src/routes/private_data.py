from flask import request
from flask_restful import Resource
from logic.private_data import get_private_data


class PrivateDataResource(Resource):
    def get(self, username):
        return get_private_data(request, username)
