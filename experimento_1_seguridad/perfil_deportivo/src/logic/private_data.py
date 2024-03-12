import os
import requests

URL_AUTORIZADOR = os.getenv("URL_AUTORIZADOR")


def get_private_data(request, username):
    if not username:
        return "Invalid data", 400

    response = requests.get(f"{URL_AUTORIZADOR}/me", headers=request.headers)
    if response.status_code == 401:
        return "Unauthorized", 401

    username_response = response.json()["username"]
    if username_response != username:
        return "Forbidden", 403

    return {
        "data": {
            "username": username,
            "height": 180,
            "weight": 80,
            "age": 25,
            "blood_type": "A+",
            "allergies": ["peanuts", "gluten"],
        }
    }
