from __init__ import sqlite3
from message_boxes import error_message


def check(func):
    ''' Guard for checking if the database file has verif table.
    '''

    def wrapper(self, name) -> None:
        try:
            func(self, name)
        except sqlite3.OperationalError:
            error_message('Provided database was not created by this program.')
            quit(1)

    return wrapper
