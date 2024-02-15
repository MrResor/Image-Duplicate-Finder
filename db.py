from __init__ import sqlite3
from os import path, remove
from decorators import check
from message_boxes import Error_message


class dbcon:
    """Class for holding database connection
    """

    def __init__(self, name, mode) -> None:
        if name == '':
            msg = Error_message('Canceled. Closing program.')
            msg.run()
            quit(2)
        if mode:
            self.connect(name)
        else:
            self.create(name)

    @check
    def connect(self, name) -> None:
        self._con = sqlite3.connect(name, check_same_thread=False)
        self._cur = self._con.cursor()
        self._cur.execute('SELECT * FROM verif')

    def create(self, name) -> None:
        p = name + '/' * (name != './') + 'local.db'
        if path.exists(p):
            remove(p)
        self._con = sqlite3.connect(p, check_same_thread=False)
        self._cur = self._con.cursor()
        self._cur.execute(
            'CREATE TABLE images(id, path, width, height, colour, format)')
        self._cur.execute(
            'CREATE TABLE verif(name)')
        self._con.commit()

    def add(self, id, path, size) -> None:
        if len(size) == 2:
            size += (1,)
        query = (f'INSERT INTO images VALUES '
                 f'({id}, "{path}", {size[1]}, {size[0]}, {size[2]}, '
                 f'"{path.split(".")[-1]}")')
        self._cur.execute(query)
        self._con.commit()

    def get(self, size, format) -> list:
        if len(size) == 2:
            size += (1,)
        query = (f'SELECT id, path FROM images WHERE width = {size[1]} '
                 f'AND height = {size[0]} AND colour = {size[2]} '
                 f'AND format = "{format}"')
        res = self._cur.execute(query)
        return res.fetchall()

    def get_duplicates(self) -> list:
        query = ('SELECT id, path FROM images WHERE id IN (SELECT id FROM '
                 'images GROUP BY id HAVING COUNT(*) > 1) ORDER BY id')
        res = self._cur.execute(query)
        return res.fetchall()

    def get_counts(self) -> list:
        query = ('SELECT id, COUNT(*) FROM images GROUP BY id '
                 'HAVING COUNT(*) > 1')
        res = self._cur.execute(query)
        return res.fetchall()
