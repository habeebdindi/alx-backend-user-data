#!usr/bin/env python3
"""Auth module for the API
"""
from flask import request


class Auth:
    """ Defines the auth class
    """
    def __init__(self):
        """ Initializes the class
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns None
        """

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None
        """
