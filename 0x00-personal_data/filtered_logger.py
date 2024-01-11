#!/usr/bin/env python3
"""
This module contains a function
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """This function returns the log message obfuscated"""
    pattern = re.compile(r'(' + '|'.join(fields) + r')=([^;]+)')
    return pattern.sub(r'\1={}'.format(redaction), message)
