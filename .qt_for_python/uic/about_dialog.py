# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Code\Python-Projects\Inventory Manager\dist\ui\about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
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
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblIcon = QtWidgets.QLabel(self.widget)
        self.lblIcon.setMinimumSize(QtCore.QSize(100, 100))
        self.lblIcon.setText("")
        self.lblIcon.setObjectName("lblIcon")
        self.verticalLayout_2.addWidget(self.lblIcon)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblVersion = QtWidgets.QLabel(self.widget)
        self.lblVersion.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lblVersion.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblVersion.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblVersion.setObjectName("lblVersion")
        self.verticalLayout.addWidget(self.lblVersion)
        self.lblTitle = QtWidgets.QLabel(self.widget)
        self.lblTitle.setObjectName("lblTitle")
        self.verticalLayout.addWidget(self.lblTitle)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.lblHome = QtWidgets.QLabel(self.widget)
        self.lblHome.setTextFormat(QtCore.Qt.RichText)
        self.lblHome.setOpenExternalLinks(True)
        self.lblHome.setObjectName("lblHome")
        self.verticalLayout_3.addWidget(self.lblHome)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setStyleSheet("subcontrol-position: top center")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 360, 69))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblLicense = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lblLicense.setText("")
        self.lblLicense.setObjectName("lblLicense")
        self.horizontalLayout_3.addWidget(self.lblLicense)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btnClose = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMaximumSize(QtCore.QSize(70, 16777215))
        self.btnClose.setStyleSheet("\n"
"        QPushButton#btnClose{\n"
"            background-color: #3daee9;\n"
"            border: 0.04em solid  #3daee9;\n"
"            border-radius: 5px;\n"
"        }\n"
"        QPushButton#btnClose:hover{\n"
"            background-color: #49b3eb;\n"
"            border: 0.04em solid  #49b3eb;\n"
"            border-radius: 5px;\n"
"        }\n"
"        QPushButton#btnClose:pressed{\n"
"            background-color: #5cbaed;\n"
"            color: #bae2f8;\n"
"            border: 0.04em solid  #5cbaed;\n"
"            border-radius: 5px;\n"
"        }")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("f:\\Code\\Python-Projects\\Inventory Manager\\dist\\ui\\BreezeStyleSheets/dist/pyqt6/dark/dialog_ok.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClose.setIcon(icon)
        self.btnClose.setCheckable(False)
        self.btnClose.setDefault(True)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout_5.addWidget(self.btnClose)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblVersion.setText(_translate("Form", "TextLabel"))
        self.lblTitle.setText(_translate("Form", "TextLabel"))
        self.lblHome.setText(_translate("Form", "TextLabel"))
        self.groupBox.setTitle(_translate("Form", "MIT License"))
        self.btnClose.setText(_translate("Form", "  OK"))
