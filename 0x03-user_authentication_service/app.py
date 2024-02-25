#!/usr/bin/env python3

"""Flask app module."""
from flask import Flask, jsonify, request, abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """home route."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """register a user."""
    if not request.form:
        abort(401)
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    try:
        user = AUTH.register_user(email, password)
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"}), 200


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login function"""
    if not request.form:
        abort(401)
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    if not AUTH.valid_login(email=email, password=password):
        abort(401)
    session_uuid = AUTH.create_session(email=email)
    if session_uuid:
        out = jsonify({"email": email, "message": "logged in"})
        out.set_cookie('session_id', session_uuid)
        return out, 200
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """logouts out a session."""
    if not request.cookies:
        abort(403)
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            # redirect to get /
            return redirect('/', code=302)
        abort(403)
    except NoResultFound:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """finda a user from the session id cookie and respond with their email."""
    if not request.cookies:
        abort(403)
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        abort(403)
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password() -> str:
    """Generate a reset token to reset a password."""
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError as err:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Updates password after reseting."""
    if not request.form:
        abort(403)
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if not email or not reset_token or not new_password:
        abort(403)
    try:
        user = AUTH._db.find_user_by(email=email)
        if user.reset_token != reset_token:
            abort(403)
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
