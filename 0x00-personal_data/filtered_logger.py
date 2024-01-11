#!/usr/bin/env python3
"""This module contains a function"""
import re
from typing import List
import logging
import csv
import os
import mysql.connector
PII_FIELDS = ("name", "email", "phone", "ssn", "ip")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ilter values in incoming log records using filter_datum
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """This function returns the log message obfuscated"""
    patt = re.compile(r'(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)')
    return re.sub(patt, lambda y: y.group(1) + '=' + redaction
                  if y.group(1) in fields else y.group(0), message)

def get_logger() -> logging.Logger:
    """ Takes no arguments and return a logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """Use mysql connector python module to connect to MySQL database"""
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "root"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "localhost"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
    )

def main() -> None:
    """ Read and filter data """
    connection = get_db()
    sql_select_Query = "SELECT * FROM users"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    for row in records:
        message = "name={};email={};phone={};ssn={};password={};ip={};\
            last_login={};user_agent={};"\
            .format(row[0], row[1], row[2], row[3], row[4], row[5],
                    row[6], row[7])
        log_record = logging.LogRecord(
            "my_logger", logging.INFO, None, None, message, None, None)
        formatter = RedactingFormatter(PII_FIELDS)
        formatter.format(log_record)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
