import os
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from delphiTools3 import base as dt
from time import strftime

from uis import efsConfig
from uis import fakeCLI
from lib.efsClasses import aflEfsClass
from lib.efsClasses import lksEfsClass
from lib.efsClasses import objEfsClass
from lib.efsClasses import tsrEfsClass
from lib.efsClasses import failsafesEfsClass
from lib.efsClasses import statsEFClass
from lib.efsClasses import dvlobjEfsClass


class EFsClass:
    def setup_ef(self):
        self.ef_inputBtn.clicked.connect(self.ef_loadInput)
        self.ef_configBtn.clicked.connect(self.ef_openConfig)
        self.ef_runBtn.clicked.connect(self.ef_runEFs)

        self.ef_refreshSchortcut = QtWidgets.QShortcut(QtGui.QKeySequence.fromString('F5'), self.tool3)
        self.ef_refreshSchortcut.activated.connect(self.ef_updateList)
        self.ef_delItemShortcut = QtWidgets.QShortcut(QtGui.QKeySequence.Delete, self.tool3)
        self.ef_delItemShortcut.activated.connect(self.ef_delItem)

        aflEventFinder = aflEfsClass.aflEFs()
        lksEventFinder = lksEfsClass.lksEFs()
        objEventFinder = objEfsClass.objEFs()
        tsrEventFinder = tsrEfsClass.tsrEFs()
        failsafesEventFinder = failsafesEfsClass.failsafesEFs()
        dvlobjEventFinder = dvlobjEfsClass.dvlobjEFs()
        statsEventFinder = statsEFClass.statsEF()

        self.ef_efObjects = [aflEventFinder, lksEventFinder,
                             objEventFinder, tsrEventFinder,
                             failsafesEventFinder,
                             dvlobjEventFinder, statsEventFinder]

        self.ef_cli = None
        self.ef_outputPath = None
        self.ef_details = False
        self.ef_dat2p0 = False
        self.ef_efsList = [[], [], [], [], [], [], [False]]


    def ef_loadInput(self):
        if self.ef_folderRadio.isChecked():
            self.loadFolder(self.ef_inputEdit)
        else:
            self.loadFile(self.ef_inputEdit)
        self.ef_outputPath = None
        self.ef_details = False
        self.ef_dat2p0 = False
        self.ef_efsList = [[], [], [], [], [], [], [False]]

        self.ef_updateList()


    def ef_updateList(self):
        self.ef_matList.clear()

        path = str(self.ef_inputEdit.text())
        if path == '':
            return

        if self.ef_folderRadio.isChecked():
            onlymats = [f for f in os.listdir(path) if
                         os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] == '.mat']
            for each in sorted(onlymats):
                self.ef_matList.insertItem(self.ef_matList.count(), each)
                QtCore.QCoreApplication.processEvents()
        else:
            try:
                with open(path, 'r') as f:
                    rawLines = set(f.readlines())
                    rawLines = [line[:-1] if line.endswith('\n') else line for line in rawLines]
                    mats = [os.path.abspath(log) for log in rawLines if os.path.splitext(log)[1] == '.mat']
            except:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Cannot open input file!')
                return

            for each in mats:
                if not os.path.isfile(each):
                    continue
                self.ef_matList.insertItem(self.ef_matList.count(), each)
                QtCore.QCoreApplication.processEvents()


    def ef_delItem(self):
        self.ef_matList.takeItem(self.ef_matList.currentRow())


    def ef_openConfig(self):
        self.ef_config = Config(self)
        if self.ef_config.exec_() == QtWidgets.QDialog.Accepted:
            self.ef_outputPath, self.ef_details, self.ef_efsList, self.ef_dat2p0 = self.ef_config.getConfig()
            return True
        else:
            return False


    def openMat(self, path, dat2p0):
        try:
            print(f'\nExtracting {os.path.basename(path)}...')

            if os.path.exists(path):
                mat = dt.loadmat(path, variableName='mudp', sort=True, reBarrierMarge=False if dat2p0 else True, dat2p0=dat2p0)
            else:
                print("Path does not exist: ", path)
            if dat2p0:
                if not len(mat['mudp']['vis']['vision_AEB_info']['visAEB']['imageIndex']):
                    print('Mat corrupted!')
                    return
            else:
                if not len(mat['mudp']['vis']['vision_function_info']['imageIndex']):
                    print('Mat corrupted!')
                    return
            return mat
        except:
            print(f'Error while loading {os.path.basename(path)}!')
            return


    def ef_runEFs(self):
        while self.ef_outputPath is None:
            status = self.ef_openConfig()
            if not status:
                return

        self.ef_cli = FakeCli(self)
        print('***  masterEF   ***')
        print('*** Work, work. ***')

        if self.ef_matList.count():
            mats = [str(self.ef_matList.item(i).text()) for i in range(self.ef_matList.count())]
            if self.ef_folderRadio.isChecked():
                mats = [os.path.join(str(self.ef_inputEdit.text()), mat) for mat in mats]
            if self.ef_cli is not None:
                self.ef_cli.setProgBarMax(len(mats))
            try:
                ef_startTime = strftime("%d-%m-%Y")
                for i, matPath in enumerate(mats):
                    if self.ef_cli is None:
                        break
                    if i>0:
                        print('\n*** More work? ***')
                    mat = self.openMat(matPath, dat2p0=self.ef_dat2p0)
                    QtCore.QCoreApplication.processEvents()
                    if mat:
                        for j, efObj in enumerate(self.ef_efObjects):
                            if self.ef_efsList[j] == []:
                                continue
                            efObj.loadmat(mat, dat2p0=self.ef_dat2p0)
                            efObj.run(self.ef_efsList[j], self.ef_details, refreshFunction=QtCore.QCoreApplication.processEvents)
                            efObj.save(self.ef_outputPath)
                            QtCore.QCoreApplication.processEvents()
                    else:
                        stats = os.path.join(self.ef_outputPath, f'STATS-EF_{ef_startTime}.csv')
                        with open(stats, 'a') as s:
                            if os.path.isfile(matPath):
                                s.write(f'{os.path.basename(matPath)},Corrupted\n')
                            else:
                                s.write(f'{os.path.basename(matPath)},Missing\n')
                    if self.ef_cli is not None:
                        self.ef_cli.setProgBar(i + 1)
            except Exception as E:
                print('Unknown error!', E)
        else:
            print('\tNo files specified')

        if self.ef_cli:
            print('\n*** Job\'s done! ***')
            self.ef_cli.finish()


