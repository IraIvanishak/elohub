"""User registration and authentication."""

from __future__ import annotations

from app import db
from app.models import User


class UserExistsError(Exception):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"{field} already taken")


def register_user(email: str, username: str, password: str) -> User:
    if User.query.filter_by(email=email).first():
        raise UserExistsError("email")
    if User.query.filter_by(username=username).first():
        raise UserExistsError("username")

    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email: str, password: str) -> User | None:
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
