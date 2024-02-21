from celery import Celery
from settings import Settings
import os
import requests

settings = Settings()
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

celery_app = Celery(
    __name__,
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
)

SERVICES = {
    "perfil_1": os.environ.get("PERFIL_1") or "http://perfil_1:5000",
    "perfil_2": os.environ.get("PERFIL_2") or "http://perfil_2:5000",
    "perfil_3": os.environ.get("PERFIL_3") or "http://perfil_3:5000",
}


@celery_app.task(name="validate_bmi")
def task(weight, height):
    service_results = {}
    for name, url in SERVICES.items():
        service_results[name] = requests.post(
            f"{url}/calculate_bmi", json={"weight": weight, "height": height}
        ).json()
    return service_results
