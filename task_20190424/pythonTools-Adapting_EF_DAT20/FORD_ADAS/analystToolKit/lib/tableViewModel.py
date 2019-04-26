import numpy as np
import operator
from PyQt5 import QtCore, QtWidgets
from copy import deepcopy
from functools import reduce

from delphiTools3 import enumerations as enum


class TableViewModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mat, header, currentFrame):
        super(self.__class__, self).__init__(parent)
        self.customHeader = header
        self.mat = mat
        if self.mat['__project__'] == 'CADS3.5':
            self.index = np.argwhere(self.mat['mudp']['vis']['vision_traffic_sign_info'][
                                          'imageIndex'] == currentFrame)[0, 0]
        else:
            self.index = np.argwhere(self.mat['mudp']['vis']['vision_AEB_info']['visAEB'][
                                         'imageIndex'] == currentFrame)[0, 0]

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.customHeader)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 1

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == QtCore.Qt.DisplayRole:
            if Qt_Orientation == QtCore.Qt.Horizontal:
                return 'Value'
            if Qt_Orientation == QtCore.Qt.Vertical:
                return self.customHeader[p_int][-1]
        if int_role == QtCore.Qt.ToolTipRole:
            if Qt_Orientation == QtCore.Qt.Horizontal:
                return 'Value of header field'
            if Qt_Orientation == QtCore.Qt.Vertical:
                return '.'.join(self.customHeader[p_int])

    def data(self, QModelIndex, int_role=None):
        if int_role == QtCore.Qt.DisplayRole:
            value = self.mat
            path = deepcopy(self.customHeader[QModelIndex.row()])
            while path:
                value = value[path.pop(0)]
            return self.phraseData(value, self.customHeader[QModelIndex.row()][-1])

    def getDataByHeader(self, header, save=False):
        value = self.mat
        path = deepcopy(header)
        while path:
            value = value[path.pop(0)]
        return self.phraseData(value, header[-1], raw=True, save=save)

    def phraseData(self, data, header, raw=False, save=False):
        if header == 'groundtruth':
            if 'gtID' in self.mat.keys() and self.mat['gtID'] != '':
                gid = self.mat['mudp']['vis']['vision_traffic_sign_info']['imageIndex'][self.index]
                if int(self.mat['gtID']) in data[gid].keys():
                    obj = data[gid][int(self.mat['gtID'])]
                    gt = '{}:\n'.format(obj['objType'])
                    gt += '  id: {}\n'.format(obj['objID'])
                    for key in obj['infoDict'].keys():
                        gt += '  {}: {}\n'.format(key, obj['infoDict'][key])
                    return gt
            return ''

        if type(data) == np.ndarray and len(data.shape) > 1:
            if 'eventColumnID' in self.mat.keys() and int(self.mat['eventColumnID']) != -1:
                col = int(self.mat['eventColumnID'])
                return str(self.phraseData(data[self.index][col], header, raw))
            else:
                if save:
                    sep = ' '
                else:
                    sep = '\n'
                return sep.join([str(self.phraseData(d, header, raw)) for d in data[self.index]])
        elif (type(data) == np.ndarray and len(data.shape) == 1) or type(data) == list:
            return self.phraseData(data[self.index], header, raw)
        else:
            if not raw and header in dir(enum):
                return eval(f'enum.{header}({data})')
            elif raw and header.endswith('_corrected') and header[:-10] in dir(enum):
                return eval(f'enum.{header[:-10]}("{data}", reverse=True)')
            else:
                value = data
                if isinstance(value, np.float64):
                    value = np.round(value, 4)
                elif isinstance(value, float):
                    value = round(value, 4)
                return str(value)

    def setData(self, QModelIndex, QVariant, int_role=None):
        if int_role == QtCore.Qt.EditRole and QVariant != '' \
                and QVariant != self.data(QModelIndex, QtCore.Qt.DisplayRole):
            full_name = self.customHeader[QModelIndex.row()]
            name = full_name[-1]
            if name == 'groundtruth':
                return False
            corrected_name = self.customHeader[QModelIndex.row()][-1] + '_corrected'
            corrected_full_name = full_name[:-1] + [corrected_name]
            if name in ['analysisStatus']:
                self.mat['analysisStatus'] = QVariant
            elif not name.endswith('_corrected'):
                if not corrected_full_name in self.customHeader:
                    self.customHeader.insert(self.customHeader.index(full_name) + 1, corrected_full_name)
                field = reduce(operator.getitem, corrected_full_name[:-1], self.mat)
                field[corrected_name] = QVariant
            else:
                field = reduce(operator.getitem, full_name[:-1], self.mat)
                field[name] = QVariant
            self.parent().efv_updateModel()
            self.dataChanged.emit(QModelIndex, QModelIndex)
            return True
        return False

    def setDataByHeader(self, header, data):
        if header in self.customHeader:
            row = self.customHeader.index(header)
            self.setData(self.createIndex(row, 0), data, QtCore.Qt.EditRole)
            return True
        else:
            return False

    def flags(self, QModelIndex):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled


class CustomDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        header = str(QModelIndex.model().headerData(QModelIndex.row(), QtCore.Qt.Vertical, QtCore.Qt.DisplayRole))
        if self.isEnum(header):
            ComboBox = QtWidgets.QComboBox(QWidget)
            ComboBox.setDuplicatesEnabled(False)
            return ComboBox
        else:
            EditLine = QtWidgets.QLineEdit(QWidget)
            return EditLine

    def setEditorData(self, QWidget, QModelIndex):
        current = QModelIndex.model().data(QModelIndex, QtCore.Qt.DisplayRole)
        header = str(QModelIndex.model().headerData(QModelIndex.row(), QtCore.Qt.Vertical, QtCore.Qt.DisplayRole))
        if self.isEnum(header):
            if header.endswith('_corrected'):
                header = header[:-10]
            for item in ([current] + [eval('enum.'+header+'(x)') for x
                                      in range(0, 101) if eval('enum.'+header+'(x)') != 'Reserved']):
                if QWidget.findText(item) == -1:
                    QWidget.addItem(item)
        else:
            QWidget.setText(str(current))

    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        header = str(QModelIndex.model().headerData(QModelIndex.row(), QtCore.Qt.Vertical, QtCore.Qt.DisplayRole))
        if self.isEnum(header):
            QAbstractItemModel.setData(QModelIndex, str(QWidget.currentText()), QtCore.Qt.EditRole)
        else:
            QAbstractItemModel.setData(QModelIndex, str(QWidget.text()), QtCore.Qt.EditRole)

    def isEnum(self, header):
        if header in dir(enum):
            return True
        elif header.endswith('_corrected') and header[:-10] in dir(enum):
            return True
        else:
            return False

    def getComboIndexes(self, model):
        indexes = []
        for i in range(model.rowCount()):
            header = str(model.headerData(i, QtCore.Qt.Vertical, QtCore.Qt.DisplayRole))
            if self.isEnum(header):
                idx = model.createIndex(i, 0)
                indexes.append(idx)
        return indexes
