# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\fj7nmq\Documents\GIT_Repos\pythonTools\FORD_ADAS\analystToolKit\uis\resimViewer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(368, 459)
        Dialog.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.rv_loadDataLine = QtWidgets.QLineEdit(self.groupBox)
        self.rv_loadDataLine.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rv_loadDataLine.setReadOnly(True)
        self.rv_loadDataLine.setObjectName("rv_loadDataLine")
        self.gridLayout.addWidget(self.rv_loadDataLine, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rv_loadFolderBtn = QtWidgets.QPushButton(self.groupBox)
        self.rv_loadFolderBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rv_loadFolderBtn.setObjectName("rv_loadFolderBtn")
        self.gridLayout_2.addWidget(self.rv_loadFolderBtn, 0, 0, 1, 1)
        self.rv_synchronized = QtWidgets.QCheckBox(self.groupBox)
        self.rv_synchronized.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rv_synchronized.setChecked(True)
        self.rv_synchronized.setObjectName("rv_synchronized")
        self.gridLayout_2.addWidget(self.rv_synchronized, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_16.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_16.addItem(spacerItem1)
        self.splitter_2 = QtWidgets.QSplitter(self.splitter)
        self.splitter_2.setEnabled(True)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rv_dataTable = QtWidgets.QTableView(self.layoutWidget)
        self.rv_dataTable.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rv_dataTable.sizePolicy().hasHeightForWidth())
        self.rv_dataTable.setSizePolicy(sizePolicy)
        self.rv_dataTable.setMinimumSize(QtCore.QSize(10, 10))
        self.rv_dataTable.setMaximumSize(QtCore.QSize(1000000, 1000000))
        self.rv_dataTable.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rv_dataTable.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.rv_dataTable.setDragEnabled(True)
        self.rv_dataTable.setDragDropOverwriteMode(False)
        self.rv_dataTable.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.rv_dataTable.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.rv_dataTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.rv_dataTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.rv_dataTable.setSortingEnabled(True)
        self.rv_dataTable.setObjectName("rv_dataTable")
        self.rv_dataTable.horizontalHeader().setDefaultSectionSize(150)
        self.rv_dataTable.horizontalHeader().setMinimumSectionSize(110)
        self.rv_dataTable.horizontalHeader().setSortIndicatorShown(False)
        self.rv_dataTable.verticalHeader().setCascadingSectionResizes(False)
        self.rv_dataTable.verticalHeader().setMinimumSectionSize(10)
        self.rv_dataTable.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.rv_dataTable)
        self.verticalLayout_2.setStretch(0, 1)
        self.layoutWidget_2 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rv_videoView = QtWidgets.QGraphicsView(self.layoutWidget_2)
        self.rv_videoView.setObjectName("rv_videoView")
        self.verticalLayout_3.addWidget(self.rv_videoView)
        self.rv_videoSlider = QtWidgets.QSlider(self.layoutWidget_2)
        self.rv_videoSlider.setOrientation(QtCore.Qt.Horizontal)
        self.rv_videoSlider.setObjectName("rv_videoSlider")
        self.verticalLayout_3.addWidget(self.rv_videoSlider)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rv_prevFrameBtn = QtWidgets.QPushButton(self.layoutWidget_2)
        self.rv_prevFrameBtn.setEnabled(False)
        self.rv_prevFrameBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rv_prevFrameBtn.setAutoRepeat(True)
        self.rv_prevFrameBtn.setAutoRepeatDelay(150)
        self.rv_prevFrameBtn.setAutoRepeatInterval(0)
        self.rv_prevFrameBtn.setObjectName("rv_prevFrameBtn")
        self.horizontalLayout_2.addWidget(self.rv_prevFrameBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.rv_frameEdit = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.rv_frameEdit.setEnabled(False)
        self.rv_frameEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.rv_frameEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rv_frameEdit.setText("")
        self.rv_frameEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.rv_frameEdit.setObjectName("rv_frameEdit")
        self.horizontalLayout_2.addWidget(self.rv_frameEdit)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.rv_nextFrameBtn = QtWidgets.QPushButton(self.layoutWidget_2)
        self.rv_nextFrameBtn.setEnabled(False)
        self.rv_nextFrameBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rv_nextFrameBtn.setAutoRepeat(True)
        self.rv_nextFrameBtn.setAutoRepeatDelay(150)
        self.rv_nextFrameBtn.setAutoRepeatInterval(0)
        self.rv_nextFrameBtn.setObjectName("rv_nextFrameBtn")
        self.horizontalLayout_2.addWidget(self.rv_nextFrameBtn)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Resim Viewer"))
        self.groupBox.setTitle(_translate("Dialog", "Load file"))
        self.rv_loadFolderBtn.setStatusTip(_translate("Dialog", "Load resim input folder"))
        self.rv_loadFolderBtn.setText(_translate("Dialog", "Load logs folder"))
        self.rv_synchronized.setStatusTip(_translate("Dialog", "Check if resim viewer has to be synchronized with event finder viewer"))
        self.rv_synchronized.setText(_translate("Dialog", "Synchronized"))
        self.rv_prevFrameBtn.setStatusTip(_translate("Dialog", "Move to previous frame in current event (Left, Ctrl+left)"))
        self.rv_prevFrameBtn.setText(_translate("Dialog", "Prev frame"))
        self.rv_prevFrameBtn.setShortcut(_translate("Dialog", "Left"))
        self.rv_frameEdit.setStatusTip(_translate("Dialog", "Move to specified frame in current event"))
        self.rv_nextFrameBtn.setStatusTip(_translate("Dialog", "Move to next frame in current event (Right, Ctrl+Right)"))
        self.rv_nextFrameBtn.setText(_translate("Dialog", "Next frame"))
        self.rv_nextFrameBtn.setShortcut(_translate("Dialog", "Right"))

