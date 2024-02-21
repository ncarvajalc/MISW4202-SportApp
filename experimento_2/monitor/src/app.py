from flask import Flask, jsonify
from celery import Celery
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="./logs_monitor.log",
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


@celery_app.task(name="ping_services")
def check_services_health(*args):
    pass


@app.route("/start_check")
def start_check():
    task = check_services_health.apply_async(queue=CELERY_QUEUE)
    return jsonify({"task_id": task.id}), 202


@app.route("/task_status/<task_id>")
def task_status(task_id):
    task_result = celery_app.AsyncResult(task_id)
    if task_result.ready():
        res = task_result.get()

        for service, status in res.items():
            if status == "down":
                # Log the error
                logging.error(f"{service} is down!")
                return (
                    jsonify({"status": "incomplete", "result": f"{service} is down!"}),
                    400,
                )

        return jsonify({"status": "complete", "result": res})
    else:
        return jsonify({"status": "pending"}), 202
