from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QLineEdit, \
    QVBoxLayout

import pandas as pd


def _getBrush(value):
    if 'error' in value:
        return QColor(200, 0, 0)
    if 'ok' in value:
        return QColor(0, 200, 0)
    else:
        return QColor(255, 255, 255)


class CheckerTable(QWidget):

    def __init__(self, table, parent=None):
        super().__init__(parent)

        self._errors = table[(table['max'].str.contains('error')) | (table['min'].str.contains('error')) |
                       (table.max_change_rate.str.contains('error')) | (table.min_change_rate.str.contains('error'))]
        self._filtered = self._errors.copy()

        self.setWindowTitle('Checker Table')
        self.setGeometry(400, 400, 900, 600)
        self._layout = QVBoxLayout(self)

        self._textFilter = QLineEdit(self)
        self._textFilter.textEdited.connect(self._onFilterTextEdited)
        self._layout.addWidget(self._textFilter)

        self._table = QTableWidget(self._errors.shape[0], self._errors.shape[1], self)
        self._layout.addWidget(self._table)

        self._saveButton = QPushButton('Save to csv')
        self._saveButton.clicked.connect(self._onSaveButtonClicked)
        self._layout.addWidget(self._saveButton)

        self.setLayout(self._layout)

        self._updateErrorsTable()

    def _updateErrorsTable(self):
        self._table.reset()
        self._table.setRowCount(self._filtered.shape[0])
        self._table.setColumnCount(self._filtered.shape[1])

        self._table.setVerticalHeaderLabels(list(self._filtered.index))
        self._table.setHorizontalHeaderLabels(list(self._filtered.columns))

        for row, (path, rowData) in enumerate(self._filtered.iterrows()):
            for column, (name, value) in enumerate(rowData.iteritems()):
                item = QTableWidgetItem(value)
                item.setBackground(_getBrush(value))
                self._table.setItem(row, column, item)

        self._table.resizeColumnsToContents()

    def _onSaveButtonClicked(self):
        path, ok = QFileDialog.getSaveFileName(self, filter='Csv (*.csv)')
        if ok:
            self._errors.to_csv(path)

    def _onFilterTextEdited(self, text):
        self._filtered = self._errors[self._errors.index.str.contains(text)]
        self._updateErrorsTable()