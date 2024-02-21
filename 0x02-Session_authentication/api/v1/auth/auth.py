#!/usr/bin/env python3

"""Authentication module
"""

import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns True if path is not in the list of strings excluded_paths"""
        if path and not path.endswith("/"):
            path = path + "/"
        if (
            excluded_paths is None
            or path is None
            or len(excluded_paths) == 0
        ):
            return True
        asterick_paths = [
                path for path in excluded_paths if path.endswith('*')
        ]
        if asterick_paths:
            # check if path match any of the asterick paths
            for ast_path in asterick_paths:
                if ast_path[:-1] in path[:-1]:
                    return False
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None."""
        if request is None or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns None."""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request."""
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        cookie = request.cookies.get(cookie_name)
        return cookie
