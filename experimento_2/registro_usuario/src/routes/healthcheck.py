from logic.healthcheck import pong
from flask_restful import Resource
import sys
import os
import random
import logging


class HealthcheckResource(Resource):

    def get(self):
        logging.info("Healthcheck started")
        if os.environ.get("STATUS") == "healthy":
            return pong()
        elif os.environ.get("STATUS") == "unhealthy":
            if random.randint(0, 10) in range(0, 5):
                logging.error("Internal Server Error")
                return "Internal Server Error", 500
