from __init__ import Qtw


def work_mode() -> int:
    msg = Qtw.QMessageBox()
    msg.setWindowTitle("Select working mode.")
    msg.setIcon(Qtw.QMessageBox.Question)
    msg.setText(
        "Would you like to load existing database created by this program?"
    )
    msg.setStandardButtons(Qtw.QMessageBox.Yes | Qtw.QMessageBox.No)
    x = msg.exec_()
    return x


def error_message(text) -> None:
    msg = Qtw.QMessageBox()
    msg.setWindowTitle("Error")
    msg.setIcon(Qtw.QMessageBox.Critical)
    msg.setText(text)
    msg.setStandardButtons(Qtw.QMessageBox.Ok)
    msg.exec_()


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
