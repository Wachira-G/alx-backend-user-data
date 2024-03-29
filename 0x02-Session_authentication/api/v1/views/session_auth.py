#!/usr/bin/env python3

"""Module for session authentication."""

import os
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth_session_login() -> str:
    """auth session login route"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    valid_user = None
    for user in users:
        if user.is_valid_password(password):
            valid_user = user
    if not valid_user:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    # set cookie
    out = jsonify(user.to_json())
    session_name = os.getenv("SESSION_NAME")
    out.set_cookie(session_name, session_id)
    return out


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False
)
def logout() -> str:
    """Auth session logout route."""
    from api.v1.app import auth
    success = auth.destroy_session(request)
    if not success:
        abort(404)
    return jsonify({}), 200
