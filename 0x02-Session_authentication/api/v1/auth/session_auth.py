#!/usr/bin/env python3

"""Session auth module"""

import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication class.

    validate if everything inherits correctly without overloading
    validate the 'switch' by using environ variables."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id."""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return user_id
