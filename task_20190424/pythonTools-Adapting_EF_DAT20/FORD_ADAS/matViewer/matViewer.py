import os
import re
import json
import sys
from collections import defaultdict
import traceback

import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QMenu, QAction, QTreeWidget

from matChecker import matchecker

from matChecker.checkertable import CheckerTable

matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
plt.switch_backend('Qt5Agg')
import numpy as np

from PyQt5 import QtGui, QtCore, QtWidgets
from delphiTools3 import base as dt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import mw
import matComperator


def openMat(parent, path):
    is_dat2p0 = False
    var_name = None

    if parent.matLoadBox.isChecked():
        var_name='mudp'
    if parent.matLoadDAT2p0.isChecked():
        is_dat2p0 = True

    try:
        mat = dt.loadmat(path, variableName=var_name, sort=True, reBarrierMarge=False, dat2p0=is_dat2p0,
                         dot_dict=False)
        if not is_dat2p0:
            objData = mat['mudp']['vis']['vision_obstacles_info']['visObs']
            for key in objData.keys():
                if key in ['tlet_match', 'tlet_match_conf']:
                    newData = objData[key]
                    tempData = {}
                    for j in range(15):
                        tempData[key + '_' + str(j + 1).zfill(2)] = newData[:, j, :]
                    objData[key] = tempData
        return mat

    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.warning(parent, 'Error', 'Error while loading ' + path.split(os.sep)[-1] + '!')
        return


def constructPath(path, dots):
    if len(path) > 0:
        exception1 = ['mudp', 'vis', 'vision_obstacles_info', 'visObs', 'tlet_match']
        exception2 = ['mudp', 'vis', 'vision_obstacles_info', 'visObs', 'tlet_match_conf']
        if exception1 == path[:-1] or exception2 == path[:-1]:
            last = path[-1][-2:]
            if dots:
                return '.'.join(path[:-1])
            else:
                return "mat['" + "']['".join(path[:-1])[:-1] + "'][:,%d,:]" % (int(last) - 1)

        if dots:
            return '.'.join(path)
        else:
            return "mat['" + "']['".join(path) + "']"
    return ''


def _getColorMapper(lower, upper):
    diff = upper - lower
    lowerHue = 240
    upperHue = 359
    diffHue = upperHue - lowerHue

    def mapper(value):
        if value < lower:
            hue = lowerHue
        elif value > upper:
            hue = upperHue
        else:
            hue = ((value - lower) / diff) * diffHue + lowerHue
        return QColor.fromHsv(hue, 100, 255)

    return mapper


