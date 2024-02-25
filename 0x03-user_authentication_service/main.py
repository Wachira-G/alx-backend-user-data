#!/usr/bin/env python3

import requests
from flask import request
from app import app, AUTH
"""Test module that has function for each of the following tasks.

Use the requests module to query the web server
for the corresponding end-point.
Use assert to validate the response’s expected status code
and payload (if any) for each task."""


# register user funct
def register_user(email: str, password: str) -> None:
    """tests the user registration functionality of our app"""
    url = 'http://localhost:5000/users'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)

    # balidate response status code
    assert response.status_code == 200, f'\
            unexpected status code: {response.status_code}'

    # validate response payload
    payload = response.json()
    assert payload.get('email') == email, f"\
            unexpected email in response: {payload.get('email')}"

    assert payload.get('message') == 'user created', f"\
            unexpected message in response: {payload.get('message')}"

    # validate second request
    response = requests.post(url, data=data)
    assert response.status_code == 400, f'\
            unexpected status code: {response.status_code}'
    payload = response.json()
    assert payload.get('message') == "email already registered", f"\
            unexpected message in response: {payload.get('message')}"


# test log in with wrong password
def log_in_wrong_password(email: str, password: str) -> None:
    """Test the functionality of the log in with wrong password
    """
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)

    # balidate response status code
    assert response.status_code == 401, f'\
            unexpected status code: {response.status_code}'


# test log in
def log_in(email: str, password: str) -> str:
    """
    Test login with valid credentials
    """
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)

    # balidate response status code
    assert response.status_code == 200, f'\
            unexpected status code: {response.status_code}'

    # validate response payload
    payload = response.json()
    assert payload.get('message') == "logged in", f"\
            unexpected message in response: {payload.get('message')}"
    assert response.cookies.get('session_id'), f"\
            session cookie not present"
    session_id = response.cookies.get('session_id')
    return session_id


# test profile unlogged
def profile_unlogged() -> None:
    """
    Test profile fetching while not logged in.
    """
    url = 'http://localhost:5000/profile'
    response = requests.get(url, data=None)

    # balidate response status code
    assert response.status_code == 403, f'\
            unexpected status code: {response.status_code}'


# test profile logged
def profile_logged(session_id: str) -> None:
    """
    Test profile fetching while logged in
    """
    url = 'http://localhost:5000/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)

    # validate response status code
    assert response.status_code == 200, f'\
            unexpected status code: {response.status_code}'

    # validate response payload
    payload = response.json()
    assert payload.get('email') == EMAIL, f'\
            unexpected message in response: {payload.get("message")}'


# test logout
def log_out(session_id: str) -> None:
    """
    Test logout functionality
    """
    url = 'http://localhost:5000/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)

    # validate response status code
    assert response.status_code == 200, f"\
            unexpected status code: {response.status_code}"

    # validate redirection
    # redirected_url = response.headers.get('Location')
    # assert redirected_url == '/', f"unexpected redirection to {
    # redirected_url}"


# test reset password
def reset_password_token(email: str) -> str:
    """Test reset token creation
    """
    url = 'http://localhost:5000/reset_password'
    data = {'email': email}
    response = requests.post(url, data=data)

    # validate response status code
    assert response.status_code == 200, f"\
            unexpected status code: {response.status_code}"

    # validate response payload
    payload = response.json()
    assert payload.get('email') == email, f"\
            unexpected email: {payload.get('email')}"

    assert payload.get('reset_token') is not None, f"\
            unexpected reset token: {payload.get('reset_token')}"


# test update password
def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test password updated after reset
    """
    url = 'http://localhost:5000/reset_password'
    data = {
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password,
    }
    response = requests.put(url, data=data)

    # validate response status code
    assert response.status_code == 200, f"\
            unexpected status code: {response.status_code}"

    # validate response payload
    payload = response.json()
    assert payload.get("message") == "Password updated", f"\
            unexpected response payload message: {payload.get('message')}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
