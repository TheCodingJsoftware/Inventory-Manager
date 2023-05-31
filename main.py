# sourcery skip: avoid-builtin-shadow
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QCursor, QFont, QIcon, QPixmap, QPalette
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QAction,
    QApplication,
    QCheckBox,
    QComboBox,
    QCompleter,
    QDoubleSpinBox,
    QFileDialog,
    QFileSystemModel,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMenu,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QFontDialog,
    QSpinBox,
    QSplashScreen,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QToolBox,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QWidgetItem,
    qApp,
)

from threads.changes_thread import ChangesThread
from threads.download_images_thread import DownloadImagesThread
from threads.download_thread import DownloadThread
from threads.load_nests import LoadNests
from threads.remove_quantity import RemoveQuantityThread
from threads.send_sheet_report_thread import SendReportThread
from threads.upload_quoted_inventory import UploadBatch
from threads.upload_thread import UploadThread
from ui.about_dialog import AboutDialog
from ui.add_item_dialog import AddItemDialog
from ui.add_item_dialog_price_of_steel import AddItemDialogPriceOfSteel
from ui.custom_widgets import (
    ClickableLabel,
    CustomTableWidget,
    CustomTabWidget,
    DeletePushButton,
    ExchangeRateComboBox,
    HumbleDoubleSpinBox,
    MultiToolBox,
    NotesPlainTextEdit,
    OrderStatusButton,
    PartInformationViewer,
    PdfTreeView,
    POPushButton,
    PriorityComboBox,
    RecutButton,
    RichTextPushButton,
    ViewTree,
    set_default_dialog_button_stylesheet,
    set_status_button_stylesheet,
)
from ui.generate_quote_dialog import GenerateQuoteDialog
from ui.image_viewer import QImageViewer
from ui.input_dialog import InputDialog
from ui.load_window import LoadWindow
from ui.message_dialog import MessageDialog
from ui.select_item_dialog import SelectItemDialog
from ui.set_custom_limit_dialog import SetCustomLimitDialog
from ui.theme import set_theme
from ui.web_scrape_results_dialog import WebScrapeResultsDialog
from utils.compress import compress_database, compress_folder
from utils.dialog_buttons import DialogButtons
from utils.dialog_icons import Icons
from utils.extract import extract
from utils.generate_quote import GenerateQuote
from utils.history_file import HistoryFile
from utils.inventory_excel_file import ExcelFile
from utils.json_file import JsonFile
from utils.json_object import JsonObject
from utils.po import check_po_directories, get_all_po
from utils.po_template import POTemplate
from utils.price_history_file import PriceHistoryFile
from utils.trusted_users import get_trusted_users
from web_scrapers.ebay_scraper import EbayScraper
from web_scrapers.exchange_rate import ExchangeRate

__author__: str = "Jared Gross"
__copyright__: str = "Copyright 2022-2023, TheCodingJ's"
__credits__: list[str] = ["Jared Gross"]
__license__: str = "MIT"
__name__: str = "Invigo"
__version__: str = "v2.0.3"
__updated__: str = "2023-05-27 12:32:51"
__maintainer__: str = "Jared Gross"
__email__: str = "jared@pinelandfarms.ca"
__status__: str = "Production"

import ast
import contextlib
import configparser
import json
import logging
import operator as op
import os
import shutil
import subprocess
import sys
import threading
import time
import markdown
import webbrowser
import winsound
from datetime import datetime
from functools import partial
from typing import Any

operators: dict = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
}


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


def default_settings() -> None:
    """
    It checks if a setting exists in the settings file, and if it doesn't, it creates
    it with a default value
    """
    check_setting(setting="exchange_rate", default_value=1.0)
    check_setting(setting="dark_mode", default_value=True)
    check_setting(setting="sort_ascending", default_value=False)
    check_setting(setting="sort_descending", default_value=True)
    check_setting(setting="sort_quantity_in_stock", default_value=True)
    check_setting(setting="sort_priority", default_value=False)
    check_setting(setting="sort_alphabatical", default_value=False)
    check_setting(setting="server_ip", default_value="10.0.0.93")
    check_setting(setting="server_port", default_value=80)
    check_setting(setting="server_buffer_size", default_value=8192)
    check_setting(setting="server_time_out", default_value=10)
    check_setting(
        setting="geometry",
        default_value={"x": 200, "y": 200, "width": 1200, "height": 600},
    )
    check_setting(
        setting="last_opened",
        default_value=str(datetime.now()),
    )
    check_setting(setting="last_category_tab", default_value=0)
    check_setting(setting="last_toolbox_tab", default_value=0)
    check_setting(setting="last_dock_location", default_value=2)
    check_setting(setting="change_quantities_by", default_value="Category")
    check_setting(setting="inventory_file_name", default_value="inventory")
    check_setting(setting="path_to_order_number", default_value="order_number.json")
    check_setting(setting="trusted_users", default_value=["itsme", "jared", "joseph"])
    check_setting(setting="quote_nest_directories", default_value=[])
    font = QFont("MS Shell Dlg 2", 8)
    font_data = {
        "family": font.family(),
        "pointSize": font.pointSize(),
        "weight": font.weight(),
        "italic": font.italic(),
    }
    check_setting(setting="tables_font", default_value=font_data)
    check_setting(
        setting="menu_tabs_order",
        default_value=[
            "Edit Inventory",
            "Sheets in Inventory",
            "Parts in Inventory",
            "Quote Generator",
            "View Inventory (Read Only)",
            "View Removed Quantities History (Read Only)",
            "View Price Changes History (Read Only)",
        ],
    )
    check_setting(
        setting="category_tabs_order",
        default_value={
            "Edit Inventory": [],
            "Sheets in Inventory": [],
            "Parts in Inventory": [],
        },
    )
    check_setting(
        setting="price_history_file_name",
        default_value=str(datetime.now().strftime("%B %d %A %Y")),
    )
    check_setting(
        setting="days_until_new_price_history_assessment",
        default_value=90,
    )


def check_setting(setting: str, default_value) -> None:
    """
    If the setting is not in the settings file, add it with the default value

    Args:
      setting (str): The name of the setting to check.
      default_value: The default value of the setting.
    """
    if settings_file.get_value(item_name=setting) is None:
        settings_file.add_item(item_name=setting, value=default_value)


def check_folders(folders: list[str]) -> None:
    """
    If the folder doesn't exist, create it

    Args:
      folders (list): list = ["data", "data/images", "data/images/thumbnails", "data/images/fullsize",
    "data/images/fullsize/temp"]
    """
    for folder in folders:
        with contextlib.suppress(FileExistsError):
            if not os.path.exists(folder):
                os.mkdir(folder)


def _play_celebrate_sound() -> None:
    winsound.PlaySound("sound.wav", winsound.SND_FILENAME)


check_folders(
    folders=[
        "logs",
        "data",
        "images",
        "backups",
        "Price History Files",
        "excel files",
        "PO's",
        "PO's/templates",
    ]
)

