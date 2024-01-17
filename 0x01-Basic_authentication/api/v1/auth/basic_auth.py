#!/usr/bin/env python3
""" Basic authentication module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Class BasicAuth
        Basic form of authentication using Base64 encoding.

        Attributes:
            Auth(class): inherit auth class to gather headers and paths.

        Methods:
            extract_base64_authorization_header: return the header string
                if it starts with the word 'Basic '.

            decode_base64_authorization_header: Encode and decode string using
                Base64 and return result.

            extract_user_credentials: Return tuple of passed in string.

            user_object_from_credentials: Return correct user instance
                given request's email and password.

            current_user: Use all methods to authenticate user for request.
    """
    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """ Return Base64 part of auth header for a basic authentication. """
        if auth_header is None or type(auth_header) is not str:
            return None
        return auth_header[6:] if auth_header.startswith('Basic ') else None

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """ Return decoded value of a Base64 string. """
        if b64_auth_header is None or type(b64_auth_header) is not str:
            return None
        try:
            header = b64_auth_header.encode('utf-8')
            header = b64decode(header)
            header = header.decode('utf-8')
            return header
        except BaseException:
            return None

    def extract_user_credentials(self, base64_auth_header: str) -> (str, str):
        """ Return user email and password. """
        if base64_auth_header is None or type(base64_auth_header) is not str \
                or ':' not in base64_auth_header:
            return (None, None)
        return tuple(base64_auth_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) ->\
            TypeVar('User'):
        """ Find and return matching user in list of users. """
        if user_email is None or user_pwd is None or \
                type(user_email) is not str or type(user_pwd) is not str:
            return None

        search = User.search({'email': user_email})

        for user in search:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Process authorization for user. """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        auth_header = self.extract_base64_authorization_header(auth_header)
        auth_header = self.decode_base64_authorization_header(auth_header)
        if not auth_header:
            return None
        user = self.extract_user_credentials(auth_header)

        return self.user_object_from_credentials(user[0], user[1])
