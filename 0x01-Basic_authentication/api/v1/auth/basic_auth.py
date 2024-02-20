#!/usr/bin/env python3


"""Basic Auth Module."""


import base64
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Auth class."""

    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """Returns the Base64 part of the Authorization header
        for a Basic Authentication"""
        if (
                authorization_header is None
                or not isinstance(authorization_header, str)
                or not authorization_header.startswith('Basic ')
        ):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """Returns the decoded value of a Base64 string
        base64_authorization_header"""
        if (
                base64_authorization_header is None
                or not isinstance(base64_authorization_header, str)
                or not self.valid_base64(base64_authorization_header)
        ):
            return None
        return base64.b64decode(base64_authorization_header).decode('utf-8')

    @staticmethod
    def valid_base64(header) -> bool:
        """Check if header string is a valid Base64."""
        try:
            decoded = base64.b64decode(header)
            return True
        except Exception:
            return False

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value"""
        if (
                decoded_base64_authorization_header is None
                or not isinstance(decoded_base64_authorization_header, str)
                or ':' not in decoded_base64_authorization_header
        ):
            return None, None
        splitted_string_list = decoded_base64_authorization_header.split(':')
        return splitted_string_list[0], splitted_string_list[1]

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """Returns the User instance based on his email and password."""
        if (
                user_email is None
                or not isinstance(user_email, str)
                or user_pwd is None
                or not isinstance(user_pwd, str)
        ):
            return None
        users = User.search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
