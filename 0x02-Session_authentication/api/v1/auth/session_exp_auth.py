#!/usr/bin/env python3

"""Module for session expiry authentication."""

import datetime
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Expiry Authentication class."""
    def __init__(self):
        """Instance initialization."""
        session_duration = os.getenv('SESSION_DURATION')
        self.session_duration = int(
                 session_duration) if session_duration else 0
        super().__init__()

    def create_session(self, user_id=None):
        """Overloads the SessionAuth session creation method."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overloads the SessionAuth method."""
        if session_id is None:
            return None
        if not self.user_id_by_session_id.get(session_id):
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']
        created_at = self.user_id_by_session_id[session_id].get('created_at')
        if not created_at:
            return None
        if created_at + datetime.timedelta(
                seconds=self.session_duration
        ) < datetime.datetime.now():
            return None
        return self.user_id_by_session_id[session_id].get('user_id')
