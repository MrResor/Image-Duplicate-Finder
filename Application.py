from MainWindow import MainWindow
from __init__ import Qtw, sys


class Application:
    """ Class responsible for PyQt initialization and exiting the program when
        it is finished\n

        Atributes:\n
        app -- holds application, for which we will present windows\n
        win -- holds main window and it's contents\n
    """

    def __init__(self, argv: list) -> None:
        """ Initializer for Application class\n
            takes argv (sys.argv) as parameters, sets up and runs Qt app.
        """
        self.app = Qtw.QApplication(argv)
        self.win = MainWindow()
        self.win.show()
        sys.exit(self.app.exec_())
