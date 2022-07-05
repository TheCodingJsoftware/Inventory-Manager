# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Code\Python-Projects\Inventory Manager\ui\download.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 528)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QtWidgets.QLabel(Dialog)
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(Dialog)
        self.stackedWidget.setEnabled(False)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.stackedWidget.setObjectName("stackedWidget")
        self.license_page = QtWidgets.QWidget()
        self.license_page.setObjectName("license_page")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.license_page)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(self.license_page)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 618, 455))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.license = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
        self.license.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.license.setFrameShadow(QtWidgets.QFrame.Plain)
        self.license.setLineWidth(0)
        self.license.setTabChangesFocus(False)
        self.license.setReadOnly(True)
        self.license.setBackgroundVisible(True)
        self.license.setObjectName("license")
        self.verticalLayout_5.addWidget(self.license)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.stackedWidget.addWidget(self.license_page)
        self.download_page = QtWidgets.QWidget()
        self.download_page.setEnabled(False)
        self.download_page.setObjectName("download_page")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.download_page)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.progressBar = QtWidgets.QProgressBar(self.download_page)
        self.progressBar.setEnabled(False)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_6.addWidget(self.progressBar)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.stackedWidget.addWidget(self.download_page)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_cancel = QtWidgets.QPushButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("f:\\Code\\Python-Projects\\Inventory Manager\\ui\\BreezeStyleSheets/dist/pyqt6/dark/dialog_cancel.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_cancel.setIcon(icon)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.button_previous = QtWidgets.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("f:\\Code\\Python-Projects\\Inventory Manager\\ui\\BreezeStyleSheets/dist/pyqt6/dark/left_arrow.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_previous.setIcon(icon1)
        self.button_previous.setObjectName("button_previous")
        self.horizontalLayout.addWidget(self.button_previous)
        self.button_next = QtWidgets.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("f:\\Code\\Python-Projects\\Inventory Manager\\ui\\BreezeStyleSheets/dist/pyqt6/dark/right_arrow.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_next.setIcon(icon2)
        self.button_next.setObjectName("button_next")
        self.horizontalLayout.addWidget(self.button_next)
        self.button_finished = QtWidgets.QPushButton(Dialog)
        self.button_finished.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("f:\\Code\\Python-Projects\\Inventory Manager\\ui\\BreezeStyleSheets/dist/pyqt6/dark/dialog_apply.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_finished.setIcon(icon3)
        self.button_finished.setObjectName("button_finished")
        self.horizontalLayout.addWidget(self.button_finished)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.setStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title.setText(_translate("Dialog", "TextLabel"))
        self.license.setDocumentTitle(_translate("Dialog", "License"))
        self.button_cancel.setText(_translate("Dialog", "Cancel"))
        self.button_previous.setText(_translate("Dialog", "Previous"))
        self.button_next.setText(_translate("Dialog", "Next"))
        self.button_finished.setText(_translate("Dialog", "Finished"))
