import qdarktheme
from PyQt5 import uic
from PyQt5.QtCore import QFile, Qt, QTextStream
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget

from utils.json_file import JsonFile

settings_file = JsonFile(file_name="settings")


class AboutDialog(QWidget):
    """
    About dialog
    """

    def __init__(self, title: str, version: str, updated: str, home: str):
        super(AboutDialog, self).__init__()
        uic.loadUi("ui/about.ui", self)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("icons/icon.png"))
        self.setFixedSize(550, 400)

        pixmap = QPixmap("icons/icon.png")
        scaled_pixmap = pixmap.scaled(self.lblIcon.size(), Qt.KeepAspectRatio)

        self.lblIcon.setFixedSize(100, 100)
        self.lblIcon.setPixmap(scaled_pixmap)

        self.lblVersion.setText(f"Build time: {updated}")

        with open("LICENSE", "r") as license_file:
            self.lblLicense.setText(license_file.read())

        self.lblTitle.setText(f"{title} {version}")

        self.lblHome.setText(
            f"Home: <a style='text-decoration:none;color:yellow'href='{home}'>{home}</a>"
        )

        self.scrollArea.setStyleSheet("border: 0px")

        self.btnClose.clicked.connect(self.close)

        if settings_file.get_value(item_name="dark_mode"):
            stylesheet_file = QFile("ui/BreezeStyleSheets/dist/qrc/dark/stylesheet.qss")
        else:
            stylesheet_file = QFile("ui/BreezeStyleSheets/dist/qrc/light/stylesheet.qss")

        stylesheet_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(stylesheet_file)
        self.setStyleSheet(stream.readAll())
