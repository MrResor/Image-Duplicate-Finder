from __init__ import Qtw


class CheckBoxFileDialog(Qtw.QFileDialog):
    def __init__(self, chkBxTitle="", filter="") -> None:
        super().__init__(filter=filter)
        self.setOption(Qtw.QFileDialog.DontUseNativeDialog)
        self.setFileMode(Qtw.QFileDialog.FileMode.Directory)

        # self.selectNameFilter("*.txt")
        self.chkBx = Qtw.QCheckBox(chkBxTitle)
        self.chkBx.setText("Search directories")
        self.layout().addWidget(self.chkBx)

    def run(self) -> int:
        return self.exec_()
