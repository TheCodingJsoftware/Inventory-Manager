from functools import partial

from PyQt5 import QtSvg, uic
from PyQt5.QtCore import QFile, Qt, QTextStream
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton

from utils.dialog_buttons import DialogButtons
from utils.dialog_icons import Icons
from utils.json_file import JsonFile

settings_file = JsonFile(file_name="settings")


class InputDialog(QDialog):
    """
    Input dialog
    """

    def __init__(
        self,
        parent=None,
        icon_name: str = Icons.question,
        button_names: str = DialogButtons.ok_cancel,
        title: str = __name__,
        message: str = "",
    ) -> None:
        """
        It's a function that takes in a bunch of arguments and sets them to variables

        Args:
          parent: The parent widget of the dialog. If no parent is given, the dialog will be shown as a
        window.
          icon_name (str): str = Icons.question,
          button_names (str): str = DialogButtons.ok_cancel,
          title (str): str = __name__,
          message (str): str = "",
        """
        super(InputDialog, self).__init__(parent)
        uic.loadUi("ui/input_dialog.ui", self)

        self.icon_name = icon_name
        self.button_names = button_names
        self.title = title
        self.message = message
        self.inputText: str = ""
        self.theme: str = (
            "dark" if settings_file.get_value(item_name="dark_mode") else "light"
        )

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("icons/icon.png"))

        self.lblTitle.setText(self.title)
        self.lblMessage.setText(self.message)
        self.lineEditInput.returnPressed.connect(self.input_enter_pressed)

        self.load_dialog_buttons()

        svg_icon = self.get_icon(icon_name)
        svg_icon.setFixedSize(62, 50)
        self.iconHolder.addWidget(svg_icon)

        self.resize(300, 150)

        self.load_theme()

        self.lineEditInput.selectAll()

    def load_theme(self) -> None:
        """
        It loads the stylesheet.qss file from the theme folder
        """
        stylesheet_file = QFile(
            f"ui/BreezeStyleSheets/dist/qrc/{self.theme}/stylesheet.qss"
        )
        stylesheet_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(stylesheet_file)
        self.setStyleSheet(stream.readAll())

    def get_icon(self, path_to_icon: str) -> QtSvg.QSvgWidget:
        """
        It returns a QSvgWidget object that is initialized with a path to an SVG icon

        Args:
          path_to_icon (str): The path to the icon you want to use.

        Returns:
          A QSvgWidget object.
        """
        return QtSvg.QSvgWidget(
            f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/{path_to_icon}"
        )

    def button_press(self, button) -> None:
        """
        The function is called when a button is pressed. It sets the response to the text of the button
        that was pressed, and the inputText to the text in the lineEditInput. Then it accepts the dialog

        Args:
          button: The button that was clicked.
        """
        self.response = button.text()
        self.inputText = self.lineEditInput.text()
        self.accept()

    def input_enter_pressed(self) -> None:
        """
        It takes the text from the lineEditInput widget and puts it into the inputText variable
        """
        self.response = "Ok"
        self.inputText = self.lineEditInput.text()
        self.accept()

    def load_dialog_buttons(self) -> None:
        """
        It takes a string of button names, splits them into a list, and then creates a button for each
        name in the list
        """
        button_names = self.button_names.split(", ")
        for name in button_names:
            button = QPushButton(name)
            button.setFixedWidth(100)
            if name == DialogButtons.copy:
                button.setToolTip("Will copy this window to your clipboard.")
            elif name == DialogButtons.save and self.icon_name == Icons.critical:
                button.setToolTip("Will save this error log to the logs directory.")
            button.clicked.connect(partial(self.button_press, button))
            self.buttonsLayout.addWidget(button)

    def get_response(self) -> str:
        """
        This function returns the response of the class

        Returns:
          The response
        """
        return self.response
