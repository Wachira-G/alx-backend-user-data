#!/usr/bin/env python3

"""Session auth module"""

from api.v1.auth.auth import Auth

class SessionAuth(Auth):
    """Session Authentication class.

    validate if everything inherits correctly without overloading
    validate the 'switch' by using environ variables."""

    pass
