from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from database.db import init_db
import logic.user as user_logic
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    print("username", username)
    if not username or not password:
        return "Invalid data", 400

    user = user_logic.get_user_by_username(username)

    if not user:
        return "User not found", 404

    if user["password"] != password:
        return "Invalid password", 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/me", methods=["GET"])
@jwt_required()  # 401 if not authorized
def me():
    current_user = get_jwt_identity()
    return jsonify(username=current_user), 200


init_db()
user_1 = user_logic.get_user_by_username("deportista-bueno")
print("user_1", user_1)
if user_1 is None:
    user_logic.create_user("deportista-bueno", "password1")

user_2 = user_logic.get_user_by_username("deportista-malo")
print("user_2", user_2)
if user_2 is None:
    user_logic.create_user("deportista-malo", "password2")
