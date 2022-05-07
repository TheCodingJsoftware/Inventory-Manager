# Form implementation generated from reading ui file 'f:\Code\Python-Projects\Inventory Manager\ui\main.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionDarkmode = QtGui.QAction(MainWindow)
        self.actionDarkmode.setCheckable(True)
        self.actionDarkmode.setObjectName("actionDarkmode")
        self.actionAbout_Qt = QtGui.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionView_License = QtGui.QAction(MainWindow)
        self.actionView_License.setObjectName("actionView_License")
        self.actionCheck_for_updates = QtGui.QAction(MainWindow)
        self.actionCheck_for_updates.setObjectName("actionCheck_for_updates")
        self.actionCheck_for_Updates = QtGui.QAction(MainWindow)
        self.actionCheck_for_Updates.setObjectName("actionCheck_for_Updates")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionUpload_Changes = QtGui.QAction(MainWindow)
        self.actionUpload_Changes.setObjectName("actionUpload_Changes")
        self.actionGet_Changes = QtGui.QAction(MainWindow)
        self.actionGet_Changes.setObjectName("actionGet_Changes")
        self.menuFile.addAction(self.actionUpload_Changes)
        self.menuFile.addAction(self.actionGet_Changes)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSettings.addAction(self.actionDarkmode)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuHelp.addAction(self.actionView_License)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionCheck_for_Updates)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit program"))
        self.actionDarkmode.setText(_translate("MainWindow", "Darkmode"))
        self.actionDarkmode.setStatusTip(_translate("MainWindow", "Toggle between darkmode and lightmode"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionView_License.setText(_translate("MainWindow", "View License"))
        self.actionCheck_for_updates.setText(_translate("MainWindow", "Check for updates"))
        self.actionCheck_for_Updates.setText(_translate("MainWindow", "Check for Updates..."))
        self.actionCheck_for_Updates.setStatusTip(_translate("MainWindow", "Checks for new updates on GitHub"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionUpload_Changes.setText(_translate("MainWindow", "Upload Changes"))
        self.actionUpload_Changes.setStatusTip(_translate("MainWindow", "Upload all files online for other users"))
        self.actionGet_Changes.setText(_translate("MainWindow", "Get Changes"))
        self.actionGet_Changes.setStatusTip(_translate("MainWindow", "Get latest changes from the online database"))
