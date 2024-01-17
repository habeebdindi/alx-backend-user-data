#!/usr/bin/env python3
"""Auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Defines the auth class
    """

    def __init__(self):
        """ Initializes the class
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False if route doesnt require auth
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0 \
           or (path not in excluded_paths and
               "{}/".format(path) not in excluded_paths):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns None
        """
        try:
            return request.get("Authorization")
        except:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None
        """
        return None
