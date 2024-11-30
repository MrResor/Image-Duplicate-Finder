from __init__ import Qtw


class ErrorMessage(Qtw.QMessageBox):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.setWindowTitle("Error")
        self.setIcon(Qtw.QMessageBox.Critical)
        self.setText(text)
        self.setStandardButtons(Qtw.QMessageBox.Ok)

    def run(self) -> int:
        return self.exec_()
