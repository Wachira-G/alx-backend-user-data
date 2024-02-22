#!/usr/bin/env python3

"""Module for session db authentication."""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """sesssion db auth class."""

    def create_session(self, user_id=None):
        "Creates, stores new instance of UserSession and returns session id."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(
                {"user_id": user_id, "session_id": session_id}
        )
        if not user_session:
            return None
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID by requesting UserSession in the database
        based on session_id."""
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """Destroy the UserSession based on Session ID from request cookie."""
        cookie = self.session_cookie(request)
        if cookie:
            user_id = self.user_id_for_session_id(cookie)
            session_id = cookie
            user_session = UserSession.get(session_id)
            if not user_session:
                return False
            del user_session
            cookie_deleted = super().destroy_session(request)
            if not cookie_deleted:
                return False
            return True
        return False
