# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customHeader.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(401, 525)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fieldsTree = QtWidgets.QTreeWidget(Dialog)
        self.fieldsTree.setDragEnabled(True)
        self.fieldsTree.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.fieldsTree.setObjectName("fieldsTree")
        self.verticalLayout.addWidget(self.fieldsTree)
        self.saveBtn = QtWidgets.QPushButton(Dialog)
        self.saveBtn.setObjectName("saveBtn")
        self.verticalLayout.addWidget(self.saveBtn)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Custom header"))
        self.fieldsTree.headerItem().setText(0, _translate("Dialog", "Mat fields"))
        self.saveBtn.setText(_translate("Dialog", "Save"))

