from flask import Flask
import logging
from celery import Celery
from flask import request
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="./logs_voting.log",
)
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
CELERY_QUEUE = os.environ.get("CELERY_QUEUE", "default")

app = Flask(__name__)

celery_app = Celery(
    __name__,
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
)


@celery_app.task(name="validate_bmi")
def get_bmi(*args):
    pass


@app.route("/calculate_bmi", methods=["POST"])
def calculate_bmi():
    data = request.json
    weight = data.get("weight")
    height = data.get("height")
    if not weight or not height:
        return "Invalid data", 400
    task = get_bmi.apply_async((weight, height), queue=CELERY_QUEUE)
    return {"task_id": task.id}, 202


@app.route("/task_status/<task_id>")
def task_status(task_id):
    task_result = celery_app.AsyncResult(task_id)
    if task_result.ready():
        res = task_result.get()
        results_count = {}
        for k, v in res.items():
            results_count[v] = results_count.get(v, [k]) + [k]

        most_common = max(results_count, key=lambda x: len(results_count[x]))
        services = results_count[most_common]
        different_services = [k for k in res.keys() if k not in services]
        logging.error(f"Services {different_services} returned different results")
        return {"bmi": most_common}
    return {"status": "pending"}, 202
