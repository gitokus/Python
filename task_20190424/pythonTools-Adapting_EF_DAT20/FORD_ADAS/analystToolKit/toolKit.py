import sys
import os
import traceback

from PyQt5 import QtCore, QtWidgets

from uis import mainWindow as mw
from lib.settings import SettingsClass
from lib.projects import ProjectClass


from lib.fileFinder import FileFinderClass
from lib.autoResim import AutoResimClass
from lib.efs import EFsClass
from lib.efViewer import EFViewerClass


class ToolKit(QtWidgets.QMainWindow, mw.Ui_MainWindow, ProjectClass,
                FileFinderClass, AutoResimClass, EFsClass, EFViewerClass):
    ar_incSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setup_ff()
        self.setup_ar()
        self.setup_ef()
        self.setup_efv()

        self.toolBar.setHidden(True)

        self.actionNewProject.triggered.connect(self.createNewProject)
        self.actionOpenProject.triggered.connect(self.openProject)
        self.actionCloseProject.triggered.connect(self.closeProject)
        self.actionSave.triggered.connect(self.saveProject)
        self.createProjectBtn.clicked.connect(self.createNewProject)
        self.openProjectBtn.clicked.connect(self.openProject)
        self.noProjectBtn.clicked.connect(self.runWithoutProject)
        self.projectFile = ''

        self.settingsWindow = SettingsClass(self)
        self.actionSettings.triggered.connect(self.settingsWindow.show)
        self.actionExit.triggered.connect(self.close)

        self.toolSelectGroup = QtWidgets.QActionGroup(self)
        for action in [self.actionFileFinder, self.actionAutoResim, self.actionEFs, self.actionEFsViewer]:
            self.toolSelectGroup.addAction(action)
            action.triggered.connect(self.changeToolTab)
        self.toolSelectGroup.setExclusive(True)

    def loadFolder(self, dest, func=None):
        if dest.text() == '':
            path = os.path.expanduser('~')
        else:
            path = os.path.abspath(dest.text())
        root = QtWidgets.QFileDialog.getExistingDirectory(self, directory=path,
                                                          options=QtWidgets.QFileDialog.ShowDirsOnly)
        if not root:
            return
        dest.setText(root)
        if func:
            func()

    def loadFile(self, dest, func=None):
        if dest.text() == '':
            path = os.path.expanduser('~')
        else:
            path = os.sep.join(os.path.abspath(dest.text()).split(os.sep)[:-1])
        root, _ = QtWidgets.QFileDialog.getOpenFileName(self, directory=path)
        if not root:
            return
        dest.setText(root)
        if func:
            func()

    def resizeEvent(self, *args, **kwargs):
        if self.toolsStackWidget.currentIndex() == 5:
            self.efv_updateFrame()

    def closeEvent(self, event):
        if self.actionSave.isEnabled():
            if not self.isTempProject:
                reply = QtWidgets.QMessageBox.question(
                    self,
                    'Warning', "Do you want to save changes\nin current project?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.Yes)

                if reply == QtWidgets.QMessageBox.Yes:
                    self.saveProject()
            else:
                os.remove(self.projectFile)

        event.accept()

    def changeToolTab(self):
        currentTab = self.toolSelectGroup.actions().index(self.toolSelectGroup.checkedAction())
        self.toolsStackWidget.setCurrentIndex(currentTab + 2)
        if self.efv_is2ndWindow:
            self.toolBar.setHidden(True)
        if self.efv_is2ndWindow and not currentTab == 3:
            self.efv_onDestroy()
        if not currentTab == 3:
            if not self.window().isMaximized():
                self.resize(400, 600)
                self.toolBar.setHidden(True)
        else:
            if not self.window().isMaximized():
                self.resize(1260, 960)
                self.toolBar.setHidden(False)
            self.efv_updateFrame()

def myExceptionhook(exctype, value, traceback_):
    formatted_exception = traceback.format_exception(exctype, value, traceback_)
    formatted_exception = ''.join(formatted_exception)
    print(formatted_exception)


def main():
        sys.excepthook = myExceptionhook
        app = QtWidgets.QApplication(sys.argv)
        tk = ToolKit()
        tk.show()
        app.exec_()


if __name__ == '__main__':
    main()
