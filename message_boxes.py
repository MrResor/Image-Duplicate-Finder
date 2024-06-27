from __init__ import Qtw, Qtg, Qtc
from auxiliary import Get_paths
import time

class ChkBxFileDialog(Qtw.QFileDialog):
    def __init__(self, chkBxTitle="", filter="") -> None:
        super().__init__(filter=filter)
        self.setOption(Qtw.QFileDialog.DontUseNativeDialog)
        self.setFileMode(Qtw.QFileDialog.FileMode.Directory)
        
        # self.selectNameFilter("*.txt")
        self.chkBx = Qtw.QCheckBox(chkBxTitle)
        self.layout().addWidget(self.chkBx)
        lbl = Qtw.QLabel("Search directories")
        self.layout().addWidget(lbl)

    def run(self):
        return self.exec_()

class Work_mode(Qtw.QMessageBox):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Select working mode.")
        self.setIcon(Qtw.QMessageBox.Question)
        self.setText(
            "Would you like to load existing database created by this program?"
        )
        self.setStandardButtons(Qtw.QMessageBox.Yes | Qtw.QMessageBox.No)
    
    def run(self) -> int:
        return self.exec_()


class Error_message(Qtw.QMessageBox):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.setWindowTitle("Error")
        self.setIcon(Qtw.QMessageBox.Critical)
        self.setText(text)
        self.setStandardButtons(Qtw.QMessageBox.Ok)
    
    def run(self) -> int:
        return self.exec_()


class Progress(Qtw.QDialog):

    def __init__(self, paths, deep_search) -> None:
        super().__init__()
        self.setWindowTitle("Working...")
        self.setFixedSize(400, 200)

        self.ui()

        self.calc = Get_paths(paths, deep_search)
        self.calc.direc_done.connect(self.on_direc_done)
        self.calc.search_done.connect(self.on_search_done)
        self.calc.start()

        self.exec_()

    def ui(self) -> None:
        self.layout = Qtw.QVBoxLayout()

        self.message = Qtw.QTextEdit()
        self.message.setReadOnly(True)
        self.message.append("Searching for images...")
        self.layout.addWidget(self.message)

        self.bar = Qtw.QProgressBar()
        self.bar.setTextVisible(True)
        self.bar.setAlignment(Qtc.Qt.AlignCenter)
        self.layout.addWidget(self.bar)

        self.button = Qtw.QPushButton("Cancel")
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def on_direc_done(self, value) -> None:
        self.message.append(str(value) + " Done!")

    def on_search_done(self) -> None:
        relevant = self.calc.relevant
        iter = len(relevant)
        self.bar.setMaximum(iter)
        self.bar.setFormat('Finding Duplicates %v / ' + str(iter))
        self.calc = External(iter)
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()

    def onCountChanged(self, value) -> None:
        self.bar.setValue(value)


class External(Qtc.QThread):
    """
    Runs a counter thread.
    """
    countChanged = Qtc.pyqtSignal(int)

    def __init__(self, max) -> None:
        super().__init__()
        self.max = max

    def run(self) -> None:
        count = 0
        while count < self.max:
            count +=1
            time.sleep(0.1)
            self.countChanged.emit(count)

    
