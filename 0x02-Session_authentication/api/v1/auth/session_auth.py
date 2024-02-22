#!/usr/bin/env python3

"""Session auth module"""

import uuid
from api.v1.auth.auth import Auth
from models.user import User


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
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID."""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value."""
        cookie = self.session_cookie(request)
        if cookie:
            user_id = self.user_id_for_session_id(cookie)
            user = User.get(user_id)
            return user
        return None

    def destroy_session(self, request=None):
        """Deletes the user session / logout."""
        if request is None:
            return False
        if not self.session_cookie(request):
            return False
        cookie = self.session_cookie(request)
        if cookie:
            user_id = self.user_id_for_session_id(cookie)
            user = User.get(user_id)
            if not user:
                return False
            del self.user_id_by_session_id[cookie]
            return True
        return False
