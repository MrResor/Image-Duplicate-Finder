from __init__ import sqlite3
from message_boxes import Error_message


def check(func):
    ''' Guard for checking if the database file has verif table.
    '''

    def wrapper(self, name) -> None:
        try:
            func(self, name)
        except sqlite3.OperationalError:
            msg = Error_message('Provided database was not created by this program.')
            msg.run()
            quit(1)

    return wrapper
