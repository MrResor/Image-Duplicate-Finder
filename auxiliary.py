from __init__ import Qtc
import time
from os import walk

class Get_paths(Qtc.QThread):
    """
    Runs a counter thread.
    """
    direc_done = Qtc.pyqtSignal(str)
    search_done = Qtc.pyqtSignal()
    relevant = []

    def __init__(self, _paths, _deep_search) -> None:
        super().__init__()
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
        