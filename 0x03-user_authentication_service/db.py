#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

try:
    from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
except Exception:
    pass

try:
    from sqlalchemy.exc import InvalidRequestError, NoResultFound
except Exception:
    pass

from typing import TypeVar
from user import Base, User

VALID_ATTRIBUTES = [
        "id", "email", "hashed_password", "session_id", "reset_token"
]


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)  # True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save a user to the database."""
        user_instance = User(email=email, hashed_password=hashed_password)
        self._session.add(user_instance)
        self._session.commit()
        return user_instance

    def find_user_by(self, **kwargs: dict) -> TypeVar("User"):
        """
        Returns the first row found in user table as filtered by kwargs.

        Args:
        **kwargs (dict): Key-value pairs to filter the query

        Returns:
        User: The first row found in the user table
        matching the filter criteria
        """
        try:
            row = self._session.query(User).filter_by(**kwargs).one()
            if row is None:
                raise NoResultFound
            return row
        except InvalidRequestError as invalid_request_error:
            # Handle InvalidRequestError
            raise invalid_request_error
        except NoResultFound as no_result_found:
            # Handle NoResultFound
            raise no_result_found

    def update_user(self, user_id: int, **kwargs: dict):
        """Locates user to update, then update user's attributes
        and commit changes to database."""
        user = self.find_user_by(id=user_id)
        if not user:
            raise NoResultFound
        if not kwargs:
            raise InvalidRequestError
        for key, value in kwargs.items():
            if key not in VALID_ATTRIBUTES:
                raise ValueError
            setattr(user, key, value)
            self._session.commit()
