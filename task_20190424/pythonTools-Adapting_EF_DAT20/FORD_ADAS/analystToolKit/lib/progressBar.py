from PyQt5 import QtCore, QtWidgets

from uis import progressBar


class ProgresBar(QtWidgets.QDialog, progressBar.Ui_Dialog):
    done = QtCore.pyqtSignal()
    def __init__(self, parent, flag, min, max):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.setModal(True)

        self.cancelBtn.clicked.connect(self.close)
        self.progressBar.setMinimum(min)
        self.progressBar.setMaximum(max)
        self.progressBar.setValue(min)

        self.flag = flag

        self.show()


    def inc(self, val=1):
        self.progressBar.setValue(min(self.progressBar.value() + val, self.progressBar.maximum()))
        if self.progressBar.value() == self.progressBar.maximum():
            self.close()

    def massage(self, txt):
        self.label.setText(txt)


    def closeEvent(self, QCloseEvent):
        self.flag[0] = False
        self.cancelBtn.setText('Canceling...')
        self.done.emit()
        self.deleteLater()
