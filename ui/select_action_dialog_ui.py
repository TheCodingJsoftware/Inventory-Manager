# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\jared\Documents\Code\Inventory-Manager\ui\select_action_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 310)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("QWidget#widget{\n"
"    border-top-left-radius:10px;\n"
"    border-bottom-left-radius:10px;\n"
"    border-top-right-radius:10px;\n"
"    border-bottom-right-radius:10px;\n"
"    border: 1px solid  rgb(0,120,212);;\n"
"}")
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblTitle = QtWidgets.QLabel(self.widget)
        self.lblTitle.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblTitle.setFont(font)
        self.lblTitle.setStyleSheet("background-color: rgb(0,120,212);\n"
"border-top-left-radius:10px;\n"
"border-top-right-radius:10px;\n"
"border: 1px solid  rgb(0,120,212);\n"
"")
        self.lblTitle.setFrameShape(QtWidgets.QFrame.Box)
        self.lblTitle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lblTitle.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblTitle.setObjectName("lblTitle")
        self.verticalLayout_3.addWidget(self.lblTitle)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.iconHolder = QtWidgets.QVBoxLayout()
        self.iconHolder.setSpacing(0)
        self.iconHolder.setObjectName("iconHolder")
        self.verticalLayout_2.addLayout(self.iconHolder)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 328, 236))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblMessage = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMessage.sizePolicy().hasHeightForWidth())
        self.lblMessage.setSizePolicy(sizePolicy)
        self.lblMessage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblMessage.setWordWrap(True)
        self.lblMessage.setObjectName("lblMessage")
        self.verticalLayout_4.addWidget(self.lblMessage)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_4.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setObjectName("buttonsLayout")
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblTitle.setText(_translate("Form", "TextLabel"))
        self.lblMessage.setText(_translate("Form", "TextLabel"))