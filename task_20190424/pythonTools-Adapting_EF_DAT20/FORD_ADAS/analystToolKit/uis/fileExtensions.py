# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fileExtensions.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(176, 288)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBox_ALL = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_ALL.setObjectName("checkBox_ALL")
        self.verticalLayout_2.addWidget(self.checkBox_ALL)
        self.checkBox_1 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_1.setChecked(True)
        self.checkBox_1.setObjectName("checkBox_1")
        self.verticalLayout_2.addWidget(self.checkBox_1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_2.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setChecked(False)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_2.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_2.addWidget(self.checkBox_4)
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_5.setChecked(True)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_2.addWidget(self.checkBox_5)
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_6.setChecked(True)
        self.checkBox_6.setObjectName("checkBox_6")
        self.verticalLayout_2.addWidget(self.checkBox_6)
        self.checkBox_7 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_7.setChecked(True)
        self.checkBox_7.setObjectName("checkBox_7")
        self.verticalLayout_2.addWidget(self.checkBox_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_8 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_8.setText("")
        self.checkBox_8.setObjectName("checkBox_8")
        self.horizontalLayout_2.addWidget(self.checkBox_8)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.acceptBtn = QtWidgets.QPushButton(Dialog)
        self.acceptBtn.setObjectName("acceptBtn")
        self.horizontalLayout.addWidget(self.acceptBtn)
        self.rejectBtn = QtWidgets.QPushButton(Dialog)
        self.rejectBtn.setObjectName("rejectBtn")
        self.horizontalLayout.addWidget(self.rejectBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "File Extensions"))
        self.groupBox.setTitle(_translate("Dialog", "Choose extensions:"))
        self.checkBox_ALL.setText(_translate("Dialog", "ALL"))
        self.checkBox_1.setText(_translate("Dialog", ".dvl"))
        self.checkBox_2.setText(_translate("Dialog", ".mudp"))
        self.checkBox_3.setText(_translate("Dialog", ".tavi"))
        self.checkBox_4.setText(_translate("Dialog", ".mat"))
        self.checkBox_5.setText(_translate("Dialog", ".avi"))
        self.checkBox_6.setText(_translate("Dialog", ".ffs"))
        self.checkBox_7.setText(_translate("Dialog", ".tapi"))
        self.acceptBtn.setText(_translate("Dialog", "OK"))
        self.rejectBtn.setText(_translate("Dialog", "Cancel"))
