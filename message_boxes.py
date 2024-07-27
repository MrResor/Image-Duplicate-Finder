from __init__ import Qtw, Qtg, Qtc
from auxiliary import Get_paths, Filter_images
import time

class ChkBxFileDialog(Qtw.QFileDialog):
    def __init__(self, chkBxTitle="", filter="") -> None:
        super().__init__(filter=filter)
        self.setOption(Qtw.QFileDialog.DontUseNativeDialog)
        self.setFileMode(Qtw.QFileDialog.FileMode.Directory)
        
        # self.selectNameFilter("*.txt")
        self.chkBx = Qtw.QCheckBox(chkBxTitle)
        self.chkBx.setText("Search directories")
        self.layout().addWidget(self.chkBx)

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

    def __init__(self, paths, deep_search, db) -> None:
        super().__init__()
        self.setWindowTitle("Working...")
        self.setWindowFlag(Qtc.Qt.WindowCloseButtonHint, False)
        self.setFixedSize(400, 200)
        self.db = db

        self.ui()

        self.calc = Get_paths(paths, deep_search)
        self.calc.direc_done.connect(self.on_direc_done)
        self.calc.search_done.connect(self.on_search_done)
        self.calc.start()

        self.exec_()

    def ui(self) -> None:
        self.layout = Qtw.QVBoxLayout()
        self.layout.setAlignment(Qtc.Qt.AlignCenter)

        self.message = Qtw.QTextEdit()
        self.message.setReadOnly(True)
        self.message.append("Searching for images...")
        self.layout.addWidget(self.message)

        self.bar = Qtw.QProgressBar()
        self.bar.setTextVisible(True)
        style = 'QProgressBar { color: black; border: 0.5px solid #c0bcbc; \
            background: #e8e4e4 }'
        self.bar.setStyleSheet(style)
        self.bar.setAlignment(Qtc.Qt.AlignCenter)
        self.layout.addWidget(self.bar)

        self.button = Qtw.QPushButton("Cancel")
        self.button.setFixedWidth(100)
        self.layout.addWidget(self.button, alignment=Qtc.Qt.AlignCenter)
        self.button.clicked.connect(self.cancel)

        self.setLayout(self.layout)

    def on_direc_done(self, value) -> None:
        self.message.append(str(value) + " - Done!")

    def on_search_done(self) -> None:
        relevant = self.calc.relevant
        iter = len(relevant)
        if iter == 0:
            # TODO this is temporary solution, instead alert should be here
            self.bar.setFormat('No images found!')
            self.bar.setMaximum(1)
            self.bar.setValue(1)
        else:
            self.bar.setMaximum(iter)
            self.bar.setFormat('Finding Duplicates %v / ' + str(iter))
            self.calc = Filter_images(relevant, self.db)
            self.calc.count_changed.connect(self.on_count_changed)
            self.calc.filtering_done.connect(self.finished)
            self.calc.start()

    def on_count_changed(self, value) -> None:
        self.bar.setValue(value)
    
    def cancel(self) -> None:
        self.reject()

    def finished(self) -> None:
        self.done(0)
