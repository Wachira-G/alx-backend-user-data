#!/usr/bin/env python3

"""Authentication module
"""

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
            or path not in excluded_paths
            or len(excluded_paths) == 0
        ):
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
