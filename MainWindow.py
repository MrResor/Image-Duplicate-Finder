from __init__ import Qtw, Qtc
from Database import Database
from Progress import Progress
from CheckBoxFileDialog import CheckBoxFileDialog


class MainWindow(Qtw.QMainWindow):
    """ Class for displaying main window and it's components.\n

        Attributes:\n

        Methods:\n
    """
    paths = []
    db_state_changed = Qtc.pyqtSignal(bool)  # potem do przycisku xd
    path_to_db = ""
    path_to_search = ""
    deep_search = False

    def __init__(self, parent=None) -> None:
        """ Constructor, changes window name and calls other setup functions.
        """
        super().__init__(parent)
        self.setWindowTitle('Image Duplicate finder')
        self.add_menu()
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

        # TODO dodać blokowanie jak nie ma otwartej bazy
        self.action_close = Qtw.QAction('Close', self)
        self.action_close.setToolTip('Close opened duplicate database.')
        self.action_close.triggered.connect(self.close_db)  # zamykanie bazy
        self.db_state_changed.connect(self.on_db_state_change)
        self.db_state_changed.emit(False)

        file_menu.addAction(self.action_close)

        file_menu.setToolTipsVisible(True)

    def create_db(self) -> None:
        self.get_working_path()
        db_path = self.path_to_search + "/" + \
            self.path_to_search.split("/")[-1] + ".sqlite3db"
        self.db = Database(db_path, False)
        progress = Progress(self.path_to_search, self.deep_search, self.db)
        self.db_state_changed.emit(True)

    def get_working_path(self) -> None:
        dialog = CheckBoxFileDialog(self, 'Select Directory')
        dialog.run()
        self.deep_search = dialog.chkBx.isChecked()
        self.path_to_search = dialog.selectedUrls()[0].toLocalFile()

    def get_database_path(self) -> None:
        file = Qtw.QFileDialog.getOpenFileName(
            self, 'Select Database file.', '', 'Database files (*.sqlite3db)')[0]
        return file

    def set_ui(self) -> None:
        # TODO CRY
        # main horizontal layout, on the left list with ids and number of how many there are images
        # left smaller vertical layout, on top image preview on bottom links to all instances
        pass

    def close_db(self) -> None:
        self.db.close()
        self.db_state_changed.emit(False)

    def on_db_state_change(self, state) -> None:
        self.action_close.setEnabled(state)