logging.basicConfig(
    filename="logs/app.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


settings_file = JsonFile(file_name="settings")

default_settings()
inventory = JsonFile(file_name=f"data/{settings_file.get_value(item_name='inventory_file_name')}")
price_of_steel_inventory = JsonFile(file_name=f"data/{settings_file.get_value(item_name='inventory_file_name')} - Price of Steel")
parts_in_inventory = JsonFile(file_name=f"data/{settings_file.get_value(item_name='inventory_file_name')} - Parts in Inventory")
price_of_steel_information = JsonFile(file_name="price_of_steel_information.json")

geometry = JsonObject(JsonFile=settings_file, object_name="geometry")
category_tabs_order = JsonObject(JsonFile=settings_file, object_name="category_tabs_order")

history_file_date = datetime.strptime(settings_file.get_value("price_history_file_name"), "%B %d %A %Y")
days_from_last_price_history_assessment: int = int((datetime.now() - history_file_date).total_seconds() / 60 / 60 / 24)


class MainWindow(QMainWindow):
    """The class MainWindow inherits from the class QMainWindow"""

    def __init__(self):
        """
        It loads the UI and starts a thread that checks for changes in a JSON file.
        """
        super().__init__()
        uic.loadUi("ui/main_menu.ui", self)
        self.username = os.getlogin().title()
        self.trusted_user: bool = False
        self.setWindowTitle(f"{__name__} - {__version__} - {self.username}")
        self.setWindowIcon(QIcon(Icons.icon))

        check_po_directories()
        self.check_for_updates(on_start_up=True)

        if days_from_last_price_history_assessment > settings_file.get_value("days_until_new_price_history_assessment"):
            settings_file.add_item("price_history_file_name", str(datetime.now().strftime("%B %d %A %Y")))
            self.show_message_dialog(
                title="Price Assessment",
                message=f"It has been {settings_file.get_value('days_until_new_price_history_assessment')} days until the last price assessment. A new price history file has been created in the 'Price History Files' directory.",
            )

        # VARIABLES
        self.theme: str = "dark"

        self.po_buttons: list[QPushButton] = []
        self.categories: list[str] = []
        self.active_layout: QVBoxLayout = None
        self.active_json_file: JsonFile = None
        self.category: str = ""
        self.is_nest_generated_from_parts_in_inventory: bool = False
        self.downloading_changes: bool = False
        self.finished_downloading_all_files: bool = False
        self.files_downloaded_count: int = 0
        self.tables_font = QFont()
        self.tables_font.setFamily(settings_file.get_value("tables_font")["family"])
        self.tables_font.setPointSize(settings_file.get_value("tables_font")["pointSize"])
        self.tables_font.setWeight(settings_file.get_value("tables_font")["weight"])
        self.tables_font.setItalic(settings_file.get_value("tables_font")["italic"])
        self.tabs: dict[str, CustomTableWidget] = {}
        self.inventory_file_name: str = settings_file.get_value(item_name="inventory_file_name")
        self.last_item_selected_index: int = 0
        self.last_item_selected_name: str = None
        self.last_selected_menu_tab: str = settings_file.get_value("menu_tabs_order")[settings_file.get_value("last_toolbox_tab")]
        self.threads = []
        self.quote_nest_directories_list_widgets = {}
        self.quote_nest_information = {}
        self.sheet_nests_toolbox: MultiToolBox = None
        self.get_upload_file_response: bool = True
        self.margins = (15, 15, 5, 5)  # top, bottom, left, right
        self.margin_format = (
            f"margin-top: {self.margins[0]}%; margin-bottom: {self.margins[1]}%; margin-left: {self.margins[2]}%; margin-right: {self.margins[3]}%;"
        )
        self.download_all_files()
        self.start_changes_thread(
            [
                f"{self.inventory_file_name}.json",
                f"{self.inventory_file_name} - Price of Steel.json",
                f"{self.inventory_file_name} - Parts in Inventory.json",
            ]
        )
        self.check_trusted_user()
        self.__load_ui()
        self.tool_box_menu_changed()
        self.quantities_change()
        self.start_exchange_rate_thread()
        # self.show()
        with contextlib.suppress(AttributeError):
            self.centralwidget.setEnabled(False)
        if geometry.get_value("x") == 0 and geometry.get_value("y") == 0:
            self.showMaximized()
        else:
            self.setGeometry(
                geometry.get_value("x"),
                geometry.get_value("y") + 30,
                geometry.get_value("width"),
                geometry.get_value("height") - 7,
            )
        self.show_whats_new()

    def __load_ui(self) -> None:
        """
        It loads the UI
        """

        menu_tabs_order = settings_file.get_value(item_name="menu_tabs_order")
        for tab_name in menu_tabs_order:
            index = self.get_tab_from_name(tab_name)
            if index != -1:
                self.tabWidget.tabBar().moveTab(index, menu_tabs_order.index(tab_name))

        self.lineEdit_search_items.textChanged.connect(self.update_list_widget)
        self.radioButton_category.toggled.connect(self.quantities_change)
        self.radioButton_single.toggled.connect(self.quantities_change)

        if settings_file.get_value(item_name="change_quantities_by") == "Category":
            self.radioButton_category.setChecked(True)
            self.radioButton_single.setChecked(False)
        else:
            self.radioButton_category.setChecked(False)
            self.radioButton_single.setChecked(True)

        # Tool Box
        self.tabWidget.setCurrentIndex(settings_file.get_value(item_name="last_toolbox_tab"))
        self.tabWidget.currentChanged.connect(self.tool_box_menu_changed)

        # Send report button
        self.pushButton_send_sheet_report.clicked.connect(self.send_sheet_report)
        self.pushButton_send_sheet_report.setIcon(QIcon("ui/BreezeStyleSheets/dist/pyqt6/dark/send_email.png"))

        # Load Nests
        self.comboBox_global_sheet_thickness.addItems(price_of_steel_information.get_value("thicknesses"))
        self.comboBox_global_sheet_thickness.wheelEvent = lambda event: None
        self.comboBox_global_sheet_thickness.activated.connect(self.global_nest_thickness_change)
        self.comboBox_global_sheet_thickness.setEnabled(False)
        self.comboBox_global_sheet_material.addItems(price_of_steel_information.get_value("materials"))
        self.comboBox_global_sheet_material.wheelEvent = lambda event: None
        self.comboBox_global_sheet_material.activated.connect(self.global_nest_material_change)
        self.comboBox_global_sheet_material.setEnabled(False)

        self.tableWidget_quote_items = CustomTableWidget(self)
        self.tableWidget_quote_items.set_editable_column_index([4])

        self.tableWidget_quote_items.setEnabled(False)
        self.tableWidget_quote_items.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_quote_items.setShowGrid(False)
        self.tableWidget_quote_items.setColumnCount(7)
        # tab.setAlternatingRowColors(True)
        self.tableWidget_quote_items.setSortingEnabled(False)
        self.tableWidget_quote_items.setSelectionBehavior(1)
        self.tableWidget_quote_items.setSelectionMode(1)
        self.tableWidget_quote_items.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget_quote_items.setHorizontalHeaderLabels(("Item;Part name;Material;Thickness;Qty;Recut;Add Part to Inventory;;").split(";"))
        self.clear_layout(self.verticalLayout_25)
        self.verticalLayout_25.addWidget(self.tableWidget_quote_items)

        self.pushButton_load_nests.clicked.connect(self.process_selected_nests)
        self.pushButton_clear_selections.clicked.connect(self.clear_nest_selections)
        self.pushButton_refresh_directories.clicked.connect(self.refresh_nest_directories)
        self.pushButton_generate_quote.clicked.connect(self.generate_quote)
        self.pushButton_generate_quote.setEnabled(False)

        # Status
        self.status_button = RichTextPushButton(self, '<p style="color:red;">Downloading all files... Please wait!</p>')
        self.status_button.setObjectName("status_button")
        self.status_button.setFlat(True)
        self.status_button.setFixedHeight(25)
        self.verticalLayout_status.addWidget(self.status_button)
        set_status_button_stylesheet(button=self.status_button, color="red")

        # Tab widget
        # self.load_categories()
        self.pushButton_create_new.clicked.connect(self.add_item)
        self.pushButton_add_new_sheet.clicked.connect(self.add_sheet_item)
        self.pushButton_add_quantity.clicked.connect(self.add_quantity)
        # self.pushButton_add_quantity.setEnabled(False)
        self.pushButton_add_quantity.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/list_add.png"))
        self.pushButton_remove_quantity.clicked.connect(self.remove_quantity)
        # self.pushButton_remove_quantity.setEnabled(False)
        self.pushButton_remove_quantity.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/list_remove.png"))
        self.pushButton_remove_quantities_from_inventory.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/list_remove.png"))
        self.listWidget_itemnames.itemSelectionChanged.connect(self.listWidget_item_changed)

        self.pushButton_remove_quantities_from_inventory.clicked.connect(self.remove_quantity_from_part_inventory)

        # Action events
        # HELP
        self.actionAbout_Qt.triggered.connect(qApp.aboutQt)
        self.actionAbout_Qt.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        self.actionCheck_for_Updates.triggered.connect(self.check_for_updates)
        self.actionCheck_for_Updates.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/refresh.png"))
        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.actionAbout.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/about.png"))
        self.actionRelease_Notes.triggered.connect(partial(self.show_whats_new, True))
        self.actionRelease_Notes.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/release_notes.png"))
        self.actionWebsite.triggered.connect(self.open_website)
        self.actionWebsite.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/website.png"))
        # PRINT
        self.actionPrint_Inventory.triggered.connect(self.print_inventory)

        # SETTINGS
        self.actionChange_tables_font.triggered.connect(self.change_tables_font)
        self.actionSet_Order_Number.triggered.connect(self.set_order_number)

        # SORT BY
        self.actionAlphabatical.triggered.connect(
            partial(
                self.action_group,
                "sorting",
                [
                    self.actionQuantity_in_Stock,
                    self.actionPriority,
                    self.actionAlphabatical,
                ],
            )
        )
        self.actionAlphabatical.setChecked(settings_file.get_value(item_name="sort_alphabatical"))
        self.actionAlphabatical.setEnabled(not settings_file.get_value(item_name="sort_alphabatical"))
        self.actionQuantity_in_Stock.triggered.connect(
            partial(
                self.action_group,
                "sorting",
                [
                    self.actionQuantity_in_Stock,
                    self.actionPriority,
                    self.actionAlphabatical,
                ],
            )
        )
        self.actionQuantity_in_Stock.setChecked(settings_file.get_value(item_name="sort_quantity_in_stock"))
        self.actionQuantity_in_Stock.setEnabled(not settings_file.get_value(item_name="sort_quantity_in_stock"))
        self.actionPriority.triggered.connect(
            partial(
                self.action_group,
                "sorting",
                [
                    self.actionQuantity_in_Stock,
                    self.actionPriority,
                    self.actionAlphabatical,
                ],
            )
        )
        self.actionPriority.setChecked(settings_file.get_value(item_name="sort_priority"))
        self.actionPriority.setEnabled(not settings_file.get_value(item_name="sort_priority"))
        self.actionAscending.triggered.connect(partial(self.action_group, "order", [self.actionAscending, self.actionDescending]))
        self.actionAscending.setChecked(settings_file.get_value(item_name="sort_ascending"))
        self.actionAscending.setEnabled(not settings_file.get_value(item_name="sort_ascending"))
        self.actionDescending.triggered.connect(partial(self.action_group, "order", [self.actionAscending, self.actionDescending]))
        self.actionDescending.setChecked(settings_file.get_value(item_name="sort_descending"))
        self.actionDescending.setEnabled(not settings_file.get_value(item_name="sort_descending"))
        self.actionSort.triggered.connect(self.sort_inventory)
        self.update_sorting_status_text()

        # PURCHASE ORDERS
        self.actionAdd_Purchase_Order.triggered.connect(partial(self.add_po_templates, [], True))
        self.actionRemove_Purchase_Order.triggered.connect(self.delete_po)
        self.actionOpen_Purchase_Order.triggered.connect(partial(self.open_po, None))
        self.actionOpen_Folder.triggered.connect(partial(self.open_folder, "PO's"))

        # QUOTE GENERATOR
        config = configparser.ConfigParser()
        config.read("laser_quote_variables.cfg")
        self.path_to_save_quotes = config.get("GLOBAL VARIABLES", "path_to_save_quotes")
        self.path_to_save_workorders = config.get("GLOBAL VARIABLES", "path_to_save_workorders")
        self.actionAdd_Nest_Directory.triggered.connect(self.add_nest_directory)
        self.actionRemove_Nest_Directory.triggered.connect(self.remove_nest_directory)
        self.actionOpen_Quotes_Directory.triggered.connect(partial(self.open_folder, self.path_to_save_quotes))
        self.actionOpen_Workorders_Directory.triggered.connect(partial(self.open_folder, self.path_to_save_workorders))
        # FILE
        self.menuOpen_Category.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/folder.png"))
        self.actionCreate_Category.triggered.connect(self.create_new_category)
        self.actionCreate_Category.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/list_add.png"))
        self.actionDelete_Category.triggered.connect(self.delete_category)
        self.actionDelete_Category.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/list_remove.png"))
        self.actionClone_Category.triggered.connect(self.clone_category)
        self.actionClone_Category.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/tab_duplicate.png"))

        self.actionBackup.triggered.connect(self.backup_database)
        self.actionBackup.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/backup.png"))
        self.actionLoad_Backup.triggered.connect(partial(self.load_backup, None))

        self.actionOpen_Item_History.triggered.connect(self.open_item_history)

        self.actionExit.triggered.connect(self.close)
        self.actionExit.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/tab_close.png"))

        if not self.trusted_user:
            self.tabWidget.setTabEnabled(settings_file.get_value("menu_tabs_order").index("Edit Inventory"), False)
            self.tabWidget.setTabEnabled(
                settings_file.get_value("menu_tabs_order").index("View Price Changes History (Read Only)"),
                False,
            )
            self.tabWidget.setTabEnabled(
                settings_file.get_value("menu_tabs_order").index("View Removed Quantities History (Read Only)"),
                False,
            )

    # ! \/ SLOTS & SIGNALS \/
    def quick_load_category(self, name: str) -> None:
        """
        This function sets the current tab index of a tab widget based on the name of a category and
        then loads the tab.

        Args:
          name (str): The name of the category that needs to be loaded.
        """
        self.tab_widget.setCurrentIndex(category_tabs_order.get_value(self.tabWidget.tabText(self.tabWidget.currentIndex())).index(name))
        self.load_active_tab()

    def tool_box_menu_changed(self) -> None:
        """
        This function changes the active layout and menu options based on the selected tab in a GUI.
        """
        inventory.load_data()
        price_of_steel_inventory.load_data()
        parts_in_inventory.load_data()
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "View Inventory (Read Only)":  # View Inventory (Read Only)
            self.menuSort.setEnabled(False)
            self.menuOpen_Category.setEnabled(False)
            self.active_layout = self.verticalLayout_4
            self.load_tree_view(inventory)
            self.status_button.setHidden(True)
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Edit Inventory":  # Edit Inventory
            if not self.trusted_user:
                self.show_not_trusted_user()
                return
            self.menuSort.setEnabled(True)
            self.menuOpen_Category.setEnabled(True)
            self.active_json_file = inventory
            self.active_layout = self.verticalLayout
            self.load_categories()
            self.status_button.setHidden(False)
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":  # Sheets in Inventory
            self.menuSort.setEnabled(True)
            self.menuOpen_Category.setEnabled(True)
            self.active_json_file = price_of_steel_inventory
            self.active_layout = self.verticalLayout_10
            self.load_categories()
            self.status_button.setHidden(False)
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Parts in Inventory":  # Parts in Inventory
            self.menuSort.setEnabled(True)
            self.menuOpen_Category.setEnabled(True)
            self.active_json_file = parts_in_inventory
            self.active_layout = self.verticalLayout_11
            self.load_categories()
            self.status_button.setHidden(False)
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Quote Generator":  # Quote Generator
            self.menuSort.setEnabled(False)
            self.menuOpen_Category.setEnabled(False)
            self.load_quote_generator_ui()
            self.status_button.setHidden(False)
        elif (
            self.tabWidget.tabText(self.tabWidget.currentIndex()) == "View Removed Quantities History (Read Only)"
        ):  # View Removed Quantities History (Read Only)
            self.menuSort.setEnabled(False)
            self.menuOpen_Category.setEnabled(False)
            if not self.trusted_user:
                self.show_not_trusted_user()
                return
            self.active_layout = self.verticalLayout_5
            self.load_history_view()
            self.status_button.setHidden(True)
        elif (
            self.tabWidget.tabText(self.tabWidget.currentIndex()) == "View Price Changes History (Read Only)"
        ):  # View Price Changes History (Read Only)
            self.menuSort.setEnabled(False)
            self.menuOpen_Category.setEnabled(False)
            if not self.trusted_user:
                self.show_not_trusted_user()
                return
            self.active_layout = self.horizontalLayout_8
            self.load_price_history_view()
            self.status_button.setHidden(True)
        settings_file.add_item("last_toolbox_tab", self.tabWidget.currentIndex())
        self.last_selected_menu_tab = self.tabWidget.tabText(self.tabWidget.currentIndex())

    def move_to_category(self, tab: CustomTableWidget, category: str) -> None:
        """
        This function moves selected parts from one category to another in a custom table widget and
        updates the inventory accordingly.

        Args:
          tab (CustomTableWidget): CustomTableWidget object representing the table widget where the
        selected parts are located.
          category (str): A string representing the category to which the selected parts will be moved.
        """
        selected_parts = self.get_all_selected_parts(tab)
        for selected_part in selected_parts:
            copy_of_item = parts_in_inventory.get_data()[self.category][selected_part]
            parts_in_inventory.remove_object_item(self.category, selected_part)
            parts_in_inventory.add_item_in_object(category, selected_part)
            parts_in_inventory.change_object_item(category, selected_part, copy_of_item)
        self.load_active_tab()
        self.sync_changes()

    def copy_to_category(self, tab: CustomTableWidget, category: str) -> None:
        """
        This function copies selected parts from one category to another in a custom table widget and
        syncs the changes.

        Args:
          tab (CustomTableWidget): CustomTableWidget object representing the table widget where the
        selected parts are located.
          category (str): A string representing the category to which the selected parts will be copied.
        """
        selected_parts = self.get_all_selected_parts(tab)
        for selected_part in selected_parts:
            copy_of_item = parts_in_inventory.get_data()[self.category][selected_part]
            parts_in_inventory.add_item_in_object(category, selected_part)
            parts_in_inventory.change_object_item(category, selected_part, copy_of_item)
        self.sync_changes()

    def add_sheet_item(self) -> None:
        """
        It adds an item to a category

        Returns:
          The response from the dialog.
        """
        add_item_dialog = AddItemDialogPriceOfSteel(
            title=f'Add new item to "{self.category}"',
            message=f"Adding a new item to \"{self.category}\".\n\nPress 'Add' when finished.",
        )

        if add_item_dialog.exec_():
            response = add_item_dialog.get_response()
            if response == DialogButtons.add:
                name: str = add_item_dialog.get_name()
                category_data = price_of_steel_inventory.get_value(item_name=self.category)
                for item in list(category_data.keys()):
                    if name == item:
                        self.show_error_dialog(
                            "Invalid name",
                            f"'{name}'\nis an invalid item name.\n\nCan't be the same as other names.",
                            dialog_buttons=DialogButtons.ok,
                        )
                        return

                price_of_steel_inventory.add_item_in_object(self.category, name)
                material: str = add_item_dialog.get_material()
                sheet_dimension: str = add_item_dialog.get_sheet_dimension()
                thickness: str = add_item_dialog.get_thickness()
                current_quantity: int = add_item_dialog.get_current_quantity()
                group: str = add_item_dialog.get_group()

                price_of_steel_inventory.change_object_in_object_item(self.category, name, "current_quantity", current_quantity)
                price_of_steel_inventory.change_object_in_object_item(self.category, name, "sheet_dimension", sheet_dimension)
                price_of_steel_inventory.change_object_in_object_item(self.category, name, "thickness", thickness)
                price_of_steel_inventory.change_object_in_object_item(self.category, name, "material", material)
                if group != "None":
                    price_of_steel_inventory.change_object_in_object_item(self.category, name, "group", group)
                price_of_steel_inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_current_quantity",
                    f"{self.username} - Item added at {datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                # self.sort_inventory()
                self.load_active_tab()
                self.sync_changes()
            elif response == DialogButtons.cancel:
                return

    def order_status_button(self, item_name: str, button: OrderStatusButton, row_index: int) -> None:
        """
        This function updates the "is_order_pending" value of an item in a steel inventory object based
        on the status of an order status button.

        Args:
          item_name (str): A string representing the name of the item for which the order status button
        is being updated.
          button (OrderStatusButton): The button parameter is an instance of
        the OrderStatusButton class, which is a graphical user interface (GUI) element that allows the
        user to toggle the status of an order. The isChecked() method of the OrderStatusButton class
        returns a boolean value indicating whether the button is currently checked or not
        """
        price_of_steel_inventory.change_object_in_object_item(
            object_name=self.category,
            item_name=item_name,
            value_name="is_order_pending",
            new_value=button.isChecked(),
        )
        self.load_active_tab()
        self.sync_changes()

    def name_change(self, tab: CustomTableWidget) -> None:
        """
        It checks if the name is the same as any other name in the category, and if it is, it sets the
        name back to the old name and displays an error message

        Args:
          category (str): str
          old_name (str): The name of the item before it was changed.
          name (QLineEdit): QLineEdit

        Returns:
          The return value is the result of the last expression evaluated in the function.
        """
        old_name = self.get_all_selected_parts(tab)[0]
        new_name: str = None
        input_dialog = InputDialog(
            title="New Name",
            message=f'Enter a new name for: "{old_name}"',
            placeholder_text=old_name,
        )
        if input_dialog.exec_():
            response = input_dialog.get_response()
            if response == DialogButtons.ok:
                new_name = input_dialog.inputText
            elif response == DialogButtons.cancel:
                return
        category_data = self.active_json_file.get_value(item_name=self.category)
        for item in list(category_data.keys()):
            if new_name == item:
                self.show_error_dialog(
                    "Invalid name",
                    f'"{new_name}" is an invalid item name. Can\'t be the same as other names.',
                    dialog_buttons=DialogButtons.ok,
                )
                return
        self.active_json_file.change_item_name(self.category, old_name, new_name)
        self.sort_inventory()

    def use_exchange_rate_change(self, category: str, item_name: str, value_name: str, combo: QComboBox) -> None:
        """
        It changes the exchange rate

        Args:
          category (str): str - The category of the item
          item_name (QLineEdit): QLineEdit
          value_name (str): str = The name of the value to change
          combo (QComboBox): QComboBox
        """
        self.value_change(
            category,
            item_name,
            value_name,
            combo.currentText() == "USD",
        )
        tab = self.tabs[self.category]
        tab.blockSignals(True)
        row_index = tab.selectedItems()[0].row()
        price: float = self.get_value_from_category(item_name=item_name, key="price")
        current_quantity: float = self.get_value_from_category(item_name=item_name, key="current_quantity")
        unit_quantity: float = self.get_value_from_category(item_name=item_name, key="unit_quantity")
        modified_date: float = self.get_value_from_category(item_name=item_name, key="latest_change_price")
        use_exchange_rate: bool = self.get_value_from_category(item_name=item_name, key="use_exchange_rate")
        converted_price: float = price * self.get_exchange_rate() if use_exchange_rate else price / self.get_exchange_rate()
        # ITEM PRICE
        price_item = tab.item(row_index, 4)
        price_item.setText(f'${price:,.2f} {"USD" if use_exchange_rate else "CAD"}')
        price_item.setToolTip(f'${converted_price:,.2f} {"CAD" if use_exchange_rate else "USD"}\n{modified_date}')
        # TOTAL COST IN STOCK
        total_cost_in_stock_item = tab.item(row_index, 6)
        total_cost_in_stock_item.setText(f'${(price*max(current_quantity, 0)):,.2f} {"USD" if use_exchange_rate else "CAD"}')
        # TOTAL UNIT COST
        total_unit_cost_item = tab.item(row_index, 7)
        total_unit_cost_item.setText(f'${(price*unit_quantity):,.2f} {"USD" if use_exchange_rate else "CAD"}')
        tab.blockSignals(False)
        self.update_stock_costs()
        self.sync_changes()

    def priority_change(self, category: str, item_name: str, value_name: str, combo: QComboBox) -> None:
        """
        It changes the priority of a task

        Args:
          category (str): str - The category of the item
          item_name (QLineEdit): QLineEdit
          value_name (str): str = The name of the value to change
          combo (QComboBox): QComboBox
        """

        self.value_change(category, item_name, value_name, combo.currentIndex())
        if combo.currentText() == "Medium":
            combo.setStyleSheet(f"color: yellow; border-color: gold; background-color: #413C28;{self.margin_format}")
        elif combo.currentText() == "High":
            combo.setStyleSheet(f"color: red; border-color: darkred; background-color: #3F1E25;{self.margin_format}")
        else:
            combo.setStyleSheet(self.margin_format)
        self.sync_changes()

    def notes_changed(self, category: str, item_name: str, value_name: str, note: QPlainTextEdit) -> None:
        """
        It takes the category, item name, value name, and note as parameters and then calls the
        value_change function with the category, item name, value name, and note as parameters

        Args:
          category (str): str = The category of the item.
          item_name (QLineEdit): QLineEdit
          value_name (str): str = The name of the value that is being changed.
          note (QPlainTextEdit): QPlainTextEdit
        """
        data = inventory.get_data()
        part_number = self.get_value_from_category(item_name, "part_number")
        self.value_change(self.category, item_name, value_name, note.toPlainText())

        for category, items in data.items():
            if category == self.category:
                continue
            for item, item_data in items.items():
                if part_number == item_data.get("part_number"):
                    inventory.change_object_in_object_item(object_name=category, item_name=item, value_name="notes", new_value=note.toPlainText())
        self.sync_changes()

    def delete_item(self, category: str, item_name: str) -> None:
        """
        It removes an item from the inventory

        Args:
          category (str): str
          item_name (QLineEdit): QLineEdit
        """
        self.active_json_file.remove_object_item(category, item_name)
        self.load_active_tab()
        self.sync_changes()

    def quantities_change(self) -> None:
        """
        If the radio button is checked, then the list widget is disabled, the add and remove buttons are
        enabled, and the add and remove buttons are connected to the add and remove quantity functions
        """
        if self.radioButton_category.isChecked():
            self.label.setText("Batches Multiplier:")
            self.pushButton_add_quantity.setText("Add Quantities")
            self.pushButton_remove_quantity.setText("Remove Quantities")
            settings_file.add_item(item_name="change_quantities_by", value="Category")
            # self.listWidget_itemnames.setEnabled(False)
            self.listWidget_itemnames.clearSelection()
            self.pushButton_add_quantity.setEnabled(False)
            self.pushButton_remove_quantity.setEnabled(True)

            # self.pushButton_add_quantity.disconnect()
            self.pushButton_remove_quantity.disconnect()

            self.pushButton_remove_quantity.clicked.connect(self.remove_quantity_from_category)
            self.spinBox_quantity.setValue(0)
        else:
            self.pushButton_remove_quantity.setEnabled(False)
            self.pushButton_add_quantity.setEnabled(False)
            self.listWidget_itemnames.clearSelection()
            self.label.setText("Quantity:")
            self.pushButton_add_quantity.setText("Add Quantity")
            self.pushButton_remove_quantity.setText("Remove Quantity")
            settings_file.add_item(item_name="change_quantities_by", value="Item")

    def remove_quantity_from_category(self) -> None:
        """
        It removes a quantity of items from a category
        """
        are_you_sure_dialog = self.show_message_dialog(
            title="Are you sure?",
            message=f'Removing quantities from the whole selected category.\n\nAre you sure you want to remove a multiple of {self.spinBox_quantity.value()} quantities from each item in "{self.category}"?',
            dialog_buttons=DialogButtons.no_yes_cancel,
        )
        if are_you_sure_dialog in [DialogButtons.no, DialogButtons.cancel]:
            return
        self.play_celebrate_sound()
        history_file = HistoryFile()
        history_file.add_new_to_category(
            date=datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"),
            description=f"Removed a multiple of {self.spinBox_quantity.value()} quantities from each item in {self.category}",
        )

        if self.spinBox_quantity.value() > 1:
            history_file.add_new_to_category(
                date=datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"),
                description=f"Removed a multiple of {self.spinBox_quantity.value()} quantities from each item in {self.category}",
            )
        elif self.spinBox_quantity.value() == 1:
            history_file.add_new_to_category(
                date=datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"),
                description=f"Removed a multiple of {self.spinBox_quantity.value()} quantity from each item in {self.category}",
            )

        self.status_button.setText("This may take awhile, please wait...", "yellow")
        self.radioButton_category.setEnabled(False)
        self.radioButton_single.setEnabled(False)
        self.pushButton_add_quantity.setEnabled(False)
        self.pushButton_remove_quantity.setEnabled(False)
        self.pushButton_create_new.setEnabled(False)
        self.centralwidget.setEnabled(False)
        self.listWidget_itemnames.setEnabled(False)

        remove_quantity_thread = RemoveQuantityThread(
            inventory,
            self.category,
            self.spinBox_quantity.value(),
        )
        remove_quantity_thread.signal.connect(self.remove_quantity_thread_response)
        self.threads.append(remove_quantity_thread)
        remove_quantity_thread.start()

        self.spinBox_quantity.setValue(0)

    # NOTE for EDIT INVENTORY
    def add_quantity(self, item_name: str, old_quantity: int) -> None:
        """
        It adds the value of the spinbox to the quantity of the item selected in the listwidget

        Args:
          item_name (str): str = the name of the item
          old_quantity (int): int = the quantity of the item before the change
        """
        are_you_sure_dialog = self.show_message_dialog(
            title="Are you sure?",
            message=f'Adding quantities to a single item.\n\nAre you sure you want to add {self.spinBox_quantity.value()} quantities to "{item_name}"?',
            dialog_buttons=DialogButtons.no_yes_cancel,
        )
        if are_you_sure_dialog in [DialogButtons.no, DialogButtons.cancel]:
            return
        data = inventory.get_data()
        part_number: str = data[self.category][item_name]["part_number"]
        current_quantity: int = data[self.category][item_name]["current_quantity"]
        inventory.change_object_in_object_item(self.category, item_name, "current_quantity", current_quantity + self.spinBox_quantity.value())
        inventory.change_object_in_object_item(
            self.category,
            item_name,
            "latest_change_current_quantity",
            f"{self.username} - Changed from {current_quantity} to {current_quantity + self.spinBox_quantity.value()} at {datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
        )
        for category in inventory.get_keys():
            if category == self.category:
                continue
            for item in list(data[category].keys()):
                if part_number == data[category][item]["part_number"]:
                    current_quantity: int = data[category][item]["current_quantity"]
                    inventory.change_object_in_object_item(category, item, "current_quantity", current_quantity + self.spinBox_quantity.value())
                    inventory.change_object_in_object_item(
                        category,
                        item,
                        "latest_change_current_quantity",
                        f"{self.username} - Changed from {current_quantity} to {current_quantity + self.spinBox_quantity.value()} at {datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                    )
        self.pushButton_add_quantity.setEnabled(False)
        self.pushButton_remove_quantity.setEnabled(False)
        self.listWidget_itemnames.setCurrentRow(self.last_item_selected_index)
        self.listWidget_item_changed()
        self.update_category_total_stock_costs()
        self.sort_inventory()
        self.sync_changes()

    # NOTE for EDIT INVENTORY
    def remove_quantity(self, item_name: str, old_quantity: int) -> None:
        """
        It removes the quantity of an item from the inventory

        Args:
          item_name (str): str = the name of the item
          old_quantity (int): int = the quantity of the item before the change
        """
        are_you_sure_dialog = self.show_message_dialog(
            title="Are you sure?",
            message=f'Removing quantities from a single item.\n\nAre you sure you want to remove {self.spinBox_quantity.value()} quantities to "{item_name}"?',
            dialog_buttons=DialogButtons.no_yes_cancel,
        )
        if are_you_sure_dialog in [DialogButtons.no, DialogButtons.cancel]:
            return

        history_file = HistoryFile()
        if self.spinBox_quantity.value() > 1:
            history_file.add_new_to_single_item(
                date=datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"),
                description=f'Removed {self.spinBox_quantity.value()} quantities from "{item_name}"',
            )
        elif self.spinBox_quantity.value() == 1:
            history_file.add_new_to_single_item(
                date=datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"),
                description=f'Removed {self.spinBox_quantity.value()} quantity from "{item_name}"',
            )

        data = inventory.get_data()
        part_number: str = self.get_value_from_category(item_name, "part_number")
        current_quantity: int = self.get_value_from_category(item_name, "current_quantity")
        inventory.change_object_in_object_item(self.category, item_name, "current_quantity", current_quantity - self.spinBox_quantity.value())
        inventory.change_object_in_object_item(
            self.category,
            item_name,
            "latest_change_current_quantity",
            f"{self.username} - Changed from {current_quantity} to {current_quantity - self.spinBox_quantity.value()} at {datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
        )
        for category in inventory.get_keys():
            if category == self.category:
                continue
            for item in list(data[category].keys()):
                if part_number == data[category][item]["part_number"]:
                    current_quantity: int = data[category][item]["current_quantity"]
                    inventory.change_object_in_object_item(category, item, "current_quantity", current_quantity - self.spinBox_quantity.value())
                    inventory.change_object_in_object_item(
                        category,
                        item,
                        "latest_change_current_quantity",
                        f"{self.username} - Changed from {current_quantity} to {current_quantity - self.spinBox_quantity.value()} at {datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                    )
        self.pushButton_add_quantity.setEnabled(False)
        self.pushButton_remove_quantity.setEnabled(False)
        self.listWidget_itemnames.setCurrentRow(self.last_item_selected_index)
        self.listWidget_item_changed()
        self.update_category_total_stock_costs()
        self.sort_inventory()
        self.sync_changes()

    def listWidget_item_changed(self) -> None:
        """
        It's a function that changes the color of a QComboBox and QDoubleSpinBox when the user clicks on
        an item in a QListWidget.
        """
        try:
            self.last_item_selected_name = self.listWidget_itemnames.currentItem().text()
        except AttributeError:
            self.pushButton_add_quantity.setEnabled(False)
            self.pushButton_remove_quantity.setEnabled(False)
            return
        try:
            quantity: int = self.get_value_from_category(self.last_item_selected_name, "current_quantity")
        except (KeyError, IndexError, TypeError):
            return
        try:
            self.last_item_selected_index = list(list(inventory.get_data()[self.category].keys())).index(self.last_item_selected_name)
        except (ValueError, KeyError):
            return
        table_widget: CustomTableWidget = self.tabs[self.category]
        table_widget.scrollTo(table_widget.model().index(self.last_item_selected_index, 0))
        table_widget.selectRow(self.last_item_selected_index)
        if self.radioButton_single.isChecked():
            self.pushButton_add_quantity.setEnabled(True)
            self.pushButton_remove_quantity.setEnabled(True)

            self.pushButton_add_quantity.disconnect()
            self.pushButton_remove_quantity.disconnect()

            self.pushButton_remove_quantity.clicked.connect(partial(self.remove_quantity, self.last_item_selected_name, quantity))
            self.pushButton_add_quantity.clicked.connect(partial(self.add_quantity, self.last_item_selected_name, quantity))
        self.spinBox_quantity.setValue(0)

    def value_change(self, category: str, item_name: str, value_name: str, new_value) -> None:
        """
        It changes the value of a value in a dictionary in a dictionary in a dictionary.

        Args:
          category (str): str = "category"
          item_name (str): str = the name of the item
          value_name (str): str = "current_quantity"
          new_value: str
        """
        add_quantity_state: bool = self.pushButton_add_quantity.isEnabled()
        remove_quantity_state: bool = self.pushButton_remove_quantity.isEnabled()
        self.pushButton_add_quantity.setEnabled(False)
        self.pushButton_remove_quantity.setEnabled(False)
        inventory.change_object_in_object_item(
            object_name=category,
            item_name=item_name,
            value_name=value_name,
            new_value=new_value,
        )
        self.pushButton_add_quantity.setEnabled(add_quantity_state)
        self.pushButton_remove_quantity.setEnabled(remove_quantity_state)

    def action_group(self, group_name: str, actions: list[QAction]) -> None:
        """
        It's a function that is called when a user clicks on a menu item in a menu bar. The function is
        supposed to check if the menu item is checked and if it is, it should uncheck the other menu
        items in the same group

        Args:
          group_name (str): str
          actions (list[QAction]): list[QAction]
        """
        if group_name == "order":
            if actions[0].isChecked() and settings_file.get_value(item_name="sort_descending"):
                actions[1].setChecked(False)
                actions[0].setEnabled(False)
                actions[1].setEnabled(True)
            if actions[1].isChecked() and settings_file.get_value(item_name="sort_ascending"):
                actions[0].setChecked(False)
                actions[1].setEnabled(False)
                actions[0].setEnabled(True)
        elif group_name == "sorting":
            if actions[0].isChecked() and (
                settings_file.get_value(item_name="sort_priority") or settings_file.get_value(item_name="sort_alphabatical")
            ):  # Quantity in Stock
                actions[1].setChecked(False)
                actions[2].setChecked(False)
                actions[0].setEnabled(False)
                actions[1].setEnabled(True)
                actions[2].setEnabled(True)
            elif actions[1].isChecked() and (
                settings_file.get_value(item_name="sort_quantity_in_stock") or settings_file.get_value(item_name="sort_alphabatical")
            ):  # Priority
                actions[0].setChecked(False)
                actions[2].setChecked(False)
                actions[0].setEnabled(True)
                actions[1].setEnabled(False)
                actions[2].setEnabled(True)
            elif actions[2].isChecked() and (
                settings_file.get_value(item_name="sort_priority") or settings_file.get_value(item_name="sort_quantity_in_stock")
            ):  # Alphabatical
                actions[0].setChecked(False)
                actions[1].setChecked(False)
                actions[0].setEnabled(True)
                actions[1].setEnabled(True)
                actions[2].setEnabled(False)

        settings_file.add_item(
            item_name="sort_quantity_in_stock",
            value=self.actionQuantity_in_Stock.isChecked(),
        )
        settings_file.add_item(
            item_name="sort_priority",
            value=self.actionPriority.isChecked(),
        )
        settings_file.add_item(
            item_name="sort_alphabatical",
            value=self.actionAlphabatical.isChecked(),
        )
        settings_file.add_item(
            item_name="sort_ascending",
            value=self.actionAscending.isChecked(),
        )
        settings_file.add_item(
            item_name="sort_descending",
            value=self.actionDescending.isChecked(),
        )
        self.update_sorting_status_text()

    def process_selected_nests(self) -> None:
        """
        This function processes selected nests by getting selected items and file paths, filtering the
        file paths based on selected items, and starting a thread to process the filtered file paths.
        """
        self.is_nest_generated_from_parts_in_inventory = False
        selected_items = self.get_all_selected_nests()
        if selected_items:
            self.start_process_nest_thread(selected_items)

    def quote_table_cell_changed(self, row: int, col: int) -> None:
        if col != 4:
            return
        item = self.tableWidget_quote_items.item(row, col)

    def global_nest_material_change(self) -> None:
        """
        This function changes the material of all items in a table to the selected material from a combo
        box.
        """
        new_material = self.comboBox_global_sheet_material.currentText()
        for row in range(self.tableWidget_quote_items.rowCount()):
            self.tableWidget_quote_items.setItem(row, 2, QTableWidgetItem(new_material))
            self.tableWidget_quote_items.item(row, 2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
        for item in list(self.quote_nest_information.keys()):
            self.quote_nest_information[item]["material"] = new_material
        toolbox_index: int = 0
        for nest_name in list(self.quote_nest_information.keys()):
            if nest_name[0] != "_":
                continue
            self.sheet_nests_toolbox.setItemText(
                toolbox_index,
                f"{self.quote_nest_information[nest_name]['gauge']} {self.quote_nest_information[nest_name]['material']} {self.quote_nest_information[nest_name]['sheet_dim']} - {nest_name.split('/')[-1].replace('.pdf', '')}",
            )
            combobox_material: QComboBox = self.sheet_nests_toolbox.getWidget(toolbox_index).findChildren(QComboBox)[0]
            combobox_material.setCurrentText(new_material)
            toolbox_index += 1

    def global_nest_thickness_change(self) -> None:
        """
        This function changes the thickness of all items in a table to a new global thickness selected
        from a combo box.
        """
        new_thickness = self.comboBox_global_sheet_thickness.currentText()
        for row in range(self.tableWidget_quote_items.rowCount()):
            self.tableWidget_quote_items.setItem(row, 3, QTableWidgetItem(new_thickness))
            self.tableWidget_quote_items.item(row, 3).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
        for item in list(self.quote_nest_information.keys()):
            self.quote_nest_information[item]["gauge"] = new_thickness
        toolbox_index: int = 0
        for nest_name in list(self.quote_nest_information.keys()):
            if nest_name[0] != "_":
                continue
            self.sheet_nests_toolbox.setItemText(
                toolbox_index,
                f"{self.quote_nest_information[nest_name]['gauge']} {self.quote_nest_information[nest_name]['material']} {self.quote_nest_information[nest_name]['sheet_dim']} - {nest_name.split('/')[-1].replace('.pdf', '')}",
            )
            combobox_thickness: QComboBox = self.sheet_nests_toolbox.getWidget(toolbox_index).findChildren(QComboBox)[1]
            combobox_thickness.setCurrentText(new_thickness)
            toolbox_index += 1

    def sheet_nest_item_change(
        self,
        toolbox_index: int,
        input_method: QComboBox | HumbleDoubleSpinBox | tuple[HumbleDoubleSpinBox, HumbleDoubleSpinBox],
        nest_name_to_update: str,
        item_to_change: str,
    ) -> None:
        """
        This function updates the information of a specific item in a nested sheet and updates the
        corresponding toolbox item and quote table.

        Args:
          toolbox_index (int): The index of the item in the toolbox that needs to be updated.
          input_method (QComboBox | HumbleDoubleSpinBox | tuple[HumbleDoubleSpinBox,
        HumbleDoubleSpinBox]): The input method can be one of three types: QComboBox,
        HumbleDoubleSpinBox, or a tuple of two HumbleDoubleSpinBoxes. This parameter is used to
        determine the current value of the input method and update the corresponding item in the quote
        nest information dictionary.
          nest_name_to_update (str): The name of the nest that needs to be updated.
          item_to_change (str): The name of the item in the quote nest information dictionary that needs
        to be updated with the new value.

        Returns:
          None is being returned.
        """
        if type(input_method) == QComboBox:
            current_value = input_method.currentText()
        elif type(input_method) == HumbleDoubleSpinBox:
            current_value = input_method.value()
        elif type(input_method) == tuple:
            current_value = f"{input_method[0].value():.3f}x{input_method[1].value():.3f}"
        else:
            return
        for item in list(self.quote_nest_information.keys()):
            if item[0] == "_":
                continue
            nest_name = "_" + self.quote_nest_information[item]["file_name"].replace("\\", "/")
            if nest_name == nest_name_to_update and type(input_method) != HumbleDoubleSpinBox:
                self.quote_nest_information[item][item_to_change] = current_value
        self.quote_nest_information[nest_name_to_update][item_to_change] = current_value
        nest_name = nest_name_to_update.split("/")[-1].replace(".pdf", "")
        self.sheet_nests_toolbox.setItemText(
            toolbox_index,
            f"{self.quote_nest_information[nest_name_to_update]['gauge']} {self.quote_nest_information[nest_name_to_update]['material']} {self.quote_nest_information[nest_name_to_update]['sheet_dim'].replace('x', ' x ')} - {nest_name}",
        )
        self.load_quote_table()

    def inventory_cell_changed(self, tab: CustomTableWidget):
        """
        This function updates the current item in a list widget based on the selected item in a table
        widget.

        Args:
          tab (CustomTableWidget): CustomTableWidget object representing the table widget where the cell
        change event occurred.
        """
        selected_item = self.tabs[self.category].selectedItems()[0].text()
        if items := self.listWidget_itemnames.findItems(selected_item, Qt.MatchExactly):
            item = items[0]
            self.listWidget_itemnames.setCurrentItem(item)

    def parts_in_inventory_cell_changed(self, tab: CustomTableWidget):
        """
        This function changes the text of a button based on the number of selected items in a table.

        Args:
          tab (CustomTableWidget): CustomTableWidget object representing the table widget where the
        inventory parts are displayed.
        """
        selected_items_count = len(self.get_all_selected_parts(tab))
        if selected_items_count == 0:
            self.pushButton_remove_quantities_from_inventory.setText("Remove Quantities from whole Category")
        else:
            self.pushButton_remove_quantities_from_inventory.setText(f"Remove Quantities from Selected ({selected_items_count}) Items")

    # ! /\ SLOTS & SIGNALS /\
    # ! \/ CALCULATION \/
    def eval_expr(self, expr):
        """
        This function evaluates a given expression using the ast module in Python.

        Args:
          expr: The expression to be evaluated as a string.

        Returns:
          The `eval_expr` method is returning the result of evaluating the expression passed as an
        argument. The expression is first parsed using the `ast.parse` method with the mode set to
        `'eval'`, which means that the expression is expected to be a single expression that can be
        evaluated. The resulting AST (Abstract Syntax Tree) is then evaluated using the `eval_` method
        (which is not shown
        """
        return self.eval_(ast.parse(expr, mode="eval").body)

    def eval_(self, node):
        """
        This function evaluates mathematical expressions represented as an abstract syntax tree in
        Python.

        Args:
          node: a node in the abstract syntax tree (AST) of a Python program. The AST is a tree-like
        data structure that represents the structure of the program's code.

        Returns:
          The function `eval_` returns the evaluated value of the given AST node. If the node is a
        number, it returns the number itself. If the node is a binary operation, it evaluates the left
        and right operands and applies the corresponding operator to them. If the node is a unary
        operation, it applies the corresponding operator to the operand. If the node is not one of these
        types, it
        """
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return operators[type(node.op)](self.eval_(node.left), self.eval_(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return operators[type(node.op)](self.eval_(node.operand))
        else:
            raise TypeError(node)

    def calculuate_price_of_steel_summary(self) -> None:
        """
        It takes the current quantity of each item in the inventory, multiplies it by the cost per
        sheet, and then adds it to the total cost of the category.
        """
        category_data = price_of_steel_inventory.get_data()
        self.clear_layout(self.gridLayout_price_of_steel)
        total: float = 0.0
        i: int = 0
        for category in list(category_data.keys()):
            category_total: float = 0.0
            if category == "Price Per Pound":
                continue
            for item in list(category_data[category].keys()):
                current_quantity: int = category_data[category][item]["current_quantity"]
                sheet_dimension: str = category_data[category][item]["sheet_dimension"]
                thickness: str = category_data[category][item]["thickness"]
                material: str = category_data[category][item]["material"]
                try:
                    pounds_per_square_foot: float = float(price_of_steel_information.get_data()["pounds_per_square_foot"][material][thickness])
                except KeyError:
                    pounds_per_square_foot: float = 0.0
                sheet_length: float = float(sheet_dimension.split("x")[0])
                sheet_width: float = float(sheet_dimension.split("x")[1])
                try:
                    pounds_per_sheet: float = ((sheet_length * sheet_width) / 144) * pounds_per_square_foot
                except ZeroDivisionError:
                    pounds_per_sheet = 0.0
                try:
                    price_per_pound: float = float(price_of_steel_inventory.get_data()["Price Per Pound"][material]["price"])
                except KeyError:
                    price_per_pound: float = 0.0
                cost_per_sheet = pounds_per_sheet * price_per_pound
                total_cost: float = current_quantity * cost_per_sheet
                category_total += total_cost
            lbl = QLabel(f"{category}:", self)
            self.gridLayout_price_of_steel.addWidget(lbl, i, 0)
            lbl = QLabel(f"${category_total:,.2f}", self)
            lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.gridLayout_price_of_steel.addWidget(lbl, i, 1)
            total += category_total
            i += 1
        lbl = QLabel("Total:", self)
        lbl.setStyleSheet("border-top: 1px solid grey; border-bottom: 1px solid grey")
        self.gridLayout_price_of_steel.addWidget(lbl, i + 1, 0)
        lbl = QLabel(f"${total:,.2f}", self)
        lbl.setStyleSheet("border-top: 1px solid grey; border-bottom: 1px solid grey")
        self.gridLayout_price_of_steel.addWidget(lbl, i + 1, 1)

    def calculate_parts_in_inventory_summary(self) -> None:
        """
        It takes a dictionary of dictionaries of dictionaries and calculates the total value of each
        category and the total value of all categories.
        """

        while self.gridLayout_parts_in_inventory_summary.count():
            item = self.gridLayout_parts_in_inventory_summary.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        category_data = parts_in_inventory.get_data()
        i: int = 0
        parts_in_inventory_total = {}
        for category in list(category_data.keys()):
            category_total: float = 0.0
            for part_name in list(category_data[category].keys()):
                price = category_data[category][part_name]["price"]
                quantity = category_data[category][part_name]["current_quantity"]
                category_total += price * quantity
                if category not in ["Recut", "Custom"]:
                    parts_in_inventory_total[part_name] = {
                        "price": price,
                        "current_quantity": quantity,
                    }
            if category in ["Recut", "Custom"]:
                lbl = QLabel(f"Total Cost in {category}:", self)
                self.gridLayout_parts_in_inventory_summary.addWidget(lbl, len(list(category_data.keys())) + i + 2, 0)
                lbl = QLabel(f"${category_total:,.2f}", self)
                self.gridLayout_parts_in_inventory_summary.addWidget(lbl, len(list(category_data.keys())) + i + 2, 1)
            else:
                lbl = QLabel(f"{category}:", self)
                self.gridLayout_parts_in_inventory_summary.addWidget(lbl, i, 0)
                lbl = QLabel(f"${category_total:,.2f}", self)
                self.gridLayout_parts_in_inventory_summary.addWidget(lbl, i, 1)
            i += 1
        total: float = 0.0
        for part_name in list(parts_in_inventory_total.keys()):
            price = parts_in_inventory_total[part_name]["price"]
            quantity = parts_in_inventory_total[part_name]["current_quantity"]
            total += price * quantity
        lbl = QLabel("Total Stoves in Inventory:", self)
        lbl.setStyleSheet("border-top: 1px solid grey; border-bottom: 1px solid grey")
        self.gridLayout_parts_in_inventory_summary.addWidget(lbl, i + 1, 0)
        lbl = QLabel(f"${total:,.2f}", self)
        lbl.setStyleSheet("border-top: 1px solid grey; border-bottom: 1px solid grey")
        self.gridLayout_parts_in_inventory_summary.addWidget(lbl, i + 1, 1)

    # ! /\ CALCULATION /\
    def sheet_notes_changed(self, category: str, item: str, note: QPlainTextEdit) -> None:
        """
        It takes the category, item name, value name, and note as parameters and then calls the
        value_change function with the category, item name, value name, and note as parameters

        Args:
          category (str): str = The category of the item.
          item_name (QLineEdit): QLineEdit
          value_name (str): str = The name of the value that is being changed.
          note (QPlainTextEdit): QPlainTextEdit
        """
        price_of_steel_inventory.get_data()
        price_of_steel_inventory.change_object_in_object_item(
            category,
            item,
            "notes",
            note.toPlainText(),
        )

    def remove_quantity_from_part_inventory(self) -> None:
        """
        This function removes a specified quantity of parts from the inventory and updates the inventory
        data accordingly.

        Returns:
          None is being returned.
        """
        batch_multiplier: int = self.spinBox_quantity_for_inventory.value()
        selected_parts = self.get_all_selected_parts(self.tabs[self.category])
        if len(selected_parts) > 0:
            are_you_sure_dialog = self.show_message_dialog(
                title="Are you sure?",
                message=f'Removing quantities from the selected ({len(self.get_all_selected_parts(self.tabs[self.category]))}) items.\n\nAre you sure you want to remove a multiple of {batch_multiplier} quantities from each selected item in "{self.category}"?',
                dialog_buttons=DialogButtons.no_yes_cancel,
            )
            if are_you_sure_dialog in [DialogButtons.no, DialogButtons.cancel]:
                return
            self.pushButton_remove_quantities_from_inventory.setEnabled(False)
            self.spinBox_quantity_for_inventory.setValue(0)
            category_data = parts_in_inventory.get_data()
            part_names_to_check = []

            for part_name in selected_parts:
                part_names_to_check.append(part_name)
                unit_quantity: int = category_data[self.category][part_name]["unit_quantity"]
                current_quantity: int = category_data[self.category][part_name]["current_quantity"]
                new_quantity = current_quantity - (unit_quantity * batch_multiplier)
                category_data[self.category][part_name]["current_quantity"] = new_quantity
                category_data[self.category][part_name][
                    "modified_date"
                ] = f'{self.username} - Removed {unit_quantity*batch_multiplier} quantity at {str(datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"))}'
            for category in list(category_data.keys()):
                if category in ["Recut", self.category]:
                    continue
                for part_name in list(category_data[category].keys()):
                    if part_name in part_names_to_check:
                        unit_quantity: int = category_data[category][part_name]["unit_quantity"]
                        current_quantity: int = category_data[category][part_name]["current_quantity"]
                        new_quantity = current_quantity - (unit_quantity * batch_multiplier)
                        category_data[category][part_name]["current_quantity"] = new_quantity
                        category_data[category][part_name][
                            "modified_date"
                        ] = f'{self.username} - Removed {unit_quantity*batch_multiplier} quantity at {str(datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"))}'
        else:
            are_you_sure_dialog = self.show_message_dialog(
                title="Are you sure?",
                message=f'Removing quantities from the whole selected category.\n\nAre you sure you want to remove a multiple of {batch_multiplier} quantities from each item in "{self.category}"?',
                dialog_buttons=DialogButtons.no_yes_cancel,
            )
            if are_you_sure_dialog in [DialogButtons.no, DialogButtons.cancel]:
                return
            self.play_celebrate_sound()
            self.pushButton_remove_quantities_from_inventory.setEnabled(False)
            self.spinBox_quantity_for_inventory.setValue(0)
            category_data = parts_in_inventory.get_data()
            part_names_to_check = list(category_data[self.category].keys())
            for part_name in list(category_data[self.category].keys()):
                unit_quantity: int = category_data[self.category][part_name]["unit_quantity"]
                current_quantity: int = category_data[self.category][part_name]["current_quantity"]
                new_quantity = current_quantity - (unit_quantity * batch_multiplier)
                category_data[self.category][part_name]["current_quantity"] = new_quantity
                category_data[self.category][part_name][
                    "modified_date"
                ] = f'{self.username} - Removed {unit_quantity*batch_multiplier} quantity at {str(datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"))}'
            for category in list(category_data.keys()):
                if category in ["Recut", self.category]:
                    continue
                for part_name in list(category_data[category].keys()):
                    if part_name in part_names_to_check:
                        unit_quantity: int = category_data[category][part_name]["unit_quantity"]
                        current_quantity: int = category_data[category][part_name]["current_quantity"]
                        new_quantity = current_quantity - (unit_quantity * batch_multiplier)
                        category_data[category][part_name]["current_quantity"] = new_quantity
                        category_data[category][part_name][
                            "modified_date"
                        ] = f'{self.username} - Removed {unit_quantity*batch_multiplier} quantity at {str(datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"))}'
        parts_in_inventory.save_data(category_data)

        for category in parts_in_inventory.get_data():
            parts_in_inventory.sort(category=category, item_name="current_quantity", ascending=True)

        self.pushButton_remove_quantities_from_inventory.setText("Remove Quantities from whole Category")
        self.pushButton_remove_quantities_from_inventory.setEnabled(True)
        self.load_categories()
        self.calculate_parts_in_inventory_summary()
        self.sync_changes()

    # ! \/ UPDATE UI ELEMENTS \/
    def change_tables_font(self) -> None:
        font, ok = QFontDialog.getFont()
        if ok:
            font_data = {
                "family": font.family(),
                "pointSize": font.pointSize(),
                "weight": font.weight(),
                "italic": font.italic(),
            }
            self.tables_font.setFamily(font.family())
            self.tables_font.setPointSize(font.pointSize())
            self.tables_font.setWeight(font.weight())
            self.tables_font.setItalic(font.italic())
            settings_file.add_item("tables_font", font_data)
            self.load_active_tab()

    def update_sorting_status_text(self) -> None:
        """
        It updates the status tip of the sorting actions in the menu bar.
        """
        sorting_from_alphabet: str = "A"
        sorting_to_alphabet: str = "Z"

        sorting_from_number: str = "0"
        sorting_to_number: str = "9"

        sorting_from_priority: str = "Low"
        sorting_to_priority: str = "High"

        if self.actionAscending.isChecked():
            self.actionAlphabatical.setStatusTip(f"Sort from {sorting_from_alphabet} to {sorting_to_alphabet}")
            self.actionPriority.setStatusTip(f"Sort from {sorting_from_priority} to {sorting_to_priority}")
            self.actionQuantity_in_Stock.setStatusTip(f"Sort from {sorting_from_number} to {sorting_to_number}")
        else:
            self.actionAlphabatical.setStatusTip(f"Sort from {sorting_to_alphabet} to {sorting_from_alphabet}")
            self.actionPriority.setStatusTip(f"Sort from {sorting_to_priority} to {sorting_from_priority}")
            self.actionQuantity_in_Stock.setStatusTip(f"Sort from {sorting_to_number} to {sorting_from_number}")

        if self.actionAlphabatical.isChecked():
            if self.actionAscending.isChecked():
                self.actionSort.setStatusTip(f"Sort from {sorting_from_alphabet} to {sorting_to_alphabet}")
            else:
                self.actionSort.setStatusTip(f"Sort from {sorting_to_alphabet} to {sorting_from_alphabet}")
            self.actionAscending.setStatusTip(f"Sort from {sorting_from_alphabet} to {sorting_to_alphabet}")
            self.actionDescending.setStatusTip(f"Sort from {sorting_to_alphabet} to {sorting_from_alphabet}")
        elif self.actionQuantity_in_Stock.isChecked():
            if self.actionAscending.isChecked():
                self.actionSort.setStatusTip(f"Sort from {sorting_from_number} to {sorting_to_number}")
            else:
                self.actionSort.setStatusTip(f"Sort from {sorting_to_number} to {sorting_from_number}")
            self.actionAscending.setStatusTip(f"Sort from {sorting_from_number} to {sorting_to_number}")
            self.actionDescending.setStatusTip(f"Sort from {sorting_to_number} to {sorting_from_number}")
        elif self.actionPriority.isChecked():
            if self.actionAscending.isChecked():
                self.actionSort.setStatusTip(f"Sort from {sorting_from_priority} to {sorting_to_priority}")
            else:
                self.actionSort.setStatusTip(f"Sort from {sorting_to_priority} to {sorting_from_priority}")
            self.actionAscending.setStatusTip(f"Sort from {sorting_from_priority} to {sorting_to_priority}")
            self.actionDescending.setStatusTip(f"Sort from {sorting_to_priority} to {sorting_from_priority}")

    def update_list_widget(self) -> None:
        """
        It takes the text from a lineEdit widget and searches for it in a dictionary. If the text is
        found, it adds the key to a listWidget

        Returns:
          the value of the item_name key in the category_data dictionary.
        """
        search_input: str = self.lineEdit_search_items.text()
        category_data = inventory.get_value(item_name=self.category)
        self.listWidget_itemnames.clear()
        self.pushButton_add_quantity.setEnabled(False)
        self.pushButton_remove_quantity.setEnabled(False)
        try:
            for item in list(category_data.keys()):
                if search_input.lower() in item.lower() or search_input.lower() in category_data[item]["part_number"].lower():
                    self.listWidget_itemnames.addItem(item)
        except AttributeError:
            return

    def update_stock_costs(self) -> None:
        """
        It takes the current quantity of an item, multiplies it by the price of the item, and then
        multiplies that by the exchange rate
        """
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) != "Edit Inventory":
            return
        self.label_total_unit_cost.setText(f"Total Unit Cost: ${inventory.get_total_unit_cost(self.category, self.get_exchange_rate()):,.2f}")
        tab = self.tabs[self.category]
        tab.blockSignals(True)
        for row_index in range(tab.rowCount()):
            item_name: str = tab.item(row_index, 0).text()
            total_cost_item = tab.item(row_index, 6)
            total_unit_cost_item = tab.item(row_index, 7)
            price: float = self.get_value_from_category(item_name, "price")
            current_quantity: float = self.get_value_from_category(item_name, "current_quantity")
            unit_quantity: float = self.get_value_from_category(item_name, "unit_quantity")
            use_exchange_rate: bool = self.get_value_from_category(item_name=item_name, key="use_exchange_rate")
            total_cost_item.setText(f'${(max(current_quantity, 0) * price):,.2f} {"USD" if use_exchange_rate else "CAD"}')
            total_unit_cost_item.setText(f'${(unit_quantity * price):,.2f} {"USD" if use_exchange_rate else "CAD"}')
        tab.blockSignals(False)

    def update_category_total_stock_costs(self) -> None:
        """
        It takes a list of categories, and then sums up the total cost of all items in those categories
        """
        total_stock_costs = {}

        categories = inventory.get_data()
        for category in list(categories.keys()):
            total_category_stock_cost: float = 0.0
            for item in list(categories[category].keys()):
                use_exchange_rate: bool = categories[category][item]["use_exchange_rate"] == "USD"
                exchange_rate: float = self.get_exchange_rate() if use_exchange_rate else 1
                price: float = categories[category][item]["price"]
                current_quantity: int = categories[category][item]["current_quantity"]
                price = max(current_quantity * price * exchange_rate, 0)
                total_category_stock_cost += price
            total_stock_costs[category] = total_category_stock_cost
        total_stock_costs["Polar Total Stock Cost"] = inventory.get_total_stock_cost_for_similar_categories("Polar")
        total_stock_costs["BL Total Stock Cost"] = inventory.get_total_stock_cost_for_similar_categories("BL")
        total_stock_costs = dict(sorted(total_stock_costs.items()))
        self.clear_layout(self.gridLayout_Categor_Stock_Prices)
        lbl = QLabel("Stock Costs:", self)
        self.gridLayout_Categor_Stock_Prices.addWidget(lbl, 0, 0)
        for i, stock_cost in enumerate(total_stock_costs, start=1):
            lbl = QLabel(stock_cost, self)
            if "Total" in stock_cost:
                lbl.setStyleSheet("border-top: 1px solid grey; border-bottom: 1px solid grey")
            self.gridLayout_Categor_Stock_Prices.addWidget(lbl, i, 0)
            lbl = QLabel(f"${total_stock_costs[stock_cost]:,.2f}", self)
            lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            if "Total" in stock_cost:
                lbl.setStyleSheet("border-top: 1px solid grey; border-bottom: 1px solid grey")
            self.gridLayout_Categor_Stock_Prices.addWidget(lbl, i, 1)
        lbl = QLabel("Total Cost in Stock:", self)
        lbl.setStyleSheet("border-top: 1px solid grey")
        self.gridLayout_Categor_Stock_Prices.addWidget(lbl, i + 1, 0)
        lbl = QLabel(f"${inventory.get_total_stock_cost(self.get_exchange_rate()):,.2f}", self)
        lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        lbl.setStyleSheet("border-top: 1px solid grey")
        self.gridLayout_Categor_Stock_Prices.addWidget(lbl, i + 1, 1)

    def update_all_parts_in_inventory_price(self) -> None:
        """
        It takes the weight and machine time of a part, and uses that to calculate the price of the part
        """
        data = parts_in_inventory.get_data()
        for category in list(data.keys()):
            if category in ["Custom", "Recut"]:
                continue
            for part_name in list(data[category].keys()):
                weight: float = data[category][part_name]["weight"]
                machine_time: float = data[category][part_name]["machine_time"]
                material: str = data[category][part_name]["material"]
                price_per_pound: float = price_of_steel_inventory.get_data()["Price Per Pound"][material]["price"]
                cost_for_laser: float = 250 if material in {"304 SS", "409 SS", "Aluminium"} else 150
                parts_in_inventory.change_object_in_object_item(
                    object_name=category,
                    item_name=part_name,
                    value_name="price",
                    new_value=float((machine_time * (cost_for_laser / 60)) + (weight * price_per_pound)),
                )

    def set_table_row_color(self, table, row_index, color):
        """
        This function sets the background color of a row in a table widget in PyQt5.

        Args:
          table: The table parameter is a QTableWidget object, which represents a table widget in PyQt5.
        It contains rows and columns of cells, each of which can contain a QTableWidgetItem object.
          row_index: The index of the row in the table that you want to set the background color for.
          color: The color parameter is a string that represents the color that the row should be set
        to. It can be any valid color name or a hexadecimal value representing the color. For example,
        "red", "#FF0000", or "rgb(255, 0, 0)" could all be valid
        """
        for j in range(table.columnCount()):
            item = table.item(row_index, j)
            if not item:
                item = QTableWidgetItem()
                table.setItem(row_index, j, item)
            item.setBackground(QColor(color))

    def set_table_row_text_color(self, table, row_index, color):
        """
        This function sets the text color of a specific row in a table widget in PyQt5.

        Args:
          table: a QTableWidget object representing the table widget
          row_index: The index of the row in the table where the text color needs to be set.
          color: The color parameter is a string that represents the color that you want to set for the
        text in the table row. It can be any valid color name or a hexadecimal value representing the
        color. For example, "red", "#FF0000", "blue", "#0000FF", etc.
        """
        for j in range(table.columnCount()):
            item = table.item(row_index, j)
            if not item:
                item = QTableWidgetItem()
                table.setItem(row_index, j, item)
            item.setForeground(QColor(color))

    def clear_nest_selections(self) -> None:
        """
        This function clears the selection of all list widgets in a dictionary of quote nest
        directories.
        """
        for tree_view in self.quote_nest_directories_list_widgets.values():
            tree_view.clearSelection()

    def nest_directory_item_selected(self) -> None:
        # self.process_selected_nests()
        selected_nests = len(self.get_all_selected_nests())
        if selected_nests == 0:
            self.pushButton_load_nests.setEnabled(False)
        else:
            self.pushButton_load_nests.setEnabled(True)
        self.pushButton_load_nests.setText(f"Load {selected_nests} Nest{'' if selected_nests == 1 else 's'}")

    def save_quote_table_values(self) -> None:
        """
        This function saves the quantities of items in a quote table to a dictionary.
        """
        for row in range(self.tableWidget_quote_items.rowCount()):
            item_name = self.tableWidget_quote_items.item(row, 1).text()
            quantity = int(self.tableWidget_quote_items.item(row, 4).text())
            recut_button: RecutButton = self.tableWidget_quote_items.cellWidget(row, 5)
            self.quote_nest_information[item_name]["quantity"] = quantity
            self.quote_nest_information[item_name]["recut"] = recut_button.isChecked()

    # ! /\ UPDATE UI ELEMENTS /\
    def sort_inventory(self) -> None:
        """
        It sorts the inventory based on the sorting method selected by the user
        """

        sorting_method: str = ""
        if self.actionQuantity_in_Stock.isChecked():
            sorting_method = "current_quantity"
        elif self.actionPriority.isChecked():
            sorting_method = "priority"
        elif self.actionAlphabatical.isChecked():
            sorting_method = "alphabet"

        self.active_json_file.sort(self.category, sorting_method, not self.actionAscending.isChecked())
        self.sync_changes()
        self.load_active_tab()

    # ! \/ GETTERS \/
    def get_all_part_numbers(self) -> list[str]:
        """
        It takes the data from the inventory module, loops through the data, and returns a list of all
        the part numbers

        Returns:
          A list of all the part numbers in the inventory.
        """
        data = inventory.get_data()
        part_numbers = []
        for category in list(data.keys()):
            try:
                part_numbers.extend(data[category][item]["part_number"] for item in list(data[category].keys()))
            except KeyError:
                continue
        return list(set(part_numbers))

    def get_all_part_names(self) -> list[str]:
        """
        It takes the data from the inventory module, loops through the data, and returns a list of all
        the part names

        Returns:
          A list of all the part names in the inventory.
        """
        data = inventory.get_data()
        part_names = []
        for category in list(data.keys()):
            part_names.extend(iter(list(data[category].keys())))
        # part_names = list(set(part_names))
        return part_names

    def get_exchange_rate(self) -> float:
        """
        It returns the exchange rate from the settings file

        Returns:
          The exchange rate from the settings file.
        """
        return settings_file.get_value(item_name="exchange_rate")

    def get_value_from_category(self, item_name: str, key: str) -> Any:
        """
        It returns the value of a key in a dictionary, if the key exists. If the key doesn't exist, it
        returns a string

        Args:
          item_name (str): The name of the item you want to get the data from.
          key (str): str = The key of the item you want to get.

        Returns:
          The value of the key in the item_name dictionary.
        """
        try:
            return self.active_json_file.get_data()[self.category][item_name][key]
        except KeyError:
            return "No changes yet." if "latest" in key else None

    def get_all_files_from_directory(self, folder_path: str, suffix: str) -> list[str]:
        """
        This function returns a list of all files in a directory that have a specified suffix.

        Args:
          folder_path (str): The path of the directory from which you want to retrieve files.
          suffix (str): The suffix parameter is a string that represents the file extension that we want
        to filter the files by. For example, if we want to get all the files with a ".txt" extension, we
        would set suffix to ".txt".

        Returns:
          a list of file names that end with the specified suffix in the specified folder path.
        """
        return [folder_path + "/" + f for f in os.listdir(folder_path) if f.endswith(suffix)]

    def get_index_from_quote_table(self, item_name: str) -> int:
        """
        This function searches for a specific item name in a quote table and returns its row index if
        found, otherwise it returns None.

        Args:
          item_name (str): A string representing the name of an item to search for in a table.
        """
        for row in range(self.tableWidget_quote_items.rowCount()):
            item = self.tableWidget_quote_items.item(row, 1)
            if item is not None and item.text() == item_name:
                row_index = row
                break
        else:
            # Handle case where target string was not found
            row_index = None

    def get_quantity_multiplier(self, item_name: str) -> int:
        """
        This Python function returns the quantity multiplier of an item based on its name and file
        location in a dictionary.

        Args:
          item_name (str): a string representing the name of an item

        Returns:
          The function `get_quantity_multiplier` returns an integer value, which is either the
        `quantity_multiplier` value of the `item_name` key in the `quote_nest_information` dictionary,
        or 1 if the `item_name` key is not found in the dictionary.
        """
        items_nest = "_" + self.quote_nest_information[item_name]["file_name"].replace("\\", "/")
        if matches := {k: v for k, v in self.quote_nest_information.items() if k == items_nest}:
            return int(matches[items_nest]["quantity_multiplier"])
        else:
            return 1

    def get_all_selected_nests(self) -> list[str]:
        """
        This function returns a list of strings representing the data of all selected indexes in
        multiple tree views.

        Returns:
          A list of strings containing the data from the selected indexes in all the tree views in
        `self.quote_nest_directories_list_widgets`.
        """
        selected_nests = []
        for tree_view in self.quote_nest_directories_list_widgets.values():
            selected_nests.extend(tree_view.full_paths)
        return list(set(selected_nests))

    def get_menu_tab_order(self) -> list[str]:
        return [self.tabWidget.tabText(i) for i in range(self.tabWidget.count())]

    def get_tab_from_name(self, name: str) -> int:
        """
        This function finds the index of a tab in a tab widget by its name.

        Args:
          name (str): A string representing the name of the tab that needs to be found.

        Returns:
          an integer value which represents the index of the tab with the given name in the tab widget.
        If the tab is not found, it returns -1.
        """
        return next(
            (i for i in range(self.tabWidget.count()) if self.tabWidget.tabText(i) == name),
            -1,
        )

    def get_all_gauges(self) -> list[str]:
        """
        This function retrieves a list of all gauges from the inventory data.

        Returns:
          A list of unique gauge values extracted from the "gauge" key of each item in the inventory
        data.
        """
        data = parts_in_inventory.get_data()
        gauges = []
        for category in list(data.keys()):
            try:
                gauges.extend(data[category][item]["gauge"] for item in list(data[category].keys()))
            except KeyError:
                continue
        return list(set(gauges))

    def get_all_selected_parts(self, tab: CustomTableWidget) -> list[str]:
        """
        This function returns a list of all selected items in the first column of a custom table widget.

        Args:
          tab (CustomTableWidget): CustomTableWidget - a custom widget that displays a table of data and
        allows for user interaction such as selecting rows and columns.

        Returns:
          a list of strings, which are the text values of the selected items in the first column of a
        CustomTableWidget.
        """
        selected_rows = tab.selectedItems()
        all_gauges = self.get_all_gauges()
        return [item.text() for item in selected_rows if item.column() == 0 and item.text() not in all_gauges]

    # ! /\ GETTERS /\
    def save_geometry(self) -> None:
        """
        It saves the geometry of the window to the settings file
        """
        geometry.set_value(item_name="x", value=max(self.pos().x(), 0))
        geometry.set_value(item_name="y", value=max(self.pos().y(), 0))
        geometry.set_value(item_name="width", value=self.size().width())
        geometry.set_value(item_name="height", value=self.size().height())

    def save_menu_tab_order(self) -> None:
        settings_file.add_item(item_name="menu_tabs_order", value=self.get_menu_tab_order())

    # ! \/ Dialogs \/
    def show_about_dialog(self) -> None:
        """
        It creates an AboutDialog object and shows it.
        """
        dialog = AboutDialog(
            self,
            __name__,
            __version__,
            __updated__,
            "https://github.com/TheCodingJsoftware/Inventory-Manager",
        )
        dialog.show()

    def show_message_dialog(self, title: str, message: str, dialog_buttons: str = DialogButtons.ok) -> str:
        """
        It creates a message dialog, shows it, and returns the response

        Args:
          title (str): str = The title of the dialog
          message (str): str = The message to display in the dialog
          dialog_buttons (str): str = DialogButtons.ok

        Returns:
          The response is being returned.
        """
        message_dialog = MessageDialog(self, Icons.information, dialog_buttons, title, message)
        message_dialog.show()

        return message_dialog.get_response() if message_dialog.exec_() else ""

    def show_error_dialog(
        self,
        title: str,
        message: str,
        dialog_buttons: str = DialogButtons.ok_save_copy_cancel,
    ) -> str:
        """
        It creates a dialog box with a message and a title, and returns the response

        Args:
          title (str): str = The title of the dialog
          message (str): str = The message to be displayed in the dialog.
          dialog_buttons (str): str = DialogButtons.ok_save_copy_cancel,

        Returns:
          The response from the dialog.
        """
        message_dialog = MessageDialog(self, Icons.critical, dialog_buttons, title, message)
        message_dialog.show()

        response = message_dialog.get_response() if message_dialog.exec_() else ""

        if response == DialogButtons.copy:
            pixmap = QPixmap(self.message_dialog.grab())
            QApplication.clipboard().setPixmap(pixmap)
        elif response == DialogButtons.save:
            self.generate_error_log(message_dialog=message_dialog)
        return response

    def show_web_scrape_results(self, data) -> None:
        """
        Shows results of webscrape

        Args:
          data: a list of dictionaries
        """
        # QApplication.restoreOverrideCursor()
        results = WebScrapeResultsDialog(title="Results", message="Ebay search results", data=data)
        if results.exec_():
            response = results.get_response()
            if response == DialogButtons.ok:
                return

    def show_whats_new(self, show: bool = False) -> None:
        """
        If the latest version of the program is newer than the last time the program was opened, show
        the changelog.
        """

        def markdown_to_html(markdown_text):
            html = markdown.markdown(markdown_text)
            return html

        try:
            response = requests.get("https://api.github.com/repos/thecodingjsoftware/Inventory-Manager/releases/latest")
            version: str = response.json()["name"].replace(" ", "")
            if version == __version__ or show:
                build_date = time.strptime(__updated__, "%Y-%m-%d %H:%M:%S")
                current_date = time.strptime(
                    settings_file.get_value(item_name="last_opened"),
                    "%Y-%m-%d %H:%M:%S.%f",
                )
                if current_date < build_date or show:
                    with open("CHANGELOG.md", "r") as change_log_file:
                        self.show_message_dialog(title="Whats new?", message=markdown_to_html(change_log_file.read()))
                    settings_file.add_item(item_name="last_opened", value=str(datetime.now()))
        except Exception:
            return

    def show_not_trusted_user(self) -> None:
        """
        It shows a message dialog with a title and a message
        """
        self.tabWidget.setCurrentIndex(settings_file.get_value("menu_tabs_order").index(self.last_selected_menu_tab))
        self.show_message_dialog(
            title="Permission error",
            message="You don't have permission to change inventory items.\n\nnot sorry \n\n(:",
        )

    def add_item(self) -> None:
        """
        It adds an item to a category

        Returns:
          The response from the dialog.
        """
        add_item_dialog = AddItemDialog(
            title=f'Add new item to "{self.category}"',
            message=f"Adding a new item to \"{self.category}\".\n\nPress 'Add' when finished.",
        )

        if add_item_dialog.exec_():
            response = add_item_dialog.get_response()
            if response == DialogButtons.add:
                name: str = add_item_dialog.get_name()
                category_data = inventory.get_value(item_name=self.category)
                for item in list(category_data.keys()):
                    if name == item:
                        self.show_error_dialog(
                            "Invalid name",
                            f"'{name}'\nis an invalid item name.\n\nCan't be the same as other names.",
                            dialog_buttons=DialogButtons.ok,
                        )
                        return

                priority: int = add_item_dialog.get_priority()
                unit_quantity: float = add_item_dialog.get_unit_quantity()
                current_quantity: int = add_item_dialog.get_current_quantity()
                price: float = add_item_dialog.get_item_price()
                notes: str = add_item_dialog.get_notes()
                part_number: str = add_item_dialog.get_part_number()
                use_exchange_rate: bool = add_item_dialog.get_exchange_rate()
                group: str = add_item_dialog.get_group()

                try:
                    inventory.add_item_in_object(self.category, name)
                    inventory.change_object_in_object_item(self.category, name, "part_number", part_number)
                except KeyError:
                    self.show_error_dialog(
                        "Invalid characters",
                        f"'{name}'\nis an invalid item name.",
                        dialog_buttons=DialogButtons.ok,
                    )
                    return
                inventory.change_object_in_object_item(self.category, name, "unit_quantity", unit_quantity)
                inventory.change_object_in_object_item(self.category, name, "current_quantity", current_quantity)
                inventory.change_object_in_object_item(self.category, name, "price", price)
                inventory.change_object_in_object_item(self.category, name, "use_exchange_rate", use_exchange_rate)
                inventory.change_object_in_object_item(self.category, name, "priority", priority)
                inventory.change_object_in_object_item(self.category, name, "notes", notes)
                if group != "None":
                    inventory.change_object_in_object_item(self.category, name, "group", group)
                inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_name",
                    f"Item added\n{self.username}\n{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_part_number",
                    f"Item added\n{self.username}\n{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_unit_quantity",
                    f"Item added\n{self.username}\n{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_current_quantity",
                    f"Item added\n{self.username}\n{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_price",
                    f"Item added\n{self.username}\n{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_use_exchange_price",
                    f"Item added\n{self.username}\n{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_priority",
                    f"Item added\n{self.username}\n{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                inventory.change_object_in_object_item(
                    self.category,
                    name,
                    "latest_change_notes",
                    f"Item added\n{self.username}\n{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}",
                )
                self.sort_inventory()
                # self.load_active_tab()
            elif response == DialogButtons.cancel:
                return

    def set_custom_quantity_limit(self, tab: CustomTableWidget) -> None:
        """
        This function sets custom quantity limits for an item in a table widget and updates the table
        row color based on the current quantity and the new limits.

        Args:
          item_name (QComboBox): The name of the item for which the custom quantity limit is being set.
        It can be either a string representing the name of the item or a QComboBox object representing
        the dropdown menu for selecting the item.
        """
        with contextlib.suppress(AttributeError):
            table_widget: CustomTableWidget = self.tabs[self.category]
            try:
                selected_index = tab.selectedIndexes()[0].row()
            except IndexError:
                return

        item_name = tab.item(selected_index, 0).text()

        red_limit: int = self.get_value_from_category(item_name=item_name, key="red_limit")
        yellow_limit: int = self.get_value_from_category(item_name=item_name, key="yellow_limit")

        set_custom_limit_dialog = SetCustomLimitDialog(
            title="Set Custom Quantity Limit",
            message=f'Set a Custom Color Quantity Limit for:\n"{item_name}"',
            red_limit=red_limit,
            yellow_limit=yellow_limit,
        )

        if set_custom_limit_dialog.exec_():
            response = set_custom_limit_dialog.get_response()
            if response == DialogButtons.set:
                red_limit: float = set_custom_limit_dialog.get_red_limit()
                yellow_limit: float = set_custom_limit_dialog.get_yellow_limit()
                try:
                    self.active_json_file.change_object_in_object_item(self.category, item_name, "red_limit", red_limit)
                    self.active_json_file.change_object_in_object_item(self.category, item_name, "yellow_limit", yellow_limit)
                except KeyError:
                    return
                current_quantity = self.get_value_from_category(item_name=item_name, key="current_quantity")
                if current_quantity <= red_limit:
                    self.set_table_row_color(tab, selected_index, "#3F1E25")
                elif current_quantity <= yellow_limit:
                    self.set_table_row_color(tab, selected_index, "#413C28")
                else:
                    self.set_table_row_color(tab, selected_index, "#2c2c2c")
                self.sync_changes()
                if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":
                    self.load_active_tab()

    # NOTE deprecated
    def search_ebay(self) -> None:
        """
        It opens a dialog box, and if the user clicks ok, it starts a thread that scrapes ebay for the
        user's input.

        Returns:
          The response is a DialogButtons enum.
        """
        input_dialog = InputDialog(title="Search Ebay", message="Search for anything")
        if input_dialog.exec_():
            response = input_dialog.get_response()
            if response == DialogButtons.ok:
                input_text = input_dialog.inputText
                ebay_scraper_thread = EbayScraper(item_to_search=input_text)
                # QApplication.setOverrideCursor(Qt.BusyCursor)
                ebay_scraper_thread.signal.connect(self.show_web_scrape_results)
                self.threads.append(ebay_scraper_thread)
                ebay_scraper_thread.start()
            elif response == DialogButtons.cancel:
                return

    def create_new_category(self, event=None) -> None:
        """
        It creates a new category

        Args:
          event: The event that triggered the function.

        Returns:
          The return value of the function is None.
        """
        input_dialog = InputDialog(title="Create category", message="Enter a name for a new category.")
        if input_dialog.exec_():
            response = input_dialog.get_response()
            if response == DialogButtons.ok:
                input_text = input_dialog.inputText
                for category in self.categories:
                    if input_text in [category, "+"]:
                        self.show_error_dialog(
                            title="Invalid name",
                            message=f"'{input_text}' is an invalid name for a category.\n\nCan't have two categories with the same name.",
                            dialog_buttons=DialogButtons.ok,
                        )
                        return
                self.active_json_file.add_item(item_name=input_text, value={})
                self.sync_changes()
                self.load_categories()
            elif response == DialogButtons.cancel:
                return

    def delete_category(self) -> None:
        """
        It's a function that deletes a category from a list of categories

        Returns:
          The response from the dialog.
        """
        select_item_dialog = SelectItemDialog(
            button_names=DialogButtons.discard_cancel,
            title="Delete category",
            message="Select a category to delete.\n\nThis action is permanent and cannot\nbe undone.",
            items=self.categories,
        )

        if select_item_dialog.exec_():
            response = select_item_dialog.get_response()
            if response == DialogButtons.discard:
                if select_item_dialog.get_selected_item() in [
                    "Price Per Pound",
                    "Recut",
                    "Custom",
                ]:
                    self.show_error_dialog(
                        "no",
                        "Cannot delete this category, it is special. ;)",
                        dialog_buttons=DialogButtons.ok,
                    )
                    return
                try:
                    self.active_json_file.remove_item(select_item_dialog.get_selected_item())
                except AttributeError:
                    return
                settings_file.add_item(item_name="last_category_tab", value=0)
                self.sync_changes()
                self.load_categories()
            elif response == DialogButtons.cancel:
                return

    def clone_category(self) -> None:
        """
        It's a function that opens a dialog box that allows the user to select a category to clone

        Returns:
          The response from the dialog.
        """
        select_item_dialog = SelectItemDialog(
            button_names=DialogButtons.clone_cancel,
            title="Clone category",
            message="Select a category to clone.",
            items=self.categories,
        )

        if select_item_dialog.exec_():
            response = select_item_dialog.get_response()
            if response == DialogButtons.clone:
                try:
                    for category in self.categories:
                        if select_item_dialog.get_selected_item() in [
                            "Price Per Pound",
                            "Recut",
                            "Custom",
                        ]:
                            self.show_error_dialog(
                                "no",
                                "Cannot clone this category, it is special. ;)",
                                dialog_buttons=DialogButtons.ok,
                            )
                            return
                        if f"Clone from: {select_item_dialog.get_selected_item()} Double click me rename me" == category:
                            self.show_error_dialog(
                                "Invalid name",
                                f"'Clone from: {select_item_dialog.get_selected_item()} Double click me rename me'\nalready exists.\n\nCan't be the same as other names.",
                                dialog_buttons=DialogButtons.ok,
                            )
                            return
                    self.active_json_file.clone_key(select_item_dialog.get_selected_item())
                except AttributeError:
                    return
                self.sync_changes()
                self.load_categories()
            elif response == DialogButtons.cancel:
                return

    def rename_category(self, index) -> None:
        """
        It takes the index of the tab that was clicked, opens a dialog box, and if the user clicks ok,
        it renames the tab.

        Args:
          index: The index of the tab that was clicked.

        Returns:
          The return value of the function is the return value of the last expression evaluated, or None
        if no expression was evaluated.
        """
        if (
            self.tab_widget.tabText(0) == ""
            or self.tab_widget.tabText(index) == "Price Per Pound"
            or self.tab_widget.tabText(index) == "Recut"
            or self.tab_widget.tabText(index) == "Custom"
        ):
            return
        input_dialog = InputDialog(
            title="Rename category",
            message=f"Enter a new name for '{self.tab_widget.tabText(index)}'.",
            placeholder_text=self.tab_widget.tabText(index),
        )

        if input_dialog.exec_():
            response = input_dialog.get_response()
            if response == DialogButtons.ok:
                input_text = input_dialog.inputText
                for category in self.categories:
                    if input_text in [category, "+"]:
                        self.show_error_dialog(
                            title="Invalid name",
                            message=f"'{input_text}'\nis an invalid name for a category.\n\nCan't have two categories with the same name.",
                            dialog_buttons=DialogButtons.ok,
                        )
                        return
                self.active_json_file.change_key_name(key_name=self.tab_widget.tabText(index), new_name=input_text)
                self.sync_changes()
                self.load_categories()
            elif response == DialogButtons.cancel:
                return

    def open_group_menu(self, menu: QMenu) -> None:
        """
        It opens a menu at the current cursor position

        Args:
          menu (QMenu): QMenu
        """
        menu.exec_(QCursor.pos())

    def add_nest_directory(self) -> None:
        """
        This function adds a new directory to a list of quote nest directories and refreshes the list.
        """
        nest_directories: list[str] = settings_file.get_value("quote_nest_directories")
        if new_nest_directory := QFileDialog.getExistingDirectory(self, "Open directory", "/"):
            nest_directories.append(new_nest_directory)
            settings_file.add_item(item_name="quote_nest_directories", value=nest_directories)
            self.refresh_nest_directories()

    def remove_nest_directory(self) -> None:
        """
        This function removes a selected nest directory from a list of nest directories and updates the
        settings file.
        """
        nest_directories: list[str] = settings_file.get_value("quote_nest_directories")
        select_item_dialog = SelectItemDialog(
            button_names=DialogButtons.discard_cancel,
            title="Remove Nest Directory",
            message="Select a nest directory to delete. (from gui. not system)\n\nThis action is permanent and cannot\nbe undone.",
            items=nest_directories,
        )

        if select_item_dialog.exec_():
            response = select_item_dialog.get_response()
            if response == DialogButtons.discard:
                try:
                    nest_directories.remove(select_item_dialog.get_selected_item())
                except ValueError:  # No Item was selected
                    return
                settings_file.add_item(item_name="quote_nest_directories", value=nest_directories)
                self.refresh_nest_directories()
            elif response == DialogButtons.cancel:
                return

    def generate_quote(self) -> None:
        select_item_dialog = GenerateQuoteDialog(
            button_names=DialogButtons.generate_cancel,
            title="Quote Generator",
            message="Select which ever you need.\n\nPress Generate when ready.",
        )

        if select_item_dialog.exec_():
            response = select_item_dialog.get_response()
            if response == DialogButtons.generate:
                try:
                    action = select_item_dialog.get_selected_item()
                except AttributeError:
                    return
                self.save_quote_table_values()
                try:
                    generate_quote = GenerateQuote(action, self.quote_nest_information)
                except FileNotFoundError:
                    self.show_error_dialog(
                        "File not found, aborted",
                        'Invalid paths set for "path_to_sheet_prices" or "price_of_steel_information" in config file "laser_quote_variables.cfg"\n\nGenerating Quote Aborted.',
                    )
                    return
                if generate_quote.should_update_inventory:
                    self.upload_batch_to_inventory_thread()
                    if not self.is_nest_generated_from_parts_in_inventory:
                        self.upload_batched_parts_images(self.quote_nest_information)
                self.status_button.setText("Generating complete", "lime")
            elif response == DialogButtons.cancel:
                return

    def generate_quote_with_selected_parts(self, tab: CustomTableWidget) -> None:
        """
        This function generates a quote with selected parts and their corresponding information.

        Args:
          tab (CustomTableWidget): The parameter `tab` is of type `CustomTableWidget` and is used as an
        input to the `generate_quote_with_selected_parts` method. It is likely a reference to a table
        widget object that contains information about selected parts.
        """
        selected_parts = self.get_all_selected_parts(tab)
        try:
            sheet_gauge = self.get_value_from_category(item_name=selected_parts[0], key="gauge")
            sheet_dimension = self.get_value_from_category(item_name=selected_parts[0], key="sheet_dim")
            sheet_material = self.get_value_from_category(item_name=selected_parts[0], key="material")
            self.is_nest_generated_from_parts_in_inventory = True
        except IndexError:  # No item selected
            return
        self.quote_nest_information.clear()
        self.quote_nest_information["_/CUSTOM NEST"] = {
            "quantity_multiplier": 1,  # Sheet count
            "gauge": sheet_gauge,
            "material": sheet_material,
            "sheet_dim": "0.000x0.000" if sheet_dimension is None else sheet_dimension,
            "scrap_percentage": 0.0,
        }
        for part_name in selected_parts:
            self.quote_nest_information[part_name] = {
                "quantity": self.get_value_from_category(item_name=part_name, key="current_quantity"),
                "machine_time": self.get_value_from_category(item_name=part_name, key="machine_time"),
                "weight": self.get_value_from_category(item_name=part_name, key="weight"),
                "part_number": self.get_value_from_category(item_name=part_name, key="part_number"),
                "image_index": part_name,
                "surface_area": self.get_value_from_category(item_name=part_name, key="surface_area"),
                "cutting_length": self.get_value_from_category(item_name=part_name, key="cutting_length"),
                "file_name": "/CUSTOM NEST",
                "piercing_time": self.get_value_from_category(item_name=part_name, key="piercing_time"),
                "gauge": self.get_value_from_category(item_name=part_name, key="gauge"),
                "material": self.get_value_from_category(item_name=part_name, key="material"),
                "recut": False,
                "sheet_dim": "0.000x0.000"
                if self.get_value_from_category(item_name=part_name, key="sheet_dim") is None
                else self.get_value_from_category(item_name=part_name, key="sheet_dim"),
                "part_dim": self.get_value_from_category(item_name=part_name, key="part_dim"),
            }
        self.tabWidget.setCurrentIndex(self.get_menu_tab_order().index("Quote Generator"))
        self.download_required_images(self.quote_nest_information)
        # self.load_nests()

    def open_image(self, path: str, title: str) -> None:
        image_viewer = QImageViewer(self, path, title)
        image_viewer.show()

    def view_part_information(self, tab: CustomTableWidget) -> None:
        try:
            selected_part = self.get_all_selected_parts(tab)[0]
        except IndexError:
            return
        item_dialog = PartInformationViewer(
            selected_part,
            parts_in_inventory.get_data()[self.category][selected_part],
            self,
        )
        item_dialog.show()

    def set_order_number(self) -> None:
        """
        This function sets the order number by prompting the user to input a new integer value and
        updating the corresponding JSON file.

        Returns:
          None.
        """
        with open(settings_file.get_value("path_to_order_number")) as json_file:
            order_number_data = json.load(json_file)
        input_dialog = InputDialog(
            title="Set a Order Number",
            message="Enter a Order Number as a integer",
            button_names=DialogButtons.set_cancel,
            placeholder_text=order_number_data["order_number"],
        )
        if input_dialog.exec_():
            response = input_dialog.get_response()
            if response in [DialogButtons.set, DialogButtons.ok]:
                try:
                    input_number = int(input_dialog.inputText)
                    order_number_data["order_number"] = input_number
                    with open(settings_file.get_value("path_to_order_number"), "w", encoding="utf-8") as json_file:
                        json.dump(order_number_data, json_file, ensure_ascii=False, indent=4)
                except Exception:
                    self.show_error_dialog(
                        title="Invalid number",
                        message=f"'{input_dialog.inputText}' is an invalid numnber",
                        dialog_buttons=DialogButtons.ok,
                    )
                    return
            elif response == DialogButtons.cancel:
                return

    # ! /\ Dialogs /\

    # ! \/ INVENTORY TABLE CHANGES \/
    # NOTE for Edit Inventory
    def edit_inventory_item_changes(self, item: QTableWidgetItem) -> None:
        tab = self.tabs[self.category]
        tab.blockSignals(True)
        row_index = item.row()
        col_index = item.column()
        item_name: str = tab.item(item.row(), 0).text()
        try:
            new_part_number: str = tab.item(item.row(), 1).text()
            old_part_number = self.get_value_from_category(item_name, "part_number")
            unit_quantity: float = float(self.eval_expr(tab.item(item.row(), 2).text().replace(" ", "")))
            current_quantity: float = float(self.eval_expr(tab.item(item.row(), 3).text().replace(" ", "")))
            old_current_quantity = self.get_value_from_category(item_name, "current_quantity")
            price: float = float(
                self.eval_expr(tab.item(item.row(), 4).text().replace("$", "").replace("CAD", "").replace("USD", "").replace(" ", ""))
            )
            old_price = self.get_value_from_category(item_name, "price")
        except (ValueError, TypeError, SyntaxError) as e:
            item.setForeground(QColor("red"))
            self.status_button.setText(f"{item_name}: Enter a valid number, aborted!", "red")
            tab.blockSignals(False)
            return
        QApplication.setOverrideCursor(Qt.BusyCursor)
        if col_index == 1:  # Part Number
            inventory.change_object_in_object_item(self.category, item_name, "part_number", new_part_number)
            for category, items in inventory.get_data().items():
                if category == self.category:
                    continue
                for item, item_data in items.items():
                    if old_part_number == item_data.get("part_number"):
                        inventory.change_object_in_object_item(
                            object_name=category, item_name=item, value_name="part_number", new_value=new_part_number
                        )
        elif col_index == 2:  # Quantity per Unit
            inventory.change_object_in_object_item(self.category, item_name, "unit_quantity", unit_quantity)
            self.update_stock_costs()
        elif col_index == 3:  # Quantity in Stock
            inventory.change_object_in_object_item(self.category, item_name, "current_quantity", current_quantity)
            modified_date: str = (
                f"{self.username} - Changed from {old_current_quantity} to {current_quantity} at {datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}"
            )
            tab.item(row_index, col_index).setToolTip(modified_date)
            inventory.change_object_in_object_item(self.category, item_name, "latest_change_current_quantity", modified_date)
            for category, items in inventory.get_data().items():
                if category == self.category:
                    continue
                for item, item_data in items.items():
                    if new_part_number == item_data.get("part_number"):
                        inventory.change_object_in_object_item(category, item, "latest_change_current_quantity", modified_date)
                        inventory.change_object_in_object_item(
                            object_name=category, item_name=item, value_name="current_quantity", new_value=current_quantity
                        )
            self.sort_inventory()
        elif col_index == 4:  # Item Price
            use_exchange_rate: bool = self.get_value_from_category(item_name=item_name, key="use_exchange_rate")
            modified_date: str = f"{self.username} - Changed from {old_price} to {price} at {datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}"
            converted_price: float = price * self.get_exchange_rate() if use_exchange_rate else price / self.get_exchange_rate()
            price_item = tab.item(row_index, col_index)
            price_item.setText(f'${price:,.2f} {"USD" if use_exchange_rate else "CAD"}')
            price_item.setToolTip(f'${converted_price:,.2f} {"CAD" if use_exchange_rate else "USD"}\n{modified_date}')
            inventory.change_object_in_object_item(self.category, item_name, "price", price)
            inventory.change_object_in_object_item(self.category, item_name, "latest_change_price", modified_date)
            self.update_stock_costs()
            for category, items in inventory.get_data().items():
                if category == self.category:
                    continue
                for item, item_data in items.items():
                    if new_part_number == item_data.get("part_number"):
                        inventory.change_object_in_object_item(object_name=category, item_name=item, value_name="price", new_value=price)
                        inventory.change_object_in_object_item(
                            object_name=category, item_name=item, value_name="latest_change_price", new_value=modified_date
                        )
        tab.blockSignals(False)
        if col_index != 3:
            self.sync_changes()
        QApplication.restoreOverrideCursor()

    # NOTE for Parts in Inventory
    def parts_in_inventory_item_changes(self, item: QTableWidgetItem) -> None:
        category_data = parts_in_inventory.get_data()
        tab = self.tabs[self.category]
        tab.blockSignals(True)
        item_name: str = tab.item(item.row(), 0).text()
        try:
            item_price: float = float(self.eval_expr(tab.item(item.row(), 1).text().replace("$", "").replace(" ", "")))
            unit_quantity: float = float(self.eval_expr(tab.item(item.row(), 2).text()))
            current_quantity: float = float(self.eval_expr(tab.item(item.row(), 3).text()))
            new_modified_date: str = (
                f'{self.username} - Manually set to {current_quantity} quantity at {str(datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"))}'
            )
        except (ValueError, TypeError, SyntaxError) as e:
            item.setForeground(QColor("red"))
            self.status_button.setText(f"{item_name}: Enter a valid number, aborted!", "red")
            tab.blockSignals(False)
            return

        item.setForeground(QColor("white"))

        if item.column() == 1:
            price_item = tab.item(item.row(), 1)
            price_item.setText(f"${item_price:,.2f}")
        elif item.column() == 3:
            notes_item = tab.item(item.row(), 5)
            notes_item.setText(new_modified_date)
            parts_in_inventory.change_object_in_object_item(self.category, item_name, "modified_date", new_modified_date)

        tab.blockSignals(False)

        for category in list(category_data.keys()):
            if category in ["Recut", self.category]:
                continue
            if item_name in list(parts_in_inventory.get_data()[category].keys()):
                parts_in_inventory.change_object_in_object_item(
                    object_name=category,
                    item_name=item_name,
                    value_name="current_quantity",
                    new_value=current_quantity,
                )
                parts_in_inventory.change_object_in_object_item(
                    object_name=category,
                    item_name=item_name,
                    value_name="modified_date",
                    new_value=new_modified_date,
                )
        parts_in_inventory.change_object_in_object_item(self.category, item_name, "unit_quantity", unit_quantity)
        parts_in_inventory.change_object_in_object_item(self.category, item_name, "price", item_price)
        parts_in_inventory.change_object_in_object_item(self.category, item_name, "current_quantity", current_quantity)

        self.calculate_parts_in_inventory_summary()
        self.sync_changes()
        QApplication.restoreOverrideCursor()

    # NOTE for Sheets in Inventory
    def sheets_in_inventory_item_changes(self, item: QTableWidgetItem) -> None:
        tab = self.tabs[self.category]
        tab.blockSignals(True)
        row_index: int = item.row()
        item_name: str = tab.item(row_index, 0).text()
        if self.category == "Price Per Pound":
            try:
                new_price: float = float(self.eval_expr(tab.item(row_index, 1).text().replace("$", "").replace(" ", "")))
            except (ValueError, TypeError, SyntaxError) as e:
                item.setForeground(QColor("red"))
                self.status_button.setText(f"{item_name}: Enter a valid number, aborted!", "red")
                tab.blockSignals(False)
                return
            item.setForeground(QColor("white"))
            price_item = tab.item(item.row(), 1)
            price_item.setText(f"${new_price:,.2f}")
            old_price = self.get_value_from_category(item_name, "price")
            modified_date: str = (
                f'{self.username} - Modified from ${old_price:,.2f} to ${new_price:,.2f} at {datetime.now().strftime("%B %d %A %Y %I:%M:%S %p")}'
            )
            price_of_steel_inventory.change_object_in_object_item(self.category, item_name, "price", new_price)
            price_of_steel_inventory.change_object_in_object_item(self.category, item_name, "latest_change_price", modified_date)
        else:
            try:
                new_quantity: float = float(self.eval_expr(tab.item(row_index, 2).text().replace(" ", "")))
            except (ValueError, TypeError, SyntaxError) as e:
                item.setForeground(QColor("red"))
                self.status_button.setText(f"{item_name}: Enter a valid number, aborted!", "red")
                tab.blockSignals(False)
                return
            item.setForeground(QColor("white"))
            notes: str = tab.item(row_index, 5).text()
            old_quantity: float = self.get_value_from_category(item_name, "current_quantity")
            modified_date: str = (
                f"{self.username} - Manually set to {new_quantity} from {old_quantity} at {datetime.now().strftime('%B %d %A %Y %I:%M:%S %p')}"
            )
            price_of_steel_inventory.change_object_in_object_item(self.category, item_name, "notes", notes)
            price_of_steel_inventory.change_object_in_object_item(self.category, item_name, "current_quantity", new_quantity)
            price_of_steel_inventory.change_object_in_object_item(self.category, item_name, "latest_change_current_quantity", modified_date)
        self.load_active_tab()
        tab.blockSignals(False)
        self.sync_changes()
        QApplication.restoreOverrideCursor()

    # ! /\ INVENTORY TABLE CHANGES /\

    # ! \/ Load UI \/
    def load_history_view(self) -> None:
        """
        It loads the history view of the application.
        """
        # CATEOGRY HISTORY
        self.categoryHistoryTable.clear()
        self.categoryHistoryTable.setRowCount(0)
        self.categoryHistoryTable.setHorizontalHeaderLabels(("Date;Description;").split(";"))
        self.categoryHistoryTable.setColumnWidth(0, 270)
        self.categoryHistoryTable.setColumnWidth(1, 600)
        history_file = HistoryFile()
        for i, date, description in zip(
            range(len(history_file.get_data_from_category()["Date"])),
            history_file.get_data_from_category()["Date"],
            history_file.get_data_from_category()["Description"],
        ):
            self.categoryHistoryTable.insertRow(self.categoryHistoryTable.rowCount())
            self.categoryHistoryTable.setItem(i, 0, QTableWidgetItem(date))
            self.categoryHistoryTable.setItem(i, 1, QTableWidgetItem(description))
        # SINGLE ITEM HISTORY
        self.singleItemHistoryTable.clear()
        self.singleItemHistoryTable.setRowCount(0)
        self.singleItemHistoryTable.setHorizontalHeaderLabels(("Date;Description;").split(";"))
        self.singleItemHistoryTable.setColumnWidth(0, 270)
        self.singleItemHistoryTable.setColumnWidth(1, 600)
        for i, date, description in zip(
            range(len(history_file.get_data_from_single_item()["Date"])),
            history_file.get_data_from_single_item()["Date"],
            history_file.get_data_from_single_item()["Description"],
        ):
            self.singleItemHistoryTable.insertRow(self.singleItemHistoryTable.rowCount())
            self.singleItemHistoryTable.setItem(i, 0, QTableWidgetItem(date))
            self.singleItemHistoryTable.setItem(i, 1, QTableWidgetItem(description))

    def load_price_history_view(self) -> None:
        """
        It loads the history view of the application.
        """
        # CATEOGRY HISTORY
        self.priceHistoryTable.clear()
        self.priceHistoryTable.setRowCount(0)
        self.priceHistoryTable.setHorizontalHeaderLabels(("Date;Part Name;Part #;Old Price;New Price").split(";"))
        self.priceHistoryTable.setColumnWidth(0, 270)
        self.priceHistoryTable.setColumnWidth(1, 600)
        price_history_file = PriceHistoryFile(file_name=f"{settings_file.get_value(item_name='price_history_file_name')}.xlsx")
        for i, date, part_name, part_number, old_price, new_price in zip(
            range(len(price_history_file.get_data_from_category()["Date"])),
            price_history_file.get_data_from_category()["Date"],
            price_history_file.get_data_from_category()["Part Name"],
            price_history_file.get_data_from_category()["Part Number"],
            price_history_file.get_data_from_category()["Old Price"],
            price_history_file.get_data_from_category()["New Price"],
        ):
            if i == 0:
                continue
            self.priceHistoryTable.insertRow(self.priceHistoryTable.rowCount())
            self.priceHistoryTable.setItem(i - 1, 0, QTableWidgetItem(str(date)))
            self.priceHistoryTable.setItem(i - 1, 1, QTableWidgetItem(str(part_name)))
            self.priceHistoryTable.setItem(i - 1, 2, QTableWidgetItem(str(part_number)))
            self.priceHistoryTable.setItem(i - 1, 3, QTableWidgetItem(str(old_price)))
            self.priceHistoryTable.setItem(i - 1, 4, QTableWidgetItem(str(new_price)))

    def load_tree_view(self, inventory: JsonFile):
        """
        > This function loads the inventory into the tree view

        Args:
          inventory: The inventory object that is being displayed.
        """
        self.clear_layout(self.search_layout)
        tree_view = ViewTree(data=inventory.get_data())
        self.search_layout.addWidget(tree_view, 0, 0)

    def load_categories(self) -> None:
        """
        It loads the categories from the inventory file and creates a tab for each category.
        """
        if (
            not self.trusted_user
            and self.tabWidget.tabText(self.tabWidget.currentIndex()) != "Sheets in Inventory"
            and self.tabWidget.tabText(self.tabWidget.currentIndex()) != "Parts in Inventory"
            and self.tabWidget.tabText(self.tabWidget.currentIndex()) != "View Inventory (Read Only)"
        ):
            # print(self.last_selected_menu_tab)
            # self.tabWidget.setCurrentIndex(settings_file.get_value('menu_tabs_order').index(self.last_selected_menu_tab))
            # self.show_not_trusted_user()

            self.set_layout_message("Insufficient Privileges, Access Denied", "", "", 0)
            return

        # No idea what this is supposed to do, but im too scared to delete it - Jared
        JsonFile(file_name=f"data/{self.inventory_file_name}")
        JsonFile(file_name=f"data/{self.inventory_file_name} - Price of Steel")
        JsonFile(file_name=f"data/{self.inventory_file_name} - Parts in Inventory")
        # QApplication.setOverrideCursor(Qt.BusyCursor)
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) not in [
            "Edit Inventory",
            "Parts in Inventory",
            "Sheets in Inventory",
        ]:
            return
        self.clear_layout(self.active_layout)
        self.tabs.clear()
        if self.active_json_file is None:
            return
        else:
            self.categories = self.active_json_file.get_keys()
        self.menuOpen_Category.clear()
        for i, category in enumerate(self.categories):
            action = QAction(self)
            action.setIcon(QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/project_open.png"))
            action.triggered.connect(partial(self.quick_load_category, category))
            action.setText(category)
            self.menuOpen_Category.addAction(action)
        self.tab_widget = CustomTabWidget(self)
        # self.tab_widget.setStyleSheet("QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
        self.tab_widget.tabBarDoubleClicked.connect(self.rename_category)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        i: int = -1
        for i, category in enumerate(self.categories):
            tab = CustomTableWidget(self)
            if category == "Price Per Pound" and self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":
                self.pushButton_add_new_sheet.setEnabled(False)
            elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":
                self.pushButton_add_new_sheet.setEnabled(True)
            if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Edit Inventory":
                tab.itemSelectionChanged.connect(partial(self.inventory_cell_changed, tab))
                tab.itemChanged.connect(self.edit_inventory_item_changes)
            if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":
                tab.itemChanged.connect(self.sheets_in_inventory_item_changes)
            if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Parts in Inventory":
                tab.itemSelectionChanged.connect(partial(self.parts_in_inventory_cell_changed, tab))
                tab.itemChanged.connect(self.parts_in_inventory_item_changes)
            self.tabs[category] = tab
            self.tab_widget.addTab(tab, category)

        if i == -1:
            tab = QScrollArea(self)
            content_widget = QWidget()
            content_widget.setObjectName("tab")
            tab.setWidget(content_widget)
            tab.setWidgetResizable(True)
            layout = QVBoxLayout(content_widget)
            layout.setAlignment(Qt.AlignTop)
            self.tabs[category] = layout
            self.tab_widget.addTab(tab, "")
            i += 1
        try:
            self.tab_widget.set_tab_order(category_tabs_order.get_value(self.tabWidget.tabText(self.tabWidget.currentIndex())))
        except:
            pass
        self.tab_widget.setCurrentIndex(settings_file.get_value("last_category_tab"))
        self.tab_widget.currentChanged.connect(self.load_active_tab)
        self.active_layout.addWidget(self.tab_widget)
        self.update_category_total_stock_costs()
        self.update_all_parts_in_inventory_price()
        self.calculate_parts_in_inventory_summary()
        self.load_active_tab()

    def load_active_tab(self) -> None:
        """
        It loads the data from the inventory file and displays it in the GUI

        Returns:
          The return value is a list of QWidget objects.
        """
        self.category = self.tab_widget.tabText(self.tab_widget.currentIndex())
        self.po_buttons.clear()
        self.pushButton_create_new.setEnabled(True)
        self.radioButton_category.setEnabled(True)
        self.radioButton_single.setEnabled(True)

        try:
            self.clear_layout(self.tabs[self.category])
        except IndexError:
            return
        settings_file.add_item("last_category_tab", self.tab_widget.currentIndex())
        tab: CustomTableWidget = self.tabs[self.category]
        category_data = self.active_json_file.get_value(item_name=self.category)
        autofill_search_options = self.get_all_part_names() + self.get_all_part_numbers()
        completer = QCompleter(autofill_search_options)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit_search_items.setCompleter(completer)

        self.update_list_widget()
        self.update_category_total_stock_costs()
        self.calculuate_price_of_steel_summary()
        self.label_category_name.setText(f"Category: {self.category}")
        self.quantities_change()

        try:
            if not list(category_data.keys()):
                self.pushButton_create_new.setEnabled(True)
                self.pushButton_add_quantity.setEnabled(False)
                self.pushButton_remove_quantity.setEnabled(False)
                self.radioButton_category.setEnabled(False)
                self.radioButton_single.setEnabled(False)
                # QApplication.restoreOverrideCursor()
                return
        except AttributeError:
            self.set_layout_message("You need to", "create", "a category", 120, self.create_new_category)
        try:
            self._iter = iter(range(len(list(category_data.keys()))))
        except AttributeError:
            self.set_layout_message("You need to", "create", "a category", 120, self.create_new_category)
            self.pushButton_create_new.setEnabled(False)
            self.pushButton_add_quantity.setEnabled(False)
            self.pushButton_remove_quantity.setEnabled(False)
            self.radioButton_category.setEnabled(False)
            self.radioButton_single.setEnabled(False)
            # QApplication.restoreOverrideCursor()
            return

        if self.category == "Price Per Pound" and self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":
            self.pushButton_add_new_sheet.setEnabled(False)
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":
            self.pushButton_add_new_sheet.setEnabled(True)
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Edit Inventory":
            self.load_inventory_items(tab, category_data)
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":
            self.price_of_steel_item(tab, category_data)
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Parts in Inventory":
            self.load_inventory_parts(tab, category_data)
        with contextlib.suppress(IndexError):
            category_tabs_order.set_value(
                self.tabWidget.tabText(self.tabWidget.currentIndex()),
                value=self.tabWidget.currentWidget().findChildren(CustomTabWidget)[0].get_tab_order(),
            )

    # NOTE PARTS IN INVENTYORY
    def load_inventory_parts(self, tab: CustomTableWidget, category_data: dict) -> None:
        """
        This function loads inventory parts data into a custom table widget in a graphical user
        interface.

        Args:
          tab (CustomTableWidget): The tab parameter is a CustomTableWidget object, which is a custom
        widget used to display data in a table format.
          category_data (dict): A dictionary containing data for items in a specific category. The keys
        of the dictionary are the names of the items, and the values are dictionaries containing various
        information about the item such as its current quantity, unit quantity, price, modified date,
        and limits for quantity levels.
        """
        tab.blockSignals(True)
        tab.set_editable_column_index([2, 3])
        tab.setEnabled(False)
        tab.clear()
        tab.setShowGrid(False)
        tab.setColumnCount(7)
        # tab.setAlternatingRowColors(True)
        tab.setRowCount(0)
        tab.setSortingEnabled(False)
        tab.setSelectionBehavior(1)
        tab.setSelectionMode(3)
        tab.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        tab.setHorizontalHeaderLabels(("Part Name;Item Price;Quantity Per Unit;Quantity in Stock;Cost in Stock;Modified Date;DEL;").split(";"))

        grouped_data = parts_in_inventory.sort_by_groups(category=category_data, groups_id="gauge")
        row_index: int = 0
        for group in list(grouped_data.keys()):
            tab.insertRow(row_index)
            item = QTableWidgetItem(group)
            item.setTextAlignment(4)  # Align text center
            font = QFont()
            font.setPointSize(15)
            item.setFont(font)
            tab.setItem(row_index, 0, item)
            tab.setSpan(row_index, 0, 1, tab.columnCount())
            self.set_table_row_color(tab, row_index, "#292929")
            row_index += 1
            for item in list(grouped_data[group].keys()):
                col_index: int = 0
                tab.insertRow(row_index)
                current_quantity: int = self.get_value_from_category(item_name=item, key="current_quantity")
                unit_quantity: int = self.get_value_from_category(item_name=item, key="unit_quantity")
                price: float = self.get_value_from_category(item_name=item, key="price")

                if self.category not in ["Recut", "Custom"]:
                    weight: float = self.get_value_from_category(item_name=item, key="weight")
                    machine_time: float = self.get_value_from_category(item_name=item, key="machine_time")
                    material: str = self.get_value_from_category(item_name=item, key="material")
                    price_per_pound: float = price_of_steel_inventory.get_data()["Price Per Pound"][material]["price"]
                    cost_for_laser: float = 250 if material in {"304 SS", "409 SS", "Aluminium"} else 150
                    price = float((machine_time * (cost_for_laser / 60)) + (weight * price_per_pound))

                modified_date: str = self.get_value_from_category(item_name=item, key="modified_date")
                red_limit: float = self.get_value_from_category(item_name=item, key="red_limit")
                if red_limit is None:
                    red_limit = 2
                yellow_limit: float = self.get_value_from_category(item_name=item, key="yellow_limit")
                if yellow_limit is None:
                    yellow_limit = 5
                tab.setItem(row_index, col_index, QTableWidgetItem(f"{item}"))
                tab.item(row_index, col_index).setFont(self.tables_font)

                col_index += 1
                # PRICE
                tab.setItem(row_index, col_index, QTableWidgetItem(f"${price:,.2f}"))
                tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
                tab.item(row_index, col_index).setFont(self.tables_font)

                col_index += 1
                # UNIT QUANTITY
                tab.setItem(row_index, col_index, QTableWidgetItem(f"{unit_quantity}"))
                tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
                tab.item(row_index, col_index).setFont(self.tables_font)

                col_index += 1
                # QUANTITY
                tab.setItem(row_index, col_index, QTableWidgetItem(f"{current_quantity}"))
                tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
                tab.item(row_index, col_index).setFont(self.tables_font)

                col_index += 1
                # TOTAL COST
                tab.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(f"${(price*current_quantity):,.2f}"),
                )
                tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
                tab.item(row_index, col_index).setFont(self.tables_font)

                col_index += 1
                # MODFIED DATE
                tab.setItem(row_index, col_index, QTableWidgetItem(modified_date))
                tab.item(row_index, col_index).setFont(self.tables_font)

                col_index += 1
                # DELETE
                btn_delete = DeletePushButton(
                    parent=self,
                    tool_tip=f"Delete {item} permanently from {self.category}",
                    icon=QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/trash.png"),
                )
                btn_delete.setStyleSheet("margin-top: 3%; margin-bottom: 3%; margin-left: 10%; margin-right: 10%;")
                btn_delete.clicked.connect(partial(self.delete_item, self.category, item))
                tab.setCellWidget(row_index, col_index, btn_delete)
                if self.category != "Recut":
                    if current_quantity <= red_limit:
                        self.set_table_row_color(tab, row_index, "#3F1E25")
                    elif current_quantity <= yellow_limit:
                        self.set_table_row_color(tab, row_index, "#413C28")
                row_index += 1
        tab.setEnabled(True)
        tab.resizeColumnsToContents()
        if tab.contextMenuPolicy() != Qt.CustomContextMenu:
            tab.setContextMenuPolicy(Qt.CustomContextMenu)
            menu = QMenu(self)
            action = QAction(self)
            action.setText("View Parts Data")
            action.triggered.connect(partial(self.view_part_information, tab))
            menu.addAction(action)
            menu.addSeparator()
            action = QAction(self)
            if self.category != "Recut":
                action.setText("Set Custom Quantity Limit")
                action.triggered.connect(partial(self.set_custom_quantity_limit, tab))
                menu.addAction(action)
                menu.addSeparator()
            categories = QMenu(menu)
            categories.setTitle("Move to category")
            for i, category in enumerate(parts_in_inventory.get_keys()):
                if self.category == category or category == "Recut":
                    continue
                if i == 1:
                    categories.addSeparator()
                action = QAction(self)
                action.setText(category)
                action.triggered.connect(partial(self.move_to_category, tab, category))
                categories.addAction(action)
            menu.addMenu(categories)

            categories = QMenu(menu)
            categories.setTitle("Copy to category")
            for i, category in enumerate(parts_in_inventory.get_keys()):
                if self.category == category or category == "Recut":
                    continue
                if i == 1:
                    categories.addSeparator()
                action = QAction(self)
                action.setText(category)
                action.triggered.connect(partial(self.copy_to_category, tab, category))
                categories.addAction(action)
            menu.addMenu(categories)
            menu.addSeparator()
            if self.category != "Recut":
                action = QAction(self)
                action.setText("Generate Quote with Selected Parts")
                action.triggered.connect(partial(self.generate_quote_with_selected_parts, tab))
                menu.addAction(action)
            tab.customContextMenuRequested.connect(partial(self.open_group_menu, menu))
        tab.blockSignals(False)
        QApplication.restoreOverrideCursor()

    # NOTE SHEETS IN INVENTORY
    def price_of_steel_item(self, tab: CustomTableWidget, category_data: dict) -> None:
        """
        This function takes a QVBoxLayout, an int, and a dict and returns None.

        Args:
          tab (QVBoxLayout): QVBoxLayout
          category_data (dict): dict = {
        """
        tab.blockSignals(True)
        tab.setEnabled(False)
        tab.clear()
        tab.setShowGrid(False)
        tab.setStyleSheet("QTableView::item#group { border-bottom: 2px solid %s; }" % QColor(0, 0, 0, 0).name())
        tab.setRowCount(0)
        tab.setSortingEnabled(False)
        tab.setSelectionBehavior(1)
        tab.setSelectionMode(1)
        tab.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        QApplication.setOverrideCursor(Qt.BusyCursor)
        row_index: int = 0
        if self.category == "Price Per Pound":
            tab.setColumnCount(3)
            tab.setHorizontalHeaderLabels(("Material;Price;Modified Date;").split(";"))
            tab.horizontalHeader().setStretchLastSection(True)
            tab.set_editable_column_index([1])
            for material in list(price_of_steel_inventory.get_data()[self.category].keys()):
                tab.insertRow(row_index)
                price = self.get_value_from_category(item_name=material, key="price")
                latest_change_price = self.get_value_from_category(item_name=material, key="latest_change_price").replace("\n", " ")
                # SHEET NAME
                tab.setItem(row_index, 0, QTableWidgetItem(material))
                tab.item(row_index, 0).setFont(self.tables_font)
                # PRICE
                tab.setItem(row_index, 1, QTableWidgetItem(f"${price:,.2f}"))
                tab.item(row_index, 1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
                tab.item(row_index, 1).setFont(self.tables_font)
                # MODIFIED DATE
                tab.setItem(row_index, 2, QTableWidgetItem(latest_change_price))
                tab.item(row_index, 2).setFont(self.tables_font)
                row_index += 1
        else:
            tab.setColumnCount(8)
            tab.setHorizontalHeaderLabels(
                ("Sheet Name;Cost per Sheet;Quantity in Stock;Total Cost in Stock;Order Status;Notes;Modified Date;DEL;").split(";")
            )
            tab.set_editable_column_index([2, 5])
            grouped_data = price_of_steel_inventory.sort_by_groups(category=category_data, groups_id="material")
            for group in list(grouped_data.keys()):
                tab.insertRow(row_index)
                item = QTableWidgetItem(group)
                item.setTextAlignment(4)  # Align text center

                font = QFont()
                font.setPointSize(15)
                item.setFont(font)
                tab.setItem(row_index, 0, item)
                tab.setSpan(row_index, 0, 1, tab.columnCount())
                self.set_table_row_color(tab, row_index, "#292929")
                row_index += 1
                for item in list(grouped_data[group].keys()):
                    col_index: int = 0
                    tab.insertRow(row_index)
                    current_quantity: float = self.get_value_from_category(item_name=item, key="current_quantity")
                    notes: str = self.get_value_from_category(item_name=item, key="notes")
                    modified_date: str = self.get_value_from_category(item_name=item, key="latest_change_current_quantity").replace("\n", " ")
                    thickness: str = self.get_value_from_category(item_name=item, key="thickness")
                    material: str = self.get_value_from_category(item_name=item, key="material")
                    sheet_dimension: str = self.get_value_from_category(item_name=item, key="sheet_dimension").replace(" x ", "x")
                    # POUNDS PER SQUARE FOOT
                    try:
                        pounds_per_square_foot: float = float(price_of_steel_information.get_data()["pounds_per_square_foot"][material][thickness])
                    except KeyError:
                        pounds_per_square_foot: float = 0.0
                    # POUNDS PER SHEET
                    try:
                        sheet_length = float(sheet_dimension.split("x")[0])
                        sheet_width = float(sheet_dimension.split("x")[1])
                    except AttributeError:
                        return
                    try:
                        pounds_per_sheet: float = ((sheet_length * sheet_width) / 144) * pounds_per_square_foot
                    except ZeroDivisionError:
                        pounds_per_sheet = 0.0
                    # PRICE PER POUND
                    try:
                        price_per_pound: float = float(price_of_steel_inventory.get_data()["Price Per Pound"][material]["price"])
                    except KeyError:
                        price_per_pound: float = 0.0

                    red_limit: float = self.get_value_from_category(item_name=item, key="red_limit")
                    if red_limit is None:
                        red_limit = 4
                    yellow_limit: float = self.get_value_from_category(item_name=item, key="yellow_limit")
                    if yellow_limit is None:
                        yellow_limit = 10

                    is_order_pending = self.get_value_from_category(item_name=item, key="is_order_pending")
                    if is_order_pending is None:
                        is_order_pending = False

                    # COST PER SHEET
                    cost_per_sheet = pounds_per_sheet * price_per_pound

                    # TOTAL COST
                    total_cost = cost_per_sheet * current_quantity

                    # ITEM
                    tab.setItem(row_index, col_index, QTableWidgetItem(item))
                    tab.item(row_index, col_index).setFont(self.tables_font)
                    col_index += 1
                    # COST
                    tab.setItem(row_index, col_index, QTableWidgetItem(f"${cost_per_sheet:,.2f}"))
                    tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
                    tab.item(row_index, col_index).setFont(self.tables_font)
                    col_index += 1
                    # CURRENT QUANTITY
                    tab.setItem(row_index, col_index, QTableWidgetItem(str(current_quantity)))
                    tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
                    tab.item(row_index, col_index).setFont(self.tables_font)
                    col_index += 1
                    # COST IN STOCK
                    tab.setItem(row_index, col_index, QTableWidgetItem(f"${total_cost:,.2f}"))
                    tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
                    tab.item(row_index, col_index).setFont(self.tables_font)
                    col_index += 1
                    # ORDER STATUS
                    order_status_button = OrderStatusButton(self)
                    order_status_button.setChecked(is_order_pending)
                    order_status_button.clicked.connect(partial(self.order_status_button, item, order_status_button, row_index))
                    order_status_button.setStyleSheet("margin-top: 3%; margin-bottom: 3%; margin-left: 10%; margin-right: 10%;")
                    tab.setCellWidget(row_index, col_index, order_status_button)
                    col_index += 1
                    # NOTES
                    tab.setItem(row_index, col_index, QTableWidgetItem(notes))
                    tab.item(row_index, col_index).setFont(self.tables_font)
                    col_index += 1
                    # MODIFIED DATE
                    tab.setItem(row_index, col_index, QTableWidgetItem(modified_date))
                    tab.item(row_index, col_index).setFont(self.tables_font)
                    col_index += 1

                    # DELETE
                    btn_delete = DeletePushButton(
                        parent=self,
                        tool_tip=f"Delete {item} permanently from {self.category}",
                        icon=QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/trash.png"),
                    )
                    # btn_delete.setFixedSize(26, 26)
                    btn_delete.clicked.connect(partial(self.delete_item, self.category, item))
                    btn_delete.setStyleSheet("margin-top: 3%; margin-bottom: 3%; margin-left: 10%; margin-right: 10%;")
                    tab.setCellWidget(row_index, col_index, btn_delete)
                    if current_quantity <= red_limit:
                        self.set_table_row_color(tab, row_index, "#3F1E25")
                    elif current_quantity <= yellow_limit:
                        self.set_table_row_color(tab, row_index, "#413C28")
                    if is_order_pending:
                        self.set_table_row_color(tab, row_index, "#29422c")
                    row_index += 1

        tab.setEnabled(True)
        tab.resizeColumnsToContents()
        tab.blockSignals(False)
        if self.category == "Price Per Pound":
            tab.setColumnWidth(1, 200)
        else:
            tab.setColumnWidth(5, 200)
        if tab.contextMenuPolicy() != Qt.CustomContextMenu:
            tab.setContextMenuPolicy(Qt.CustomContextMenu)
            menu = QMenu(self)
            action = QAction(self)
            action.triggered.connect(partial(self.set_custom_quantity_limit, tab))
            action.setText("Set Custom Quantity Limit")
            menu.addAction(action)
            tab.customContextMenuRequested.connect(partial(self.open_group_menu, menu))
        QApplication.restoreOverrideCursor()

    # NOTE EDIT INVENTORY
    def load_inventory_items(self, tab: CustomTableWidget, category_data: dict) -> None:
        """
        This function loads data into a QTableWidget for a specific category.

        Args:
          tab (QTableWidget): The QTableWidget object that is being loaded with data.
          category_data (dict): The `category_data` parameter is a dictionary containing information
        about the items in a particular category. The keys of the dictionary are the names of the items,
        and the values are dictionaries containing various information about each item, such as its part
        number, current quantity, price, priority, and notes. This
        """
        tab.blockSignals(True)
        tab.setEnabled(False)
        tab.clear()
        tab.setShowGrid(False)
        tab.setColumnCount(12)
        # tab.setAlternatingRowColors(True)
        tab.setRowCount(0)
        tab.setSortingEnabled(False)
        tab.setSelectionBehavior(1)
        tab.setSelectionMode(1)
        tab.set_editable_column_index([1, 2, 3, 4])
        tab.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        tab.setHorizontalHeaderLabels(
            (
                "Part Name;Part Number;Quantity Per Unit;Quantity in Stock;Item Price;USD/CAD;Total Cost in Stock;Total Unit Cost;Priority;Notes;PO;DEL;"
            ).split(";")
        )
        QApplication.setOverrideCursor(Qt.BusyCursor)

        # else:
        po_menu = QMenu(self)
        for po in get_all_po():
            po_menu.addAction(po, partial(self.open_po, po))
        for row_index in range(len(list(category_data.keys()))):
            item = list(category_data.keys())[row_index]

            part_number: str = self.get_value_from_category(item_name=item, key="part_number")
            self.get_value_from_category(item_name=item, key="group")

            current_quantity: int = int(self.get_value_from_category(item_name=item, key="current_quantity"))

            unit_quantity: float = float(self.get_value_from_category(item_name=item, key="unit_quantity"))
            priority: int = self.get_value_from_category(item_name=item, key="priority")
            price: float = self.get_value_from_category(item_name=item, key="price")
            notes: str = self.get_value_from_category(item_name=item, key="notes")
            use_exchange_rate: bool = self.get_value_from_category(item_name=item, key="use_exchange_rate")
            converted_price: float = price * self.get_exchange_rate() if use_exchange_rate else price / self.get_exchange_rate()
            exchange_rate: float = self.get_exchange_rate() if use_exchange_rate else 1
            total_cost_in_stock: float = current_quantity * price * exchange_rate
            total_cost_in_stock = max(total_cost_in_stock, 0)
            total_unit_cost: float = unit_quantity * price * exchange_rate
            self.get_value_from_category(item_name=item, key="latest_change_part_number")
            latest_change_unit_quantity: str = self.get_value_from_category(item_name=item, key="latest_change_unit_quantity")
            latest_change_current_quantity = self.get_value_from_category(item_name=item, key="latest_change_current_quantity")
            latest_change_price: str = self.get_value_from_category(item_name=item, key="latest_change_price")
            latest_change_use_exchange_rate: str = self.get_value_from_category(item_name=item, key="latest_change_use_exchange_rate")
            latest_change_priority: str = self.get_value_from_category(item_name=item, key="latest_change_priority")
            latest_change_notes: str = self.get_value_from_category(item_name=item, key="latest_change_notes")
            self.get_value_from_category(item_name=item, key="latest_change_name")

            red_limit: float = self.get_value_from_category(item_name=item, key="red_limit")
            if red_limit is None:
                red_limit = 10
            yellow_limit: float = self.get_value_from_category(item_name=item, key="yellow_limit")
            if yellow_limit is None:
                yellow_limit = 20

            col_index: int = 0

            tab.insertRow(row_index)
            tab.setRowHeight(row_index, 60)

            # PART NAME
            table_item = QTableWidgetItem(item)
            table_item.setFont(self.tables_font)
            tab.setItem(row_index, col_index, table_item)
            tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
            col_index += 1

            # PART NUMBER
            tab.setItem(row_index, col_index, QTableWidgetItem(part_number))
            tab.item(row_index, col_index).setFont(self.tables_font)
            tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)

            col_index += 1

            # UNIT QUANTITY
            tab.setItem(row_index, col_index, QTableWidgetItem(str(unit_quantity)))
            tab.item(row_index, col_index).setFont(self.tables_font)
            tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)

            col_index += 1

            # ITEM QUANTITY
            tab.setItem(row_index, col_index, QTableWidgetItem(str(current_quantity)))
            tab.item(row_index, col_index).setFont(self.tables_font)
            tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
            tab.item(row_index, col_index).setToolTip(latest_change_current_quantity)

            col_index += 1

            # PRICE
            tab.setItem(row_index, col_index, QTableWidgetItem(f'${price:,.2f} {"USD" if use_exchange_rate else "CAD"}'))
            tab.item(row_index, col_index).setFont(self.tables_font)
            tab.item(row_index, col_index).setToolTip(f'${converted_price:,.2f} {"CAD" if use_exchange_rate else "USD"}\n{latest_change_price}')
            tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)
            col_index += 1

            # EXCHANGE RATE
            combo_exchange_rate = ExchangeRateComboBox(
                parent=self,
                selected_item="USD" if use_exchange_rate else "CAD",
            )
            combo_exchange_rate.currentIndexChanged.connect(
                partial(
                    self.use_exchange_rate_change,
                    self.category,
                    item,
                    "use_exchange_rate",
                    combo_exchange_rate,
                )
            )
            combo_exchange_rate.setStyleSheet(self.margin_format)
            # layout.addWidget(combo_exchange_rate)
            tab.setCellWidget(row_index, col_index, combo_exchange_rate)

            col_index += 1

            # TOTAL COST
            tab.setItem(row_index, col_index, QTableWidgetItem(f"${total_cost_in_stock:,.2f} {combo_exchange_rate.currentText()}"))
            tab.item(row_index, col_index).setFont(self.tables_font)
            tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)

            col_index += 1

            # TOTAL UNIT COST
            tab.setItem(row_index, col_index, QTableWidgetItem(f"${total_unit_cost:,.2f} {combo_exchange_rate.currentText()}"))
            tab.item(row_index, col_index).setFont(self.tables_font)
            tab.item(row_index, col_index).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)

            col_index += 1

            # PRIORITY
            combo_priority = PriorityComboBox(parent=self, selected_item=priority)
            if combo_priority.currentText() == "Medium":
                combo_priority.setStyleSheet(f"color: yellow; border-color: gold; background-color: #413C28;{self.margin_format}")
            elif combo_priority.currentText() == "High":
                combo_priority.setStyleSheet(f"color: red; border-color: darkred; background-color: #3F1E25;{self.margin_format}")
            else:
                combo_priority.setStyleSheet(self.margin_format)
            combo_priority.currentIndexChanged.connect(
                partial(
                    self.priority_change,
                    self.category,
                    item,
                    "priority",
                    combo_priority,
                )
            )
            tab.setCellWidget(row_index, col_index, combo_priority)

            col_index += 1

            # NOTES
            text_notes = NotesPlainTextEdit(self, notes, "")
            text_notes.textChanged.connect(partial(self.notes_changed, self.category, item, "notes", text_notes))
            tab.setCellWidget(row_index, col_index, text_notes)
            col_index += 1

            # PURCHASE ORDER
            btn_po = POPushButton(parent=self)
            btn_po.setMenu(po_menu)
            btn_po.setStyleSheet(self.margin_format)
            tab.setCellWidget(row_index, col_index, btn_po)
            self.po_buttons.append(btn_po)

            col_index += 1

            # DELETE
            btn_delete = DeletePushButton(
                parent=self,
                tool_tip=f"Delete {item} permanently from {self.category}",
                icon=QIcon(f"ui/BreezeStyleSheets/dist/pyqt6/{self.theme}/trash.png"),
            )
            btn_delete.clicked.connect(partial(self.delete_item, self.category, item))
            btn_delete.setStyleSheet(self.margin_format)
            tab.setCellWidget(row_index, col_index, btn_delete)
            if current_quantity <= red_limit:
                self.set_table_row_color(tab, row_index, "#3F1E25")
            elif current_quantity <= yellow_limit:
                self.set_table_row_color(tab, row_index, "#413C28")

        self.update_stock_costs()
        # set context menu
        if tab.contextMenuPolicy() != Qt.CustomContextMenu:
            tab.setContextMenuPolicy(Qt.CustomContextMenu)
            menu = QMenu(self)
            action = QAction(self)
            action.triggered.connect(partial(self.set_custom_quantity_limit, tab))
            action.setText("Set Custom Quantity Limit")
            menu.addAction(action)
            menu.addSeparator()
            action = QAction(self)
            action.triggered.connect(partial(self.name_change, tab))
            action.setText("Change part name")
            menu.addAction(action)
            tab.customContextMenuRequested.connect(partial(self.open_group_menu, menu))
        tab.resizeColumnsToContents()
        tab.setColumnWidth(0, 250)
        tab.setColumnWidth(1, 150)
        tab.setEnabled(True)
        tab.blockSignals(False)
        with contextlib.suppress(Exception):
            self.last_item_selected_index = list(category_data.keys()).index(self.last_item_selected_name)
            tab.scrollTo(tab.model().index(self.last_item_selected_index, 0))
            tab.selectRow(self.last_item_selected_index)
            self.listWidget_itemnames.setCurrentRow(self.last_item_selected_index)
        QApplication.restoreOverrideCursor()

    def load_quote_generator_ui(self) -> None:
        self.refresh_nest_directories()

    def refresh_nest_directories(self) -> None:
        self.clear_layout(self.verticalLayout_24)
        self.quote_nest_directories_list_widgets.clear()
        nest_directories: list[str] = settings_file.get_value("quote_nest_directories")
        toolbox = QToolBox(self)
        toolbox.setLineWidth(0)
        toolbox.layout().setSpacing(0)
        self.verticalLayout_24.addWidget(toolbox)
        for nest_directory in nest_directories:
            nest_directory_name: str = nest_directory.split("/")[-1]
            tree_view = PdfTreeView(nest_directory)
            tree_view.selectionModel().selectionChanged.connect(self.nest_directory_item_selected)

            self.quote_nest_directories_list_widgets[nest_directory] = tree_view
            toolbox.addItem(tree_view, nest_directory_name)
        self.nest_directory_item_selected()

    def load_nests(self) -> None:
        """
        This function loads nests and their corresponding information into a QToolBox widget and a
        table, and connects signals to update the table when cells are changed.
        """
        self.clear_layout(self.verticalLayout_sheets)
        self.pushButton_generate_quote.setEnabled(True)
        self.comboBox_global_sheet_thickness.setEnabled(True)
        self.comboBox_global_sheet_material.setEnabled(True)
        self.sheet_nests_toolbox = MultiToolBox(self)
        self.sheet_nests_toolbox.layout().setSpacing(0)
        self.verticalLayout_sheets.addWidget(self.sheet_nests_toolbox)
        row_index: int = 0
        tab_index: int = 0
        for item in list(self.quote_nest_information.keys()):
            if item[0] == "_":
                nest_name = item.split("/")[-1].replace(".pdf", "")
                widget = QWidget(self)
                widget.setMinimumHeight(120)
                widget.setMaximumHeight(120)
                widget.setObjectName("nest_widget")
                widget.setStyleSheet(
                    "QWidget#nest_widget{border: 0.04em solid  #3daee9; border-bottom-left-radius: 4px;border-bottom-right-radius: 4px; border-top: 0px solid #3daee9; margin-top: -1px; background-color: rgba(29, 29, 29, 57);}"
                )
                grid_layout = QGridLayout(widget)
                labels = [
                    "Sheet Count:",
                    "Sheet Material:",
                    "Sheet Thickness:",
                    "Sheet Dimension:",
                ]
                for i, label in enumerate(labels):
                    label = QLabel(label, self)
                    grid_layout.addWidget(label, i, 0)

                spinBox_sheet_count = HumbleDoubleSpinBox(self)
                spinBox_sheet_count.setValue(self.quote_nest_information[item]["quantity_multiplier"])
                spinBox_sheet_count.valueChanged.connect(
                    partial(
                        self.sheet_nest_item_change,
                        tab_index,
                        spinBox_sheet_count,
                        item,
                        "quantity_multiplier",
                    )
                )

                grid_layout.addWidget(spinBox_sheet_count, 0, 2)

                comboBox_sheet_material = QComboBox(self)
                comboBox_sheet_material.wheelEvent = lambda event: None
                comboBox_sheet_material.addItems(price_of_steel_information.get_value("materials"))
                comboBox_sheet_material.setCurrentText(self.quote_nest_information[item]["material"])
                comboBox_sheet_material.activated.connect(
                    partial(
                        self.sheet_nest_item_change,
                        tab_index,
                        comboBox_sheet_material,
                        item,
                        "material",
                    )
                )
                grid_layout.addWidget(comboBox_sheet_material, 1, 2)

                comboBox_sheet_thickness = QComboBox(self)
                comboBox_sheet_thickness.wheelEvent = lambda event: None
                comboBox_sheet_thickness.addItems(price_of_steel_information.get_value("thicknesses"))
                comboBox_sheet_thickness.setCurrentText(self.quote_nest_information[item]["gauge"])
                comboBox_sheet_thickness.activated.connect(
                    partial(
                        self.sheet_nest_item_change,
                        tab_index,
                        comboBox_sheet_thickness,
                        item,
                        "gauge",
                    )
                )
                grid_layout.addWidget(comboBox_sheet_thickness, 2, 2)
                lineEdit_sheet_size_x = HumbleDoubleSpinBox(self)
                lineEdit_sheet_size_x.setDecimals(3)
                try:
                    lineEdit_sheet_size_x.setValue(float(self.quote_nest_information[item]["sheet_dim"].replace(" x ", "x").split("x")[0]))
                except AttributeError:
                    lineEdit_sheet_size_x.setValue(0.0)
                grid_layout.addWidget(lineEdit_sheet_size_x, 4, 0)
                label = QLabel("x", self)
                label.setFixedWidth(15)
                grid_layout.addWidget(label, 4, 1)
                lineEdit_sheet_size_y = HumbleDoubleSpinBox(self)
                lineEdit_sheet_size_y.setDecimals(3)
                try:
                    lineEdit_sheet_size_y.setValue(float(self.quote_nest_information[item]["sheet_dim"].replace(" x ", "x").split("x")[1]))
                except AttributeError:
                    lineEdit_sheet_size_y.setValue(0.0)
                grid_layout.addWidget(lineEdit_sheet_size_y, 4, 2)
                lineEdit_sheet_size_x.valueChanged.connect(
                    partial(
                        self.sheet_nest_item_change,
                        tab_index,
                        (lineEdit_sheet_size_x, lineEdit_sheet_size_y),
                        item,
                        "sheet_dim",
                    )
                )
                lineEdit_sheet_size_y.valueChanged.connect(
                    partial(
                        self.sheet_nest_item_change,
                        tab_index,
                        (lineEdit_sheet_size_x, lineEdit_sheet_size_y),
                        item,
                        "sheet_dim",
                    )
                )

                self.sheet_nests_toolbox.addItem(
                    widget,
                    f"{self.quote_nest_information[item]['gauge']} {self.quote_nest_information[item]['material']} {self.quote_nest_information[item]['sheet_dim']} - {nest_name}",
                )
                self.sheet_nests_toolbox.setItemIcon(
                    tab_index,
                    QIcon(r"ui\BreezeStyleSheets\dist\pyqt6\dark\project_open.png"),
                )
                tab_index += 1
        self.load_quote_table()
        self.tableWidget_quote_items.setEnabled(True)
        self.tableWidget_quote_items.resizeColumnsToContents()
        self.tableWidget_quote_items.setColumnWidth(1, 250)
        # self.tableWidget_quote_items.cellChanged.connect(self.quote_table_cell_changed)

    def load_quote_table(self) -> None:
        """
        This function loads a table with information about quotes, including images, item names,
        materials, gauges, and quantities.
        """
        row_index: int = 0
        self.tableWidget_quote_items.setRowCount(0)
        for item in list(self.quote_nest_information.keys()):
            if item[0] != "_":
                self.tableWidget_quote_items.insertRow(row_index)
                self.tableWidget_quote_items.setRowHeight(row_index, 50)
                label = ClickableLabel(self)
                label.setToolTip("Click to make bigger.")
                label.setFixedSize(50, 50)
                pixmap = QPixmap(f"images/{self.quote_nest_information[item]['image_index']}.jpeg")
                does_part_exist: bool = True
                if pixmap.isNull():
                    does_part_exist = False
                    pixmap = QPixmap("images/404.png")
                    label.clicked.connect(
                        partial(
                            self.open_image,
                            "images/404.png",
                            "Part does not exist",
                        )
                    )
                else:
                    label.clicked.connect(
                        partial(
                            self.open_image,
                            f"images/{self.quote_nest_information[item]['image_index']}.jpeg",
                            item,
                        )
                    )
                scaled_pixmap = pixmap.scaled(label.size(), aspectRatioMode=Qt.KeepAspectRatio)
                label.setPixmap(scaled_pixmap)
                self.tableWidget_quote_items.setCellWidget(row_index, 0, label)

                self.tableWidget_quote_items.setItem(row_index, 1, QTableWidgetItem(item))
                self.tableWidget_quote_items.item(row_index, 1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)

                self.tableWidget_quote_items.setItem(
                    row_index,
                    2,
                    QTableWidgetItem(self.quote_nest_information[item]["material"]),
                )
                self.tableWidget_quote_items.item(row_index, 2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)

                self.tableWidget_quote_items.setItem(
                    row_index,
                    3,
                    QTableWidgetItem(self.quote_nest_information[item]["gauge"]),
                )
                self.tableWidget_quote_items.item(row_index, 3).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)

                self.tableWidget_quote_items.setItem(
                    row_index,
                    4,
                    QTableWidgetItem(str(int(self.quote_nest_information[item]["quantity"]) * self.get_quantity_multiplier(item))),
                )
                self.tableWidget_quote_items.item(row_index, 4).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWrapAnywhere)

                recut_button = RecutButton(self)
                recut_button.setStyleSheet("margin: 5%;")
                self.tableWidget_quote_items.setCellWidget(row_index, 5, recut_button)

                send_part_to_inventory = QPushButton(self)
                send_part_to_inventory.setText("Add Part to Inventory")
                send_part_to_inventory.setStyleSheet("margin: 5%;")
                send_part_to_inventory.setFixedWidth(150)
                send_part_to_inventory.clicked.connect(partial(self.upload_part_to_inventory_thread, item, send_part_to_inventory))
                self.tableWidget_quote_items.setCellWidget(row_index, 6, send_part_to_inventory)

                if not does_part_exist:
                    self.set_table_row_color(self.tableWidget_quote_items, row_index, "#3F1E25")
                row_index += 1

    # ! /\ Load UI /\
    # ! \/ CHECKERS \/
    def check_for_updates(self, on_start_up: bool = False) -> None:
        """
        It checks for updates on GitHub and displays a message dialog if there is a new update available

        Args:
          on_start_up (bool): bool = False. Defaults to False
        """
        try:
            try:
                response = requests.get("https://api.github.com/repos/thecodingjsoftware/Inventory-Manager/releases/latest")
            except ConnectionError:
                return
            version: str = response.json()["name"].replace(" ", "")
            if version != __version__:
                message_dialog = self.show_message_dialog(
                    title=__name__,
                    message=f"There is a new update available.\n\nNew Version: {version}\n\nMake sure to make a backup\nbefore installing new version.",
                    dialog_buttons=DialogButtons.ok_update,
                )
                if message_dialog == DialogButtons.update:
                    subprocess.Popen("start update.exe", shell=True)
                    # sys.exit()
            elif not on_start_up:
                self.show_message_dialog(
                    title=__name__,
                    message=f"There are currently no updates available.\n\nCurrent Version: {__version__}",
                )
        except Exception as e:
            if not on_start_up:
                self.show_error_dialog(title=__name__, message=f"Error\n\n{e}")

    def check_trusted_user(self) -> None:
        """
        If the user is not in the trusted_users list, then the user is not trusted
        """
        trusted_users = get_trusted_users()
        check_trusted_user = (user for user in trusted_users if not self.trusted_user)
        for user in check_trusted_user:
            self.trusted_user = self.username.lower() == user.lower()

        # if not self.trusted_user:
        # self.menuSort.setEnabled(False)
        # self.menuOpen_Category.setEnabled(False)

    # ! /\ CHECKERS /\

    # ! \/ Purchase Order \/
    def open_po(self, po_name: str = None) -> None:
        """
        It opens a dialog box with a list of items
        """
        if po_name is None:
            input_dialog = SelectItemDialog(
                title="Open PO",
                message="Select a PO to open",
                items=get_all_po(),
                button_names=DialogButtons.open_cancel,
            )
            if input_dialog.exec_():
                response = input_dialog.get_response()
                if response == DialogButtons.open:
                    try:
                        po_template = POTemplate(f"{os.path.abspath(os.getcwd())}/PO's/templates/{input_dialog.get_selected_item()}.xlsx")
                        po_template.generate()
                        os.startfile(po_template.get_output_path())
                    except AttributeError:
                        return
                elif response == DialogButtons.cancel:
                    return
        else:
            po_template = POTemplate(f"{os.path.abspath(os.getcwd())}/PO's/templates/{po_name}.xlsx")
            po_template.generate()
            os.startfile(po_template.get_output_path())

    def delete_po(self) -> None:
        """
        It opens a dialog box with a list of items
        """
        input_dialog = SelectItemDialog(
            title="Delete PO",
            message="Select a PO to delete.\n\nThis cannot be undone.",
            items=get_all_po(),
            button_names=DialogButtons.discard_cancel,
        )
        if input_dialog.exec_():
            response = input_dialog.get_response()
            if response == DialogButtons.discard:
                try:
                    os.remove(f"PO's/templates/{input_dialog.get_selected_item()}.xlsx")
                    self.show_message_dialog(title="Success", message="Successfully removed template.")
                except AttributeError:
                    return
            elif response == DialogButtons.cancel:
                return

    def add_po_templates(self, po_file_paths: list[str], open_select_file_dialog: bool = False) -> None:
        """
        It takes a list of file paths, copies them to a new directory, and then shows a message dialog

        Args:
          po_file_paths (list[str]): list[str]
          open_select_file_dialog (bool): bool = False. Defaults to False
        """
        if open_select_file_dialog:
            po_file_paths, check = QFileDialog.getOpenFileNames(None, "Add Purchase Order Template", "", "Excel Files (*.xlsx)")
            if not po_file_paths:
                return
            for po_file_path in po_file_paths:
                try:
                    po_file: POTemplate = POTemplate(po_file_path)
                except Exception as error:
                    self.show_error_dialog(
                        title="Error",
                        message=f"Error parsing excel file. Please double check Order number and Vendor cell positions, or email me the excel file.\n\n{error}\n\n{po_file_path}",
                    )
                    return
                new_file_path = f"PO's/templates/{po_file.get_vendor().replace('.','')}.xlsx"
                shutil.copyfile(po_file_path, new_file_path)
            check_po_directories()
            self.show_message_dialog(title="Success", message="Successfully added new Purchase Order template.")
        if not open_select_file_dialog:
            for po_file_path in po_file_paths:
                try:
                    po_file: POTemplate = POTemplate(po_file_path)
                except Exception as error:
                    self.show_error_dialog(
                        title="Error",
                        message=f"Error parsing excel file. Please double check Order number and Vendor cell positions, or email me the excel file.\n\n{error}",
                    )
                    return
                new_file_path = f"PO's/templates/{po_file.get_vendor().replace('.','')}.xlsx"
                shutil.copyfile(po_file_path, new_file_path)
            check_po_directories()
            self.show_message_dialog(title="Success", message="Successfully added new Purchase Order template.")

        self.reload_po_menu()

    def reload_po_menu(self) -> None:
        """
        It creates a menu for each button in a list of buttons, and then adds an action to each menu for
        each item in a list of items
        """
        for po_button in self.po_buttons:
            po_menu = QMenu(self)
            for po in get_all_po():
                po_menu.addAction(po, partial(self.open_po, po))
            po_button.setMenu(po_menu)

    # ! /\ Purchase Order /\
    def print_inventory(self) -> None:
        """
        It takes a file path as an argument, opens the file, generates an excel file, and saves it

        Returns:
          The return value is None.
        """
        try:
            file_name = f"excel files/{datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}"
            excel_file = ExcelFile(inventory, f"{file_name}.xlsx")
            excel_file.generate()
            excel_file.save()

            input_dialog = MessageDialog(
                title="Success",
                message="Successfully generated inventory.\n\nWould you love to open it?",
                button_names=DialogButtons.open_cancel,
            )
            if input_dialog.exec_():
                response = input_dialog.get_response()
                if response == DialogButtons.open:
                    try:
                        os.startfile(f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/{file_name}.xlsx")
                    except AttributeError:
                        return
                elif response == DialogButtons.cancel:
                    return
        except Exception as error:
            self.show_error_dialog(
                title="Error",
                message=f"Error generating inventory excel file. Please review the error message below.\n\n{error}",
            )
            return

    # !  \/ External Actions \/
    def open_website(self) -> None:
        """
        This function opens the website in the default browser.
        """
        webbrowser.open("http://10.0.0.92:5051", new=0)

    def open_item_history(self) -> None:
        """
        It opens the inventory history file in the data folder.
        """
        os.startfile(f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/data/inventory history.xlsx")

    def open_folder(self, path: str) -> None:
        """
        It opens the folder in the default file browser

        Args:
          path: The path to the folder
        """
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            self.show_error_dialog("Error opening folder", f"{e}\n\nPlatform: {sys.platform}")

    def generate_error_log(self, message_dialog: MessageDialog) -> None:
        """
        It takes a screenshot of the error message dialog, saves it to a folder, writes the error
        message to a file, copies the app log to the folder, compresses the folder, and deletes the
        folder

        Args:
          message_dialog (MessageDialog): MessageDialog = The error message dialog that pops up when an
        error occurs.
        """
        output_directory: str = f"logs/ErrorLog_{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
        check_folders([output_directory])
        pixmap = QPixmap(message_dialog.grab())
        pixmap.save(f"{output_directory}/screenshot.png")
        with open(f"{output_directory}/error.log", "w", encoding="utf-8") as error_log:
            error_log.write(message_dialog.message)
        shutil.copyfile("logs/app.log", f"{output_directory}/app.log")
        compress_folder(foldername=output_directory, target_dir=output_directory)
        shutil.rmtree(output_directory)

    def play_celebrate_sound(self) -> None:
        """
        It starts a new thread that calls the function _play_celebrate_sound
        """
        threading.Thread(target=_play_celebrate_sound).start()

    # !  /\ External Actions /\
    # ! \/ THREADS \/
    def sync_changes(self) -> None:
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Edit Inventory":
            self.status_button.setText(f'Synching - {datetime.now().strftime("%r")}', "lime")
            self.upload_file(
                [
                    f"{self.inventory_file_name}.json",
                ],
                False,
            )
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Parts in Inventory":
            self.status_button.setText(f'Synching - {datetime.now().strftime("%r")}', "lime")
            self.upload_file(
                [
                    f"{self.inventory_file_name} - Parts in Inventory.json",
                ],
                False,
            )
        elif self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Sheets in Inventory":
            self.status_button.setText(f'Synching - {datetime.now().strftime("%r")}', "lime")
            self.upload_file(
                [
                    f"{self.inventory_file_name} - Price of Steel.json",
                ],
                False,
            )

    def download_required_images(self, batch_data: dict) -> None:
        """
        This function downloads required images using a separate thread and emits a signal when the
        download is complete.

        Args:
          batch_data (dict): A dictionary containing information about the batch of data being
        processed. Each key in the dictionary represents an item in the batch, and the corresponding
        value is a dictionary containing information about that item.

        Returns:
          The function does not return anything explicitly, but it may return None implicitly if the
        condition in the if statement is True and the load_nests() method is called.
        """
        required_images = [batch_data[item]["image_index"] + ".jpeg" for item in list(batch_data.keys()) if item[0] != "_"]
        if not required_images:
            self.load_nests()
            return
        download_thread = DownloadImagesThread(required_images)
        download_thread.signal.connect(self.download_required_images_response)
        self.threads.append(download_thread)
        download_thread.start()

    def download_required_images_response(self, response: str) -> None:
        """
        This function loads nests if images are successfully downloaded and updates the status button
        text.

        Args:
          response (str): A string representing the response received after attempting to download
        required images.
        """
        if response == "Successfully downloaded":
            self.load_nests()
            self.status_button.setText(
                f"Successfully loaded {len(self.get_all_selected_parts(self.tabs[self.category]))} parts",
                "lime",
            )

    def upload_batched_parts_images(self, batch_data) -> None:
        """
        This function uploads a batch of images by extracting their names from a dictionary and
        appending ".jpeg" to them before calling another function to upload the files.

        Args:
          batch_data: batch_data is a dictionary containing data for a batch of parts. The keys of the
        dictionary are the part names and the values are the corresponding data for each part.
        """
        images_to_upload: list[str] = [f"{item}.jpeg" for item in list(batch_data.keys()) if item[0] != "_"]
        self.upload_file(images_to_upload)

    def remove_quantity_thread_response(self, data) -> None:
        """
        It's a function that is called when a thread is finished. It's purpose is to update the GUI with
        the results of the thread.

        Args:
          data: str = "Done" or "count, total"
        """
        if data != "Done":
            count = int(data.split(", ")[0])
            total = int(data.split(", ")[1])
            __start: float = count / total
            __middle: float = __start + 0.001 if __start <= 1 - 0.001 else 1.0
            __end: float = __start + 0.0011 if __start <= 1 - 0.0011 else 1.0
            self.status_button.setText(f'Loading... {data.replace(", ", "/")}', color="white")
            self.status_button.setStyleSheet(
                """QPushButton#status_button {background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,stop:%(start)s #3daee9,stop:%(middle)s #3daee9,stop:%(end)s #1E363F)}"""
                % {"start": str(__start), "middle": str(__middle), "end": str(__end)}
            )
        else:
            self.status_button.setText("Done", "lime")
            inventory.load_data()
            self.centralwidget.setEnabled(True)
            self.listWidget_itemnames.setEnabled(True)
            self.pushButton_create_new.setEnabled(True)
            self.pushButton_add_quantity.setEnabled(False)
            self.pushButton_remove_quantity.setEnabled(True)
            self.radioButton_category.setEnabled(True)
            self.radioButton_single.setEnabled(True)
            self.sort_inventory()
            self.sync_changes()

    def changes_response(self, response: str) -> None:
        """
        This function updates the status button text to indicate syncing, downloads all files, and
        updates the status button text again to indicate completion.

        Args:
          response (str): A string representing the response received from a server or API call.
        """
        self.status_button.setText(f'Syncing - {datetime.now().strftime("%r")}', "yellow")
        self.downloading_changes = True
        self.download_all_files()
        self.status_button.setText(f'Synched - {datetime.now().strftime("%r")}', "lime")

    def data_received(self, data) -> None:
        """
        This function handles the data received from the server and performs various actions based on
        the received data.

        Args:
          data: The data received by the function. It is of type string.
        """
        if data == "Successfully uploaded":
            self.status_button.setText(f'Synched - {datetime.now().strftime("%r")}', "lime")
        if self.downloading_changes and data == "Successfully downloaded":
            if self.tabWidget.tabText(self.tabWidget.currentIndex()) in [
                "Parts in Inventory",
                "Sheets in Inventory",
            ]:
                inventory.load_data()
                price_of_steel_inventory.load_data()
                parts_in_inventory.load_data()
                self.load_categories()
            self.downloading_changes = False

        if not self.finished_downloading_all_files:
            self.files_downloaded_count += 1
        if self.files_downloaded_count == 1 and not self.finished_downloading_all_files:
            self.finished_downloading_all_files = True
            inventory.load_data()
            price_of_steel_inventory.load_data()
            parts_in_inventory.load_data()
            self.load_categories()
            self.status_button.setText(f'Downloaded all files - {datetime.now().strftime("%r")}', "lime")
            self.centralwidget.setEnabled(True)
        if "timed out" in str(data).lower() or "fail" in str(data).lower():
            self.show_error_dialog(
                title="Time out",
                message=f"Server is either offline, try again or not connected to internet. Make sure VPN's are disabled, else contact server or netowrk administrator.\n\n{str(data)}",
            )
            self.status_button.setText("Cannot connect to server", "red")
        QApplication.restoreOverrideCursor()

    def start_changes_thread(self, files_to_download: list[str]) -> None:
        """
        It creates a thread that will run a function that will download a list of files from a server

        Args:
          files_to_download (list[str]): list[str]
        """
        changes_thread = ChangesThread(files_to_download)  # 5 minutes
        changes_thread.signal.connect(self.changes_response)
        self.threads.append(changes_thread)
        changes_thread.start()

    def start_exchange_rate_thread(self) -> None:
        """
        It creates an instance of the ExchangeRate class and starts it
        """
        exchange_rate_thread = ExchangeRate()
        exchange_rate_thread.signal.connect(self.exchange_rate_received)
        self.threads.append(exchange_rate_thread)
        exchange_rate_thread.start()

    def exchange_rate_received(self, exchange_rate: float) -> None:
        """
        It takes the exchange rate from the API and updates the label on the GUI with the exchange rate
        and the time it was received

        Args:
          exchange_rate (float): float
        """
        self.label_exchange_price.setText(f"1.00 USD: {exchange_rate} CAD - {datetime.now().strftime('%r')}")
        self.label_total_unit_cost.setText(f"Total Unit Cost: ${inventory.get_total_unit_cost(self.category, self.get_exchange_rate()):,.2f}")
        settings_file.change_item(item_name="exchange_rate", new_value=exchange_rate)
        self.update_stock_costs()

    def send_sheet_report(self) -> None:
        thread = SendReportThread()
        self.start_thread(thread)

    def upload_file(self, files_to_upload: list[str], get_response: bool = True) -> None:
        """
        It creates a new thread, sets the cursor to wait, and starts the thread

        Args:
          files_to_upload (str): str - The file to upload
        """
        self.get_upload_file_response = get_response
        upload_thread = UploadThread(files_to_upload)
        # if get_response:
        # QApplication.setOverrideCursor(Qt.BusyCursor)
        self.start_thread(upload_thread)

    def download_file(self, files_to_download: list[str], get_response: bool = True) -> None:
        """
        It starts a thread that downloads a file from a server

        Args:
          files_to_download (list[str]): list[str]
        """
        self.get_upload_file_response = get_response
        download_thread = DownloadThread(files_to_download)
        # QApplication.setOverrideCursor(Qt.BusyCursor)
        self.start_thread(download_thread)

    def start_thread(self, thread) -> None:
        """
        It connects the signal from the thread to the data_received function, then appends the thread to
        the threads list, and finally starts the thread

        Args:
          thread: The thread to start
        """
        thread.signal.connect(self.data_received)
        self.threads.append(thread)
        thread.start()

    def download_all_files(self) -> None:
        """
        This function downloads three JSON files related to inventory and steel prices.
        """
        self.download_file(
            [
                f"{self.inventory_file_name} - Parts in Inventory.json",
                f"{self.inventory_file_name} - Price of Steel.json",
                f"{self.inventory_file_name}.json",
            ],
            False,
        )

    def start_process_nest_thread(self, nests: list[str]) -> None:
        self.status_button.setText("Loadings Nests", "yellow")
        QApplication.setOverrideCursor(Qt.BusyCursor)
        self.pushButton_load_nests.setEnabled(False)
        load_nest_thread = LoadNests(self, nests)
        self.threads.append(load_nest_thread)
        load_nest_thread.signal.connect(self.response_from_load_nest_thread)
        load_nest_thread.start()

    def response_from_load_nest_thread(self, data) -> None:
        if "ERROR!" in data:
            self.status_button.setText("Encountered error processing pdfs", "red")
            self.pushButton_load_nests.setEnabled(True)
            self.show_error_dialog("oh no. Encountered error processing pdfs.", data)
            return
        if type(data) == dict:
            self.quote_nest_information.clear()
            self.quote_nest_information = data
            self.pushButton_load_nests.setEnabled(True)
            self.load_nests()
            self.status_button.setText(f"Successfully loaded {len(self.get_all_selected_nests())} nests", "lime")
        QApplication.restoreOverrideCursor()

    def upload_part_to_inventory_thread(self, item_name: str, send_part_to_inventory: QPushButton) -> None:
        send_part_to_inventory.setEnabled(False)
        self.save_quote_table_values()
        data = {item_name: self.quote_nest_information[item_name]}
        QApplication.setOverrideCursor(Qt.BusyCursor)
        with open("parts_batch_to_upload.json", "w") as f:
            json.dump(data, f, sort_keys=True, indent=4)
        upload_batch = UploadBatch("parts_batch_to_upload.json")
        upload_batch.signal.connect(self.upload_batch_to_inventory_response)
        self.threads.append(upload_batch)
        self.status_button.setText("Uploading Part", "yellow")
        upload_batch.start()
        self.upload_batched_parts_images(data)
        send_part_to_inventory.setEnabled(True)

    def upload_batch_to_inventory_thread(self) -> None:
        QApplication.setOverrideCursor(Qt.BusyCursor)
        with open("parts_batch_to_upload.json", "w") as f:
            json.dump(self.quote_nest_information, f, sort_keys=True, indent=4)
        upload_batch = UploadBatch("parts_batch_to_upload.json")
        upload_batch.signal.connect(self.upload_batch_to_inventory_response)
        self.threads.append(upload_batch)
        self.status_button.setText("Uploading Batch", "yellow")
        upload_batch.start()

    def upload_batch_to_inventory_response(self, response) -> None:
        if response == "Batch sent successfully":
            self.status_button.setText("Batch was sent successfully", "lime")
            # self.show_message_dialog('Success', 'Batch was sent successfully')
        else:
            self.status_button.setText("Batch Failed to send", "red")
            self.show_error_dialog("Error", f"Something went wrong.\n\n{response}")
        QApplication.restoreOverrideCursor()
        os.remove("parts_batch_to_upload.json")

    # ! /\ THREADS /\

    # ! \/ BACKUP ACTIONS \/
    def load_backup(self, file_path: str = None) -> None:
        """
        It opens a file dialog, and if the user selects a file, it extracts the file and then loads the
        categories
        """
        if file_path is None:
            backup_file, check = QFileDialog.getOpenFileName(
                None,
                "Load backup",
                "backups/",
                "Zip Files (*.zip)",
            )
            if check:
                extract(file_to_extract=backup_file)
                self.load_categories()
                self.show_message_dialog(title="Success", message="Successfully loaded backup!")
        else:
            extract(file_to_extract=file_path)
            self.load_categories()
            self.show_message_dialog(title="Success", message="Successfully loaded backup!")

    def backup_database(self) -> None:
        """
        This function compresses the database file and shows a message dialog to the user
        """
        compress_database(path_to_file=f"data/{self.inventory_file_name}.json")
        self.show_message_dialog(
            title="Success",
            message="Backup was successful!\n\nNote! Loading a backup will not sync changes. Syncing is being done under the hood consistently, and there is no need for creating local backups anymore.",
        )

    # ! /\ BACKUP ACTIONS /\
    def clear_layout(self, layout) -> None:
        """
        If the layout is not None, while the layout has items, take the first item, get the widget, if
        the widget is not None, delete it, otherwise clear the layout

        Args:
          layout: The layout to be cleared
        """
        with contextlib.suppress(AttributeError):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self.clear_layout(item.layout())

    def set_layout_message(
        self,
        left_label: str,
        highlighted_message: str,
        right_label: str,
        highlighted_message_width: int,
        button_pressed_event=None,
    ) -> None:
        """
        It sets the layout of the window to a left label, a highlighted message, and a right label.

        Args:
          left_label (str): str,
          highlighted_message (str): str = "Click Me"
          right_label (str): str = "",
          highlighted_message_width (int): int = The width of the highlighted message
          button_pressed_event: The function to be called when the button is pressed.
        """
        self.clear_layout(self.active_layout)
        self.tabs.clear()

        self.tab_widget = QTabWidget(self)
        self.tab_widget.tabBarDoubleClicked.connect(self.rename_category)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        with contextlib.suppress(AttributeError):
            self.active_layout.addWidget(self.tab_widget)
        tab = QScrollArea(self)
        content_widget = QWidget()
        tab.setWidget(content_widget)
        grid_layout = QGridLayout(content_widget)
        tab.setWidgetResizable(True)
        self.tabs["layout_message"] = grid_layout
        self.tab_widget.addTab(tab, "")

        lbl1 = QLabel(left_label)
        lbl1.setStyleSheet("font:30px")
        if not left_label:
            lbl1.setFixedWidth(650)
            lbl1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        else:
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        font_size = QFont()
        font_size.setPointSize(25)
        btn = QPushButton(highlighted_message)
        btn.setFont(font_size)
        btn.setObjectName("default_dialog_button")
        if button_pressed_event is not None:
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(button_pressed_event)
        btn.setStyleSheet("QPushButton#default_dialog_button{text-align: center; vertical-align: center }")
        set_default_dialog_button_stylesheet(btn)
        btn.setFixedSize(highlighted_message_width, 45)
        lbl2 = QLabel(right_label)
        if not right_label:
            lbl2.setFixedWidth(650)
            lbl2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        else:
            lbl2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lbl2.setStyleSheet("font:30px")

        tab = self.tabs["layout_message"]
        tab.addWidget(lbl1, 0, 0)
        tab.addWidget(btn, 0, 1)
        tab.addWidget(lbl2, 0, 2)

    # ! \/ OVERIDDEN UI EVENTS \/
    def dragEnterEvent(self, event) -> None:
        """
        If the event has a URL, accept it, otherwise ignore it.

        Args:
          event: This is the event object that is passed to the method.
        """
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event) -> None:
        """
        If the file is an Excel file, then accept the drop event and display a message. Otherwise,
        ignore the drop event.

        Args:
          event: The event object.
        """
        if event.mimeData().hasUrls:
            for url in event.mimeData().urls():
                if str(url.toLocalFile()).endswith(".xlsx"):
                    event.setDropAction(Qt.CopyAction)
                    event.accept()
                    self.set_layout_message("", "Add", "a new Purchase Order template", 80, None)
                elif str(url.toLocalFile()).endswith(".zip"):
                    event.setDropAction(Qt.CopyAction)
                    event.accept()
                    self.set_layout_message("", "Load", "backup", 80, None)
                else:
                    event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event) -> None:
        """
        It loads the categories from the database and displays them in the list widget

        Args:
          event: QDragLeaveEvent
        """
        # self.load_categories()
        pass

    def dropEvent(self, event) -> None:
        """
        If the event has URLs, set the drop action to copy, accept the event, get the local file paths
        from the URLs, add the PO files to the database, and reload the categories

        Args:
          event: The event object
        """
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                if str(url.toLocalFile()).endswith(".xlsx"):
                    files = [str(url.toLocalFile()) for url in event.mimeData().urls()]
                    # self.load_categories()
                    self.add_po_templates(files)
                    break
                elif str(url.toLocalFile()).endswith(".zip"):
                    self.load_backup([str(url.toLocalFile()) for url in event.mimeData().urls()][0])
            event.ignore()

    def closeEvent(self, event) -> None:
        """
        The function saves the geometry of the window and then closes the window

        Args:
          event: the event that triggered the close_event() method
        """
        # compress_database(
        #     path_to_file=f"data/{self.inventory_file_name}.json",
        #     on_close=True,
        # )
        self.save_geometry()
        self.save_menu_tab_order()
        super().closeEvent(event)

    # ! /\ OVERIDDEN UI EVENTS /\


def main() -> None:
    """
    It creates a QApplication, creates a MainWindow, shows the MainWindow, and then runs the
    QApplication
    """
    app = QApplication([])
    loading_window = LoadWindow()
    loading_screen = QSplashScreen(loading_window)
    app.processEvents()
    set_theme(app, theme="dark")
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(lambda: loading_window.close())
    timer.timeout.connect(lambda: loading_screen.close())
    timer.start(1500)
    m = MainWindow()
    m.show()
    app.exec_()


main()
