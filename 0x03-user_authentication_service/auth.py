#!/usr/bin/env python3

"""auth module."""

import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash a password."""
    password = "my_password".encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a uuid."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize auth class instance"""
        self._db = DB()

    def register_user(self, email: str = None, password: str = None) -> User:
        """Regiester a user."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str = None, password: str = None) -> bool:
        """validate credentials."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                        password.encode("utf-8"),
                        user.hashed_password)
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str = None) -> str:
        """Returns session id."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_uuid = _generate_uuid()
                self._db.update_user(user_id, session_id=session_uuid)
        except NoResultFound:
            return None
