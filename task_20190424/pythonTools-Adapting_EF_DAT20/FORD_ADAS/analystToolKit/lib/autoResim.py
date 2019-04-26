import os
import subprocess

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from PyQt5 import QtCore, QtWidgets, QtGui
from functools import partial

from lib.progressBar import ProgresBar


class AutoResimClass:
    def setup_ar(self):
        self.ar_exeBtn.clicked.connect(partial(self.loadFile, self.ar_exeEdit))
        self.ar_inputBtn.clicked.connect(self.ar_loadInput)
        self.ar_historyCheckBox.toggled.connect(self.ar_updateList)
        self.ar_historySpinBox.valueChanged.connect(self.ar_updateList)
        self.ar_mmrCheckBox.stateChanged.connect(self.ar_updateList)
        self.ar_outDirBox.toggled.connect(self.ar_altDirParam)
        self.ar_runBtn.clicked.connect(self.ar_runResim)

        self.ar_refreshSchortcut = QtWidgets.QShortcut(QtGui.QKeySequence.fromString('F5'), self.tool2)
        self.ar_refreshSchortcut.activated.connect(self.ar_updateList)
        self.ar_delItemShortcut =  QtWidgets.QShortcut(QtGui.QKeySequence.Delete, self.tool2)
        self.ar_delItemShortcut.activated.connect(self.ar_delItem)


    def ar_loadInput(self):
        if self.ar_folderRadio.isChecked():
            self.loadFolder(self.ar_inputEdit)
        else:
            self.loadFile(self.ar_inputEdit)
        self.ar_updateList()


    def ar_updateList(self):
        self.ar_logsList.clear()

        path = str(self.ar_inputEdit.text())
        if path == '':
            return

        if self.ar_folderRadio.isChecked():
            onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            for each in sorted(set([os.path.splitext(f)[0] for f in onlyfiles])):
                if (each + '.dvl' in onlyfiles and  each + '.mudp' in onlyfiles and
                        (each + '_alt.avi' in onlyfiles or self.ar_mmrCheckBox.isChecked()) and
                        (each + '.avi' in onlyfiles or self.ar_mmrCheckBox.isChecked()) and
                        (each + '.tapi' in onlyfiles or self.ar_mmrCheckBox.isChecked()) and
                        (each + '.ffs' in onlyfiles or self.ar_mmrCheckBox.isChecked()) ):
                    self.ar_logsList.insertItem(self.ar_logsList.count(), each + '.dvl')
                    QtCore.QCoreApplication.processEvents()
        else:
            try:
                with open(path, 'r') as f:
                    rawLines = set(f.readlines())
                    rawLines = [line[:-1] if line.endswith('\n') else line for line in rawLines]
                    logs = sorted([os.path.abspath(log) for log in rawLines if os.path.splitext(log)[1] == '.dvl'])
            except:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Cannot open input file!')
                return

            if self.ar_historyCheckBox.isChecked():
                logsHist = []
                param = int(self.ar_historySpinBox.value())
                for log in logs:
                    for i in range(-param, 1):
                        newLog = log[:-7] + str(max(int(log[-7:-4]) + i, 1)).zfill(3) + '.dvl'
                        if newLog not in logsHist:
                            logsHist.append(newLog)
                logs = logsHist

            for log in logs:
                if not os.path.isfile(log):
                    continue
                logDir = os.path.dirname(log)
                logName = os.path.splitext(os.path.basename(log))[0]
                dirFiles = [f for f in os.listdir(logDir) if os.path.isfile(os.path.join(logDir, f))]
                if (logName + '.dvl' in dirFiles and logName + '.mudp' in dirFiles and
                        (logName + '_alt.avi' in dirFiles or self.ar_mmrCheckBox.isChcecked()) and
                        (logName + '.avi' in dirFiles or self.ar_mmrCheckBox.isChcecked()) and
                        (logName + '.tapi' in dirFiles or self.ar_mmrCheckBox.isChcecked()) and
                        (logName + '.ffs' in dirFiles or self.ar_mmrCheckBox.isChcecked()) and
                        logName not in [str(self.ar_logsList.item(i).text()) for i in range(self.ar_logsList.count())]):
                    self.ar_logsList.insertItem(self.ar_logsList.count(), log)
                QtCore.QCoreApplication.processEvents()


    def ar_delItem(self):
        self.ar_logsList.takeItem(self.ar_logsList.currentRow())


    def ar_altDirParam(self, state):
        if state:
            altDir = QtWidgets.QFileDialog.getExistingDirectory(self, directory=os.path.expanduser('~'),
                                                              options=QtWidgets.QFileDialog.ShowDirsOnly)
            if not altDir:
                self.ar_outDirBox.setChecked(False)
                return
            self.ar_paramsEdit.setText(f'{self.ar_paramsEdit.text()} -altdir {altDir}')
        else:
            params = str(self.ar_paramsEdit.text()).split(' ')
            if '-altdir' in params:
                index = params.index('-altdir')
                params.pop(index)
                params.pop(index)
                self.ar_paramsEdit.setText(' '.join(params))


    def ar_genCmd(self):
        def nexts_number(log, logs):
            next = log[:-7] + str(int(log[-7:-4]) + 1).zfill(3) + '.dvl'
            if (next in logs):
                return nexts_number(next, logs) + 1
            else:
                return 0

        logs = [str(self.ar_logsList.item(i).text()) for i in range(self.ar_logsList.count())]
        commands = []
        nexts = [nexts_number(log, logs) for log in logs]
        i = 0
        while i < len(logs):
            sim = str(self.ar_exeEdit.text())
            log = logs[i] if self.ar_fileRadio.isChecked() else str(self.ar_inputEdit.text()) + '/' + logs[i]
            params = str(self.ar_paramsEdit.text())
            if nexts[i] == 0:
                cmd = sim + ' "' + log + '" ' + params
            else:
                cmd = sim + ' "' + log[:-7] + '[' + log[-7:-4] + '].dvl" -nfiles ' + str(nexts[i] + 1) + ' ' + params

            if self.ar_outDirBox.isChecked():
                params = str(self.ar_paramsEdit.text()).split(' ')
                logFolder = params[params.index('-altdir') + 1]
            else:
                logFolder = os.path.dirname(log)  # folder with the original log
            logName = os.path.splitext(os.path.basename(log))[0]  # name of the log (without .dvl)
            resimFolderName = sim.split('/')[-3]  # e.g. 'ADASIFVResim_20170117_Release_rE24030017_rM7724052'
            resimName = resimFolderName.split('_')[-1]  # e.g. 'rM7724052'
            txtFile = logFolder + '/' + resimName + '/' + logName + '_' + resimName + '.txt'
            if not os.path.isdir(logFolder + '/' + resimName):
                os.mkdir(logFolder + '/' + resimName)
            cmd += ' 1>' + txtFile + ' 2>&1'

            commands.append(cmd)
            i += nexts[i] + 1
        return commands


    def ar_runResim(self):
        self.pList = []
        if not str(self.ar_exeEdit.text()) or not str(self.ar_inputEdit.text()):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Choose resim exe and input data!')
            return
        try:
            cmds = self.ar_genCmd()
        except:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Incorrect input!')
            return
        if not len(cmds):
            return
        self.ar_runFlag = [True]
        self.ar_progressBar = ProgresBar(self, self.ar_runFlag, 0, len(cmds))
        self.ar_progressBar.massage('Resimulating...')
        self.ar_incSignal.connect(self.ar_progressBar.inc)
        self.ar_progressBar.done.connect(self.ar_resimDone)
        self.ar_pool = ThreadPool(cpu_count())
        for cmd in cmds:
            self.ar_pool.apply_async(self.run, (cmd,))

    def run(self, line):
        p = subprocess.Popen(line, shell=True)
        self.pList.append(p)
        p.wait()
        self.ar_incSignal.emit()


    def ar_resimDone(self):
        for p in self.pList:
            p.kill()
        self.ar_progressBar.close()
        self.ar_pool.terminate()
        self.ar_pool.join()