#!/usr/bin/env python3


"""Basic Auth Module."""


import base64
from api.v1.auth.auth import Auth


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