class Config(QtWidgets.QDialog, efsConfig.Ui_Dialog):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)

        self.acceptBtn.clicked.connect(self.onAccept)
        self.rejectBtn.clicked.connect(self.reject)

        self.outputBtn.clicked.connect(self.loadOutFolder)

        if self.parent().ef_outputPath is not None:
            self.outputEdit.setText(self.parent().ef_outputPath)
        self.detailsBox.setChecked(self.parent().ef_details)
        self.DAT2p0_CheckBox.setChecked(self.parent().ef_dat2p0)

        self.fillTree(self.parent().ef_efsList)

        self.show()


    def fillTree(self, currentEfsList):
        for i in range(6):
            AllEfsNames = self.parent().ef_efObjects[i].getEFsList()
            childStates = []
            for name in AllEfsNames:
                item = QtWidgets.QTreeWidgetItem(self.EFsTree.topLevelItem(i))
                item.setText(0, name)
                item.setCheckState(0, int(name in currentEfsList[i])*2)
                childStates.append(name in currentEfsList[i])
            self.EFsTree.topLevelItem(i).setExpanded(1)
            self.EFsTree.topLevelItem(i).setCheckState(0, all(childStates) * 2)
        self.EFsTree.topLevelItem(6).setCheckState(0, int(currentEfsList[6][0])*2)
        self.EFsTree.itemChanged.connect(self.updateTree)


    def updateTree(self, topItem):
        for i in range(topItem.childCount()):
            if topItem.checkState(0) == 2:
                topItem.child(i).setCheckState(0, 2)
            else:
                topItem.child(i).setCheckState(0, 0)


    def loadOutFolder(self):
        if self.outputEdit.text() == '':
            path = os.path.expanduser('~')
        else:
            path = os.path.abspath(self.outputEdit.text())
        root = QtWidgets.QFileDialog.getExistingDirectory(self, directory=path,
                                                          options=QtWidgets.QFileDialog.ShowDirsOnly)
        if not root:
            return
        self.outputEdit.setText(root)


    def onAccept(self):
        self.accept()


    def getConfig(self):
        efList = []
        for i in range(self.EFsTree.topLevelItemCount()):
            funcList = []
            top = self.EFsTree.topLevelItem(i)
            if top.childCount():
                for j in range(top.childCount()):
                    if top.child(j).checkState(0) == 2:
                        funcList.append(str(top.child(j).text(0)))
            else:
                if top.checkState(0) == 2:
                    funcList = [True]
                else:
                    funcList = [False]
            efList.append(funcList)
            QtCore.QCoreApplication.processEvents()
        details = self.detailsBox.isChecked()
        dat2p0 = self.DAT2p0_CheckBox.isChecked()
        outPath = str(self.outputEdit.text()) if self.outputEdit.text() != '' else None
        return outPath, details, efList, dat2p0


    def closeEvent(self, event):
        self.deleteLater()


class FakeCli(QtWidgets.QDialog, fakeCLI.Ui_Dialog):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry(parent.geometry().adjusted(10, 10,-10,-10))
        self.setModal(True)
        self.parent().tool3.setEnabled(False)

        self.saveBtn.clicked.connect(self.onSave)
        self.closeBtn.clicked.connect(self.onCancel)

        sys.stdout = EmittingStream(textWritten=self.writeToCLI)
        sys.stderr = EmittingStream(textWritten=self.writeToCLI)

        self.setProgBarMax(1)
        self.setProgBar(0)

        self.show()

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


    def setProgBarMax(self, int):
        self.progressBar.setMaximum(int)

    def setProgBar(self, int):
        self.progressBar.setValue(int)


    def writeToCLI(self, text):
        cursor = self.fakeCLI.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.fakeCLI.setTextCursor(cursor)
        self.fakeCLI.ensureCursorVisible()


    def onSave(self):
        outputPath, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Save output', directory='out.txt',
                                                       filter='Text (*.txt)')
        if outputPath == '':
            return

        with open(outputPath, 'w') as f:
            f.writelines(self.fakeCLI.toPlainText())

        self.onCancel()


    def onCancel(self):
        self.parent().tool3.setEnabled(True)
        self.parent().ef_cli = None
        self.close()


    def finish(self):
        self.saveBtn.setEnabled(True)
        self.closeBtn.setText('Close')


    def closeEvent(self, event):
        self.deleteLater()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))