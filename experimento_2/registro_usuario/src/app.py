from flask import Flask
from database.db import init_db, db_session
from flask_restful import Api

from routes.healthcheck import HealthcheckResource
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="./log.log",
)

app = Flask(__name__)
Api = Api(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Routes
Api.add_resource(HealthcheckResource, "/ping")


init_db()
