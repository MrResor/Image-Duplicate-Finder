import matplotlib.pyplot as plt
import argparse
import os
import sqlite3


class dbcon:
    """Class for holding database connection
    """

    def __init__(self, name) -> None:
        self._con = sqlite3.connect(name + "/" * (name != "./") + "local.db")
        self._cur = self._con.cursor()
        self._cur.execute("CREATE TABLE images(id, path, width, height)")
        self._con.commit()

    def add(self, id, path, size) -> None:
        query = (f"INSERT INTO images VALUES "
                 f"({id}, '{path}', {size[1]}, {size[0]})")
        self._cur.execute(query)
        self._con.commit()

    def get(self, size) -> list:
        query = (f"SELECT id, path FROM images WHERE width = {size[1]} "
                 f"AND height = {size[0]}")
        res = self._cur.execute(query)
        return res.fetchall()


def main() -> None:
    args = setup_parser()
    db = dbcon(args.path)
    relevant = get_paths(args.path)
    print("Paths obtained.")
    filter_images(relevant, db)
    print("Done.")


def setup_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='DuplicateImageFinder',
        description='Program checks provided directory for any types of images\
            and compiles a database that will inform of any duplicates.')
    parser.add_argument('path')
    args = parser.parse_args()
    return args


def get_paths(path) -> list:
    relevant = []
    for root, dirs, files in os.walk(path):
        relevant += [root + "/" * (root != "./") +
                     x for x in files if x.endswith((".png", ".jpg"))]
    print(relevant)
    return relevant


def filter_images(paths, db) -> None:
    index = 1
    for path in paths:
        img1 = plt.imread(path)
        new = True
        similar = db.get(img1.shape)
        for s in similar:
            img2 = plt.imread(s[1])
            if not (img1 - img2).any():
                db.add(s[0], path, img1.shape)
                new = False
                break
        if new:
            db.add(index, path, img1.shape)
            index += 1


if __name__ == "__main__":
    main()
