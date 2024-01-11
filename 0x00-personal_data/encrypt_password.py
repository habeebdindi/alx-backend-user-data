#!/usr/bin/env python3
"""Password encryption module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash and salt input password """
    if password:
        return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check validity of password """
    if hashed_password and password:
        return bcrypt.checkpw(str.encode(password), hashed_password)
