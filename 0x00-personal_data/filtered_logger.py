#!/usr/bin/env python3
"""This module contains a function"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """This function returns the log message obfuscated"""
    patt = re.compile(r'(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)')
    return re.sub(patt, lambda y: y.group(1) + '=' + redaction
                  if y.group(1) in fields else y.group(0), message)
