from __init__ import Qtw, Qtc
from db import dbcon
from os import walk
from matplotlib.pyplot import imread
from message_boxes import work_mode, Progress
from threading import Thread
from time import sleep


class MainWindow(Qtw.QMainWindow):
    """ Class for displaying main window and it's components.\n

        Attributes:\n

        Methods:\n
    """
    paths = []

    def __init__(self, parent=None) -> None:
        """ Constructor, changes window name and calls other setup functions.
        """
        super().__init__(parent)
        self.setWindowTitle('Image Duplicate finder.')
        mode = work_mode()
        if mode == 16384:
            # load existing database
            path = self.get_database_path()
            self.db = dbcon(path, True)
        else:
            # create new one
            path = self.get_working_path()
            self.db = dbcon(path, False)
        if mode != 16384:
            self.filtering(path)
        self.set_ui()
        self.showMaximized()

    def get_database_path(self) -> str:
        file = Qtw.QFileDialog.getOpenFileName(
            self, 'Select Database file.', '', 'Database files (*.db)')[0]
        return file

    def get_working_path(self) -> str:
        file = str(Qtw.QFileDialog.getExistingDirectory(
            self, 'Select Directory'))
        return file

    def filtering(self, path) -> None:
        self.get_paths(path)
        self.filter_images()

    def get_paths(self, path) -> list:
        relevant = []
        ext = ('.png', '.jpg', '.jpeg', '.raw', '.tiff', '.JPG')
        for root, _, files in walk(path):
            relevant += [root + '/' * (root != './') +
                         x for x in files if x.endswith(ext)]
        self.paths = relevant
        print("Got paths")

    def filter_images(self) -> None:
        index = 1
        for path in self.paths:
            img1 = imread(path)
            new = True
            similar = self.db.get(img1.shape, path.split('.')[-1])
            for s in similar:
                img2 = imread(s[1])
                if not (img1 - img2).any():
                    self.db.add(s[0], path, img1.shape)
                    new = False
                    break
            if new:
                self.db.add(index, path, img1.shape)
                index += 1
        print("Filtered")

    def set_ui(self) -> None:
        # TODO CRY
        # main horizontal layout, on the left list with ids and number of how many there are images
        # left smaller vertical layout, on top image preview on bottom links to all instances
        Qtw.QLabel("nyan", self)
        print(self.paths)
