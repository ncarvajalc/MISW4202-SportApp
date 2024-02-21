from flask import request
from flask_restful import Resource


class UserListResource(Resource):
    def get(self):
        return get_users()
