#!/usr/bin/env python3

"""Flask app module."""
from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
