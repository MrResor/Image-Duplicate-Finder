from __init__ import sys, Qtw, Qtc


class MainWindow(Qtw.QMainWindow):
    """ Class for displaying main window and it's components.\n

        Attributes:\n

        Methods:\n
    """
    countChanged = Qtc.pyqtSignal(int)

    def __init__(self, parent=None) -> None:
        """ Constructor, changes window name and calls other setup functions.
        """
        super().__init__(parent)
        window = Qtw.QWidget()
        self.layout = Qtw.QVBoxLayout()
        self.progress = Qtw.QProgressBar(self)
        self.progress.setMaximum(100)
        self.layout.addWidget(self.progress)

        self.btn1 = Qtw.QPushButton("1", self)
        self.btn1.clicked.connect(lambda: self.countChanged.emit(1))
        self.layout.addWidget(self.btn1)

        self.btn2 = Qtw.QPushButton("50", self)
        self.btn2.clicked.connect(lambda: self.countChanged.emit(50))
        self.layout.addWidget(self.btn2)

        self.btn3 = Qtw.QPushButton("100", self)
        self.btn3.clicked.connect(lambda: self.countChanged.emit(100))
        self.layout.addWidget(self.btn3)

        self.countChanged.connect(self.set)

        window.setLayout(self.layout)
        self.setCentralWidget(window)

    def set(self, value):
        print(value)
        self.progress.setValue(value)


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


if __name__ == '__main__':
    # Run the window
    run = Application(sys.argv)
