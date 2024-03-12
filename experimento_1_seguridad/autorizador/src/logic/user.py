from models.user import User
from database.db import db_session
from schemas.user import user_schema


def get_user_by_username(username: str):
    user = db_session.query(User).filter(User.username == username).first()
    if user is None:
        return None
    return user_schema.dump(user)


def create_user(username, password):
    new_user = User(username=username, password=password)
    db_session.add(new_user)
    db_session.commit()
    return user_schema.dump(new_user), 201
