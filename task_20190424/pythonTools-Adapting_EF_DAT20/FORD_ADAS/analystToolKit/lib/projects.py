import os
import pickle

from PyQt5 import QtWidgets


class ProjectClass:
    def createNewProject(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, directory=os.getcwd(),
                                                     filter='ToolKit project (*.tkp)')[0]
        self.closeProject()
        self.isTempProject = False
        if file:

            self.projectFile = file
            self.setWindowTitle(f'Analyst ToolKit - {os.path.basename(file)}')

            self.menuToolSelect.setEnabled(True)
            self.actionSave.setEnabled(True)
            self.toolsStackWidget.setCurrentIndex(1)

            self.saveProject()

    def openProject(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, directory=os.getcwd(),
                                                     filter='ToolKit project (*.tkp)')[0]
        self.closeProject()
        self.isTempProject = False
        if file:
            self.projectFile = file
            self.setWindowTitle(f'Analyst ToolKit - {os.path.basename(file)}')
            self.loadProject()

            self.menuToolSelect.setEnabled(True)
            self.actionSave.setEnabled(True)
            self.toolsStackWidget.setCurrentIndex(1)

    def runWithoutProject(self):
        file = os.path.join(os.getcwd(), 'TempToolkitProjectItWillDeleteItselfAutomaticallyDontWorry.tkp')
        self.closeProject()
        self.isTempProject = True

        if file:
            self.projectFile = file
            self.setWindowTitle('Analyst ToolKit - No project')

            self.menuToolSelect.setEnabled(True)
            self.actionSave.setEnabled(True)
            self.toolsStackWidget.setCurrentIndex(1)

            self.saveProject()


    def closeProject(self):
        if self.actionSave.isEnabled():
            if not self.isTempProject:
                reply = QtWidgets.QMessageBox.question(self,
                    'Warning', "Do you want to save changes\nin current project?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.Yes)
                if reply == QtWidgets.QMessageBox.Yes:
                    self.saveProject()
            else:
                # os.remove(os.path.join(os.getcwd(), 'TempToolkitProjectItWillDeleteItselfAutomaticallyDontWorry.tkp'))
                os.remove(self.projectFile)

        self.actionSave.setEnabled(False)
        if self.toolSelectGroup.checkedAction():
            self.toolSelectGroup.checkedAction().setChecked(False)
        self.menuToolSelect.setEnabled(False)
        self.toolsStackWidget.setCurrentIndex(0)
        self.clearProject()

    def saveProject(self):
        data = {'ff_rootEdit': str(self.ff_rootEdit.text()),
                'ff_logsEdit': str(self.ff_logsEdit.toPlainText()),
                'ff_historyBox': self.ff_historyBox.value(),
                'ff_historyCheckBox': self.ff_historyCheckBox.isChecked(),
                'ff_outputRadioBtn_1': self.ff_outputRadioBtn_1.isChecked(),
                'ff_outputRadioBtn_2': self.ff_outputRadioBtn_2.isChecked(),
                'ff_outputEdit': str(self.ff_outputEdit.text()),

                'ar_exeEdit': str(self.ar_exeEdit.text()),
                'ar_inputEdit': str(self.ar_inputEdit.text()),
                'ar_folderRadio': self.ar_folderRadio.isChecked(),
                'ar_fileRadio': self.ar_fileRadio.isChecked(),
                'ar_logsList': [str(self.ar_logsList.item(i).text()) for i in range(self.ar_logsList.count())],
                'ar_historyCheckBox': self.ar_historyCheckBox.isChecked(),
                'ar_historySpinBox': self.ar_historySpinBox.value(),
                'ar_paramsEdit': str(self.ar_paramsEdit.text()),
                'ar_outDirBox': self.ar_outDirBox.isChecked(),

                'ef_inputEdit': str(self.ef_inputEdit.text()),
                'ef_folderRadio': self.ef_folderRadio.isChecked(),
                'ef_fileRadio': self.ef_fileRadio.isChecked(),
                'ef_matList': [str(self.ef_matList.item(i).text()) for i in range(self.ef_matList.count())],
                'ef_outputPath': self.ef_outputPath,
                'ef_details': self.ef_details,
                'ef_dat2p0': self.ef_dat2p0,

                'ef_efsList': self.ef_efsList,

                'efv_loadReportLine': str(self.efv_loadReportLine.text()),
                'efv_loadDataLine': str(self.efv_loadDataLine.text()),
                'efv_loadBox': self.efv_loadBox.isChecked(),
                'efv_frameEdit': str(self.efv_frameEdit.text()),
                'efv_eventEdit': str(self.efv_eventEdit.text()),
                'efv_currentEvent': self.efv_currentEvent,
                'efv_currentFrame': self.efv_currentFrame,
                'efv_header': self.efv_header,
                'efv_saveAction': self.efv_saveAction.isChecked(),
                'efv_gtLayoutAction': self.efv_gtLayoutAction.isChecked(),
                'efv_binds': self.efv_bindMenu.getBinds(),
                'efv_autonext': self.efv_bindMenu.checkBox.isChecked(),
                'efv_aflLayoutAction': self.efv_aflLayoutAction.isChecked(),
                'efv_hrsLayoutAction': self.efv_hrsLayoutAction.isChecked(),
                'efv_tsrLayoutAction': self.efv_tsrLayoutAction.isChecked(),
                'efv_tsrPlusLayoutAction': self.efv_tsrPlusLayoutAction.isChecked(),
                'efv_obj2dLayoutAction': self.efv_obj2dLayoutAction.isChecked(),
                'efv_obj3dLayoutAction': self.efv_obj3dLayoutAction.isChecked(),
                'efv_lksIndLayoutAction': self.efv_lksIndLayoutAction.isChecked(),
                'efv_lksParLayoutAction': self.efv_lksParLayoutAction.isChecked(),
                'efv_lksHspLayoutAction': self.efv_lksHspLayoutAction.isChecked(),
                'efv_lksReLayoutAction': self.efv_lksReLayoutAction.isChecked(),
                'efv_lksBarLayoutAction': self.efv_lksBarLayoutAction.isChecked(),
                'efv_lksHostLayoutAction': self.efv_lksHostLayoutAction.isChecked(),
                'efv_lksNextLLayoutAction': self.efv_lksNextLLayoutAction.isChecked(),
                'efv_lksNextRLayoutAction': self.efv_lksNextRLayoutAction.isChecked(),
                'efv_lksBordLayoutAction': self.efv_lksBordLayoutAction.isChecked(),
                'efv_fusLayoutAction': self.efv_fusLayoutAction.isChecked(),
                'efv_fusPedLayoutAction': self.efv_fusPedLayoutAction.isChecked(),
                'efv_tselLayoutAction': self.efv_tselLayoutAction.isChecked(),
                'efv_tselPathLayoutAction': self.efv_tselPathLayoutAction.isChecked(),
                'efv_pcaLayoutAction': self.efv_pcaLayoutAction.isChecked(),
                'efv_failSafeLayoutAction': self.efv_failSafeLayoutAction.isChecked(),
                }

        with open(self.projectFile, 'wb') as settingsFile:
            pickle.dump(data, settingsFile)

    def loadProject(self):
        with open(self.projectFile, 'rb') as dataFile:
            data = pickle.load(dataFile)

        self.ff_rootEdit.setText(data['ff_rootEdit'])
        self.ff_logsEdit.setPlainText(data['ff_logsEdit'])
        self.ff_historyBox.setValue(data['ff_historyBox'])
        self.ff_historyCheckBox.setChecked(data['ff_historyCheckBox'])
        self.ff_outputRadioBtn_1.setChecked(data['ff_outputRadioBtn_1'])
        self.ff_outputRadioBtn_2.setChecked(data['ff_outputRadioBtn_2'])
        self.ff_outputEdit.setText(data['ff_outputEdit'])

        self.ar_exeEdit.setText(data['ar_exeEdit'])
        self.ar_inputEdit.setText(data['ar_inputEdit'])
        self.ar_folderRadio.setChecked(data['ar_folderRadio'])
        self.ar_fileRadio.setChecked(data['ar_fileRadio'])
        for line in data['ar_logsList']:
            self.ar_logsList.insertItem(self.ar_logsList.count(), line)
        self.ar_historyCheckBox.setChecked(data['ar_historyCheckBox'])
        self.ar_historySpinBox.setValue(data['ar_historySpinBox'])
        self.ar_paramsEdit.setText(data['ar_paramsEdit'])
        oldState = self.ar_outDirBox.blockSignals(True)
        self.ar_outDirBox.setChecked(data['ar_outDirBox'])
        self.ar_outDirBox.blockSignals(oldState)

        self.ef_inputEdit.setText(data['ef_inputEdit'])
        self.ef_folderRadio.setChecked(data['ef_folderRadio'])
        self.ef_fileRadio.setChecked(data['ef_fileRadio'])
        for line in data['ef_matList']:
            self.ef_matList.insertItem(self.ef_matList.count(), line)
        self.ef_outputPath = data['ef_outputPath']
        self.ef_details = data['ef_details']
        self.ef_efsList = data['ef_efsList']
        self.ef_dat2p0 = data['ef_dat2p0']

        self.efv_loadReportLine.setText(data['efv_loadReportLine'])
        self.efv_loadDataLine.setText(data['efv_loadDataLine'])
        self.efv_loadBox.setChecked(data['efv_loadBox'])
        self.efv_frameEdit.setText(data['efv_frameEdit'])
        self.efv_eventEdit.setText(data['efv_eventEdit'])
        self.efv_currentEvent = data['efv_currentEvent']
        self.efv_currentFrame = data['efv_currentFrame']
        self.efv_header = data['efv_header']
        if data['efv_loadReportLine'] != '':
            try:
                self.efv_loadReport(quietLoad=True)
                self.setFocus()
            except:
                pass
        self.efv_saveAction.setChecked(data['efv_saveAction'])

        self.efv_aflLayoutAction.setChecked(data['efv_aflLayoutAction'])
        self.efv_tsrLayoutAction.setChecked(data['efv_tsrLayoutAction'])
        self.efv_tselLayoutAction.setChecked(data['efv_tselLayoutAction'])
        self.efv_aflLayoutAction.setChecked(data['efv_aflLayoutAction']),
        self.efv_hrsLayoutAction.setChecked(data['efv_hrsLayoutAction']),
        self.efv_tsrLayoutAction.setChecked(data['efv_tsrLayoutAction']),
        self.efv_tsrPlusLayoutAction.setChecked(data['efv_tsrPlusLayoutAction']),
        self.efv_obj2dLayoutAction.setChecked(data['efv_obj2dLayoutAction']),
        self.efv_obj3dLayoutAction.setChecked(data['efv_obj3dLayoutAction']),
        self.efv_lksIndLayoutAction.setChecked(data['efv_lksIndLayoutAction']),
        self.efv_lksParLayoutAction.setChecked(data['efv_lksParLayoutAction']),
        self.efv_lksHspLayoutAction.setChecked(data['efv_lksHspLayoutAction']),
        self.efv_lksReLayoutAction.setChecked(data['efv_lksReLayoutAction']),
        self.efv_lksBarLayoutAction.setChecked(data['efv_lksBarLayoutAction']),
        self.efv_lksHostLayoutAction.setChecked(data['efv_lksHostLayoutAction']),
        self.efv_lksNextLLayoutAction.setChecked(data['efv_lksNextLLayoutAction']),
        self.efv_lksNextRLayoutAction.setChecked(data['efv_lksNextRLayoutAction']),
        self.efv_lksBordLayoutAction.setChecked(data['efv_lksBordLayoutAction']),
        self.efv_fusLayoutAction.setChecked(data['efv_fusLayoutAction']),
        self.efv_fusPedLayoutAction.setChecked(data['efv_fusPedLayoutAction']),
        self.efv_tselLayoutAction.setChecked(data['efv_tselLayoutAction']),
        self.efv_tselPathLayoutAction.setChecked(data['efv_tselPathLayoutAction']),
        self.efv_pcaLayoutAction.setChecked(data['efv_pcaLayoutAction']),
        self.efv_failSafeLayoutAction.setChecked(data['efv_failSafeLayoutAction']),

        self.efv_gtLayoutAction.setChecked(data['efv_gtLayoutAction'])
        self.efv_bindMenu.updateComboBox()
        self.efv_bindMenu.setBinds(data['efv_binds'])
        self.efv_bindMenu.checkBox.setChecked(data['efv_autonext'])

    def clearProject(self):
        self.toolsStackWidget.setCurrentIndex(0)
        if not self.window().isMaximized():
            self.resize(400, 600)
        self.setWindowTitle('Analyst ToolKit')

        self.ff_rootEdit.setText('')
        self.ff_logsEdit.setPlainText('')
        self.ff_historyBox.setValue(1)
        self.ff_historyCheckBox.setChecked(False)
        self.ff_outputRadioBtn_1.setChecked(True)
        self.ff_outputRadioBtn_2.setChecked(False)
        self.ff_outputEdit.setText('')

        self.ar_exeEdit.setText('')
        self.ar_inputEdit.setText('')
        self.ar_folderRadio.setChecked(True)
        self.ar_fileRadio.setChecked(False)
        self.ar_logsList.clear()
        self.ar_historyCheckBox.setChecked(False)
        self.ar_historySpinBox.setValue(1)
        self.ar_paramsEdit.setText('-visopt -minout -endopt')
        oldState = self.ar_outDirBox.blockSignals(True)
        self.ar_outDirBox.setChecked(False)
        self.ar_outDirBox.blockSignals(oldState)

        self.ef_inputEdit.setText('')
        self.ef_folderRadio.setChecked(True)
        self.ef_fileRadio.setChecked(False)
        self.ef_matList.clear()
        self.ef_outputPath = None
        self.ef_details = False
        self.ef_dat2p0 = False
        self.ef_efsList = [[], [], [], [], [], [], [False]]

        self.efv_loadReportLine.setText('')
        self.efv_loadDataLine.setText('')
        self.efv_loadBox.setChecked(True)
        self.efv_frameEdit.setText('')
        self.efv_eventEdit.setText('')
        self.efv_currentEvent = 0
        self.efv_currentFrame = 0
        self.efv_header = []
        self.efv_videoHandler = None
        self.efv_mat = {'__path__': ''}
        self.efv_videoView.scene().clear()
        self.efv_nextFrameBtn.setEnabled(False)
        self.efv_prevFrameBtn.setEnabled(False)
        self.efv_frameEdit.setEnabled(False)
        try:
            oldModel, oldSelectionModel = self.efv_dataTable.model(), self.efv_dataTable.selectionModel()
            self.efv_dataTable.clearSpans()
            if oldModel is not None and oldSelectionModel is not None:
                oldModel.deleteLater()
                oldSelectionModel.deleteLater()
        except:
            pass
        self.efv_saveAction.setChecked(False)
        self.efv_tselLayoutAction.setChecked(False),
        self.efv_aflLayoutAction.setChecked(False),
        self.efv_hrsLayoutAction.setChecked(False),
        self.efv_tsrLayoutAction.setChecked(False),
        self.efv_tsrPlusLayoutAction.setChecked(False),
        self.efv_obj2dLayoutAction.setChecked(False),
        self.efv_obj3dLayoutAction.setChecked(False),
        self.efv_lksIndLayoutAction.setChecked(False),
        self.efv_lksParLayoutAction.setChecked(False),
        self.efv_lksHspLayoutAction.setChecked(False),
        self.efv_lksReLayoutAction.setChecked(False),
        self.efv_lksBarLayoutAction.setChecked(False),
        self.efv_lksHostLayoutAction.setChecked(False),
        self.efv_lksNextLLayoutAction.setChecked(False),
        self.efv_lksNextRLayoutAction.setChecked(False),
        self.efv_lksBordLayoutAction.setChecked(False),
        self.efv_fusLayoutAction.setChecked(False),
        self.efv_fusPedLayoutAction.setChecked(False),
        self.efv_tselLayoutAction.setChecked(False),
        self.efv_tselPathLayoutAction.setChecked(False),
        self.efv_pcaLayoutAction.setChecked(False),
        self.efv_failSafeLayoutAction.setChecked(False),
        self.efv_bindMenu.setBinds(['']*9)
        self.efv_bindMenu.checkBox.setChecked(False)
