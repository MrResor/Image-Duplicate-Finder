from __init__ import Qtw, Qtg, Qtc

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


class Progress(Qtw.QProgressDialog):

    msg_list = {0: 'Preparing.', 1: 'Finding all photos.',
                2: 'Comparing photos.', 3: 'Setting up UI.'}

    def __init__(self, prog_sig) -> None:
        super().__init__()
        self.sig = prog_sig[0]
        self.setWindowTitle("Working...")
        self.setFixedSize(300, 400)
        # self.setIcon(Qtw.QProgressBox.Information)
        self.set_text(0)
        self.sig.connect(self.set_text)
        # self.setStandardButtons(Qtw.QProgressBox.NoButton)
        self.show()

    def set_text(self, code) -> None:
        self.setLabelText(self.msg_list[code])
        self.update()
