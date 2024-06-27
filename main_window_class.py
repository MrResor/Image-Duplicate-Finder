from __init__ import Qtw, Qtc
from db import dbcon
from os import walk
from matplotlib.pyplot import imread
from message_boxes import Work_mode, Progress, ChkBxFileDialog
from threading import Thread


class MainWindow(Qtw.QMainWindow):
    """ Class for displaying main window and it's components.\n

        Attributes:\n

        Methods:\n
    """
    paths = []
    db_open = False
    db_state_changed = Qtc.pyqtSignal(bool) #potem do przycisku xd
    path_to_db = ""
    path_to_search = ""
    deep_search = False

    def __init__(self, parent=None) -> None:
        """ Constructor, changes window name and calls other setup functions.
        """
        super().__init__(parent)
        self.setWindowTitle('Image Duplicate finder')
        self.add_menu()
        # mode = work_mode()
        # choice = mode.run()
        # if choice == 16384:
        #     # load existing database
        #     path = self.get_database_path()
        #     self.db = dbcon(path, True)
        # else:
        #     # create new one
        #     path = self.get_working_path()
        #     self.db = dbcon(path, False)
        # if choice != 16384:
        #     self.filtering(path)
        self.set_ui()
        self.showMaximized()

    def add_menu(self) -> None:
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        action_create = Qtw.QAction('Create', self)
        action_create.setToolTip('Create duplicate database and open it.')
        action_create.setShortcut('Ctrl+N')
        action_create.triggered.connect(self.create_db)
        file_menu.addAction(action_create)

        action_open = Qtw.QAction('Open', self)
        action_open.setToolTip('Open existing duplicate database.')
        action_open.setShortcut('Ctrl+O')
        action_open.triggered.connect(self.get_database_path)
        file_menu.addAction(action_open)
        
        #TODO dodać blokowanie jak nie ma otwartej bazy
        action_close = Qtw.QAction('Close', self)
        action_close.setToolTip('Close opened duplicate database.')
        action_close.triggered.connect(self.get_working_path) #zamykanie bazy
        action_close.setEnabled(self.db_open)
        file_menu.addAction(action_close)

        file_menu.setToolTipsVisible(True)

    def create_db(self) -> None:
        self.get_working_path()
        # tu powinien być progress stworzony i get paths w progresie
        progress = Progress(self.path_to_search, self.deep_search)
        # self.get_paths()
        # db_path = self.path_to_search + "/" + \
        #     self.path_to_search.split("/")[-1] + ".ddb"
        # self.db = dbcon(db_path, False)
        # self.filter_images()

    def get_working_path(self) -> None:
        dialog = ChkBxFileDialog(self, 'Select Directory')
        dialog.run()
        self.deep_search = dialog.chkBx.isChecked()
        self.path_to_search = dialog.selectedUrls()[0].toLocalFile()

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

    def get_database_path(self) -> None:
        file = Qtw.QFileDialog.getOpenFileName(
            self, 'Select Database file.', '', 'Database files (*.db)')[0]
        return file

    def set_ui(self) -> None:
        # TODO CRY
        # main horizontal layout, on the left list with ids and number of how many there are images
        # left smaller vertical layout, on top image preview on bottom links to all instances
        pass
