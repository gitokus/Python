# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(527, 361)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.settingsTree = QtWidgets.QTreeWidget(Dialog)
        self.settingsTree.setItemsExpandable(True)
        self.settingsTree.setObjectName("settingsTree")
        item_0 = QtWidgets.QTreeWidgetItem(self.settingsTree)
        item_0.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.verticalLayout.addWidget(self.settingsTree)
        self.saveBtn = QtWidgets.QPushButton(Dialog)
        self.saveBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.saveBtn.setObjectName("saveBtn")
        self.verticalLayout.addWidget(self.saveBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.settingsWidgets = QtWidgets.QStackedWidget(Dialog)
        self.settingsWidgets.setObjectName("settingsWidgets")
        self.General = QtWidgets.QWidget()
        self.General.setObjectName("General")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.General)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.General)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.General)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.generalNameEdit = QtWidgets.QLineEdit(self.General)
        self.generalNameEdit.setObjectName("generalNameEdit")
        self.verticalLayout_3.addWidget(self.generalNameEdit)
        self.generalEmail = QtWidgets.QLineEdit(self.General)
        self.generalEmail.setObjectName("generalEmail")
        self.verticalLayout_3.addWidget(self.generalEmail)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 266, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.settingsWidgets.addWidget(self.General)
        self.horizontalLayout.addWidget(self.settingsWidgets)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(Dialog)
        self.settingsWidgets.setCurrentIndex(0)
        self.generalNameEdit.returnPressed.connect(Dialog.setFocus)
        self.generalEmail.returnPressed.connect(Dialog.setFocus)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.settingsTree.headerItem().setText(0, _translate("Dialog", "Settings"))
        __sortingEnabled = self.settingsTree.isSortingEnabled()
        self.settingsTree.setSortingEnabled(False)
        self.settingsTree.topLevelItem(0).setText(0, _translate("Dialog", "General"))
        self.settingsTree.setSortingEnabled(__sortingEnabled)
        self.saveBtn.setText(_translate("Dialog", "Save and Close"))
        self.label.setText(_translate("Dialog", "Analyst Name:"))
        self.label_2.setText(_translate("Dialog", "Email:"))