class gui(QtWidgets.QMainWindow, mw.Ui_MainWindow):
    itemChanged = QtCore.pyqtSignal(list)
    columnChanged = QtCore.pyqtSignal(int, int)

    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        if self.parent:
            self.move(self.parent.pos().x() + 40, self.parent.pos().y() + 40)
        self.show()

        self.loadMatBtn.clicked.connect(self.loadMatPath)
        self.fieldsTree.currentItemChanged.connect(self.showItem)
        self.valuesTable.currentItemChanged.connect(self.showPlot)
        self.actionCompare.triggered.connect(self.onCompare)

        self.figure, self.ax = plt.subplots(1, 1)
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plotLayout.addWidget(self.canvas)
        self.plotLayout.addWidget(self.toolbar)
        self.splitter.setSizes([self.height() // 2, self.height() // 2, self.height() // 10])

        self.is2ndWindow = False
        self.isMatLoaded = False
        self.matCheckButton.setEnabled(False)
        self._checkerTable = None

        self.lineFind.textChanged.connect(self._onFindTextEdited)
        self.regexCheck.stateChanged.connect(self._onRegexStateChange)
        self.index0Check.stateChanged.connect(self._onIndex0StateChange)
        self.matCheckButton.clicked.connect(self._onMatCheckButton)
        self.dotFormatCheck.stateChanged.connect(self._onDotFormatCheckChanged)
        self.colorsCheck.stateChanged.connect(self._onColorCheckChanged)

    def loadMatPath(self):
        path = str(self.loadMatEdit.text())
        if path == '':
            path = os.getcwd()
        f, result = QtWidgets.QFileDialog.getOpenFileName(self, directory=path, filter="*.mat")
        if f != '':
            self.loadMatEdit.setText(f)
            self.load()

    def load(self):
        path = str(self.loadMatEdit.text())
        self.mat = openMat(self, path)
        if not self.mat:
            return
        if not self.fieldsTree.currentItem() is None:
            lastPath = self.getFullTreePath(self.fieldsTree.currentItem())
        else:
            lastPath = ''

        # self.fieldsTree.currentItemChanged.connect(self.showItem)
        # self.valuesTable.currentItemChanged.connect(self.showPlot)

        self._appendPathToRecent(path)
        self.valuesTable.clear()
        self.fieldsTree.clear()
        self._fillTree(self.fieldsTree.invisibleRootItem(), self.mat, '')
        if lastPath:
            self.onItemChange(lastPath)

        self.isMatLoaded = True
        self.matCheckButton.setEnabled(True)
        self._onFindTextEdited('')

    def _loadPath(self, path):
        self.loadMatEdit.setText(path)
        self.load()

    def _appendPathToRecent(self, path):
        action = QAction(path, self)
        action.triggered.connect(lambda x: self._loadPath(path))
        self.menuOpenRecent.addAction(action)

    def _find(self, pattern):
        name_dict = defaultdict(int)

        def rec(data):
            acc = dict()
            for key, item in data.items():
                try:
                    re_match = re.search(pattern, key)
                except Exception as e:
                    re_match = None
                if isinstance(item, dict):
                    rec_result = rec(item)
                    if re_match is not None or len(rec_result) > 0:
                        acc[key] = rec_result
                elif re_match is not None:
                    if key in name_dict:
                        name_dict[key] += 1
                    else:
                        name_dict[key] = 0
                    acc[key] = key + '_' + str(name_dict[key])
            return acc

        def rec_contains(data):
            acc = dict()
            for key, item in data.items():
                re_match = pattern in key

                if isinstance(item, dict):
                    rec_result = rec_contains(item)
                    if re_match or len(rec_result) > 0:
                        acc[key] = rec_result
                elif re_match:
                    if key in name_dict:
                        name_dict[key] += 1
                    else:
                        name_dict[key] = 0
                    acc[key] = key + '_' + str(name_dict[key])
            return acc

        return rec(self.mat) if self.regexCheck.isChecked() else rec_contains(self.mat)

    def _fillTree(self, item, value, find):
        if type(value) is dict and isinstance(find, dict):
            for key, val in sorted(value.items()):
                if key in find:
                    child = QtWidgets.QTreeWidgetItem()
                    child.setText(0, key)
                    item.addChild(child)
                    self._fillTree(child, val, find[key])

    def _onFindTextEdited(self, text):
        if self.isMatLoaded:
            currentItem = self.fieldsTree.currentItem()
            # pathToCurrentItem = [] if currentItem is None else self.getFullTreePath(currentItem)
            self.valuesTable.clear()
            self.fieldsTree.clear()
            findResult = self._find(text)
            self._fillTree(self.fieldsTree.invisibleRootItem(), self.mat, findResult)
            # if len(pathToCurrentItem) > 0:
            #     item = self._getItemByPath(pathToCurrentItem)

    def _onRegexStateChange(self, value):
        self._onFindTextEdited(self.lineFind.text())

    def _onIndex0StateChange(self, value):
        self.showItem(self.fieldsTree.currentItem())

    def getFullTreePath(self, item):
        path = [str(item.text(0))]
        while item.parent():
            item = item.parent()
            path.append(str(item.text(0)))
        path.reverse()
        return path

    def _getItemByPath(self, path):
        item = self.fieldsTree.invisibleRootItem()
        for pathItem in path:
            children = [child for child in item.takeChildren() if child.text(0) == pathItem]
            if len(children) == 0:
                return None
            item = children[0]
        return item

    def showItem(self, item):
        if item == None:
            self.valuesTable.clear()
        else:
            self.valuesTable.clear()
            value = self.mat
            path = self.getFullTreePath(item)
            self.itemChanged.emit(path[:])
            self.linePath.setText(constructPath(path[:], self.dotFormatCheck.isChecked()))
            while path:
                value = value[path.pop(0)]
            if type(value) is dict:
                self.valuesTable.setRowCount(0)
                self.valuesTable.setColumnCount(0)
                self.valuesTable.setHorizontalHeaderLabels([])
            elif type(value) is list or type(value) is np.ndarray:
                if isinstance(value, np.ndarray):
                    minValue = np.min(value)
                    maxValue = np.max(value)
                elif isinstance(value, list):
                    minValue = min(value)
                    maxValue = max(value)
                else:
                    minValue, maxValue = 0, 1

                if minValue < maxValue and self.colorsCheck.isChecked():
                    mapper = _getColorMapper(minValue, maxValue)
                else:
                    mapper = None

                self.valuesTable.setRowCount(len(value))
                shift = 0 if self.index0Check.isChecked() else 1
                for i, v in enumerate(value):
                    if type(v) is list or type(v) is np.ndarray:
                        self.valuesTable.setColumnCount(len(v) + 1)
                        self.valuesTable.setHorizontalHeaderLabels(['Index'] +
                                                                   ['Value ' + str(number + shift) for number in range(len(v))])
                        self.valuesTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + shift)))
                        for j, each in enumerate(v):
                            item = QtWidgets.QTableWidgetItem(str(each))
                            if mapper is not None:
                                colorRGB = mapper(each)
                                item.setData(Qt.BackgroundRole, colorRGB)
                            self.valuesTable.setItem(i, j + 1, item)
                            # print(each, cmap(each))
                    else:
                        self.valuesTable.setColumnCount(2)
                        self.valuesTable.setHorizontalHeaderLabels(['Index', 'Value'])
                        self.valuesTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + shift)))
                        item = QtWidgets.QTableWidgetItem(str(v))
                        if mapper is not None:
                            colorRGB = mapper(v)
                            item.setData(Qt.BackgroundRole, colorRGB)
                        self.valuesTable.setItem(i, 1, item)
                        # print(v, cmap(v))
            else:
                self.valuesTable.setRowCount(1)
                self.valuesTable.setColumnCount(1)
                self.valuesTable.setHorizontalHeaderLabels(['Value'])
                self.valuesTable.setItem(0, 0, QtWidgets.QTableWidgetItem(str(value)))

            self.valuesTable.resizeColumnsToContents()
            self.showPlot()

    def showPlot(self):
        tableSize = self.valuesTable.rowCount(), self.valuesTable.columnCount()

        self.ax.axis('on')
        self.ax.cla()
        try:
            if self.valuesTable.currentColumn() == -1:
                self.ax.plot(range(tableSize[0]),
                        [float(self.valuesTable.item(i, 1).text())
                         for i in range(tableSize[0])])
            else:
                self.ax.plot(range(tableSize[0]),
                        [float(self.valuesTable.item(i, self.valuesTable.currentColumn()).text())
                         for i in range(tableSize[0])])
        except:
            self.ax.plot([0, 0], [0, 0])

        self.ax.grid()
        self.ax.set_xlabel('Frame number')
        self.ax.set_ylabel(str(self.fieldsTree.currentItem().text(0)))

        self.columnChanged.emit(self.valuesTable.currentRow(), self.valuesTable.currentColumn())
        self.canvas.get_default_filename = lambda: str(os.path.splitext(self.mat['mudp']['bfname'])[0])
        self.canvas.draw()

    def onItemChange(self, list):
        item = self.fieldsTree.invisibleRootItem()
        while list:
            name = list.pop(0)
            for i in range(item.childCount()):
                if item.child(i).text(0) == name:
                    item = item.child(i)
                    break
                elif i == item.childCount() - 1:
                    return
        self.fieldsTree.setCurrentItem(item, 0)

    def onColumnChange(self, row, col):
        self.valuesTable.setCurrentCell(row, col)

    def onCompare(self):
        if not self.is2ndWindow:
            self.window = gui(self)
            self.itemChanged.connect(self.window.onItemChange)
            self.columnChanged.connect(self.window.onColumnChange)
            self.is2ndWindow = True
        else:
            path = self.getFullTreePath(self.fieldsTree.currentItem())
            comp = matComperator.compareSignal(self.mat, self.window.mat, path, max(self.valuesTable.currentColumn(), 1), True)
            if comp:
                s1, s2 = comp[0], comp[1]
                if not len(np.where((s1 == s2)[~(s1 == s2).mask] == False)[0]):
                    self.fieldsTree.currentItem().setBackground(0, QtGui.QBrush(QtGui.QColor('green')))
                    self.window.fieldsTree.currentItem().setBackground(0, QtGui.QBrush(QtGui.QColor('green')))
                else:
                    self.fieldsTree.currentItem().setBackground(0, QtGui.QBrush(QtGui.QColor('red')))
                    self.window.fieldsTree.currentItem().setBackground(0, QtGui.QBrush(QtGui.QColor('red')))
                self.colorTable((s1 == s2)[~s1.mask], max(self.valuesTable.currentColumn(), 1))
                self.window.colorTable((s1 == s2)[~s2.mask], max(self.valuesTable.currentColumn(), 1))
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Cannot compare signals')

    def colorTable(self, signal, column):
        for i, s in enumerate(signal):
            if s == True:
                self.valuesTable.item(i, column).setBackground(QtGui.QBrush(QtGui.QColor('green')))
            elif s == False:
                self.valuesTable.item(i, column).setBackground(QtGui.QBrush(QtGui.QColor('red')))
            else:
                self.valuesTable.item(i, column).setBackground(QtGui.QBrush(QtGui.QColor('gray')))

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        report = str(e.mimeData().urls()[0].toString())
        if '///' in report:
            report = report.split('///')[1]
        else:
            report = '//' + report.split('//')[1]
        if os.path.isfile(report):
            self.loadMatEdit.setText(report)
            self.load()

    def closeEvent(self, *args, **kwargs):
        if self.parent:
            self.parent.is2ndWindow = False
        if self.is2ndWindow:
            self.window.close()
        self.deleteLater()

    def _onMatCheckButton(self):
        file, ok = QFileDialog.getOpenFileName(self, filter='Csv (*.csv)')
        if ok:
            df = matchecker.checkMatDict(self.mat, file)[['min', 'max', 'min_change_rate', 'max_change_rate']]
            self._checkerTable = CheckerTable(df)
            self._checkerTable.show()

    def _onDotFormatCheckChanged(self, state):
        item = self.fieldsTree.currentItem()
        if item is not None:
            path = self.getFullTreePath(item)
            self.linePath.setText(constructPath(path[:], self.dotFormatCheck.isChecked()))

    def _onColorCheckChanged(self, state):
        self.showItem(self.fieldsTree.currentItem())


def myExceptionhook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys.excepthook(exctype, value, traceback)
    sys.exit(1)


def main():
    sys.excepthook = myExceptionhook
    app = QtWidgets.QApplication(sys.argv)
    myGui = gui()
    app.exec_()


if __name__ == '__main__':
    main()
