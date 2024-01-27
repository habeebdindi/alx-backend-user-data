#!/usr/bin/env python3
""" Flask app entry point
"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


AUTH = Auth()
app = Flask(__name__)


@app_views.route('/', methods=['GET'])
def greeting() -> str:
    """ Welcome page """
    return jsonify({"message": "Bienvenue"})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ Authenticate user """
    email = request.form.get('email')
    password = request.form('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email}, {"message", "user created"}), 200
    except Exception:
        return jsonify({"message", "email already registered"}), 400


@app_views.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ Login function to respond to the /sessions route """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app_views.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Empty session id and redirect """
    s_id = request.cookies.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(s_id)
        AUTH.destroy_session(user)
        return redirect("/")
    except Exception:
        abort(403)


@app_views.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ Find profile in db """
    s_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(s_id)
        return jsonify({"email", user.email}), 200
    except Exception:
        abort(403)


@app_views.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ Generate a reset password token """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": user.email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app_views.route('/reset_password', methods=["POST"], strict_slashes=False)
def update_password() -> str:
    """ Update password for user endpoint """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password Updated"}), 403
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
