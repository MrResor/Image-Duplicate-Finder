from __init__ import Qtc
from os import walk
from matplotlib.pyplot import imread

class Get_paths(Qtc.QThread):
    """
    Runs a counter thread.
    """
    direc_done = Qtc.pyqtSignal(str)
    search_done = Qtc.pyqtSignal()

    def __init__(self, _paths, _deep_search) -> None:
        super().__init__()
        self.relevant = []
        self.paths = _paths
        self.deep_search = _deep_search

    def run(self) -> None:
        ext = ('.png', '.jpg', '.jpeg', '.raw', '.tiff', '.JPG')
        for root, _, files in walk(self.paths):
            self.relevant += [root + '/' * (root != './') +
                              x for x in files if x.endswith(ext)]
            self.direc_done.emit(root)
            if not self.deep_search:
                break
        self.search_done.emit()

class Filter_images(Qtc.QThread):
    """
    Runs a counter thread.
    """
    count_changed = Qtc.pyqtSignal(int)
    filtering_done = Qtc.pyqtSignal()

    def __init__(self, paths, db) -> None:
        super().__init__()
        self.paths = paths
        self.db = db

    def run(self) -> None:
        index = 1
        for i, path in enumerate(self.paths):
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
            self.count_changed.emit(i+1)
        self.filtering_done.emit()
