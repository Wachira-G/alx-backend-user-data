#!/usr/bin/env python3

"""Module for user session."""

from models.base import Base


class UserSession(Base):
    """User session class."""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialise user instance."""
        super().__init__(*args, **kwargs)
        self.user_id: string = kwargs.get("user_id")
        self.session_id: string = kwargs.get("session_id")
