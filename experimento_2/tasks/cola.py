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
    "registro_usuario_1": os.environ.get("REGISTRO_USUARIO_1")
    or "http://registro_usuario_1:5000",
    "registro_usuario_2": os.environ.get("REGISTRO_USUARIO_2")
    or "http://registro_usuario_2:5000",
    "registro_usuario_3": os.environ.get("REGISTRO_USUARIO_3")
    or "http://registro_usuario_3:5000",
}


@celery_app.task(name="ping_services")
def ping_services():
    service_statuses = {}
    for name, url in SERVICES.items():
        try:
            response = requests.get(url + "/ping")
            if response.status_code == 200:
                print(f"{name} is up!")
                service_statuses[name] = "up"
            else:
                print(f"{name} is down! Status Code: {response.status_code}")
                service_statuses[name] = "down"
        except requests.exceptions.RequestException as e:
            print(f"{name} is down! Exception: {e}")
            service_statuses[name] = "down"
        except Exception as e:
            print(f"{name} is down! Exception: {e}")
            service_statuses[name] = "down"
    return service_statuses
