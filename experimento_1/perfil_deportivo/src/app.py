from flask import Flask
from database.db import init_db, db_session
from flask_restful import Api

from routes.user import UserListResource


app = Flask(__name__)
Api = Api(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Routes
Api.add_resource(UserListResource, "/users")


init_db()
