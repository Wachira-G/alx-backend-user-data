#!/usr/bin/env python3

"""auth module."""

import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash a password."""
    binary_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(binary_password, salt)
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
                self._db.update_user(user.id, session_id=session_uuid)
                return session_uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Take a single session_id string argument
        and returns the corresponding User or None."""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            return None
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """destroy a session by updating user session_id to None."""
        if user_id is None:
            return
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound as err:
            print(err)
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Takes an email as argument and returns a a reset token str."""
        if not email:
            raise ValueError
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound as err:
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """updates a users password after reset."""
        if not token or not password:
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=hashed_password
                    reset_token=None
            )
            return
        except NoResultFound as err:
            raise ValueError
