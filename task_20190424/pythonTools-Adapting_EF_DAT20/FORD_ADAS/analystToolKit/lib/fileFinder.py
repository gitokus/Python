import os

from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import Process, freeze_support
from shutil import copy2

from uis import fileExtensions
from lib.progressBar import ProgresBar


class FileFinderClass:
    def setup_ff(self):
        self.ff_rootBtn.clicked.connect(partial(self.loadFolder, self.ff_rootEdit))
        self.ff_outputBtn.clicked.connect(partial(self.loadFolder, self.ff_outputEdit))
        self.ff_searchBtn.clicked.connect(self.ff_search)


    def ff_search(self):
        freeze_support()
        self.ff_searchFlag = [True]

        if str(self.ff_rootEdit.text()) == '':
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please choose root folder!')
            self.ff_searchBtn.setEnabled(True)
            return
        if str(self.ff_outputEdit.text()) == '':
            self.ff_outputEdit.setText(str(self.ff_rootEdit.text()) + '/' + 'out')
            if not os.path.isdir(str(self.ff_outputEdit.text())):
                os.mkdir(str(self.ff_outputEdit.text()))

        if self.ff_logsEdit.toPlainText() == '':
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please enter logs to find!')
            self.ff_searchBtn.setEnabled(True)
            return

        extDialog = Extensions(self)
        if extDialog.exec_() == QtWidgets.QDialog.Accepted:
            self.ff_extList = extDialog.getExts()
        else:
            self.ff_searchBtn.setEnabled(True)
            return

        self.ff_logs = []
        for log in self.ff_logsEdit.toPlainText().split('\n'):
            if len(log) > 0:
                self.ff_logs.append(str(log).translate({ord(c): '' for c in ' \n\t\r'}))
        self.ff_logs = list(set(self.ff_logs))

        if self.ff_historyCheckBox.isChecked():
            logsHist = []
            for log in self.ff_logs:
                no = int(log[-3:])
                for i in [j for j in range(no - self.ff_historyBox.value(), no + 1) if j > 0]:
                    newLog = log[:-3] + str(i).zfill(3)
                    if newLog not in logsHist:
                        logsHist.append(newLog)
            self.ff_logs = logsHist

        logsExts = []
        for log in self.ff_logs:
            for ext in self.ff_extList:
                newLog = os.path.splitext(log)[0] + ext
                if newLog not in logsExts:
                    logsExts.append(newLog)
        self.ff_logs = logsExts

        progBar = ProgresBar(self, self.ff_searchFlag, 0, len(self.ff_logs))

        with open(str(self.ff_outputEdit.text()) + os.sep + 'searchReport.txt', 'w') as reportFile:
            reportFile.write('***Found files:***\n\n')

        chceckedFiles = 0
        for root, dirnames, filenames in os.walk(str(self.ff_rootEdit.text())):
            matches = list(set(self.ff_logs) & set(filenames))
            chceckedFiles += len(filenames)
            if matches:
                for match in matches:
                    try:
                        if self.ff_outputRadioBtn_1.isChecked():
                            if self.ff_searchFlag[0]:
                                with open(str(self.ff_outputEdit.text()) +
                                                  os.sep + 'searchReport.txt', 'a') as reportFile:
                                    reportFile.write(root + os.sep + match + '\n')
                            else:
                                break
                        elif self.ff_outputRadioBtn_2.isChecked():
                            progBar.massage('Copying: ' + match)
                            self.process = Process(target=copy2, args=(
                            root + os.sep + match, str(self.ff_outputEdit.text()) + os.sep + match,))
                            self.process.start()
                            while self.process.is_alive() and self.ff_searchFlag[0]:
                                QtWidgets.QApplication.processEvents()
                            self.process.terminate()
                            self.process.join()
                            if self.ff_searchFlag[0]:
                                with open(str(self.ff_outputEdit.text()) +
                                                  os.sep + 'searchReport.txt', 'a') as reportFile:
                                    reportFile.write(root + os.sep + match + '\n')
                            else:
                                os.remove(str(self.ff_outputEdit.text()) + os.sep + match)
                                break
                        progBar.inc()
                        self.ff_logs.remove(match)
                        QtWidgets.QApplication.processEvents()
                    except:
                        continue
            if not self.ff_searchFlag[0]:
                break
            else:
                progBar.massage(f'Found files: {progBar.progressBar.value()}/'
                                f'{progBar.progressBar.maximum()} (scanned: {chceckedFiles})')
            QtWidgets.QApplication.processEvents()

        with open(str(self.ff_outputEdit.text()) + os.sep + 'searchReport.txt', 'a') as reportFile:
            reportFile.write('\n\n***Missing files:***\n\n')
            for log in sorted(self.ff_logs):
                reportFile.write(log + '\n')


        self.ff_colorOutput()
        try:
            progBar.close()
        except:
            pass


    def ff_colorOutput(self):
        logs = [log[:-4] if log[-4:] == '_alt' else log for log in [os.path.splitext(log)[0] for log in self.ff_logs]]
        log = self.ff_logsEdit.firstVisibleBlock()
        fmt = QtGui.QTextBlockFormat()
        while log.previous().isValid():
            log = log.previous()
        while log.isValid():
            if logs.count(log.text()) == len(self.ff_extList):
                fmt.setBackground(QtGui.QBrush(QtCore.Qt.red))
            elif logs.count(log.text()) == 0:
                fmt.setBackground(QtGui.QBrush(QtCore.Qt.green))
            else:
                fmt.setBackground(QtGui.QBrush(QtCore.Qt.yellow))
            QtGui.QTextCursor(log).setBlockFormat(fmt)
            log = log.next()


class Extensions(QtWidgets.QDialog, fileExtensions.Ui_Dialog):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.acceptBtn.clicked.connect(self.onAccept)
        self.rejectBtn.clicked.connect(self.reject)

        self.checkBox_ALL.stateChanged.connect(self.onAll)
        self.extList = []
        self.show()


    def onAccept(self):
        self.extList = []
        for i in range(1, 8):
            if (eval('self.checkBox_' + str(i)).isChecked()):
                self.extList.append(str(eval('self.checkBox_' + str(i)).text()))
        if self.checkBox_8.isChecked():
            self.extList += self.lineEdit.text().split(',')
        if '.avi' in self.extList:
            self.extList.append('_alt.avi')
        self.accept()


    def getExts(self):
        return self.extList


    def onAll(self):
        if self.checkBox_ALL.isChecked():
            for i in range(1, 8):
                eval('self.checkBox_' + str(i)).setChecked(True)
        else:
            for i in range(1, 8):
                eval('self.checkBox_' + str(i)).setChecked(False)


    def closeEvent(self, QCloseEvent):
        self.deleteLater()