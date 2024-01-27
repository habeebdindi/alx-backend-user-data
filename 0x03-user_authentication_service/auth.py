#!/usr/bin/env python3
""" Auth module
"""

from db import DB
from typing import TypeVar
import bcrypt
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> str:
    """ Return a salted hash of the input password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Return a uuid in string representation """
    return str(uuid4())


class Auth:
    """ Auth class
        Create and handle the authentication database.

        Methods:
            register_user: save a user to the authentication database.
    """

    def __init__(self):
        """ Initialize database """
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ If user doesn't exist in db, add the, and return User object """
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError("User {email} already exists")
        new_user = self._db.add_user(email, _hash_password(password))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if credentials are valid """
        try:
            email = self._db.find_user_by(email=email)
            if email:
                hash_p = _hash_password(password)
                return bcrypt.checkpw(password.encode('utf-8'), hash_p)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ Generate a new UUID and store it in the db as the user's
         session_id """
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=uuid)
            return uuid
        except Exception:
            return None

    def get_user_from_session_id(session_id: str) -> Union[str, None]:
        """ Find user based on session id """
        if not session_id or not self._db.find_user_by(session_id=session_id):
            return None
        else:
            return self._db.find_user_by(session_id=session_id)

    def destroy_session(user_id: int) -> None:
        """ Set session to None """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(email: str) -> str:
        """ Find user corresponding to email """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        uuid = _generate_uuid()
        self._db.update_user(user.id, reset_token=uuid)
        return uuid

    def update_password(reset_token: str, password: str) -> None:
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except Exception:
            raise ValueError
