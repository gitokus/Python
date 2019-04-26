import os
import pickle

from PyQt5 import QtWidgets

from uis import settingsWindow


class SettingsClass(QtWidgets.QDialog, settingsWindow.Ui_Dialog):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        self.settingsTree.expandAll()

        self.saveBtn.clicked.connect(self.saveAndClose)
        self.settingsTree.currentItemChanged.connect(self.changeSettingWidget)

        if not os.path.isdir('data'):
            os.mkdir('data')
        self.setFromFile()


    def changeSettingWidget(self, item):
        order = ['General']
        if type(item) == str:
            widget = order.index(item)
        else:
            if item.childCount() == 0:
                widget = order.index(item.text(0))
            else:
                widget = 0
        self.settingsWidgets.setCurrentIndex(widget)


    def getSettings(self):
        return {'General': {'name': str(self.generalNameEdit.text()),
                            'email': str(self.generalEmail.text())}}


    def setFromFile(self):
        if os.path.isfile('data/settings'):
            try:
                with open('data/settings', 'rb') as settingsFile:
                    data = pickle.loads(settingsFile.read())

                self.generalNameEdit.setText(data['General']['name'])
                self.generalEmail.setText(data['General']['email'])
            except:
                os.remove('data/settings')


    def saveAndClose(self):
        with open('data/settings', 'wb') as settingsFile:
            settingsFile.write(pickle.dumps(self.getSettings()))
        self.hide()


    def closeEvent(self, QCloseEvent):
        self.deleteLater()



