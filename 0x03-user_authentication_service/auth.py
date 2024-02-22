#!/usr/bin/env python3

"""auth module."""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hash a password."""
    password = "my_password".encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password
