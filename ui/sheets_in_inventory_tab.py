import contextlib
import os
from datetime import datetime
from functools import partial

import sympy
from PyQt6 import uic
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QAction, QColor, QCursor, QFont, QIcon
from PyQt6.QtWidgets import QAbstractItemView, QComboBox, QDateEdit, QGridLayout, QInputDialog, QLabel, QMenu, QMessageBox, QPushButton, QTableWidgetItem, QVBoxLayout, QWidget

from ui.add_sheet_dialog import AddSheetDialog
from ui.custom_widgets import CustomTableWidget, CustomTabWidget, DeletePushButton, HumbleDoubleSpinBox, OrderStatusButton
from ui.edit_category_dialog import EditCategoryDialog
from ui.set_custom_limit_dialog import SetCustomLimitDialog
from ui.set_order_pending_dialog import SetOrderPendingDialog
from utils.inventory.category import Category
from utils.settings import Settings
from utils.sheet_settings.sheet_settings import SheetSettings
from utils.sheets_inventory.sheet import Sheet
from utils.sheets_inventory.sheets_inventory import SheetsInventory

settings_file = Settings()


class SheetsTableWidget(CustomTableWidget):
    def __init__(self, parent=None):
        super(SheetsTableWidget, self).__init__(parent)
        self.setShowGrid(True)
        self.setSortingEnabled(False)
        self.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.set_editable_column_index([5, 9])
        headers: list[str] = [
            "Thickness",
            "Material",
            "Length",
            "Width",
            "Cost per Sheet",
            "Quantity in Stock",
            "Total Cost in Stock",
            "Order Status",
            "Set Arrival Time",
            "Notes",
            "Modified Date",
            "DEL",
        ]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)


class SheetsTabWidget(CustomTabWidget):
    def __init__(self, parent: QWidget) -> None:
        super(SheetsTabWidget, self).__init__(parent)


class SheetsInInventoryTab(QWidget):
    def __init__(self, sheets_inventory: SheetsInventory, sheet_settings: SheetSettings, parent: QWidget) -> None:
        super(SheetsInInventoryTab, self).__init__(parent)
        uic.loadUi("ui/sheets_in_inventory_tab.ui", self)
        self.parent = parent
        self.sheets_inventory = sheets_inventory
        self.sheet_settings = sheet_settings

        self.settings_file = Settings()

        self.tab_widget = SheetsTabWidget(self)
        self.tab_widget.addCategory.connect(self.add_category)
        self.tab_widget.removeCategory.connect(self.remove_category)

        self.category: Category = None
        self.finished_loading: bool = False
        self.category_tables: dict[Category, SheetsTableWidget] = {}
        self.table_sheets_widgets: dict[Sheet, dict[str, QTableWidgetItem | HumbleDoubleSpinBox | QComboBox]] = {}
        self.margins = (15, 15, 5, 5)  # top, bottom, left, right
        self.margin_format = f"margin-top: {self.margins[0]}%; margin-bottom: {self.margins[1]}%; margin-left: {self.margins[2]}%; margin-right: {self.margins[3]}%;"
        self.last_selected_sheet: str = ""
        self.last_selected_index: int = 0
        self.load_ui()
        self.load_categories()
        self.restore_last_selected_tab()
        self.update_stock_costs()
        self.finished_loading = True

    def load_ui(self):
        self.tables_font = QFont()
        self.tables_font.setFamily(settings_file.get_value("tables_font")["family"])
        self.tables_font.setPointSize(settings_file.get_value("tables_font")["pointSize"])
        self.tables_font.setWeight(settings_file.get_value("tables_font")["weight"])
        self.tables_font.setItalic(settings_file.get_value("tables_font")["italic"])

        self.gridLayout_sheet_prices = self.findChild(QGridLayout, "gridLayout_sheet_prices")
        self.pushButton_add_new_sheet = self.findChild(QPushButton, "pushButton_add_new_sheet")
        self.pushButton_add_new_sheet.clicked.connect(self.add_sheet)
        self.verticalLayout_10 = self.findChild(QVBoxLayout, "verticalLayout_10")
        self.verticalLayout_10.addWidget(self.tab_widget)

    def add_category(self):
        new_category_name, ok = QInputDialog.getText(self, "New Category", "Enter a name for a category:")
        if new_category_name and ok:
            new_category = Category(new_category_name)
            self.sheets_inventory.add_category(new_category)
            table = SheetsTableWidget(self.tab_widget)
            self.category_tables.update({new_category: table})
            self.tab_widget.addTab(table, new_category.name)
            table.cellChanged.connect(self.table_changed)
            table.cellPressed.connect(self.table_selected_changed)
            self.sheets_inventory.save()
            self.sync_changes()
            self.update_stock_costs()

    def remove_category(self):
        category_to_remove, ok = QInputDialog.getItem(self, "Remove Category", "Select a category to remove", [category.name for category in self.sheets_inventory.get_categories()], editable=False)
        if category_to_remove and ok:
            category = self.sheets_inventory.delete_category(category_to_remove)
            tab_index_to_remove = self.tab_widget.get_tab_order().index(category_to_remove)
            self.tab_widget.removeTab(tab_index_to_remove)
            self.clear_layout(self.category_tables[category])
            del self.category_tables[category]
            self.sheets_inventory.save()
            self.sync_changes()
            self.update_stock_costs()

    def edit_category(self):
        edit_dialog = EditCategoryDialog(f"Edit {self.category.name}", f"Delete, duplicate, or rename: {self.category.name}.", self.category.name, self.category, self.sheets_inventory, self)
        if edit_dialog.exec():
            action = edit_dialog.action
            input_text = edit_dialog.lineEditInput.text()
            if action == "DUPLICATE":
                new_name = input_text
                if new_name == self.category.name:
                    new_name += " - Copy"
                new_category = self.sheets_inventory.duplicate_category(self.category, new_name)
                self.sheets_inventory.add_category(new_category)
                table = SheetsTableWidget(self.tab_widget)
                self.category_tables.update({new_category: table})
                self.tab_widget.insertTab(self.tab_widget.currentIndex() + 1, table, new_category.name)
                table.cellChanged.connect(self.table_changed)
                table.cellPressed.connect(self.table_selected_changed)
            elif action == "RENAME":
                self.category.rename(input_text)
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), input_text)
            elif action == "DELETE":
                self.clear_layout(self.category_tables[self.category])
                del self.category_tables[self.category]
                self.sheets_inventory.delete_category(self.category)
                self.tab_widget.removeTab(self.tab_widget.currentIndex())
            self.sheets_inventory.save()
            self.sync_changes()

    def load_categories(self):
        self.settings_file.load_data()
        self.tab_widget.clear()
        self.category_tables.clear()
        all_categories = [category.name for category in self.sheets_inventory.get_categories()]
        tab_order: list[str] = self.settings_file.get_value("category_tabs_order")["Sheets in Inventory"]

        # Updates the tab order to add categories that have not previously been added
        for category in all_categories:
            if category not in tab_order:
                tab_order.append(category)

        for tab in tab_order:
            if category := self.sheets_inventory.get_category(tab):
                table = SheetsTableWidget(self.tab_widget)
                self.category_tables.update({category: table})
                self.tab_widget.addTab(table, category.name)
                table.cellChanged.connect(self.table_changed)
                table.cellPressed.connect(self.table_selected_changed)
                table.verticalScrollBar().valueChanged.connect(self.save_scroll_position)
        self.tab_widget.currentChanged.connect(self.load_table)
        self.tab_widget.tabOrderChanged.connect(self.save_category_tabs_order)
        self.tab_widget.tabOrderChanged.connect(self.save_current_tab)
        self.tab_widget.tabBarDoubleClicked.connect(self.edit_category)

    def load_table(self):
        self.category: Category = self.sheets_inventory.get_category(self.tab_widget.tabText(self.tab_widget.currentIndex()))
        current_table = self.category_tables[self.category]
        current_table.blockSignals(True)
        current_table.clearContents()
        current_table.setRowCount(0)
        self.table_sheets_widgets.clear()
        row_index = 0
        for group in self.sheets_inventory.get_all_sheets_material(self.sheets_inventory.get_sheets_by_category(self.category)):
            current_table.insertRow(row_index)
            group_table_item = QTableWidgetItem(group)
            group_table_item.setTextAlignment(4)  # Align text center

            font = QFont()
            font.setPointSize(15)
            group_table_item.setFont(font)
            current_table.setItem(row_index, 0, group_table_item)
            current_table.setSpan(row_index, 0, 1, current_table.columnCount())
            self.set_table_row_color(current_table, row_index, "#141414")
            row_index += 1

            for sheet in self.sheets_inventory.sheets:
                if group != sheet.material:
                    continue

                self.table_sheets_widgets.update({sheet: {}})
                self.table_sheets_widgets[sheet].update({"row": row_index})
                col_index: int = 0
                current_table.insertRow(row_index)
                current_table.setRowHeight(row_index, 35)

                # NAME
                # table_item_sheet_name = QTableWidgetItem(sheet.get_name())
                # current_table.setItem(row_index, col_index, table_item_sheet_name)
                # current_table.item(row_index, col_index).setFont(self.tables_font)
                # self.table_sheets_widgets[sheet].update({"name": table_item_sheet_name})
                # col_index += 1

                # THICKNESS
                comboBox_thickness = QComboBox(self)
                comboBox_thickness.setStyleSheet("border-radius: none;")
                comboBox_thickness.wheelEvent = lambda event: event.ignore()
                comboBox_thickness.addItems(self.sheet_settings.get_thicknesses())
                comboBox_thickness.setCurrentText(sheet.thickness)
                comboBox_thickness.currentTextChanged.connect(self.table_changed)
                current_table.setCellWidget(row_index, col_index, comboBox_thickness)
                self.table_sheets_widgets[sheet].update({"thickness": comboBox_thickness})
                col_index += 1

                # MATERIAL
                comboBox_material = QComboBox(self)
                comboBox_material.setStyleSheet("border-radius: none;")
                comboBox_material.wheelEvent = lambda event: event.ignore()
                comboBox_material.addItems(self.sheet_settings.get_materials())
                comboBox_material.setCurrentText(sheet.material)
                comboBox_material.currentTextChanged.connect(self.table_changed)
                current_table.setCellWidget(row_index, col_index, comboBox_material)
                self.table_sheets_widgets[sheet].update({"material": comboBox_material})
                col_index += 1

                # LENGTH
                spinbox_length = HumbleDoubleSpinBox(self)
                spinbox_length.setDecimals(3)
                spinbox_length.setStyleSheet("border-radius: none;")
                spinbox_length.setValue(sheet.length)
                spinbox_length.valueChanged.connect(self.table_changed)
                current_table.setCellWidget(row_index, col_index, spinbox_length)
                self.table_sheets_widgets[sheet].update({"length": spinbox_length})
                col_index += 1

                # WIDTH
                spinbox_width = HumbleDoubleSpinBox(self)
                spinbox_width.setDecimals(3)
                spinbox_width.setStyleSheet("border-radius: none;")
                spinbox_width.setValue(sheet.width)
                spinbox_width.valueChanged.connect(self.table_changed)
                current_table.setCellWidget(row_index, col_index, spinbox_width)
                self.table_sheets_widgets[sheet].update({"width": spinbox_width})
                col_index += 1

                # COST
                cost_per_sheet = self.sheets_inventory.get_sheet_cost(sheet)
                table_item_cost = QTableWidgetItem(f"${cost_per_sheet:,.2f}")
                current_table.setItem(
                    row_index,
                    col_index,
                    table_item_cost,
                )
                current_table.item(row_index, col_index).setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                current_table.item(row_index, col_index).setFont(self.tables_font)
                self.table_sheets_widgets[sheet].update({"cost": table_item_cost})
                col_index += 1

                # CURRENT QUANTITY
                table_item_quantity = QTableWidgetItem(str(sheet.quantity))
                current_table.setItem(row_index, col_index, table_item_quantity)
                current_table.item(row_index, col_index).setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                current_table.item(row_index, col_index).setFont(self.tables_font)
                self.table_sheets_widgets[sheet].update({"quantity": table_item_quantity})
                col_index += 1

                # COST IN STOCK
                total_cost_in_stock = cost_per_sheet * sheet.quantity
                table_item_cost_in_stock = QTableWidgetItem(f"${total_cost_in_stock:,.2f}")
                current_table.setItem(row_index, col_index, table_item_cost_in_stock)
                current_table.item(row_index, col_index).setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                current_table.item(row_index, col_index).setFont(self.tables_font)
                self.table_sheets_widgets[sheet].update({"total_cost_in_stock": table_item_cost_in_stock})
                col_index += 1

                # ORDER STATUS
                order_status_button = OrderStatusButton()
                order_status_button.setChecked(sheet.is_order_pending)
                order_status_button.clicked.connect(
                    partial(
                        self.order_status_button_sheets_in_inventory,
                        sheet,
                        order_status_button,
                    )
                )
                order_status_button.setStyleSheet("margin-top: 3%; margin-bottom: 3%; margin-left: 5%; margin-right: 5%;")
                current_table.setCellWidget(row_index, col_index, order_status_button)
                self.table_sheets_widgets[sheet].update({"order_pending": order_status_button})
                col_index += 1
                if sheet.is_order_pending:
                    arrival_date = QDateEdit(self)
                    arrival_date.setStyleSheet("border-radius: 0px;")
                    order_status_button.setText(f"Order Pending ({int(sheet.order_pending_quantity)})")
                    year, month, day = map(int, sheet.expected_arrival_time.split("-"))
                    date = QDate(year, month, day)
                    arrival_date.wheelEvent = lambda event: None
                    arrival_date.setDate(date)
                    arrival_date.setCalendarPopup(True)
                    arrival_date.dateChanged.connect(
                        partial(
                            self.arrival_date_change_sheets_in_inventory,
                            sheet,
                            arrival_date,
                        )
                    )
                    current_table.setCellWidget(row_index, col_index, arrival_date)
                    # order_pending_date: str = self.get_value_from_category(item_name=item, key="order_pending_date")
                    order_status_button.setToolTip(f"Order Pending was set at {sheet.order_pending_date} for {sheet.order_pending_quantity} sheets")

                col_index += 1

                # NOTES
                table_item_notes = QTableWidgetItem(sheet.notes)
                current_table.setItem(row_index, col_index, table_item_notes)
                current_table.item(row_index, col_index).setFont(self.tables_font)
                self.table_sheets_widgets[sheet].update({"notes": table_item_notes})
                col_index += 1

                # MODIFIED DATE
                table_item_modified_date = QTableWidgetItem(sheet.latest_change_quantity)
                table_item_modified_date.setToolTip(sheet.latest_change_quantity)
                current_table.setItem(row_index, col_index, table_item_modified_date)
                current_table.item(row_index, col_index).setFont(self.tables_font)
                self.table_sheets_widgets[sheet].update({"modified_date": table_item_modified_date})
                col_index += 1

                # DELETE
                btn_delete = DeletePushButton(
                    parent=self,
                    tool_tip=f"Delete {sheet.get_name()} permanently from {self.category.name}",
                    icon=QIcon("icons/trash.png"),
                )

                def remove_sheet(sheet_to_remove: Sheet, row: int):
                    self.sheets_inventory.remove_sheet(sheet_to_remove)
                    current_table.removeRow(row)
                    self.sheets_inventory.save()
                    self.sync_changes()

                btn_delete.clicked.connect(partial(remove_sheet, sheet, row_index))
                btn_delete.setStyleSheet("border-radius: 0px;")
                current_table.setCellWidget(row_index, col_index, btn_delete)
                if sheet.quantity <= sheet.red_quantity_limit:
                    self.set_table_row_color(current_table, row_index, "#3F1E25")
                elif sheet.quantity <= sheet.yellow_quantity_limit:
                    self.set_table_row_color(current_table, row_index, "#413C28")
                if sheet.is_order_pending:
                    self.set_table_row_color(current_table, row_index, "#29422c")
                row_index += 1

        current_table.blockSignals(False)

        current_table.resizeColumnsToContents()

        if current_table.contextMenuPolicy() != Qt.ContextMenuPolicy.CustomContextMenu:
            current_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            menu = QMenu(self)
            action = QAction(self)
            action.triggered.connect(self.set_custom_quantity_limit)
            action.setText("Set Custom Quantity Limit")
            menu.addAction(action)
            current_table.customContextMenuRequested.connect(partial(self.open_group_menu, menu))

        self.save_current_tab()
        self.save_category_tabs_order()
        self.restore_scroll_position()

    def table_selected_changed(self):
        if sheet := self.get_selected_sheet():
            self.last_selected_sheet = sheet.name
            self.last_selected_index = self.get_selected_row()

    def table_changed(self):
        if not (sheet := self.get_selected_sheet()):
            return
        old_quantity = sheet.quantity
        sheet.quantity = float(
            sympy.sympify(
                self.table_sheets_widgets[sheet]["quantity"].text().strip().replace(",", ""),
                evaluate=True,
            )
        )
        if old_quantity != sheet.quantity:
            sheet.latest_change_quantity = f'{os.getlogin().title()} - Manually set to {sheet.quantity} from {old_quantity} quantity at {str(datetime.now().strftime("%B %d %A %Y %I:%M:%S %p"))}'
        sheet.notes = self.table_sheets_widgets[sheet]["notes"].text()
        sheet.material = self.table_sheets_widgets[sheet]["material"].currentText()
        sheet.thickness = self.table_sheets_widgets[sheet]["thickness"].currentText()
        sheet.length = self.table_sheets_widgets[sheet]["length"].value()
        sheet.width = self.table_sheets_widgets[sheet]["width"].value()
        self.sheets_inventory.save()
        self.sync_changes()
        self.category_tables[self.category].blockSignals(True)
        self.table_sheets_widgets[sheet]["quantity"].setText(f"{sheet.quantity:,.2f}")
        self.table_sheets_widgets[sheet]["modified_date"].setText(sheet.latest_change_quantity)
        self.category_tables[self.category].blockSignals(False)
        self.update_sheet_costs()
        self.update_stock_costs()

    def add_sheet(self) -> None:
        add_sheet_dialog = AddSheetDialog(None, self.category, self.sheets_inventory, self.sheet_settings, self)

        if add_sheet_dialog.exec():
            new_sheet = Sheet(
                "new_name",
                {
                    "quantity": add_sheet_dialog.get_quantity(),
                    "length": add_sheet_dialog.get_length(),
                    "width": add_sheet_dialog.get_width(),
                    "thickness": add_sheet_dialog.get_thickness(),
                    "material": add_sheet_dialog.get_material(),
                    "latest_change_quantity": f"Sheet added at {datetime.now().strftime('%B %d %A %Y %I:%M:%S %p')}",
                },
                self.sheets_inventory,
            )
            new_sheet.add_to_category(self.sheets_inventory.get_category(add_sheet_dialog.get_category()))
            for sheet in self.sheets_inventory.sheets:
                if new_sheet.get_name() == sheet.get_name():
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setWindowTitle("Exists")
                    msg.setText(f"'{new_sheet.get_name()}'\nAlready exists.")
                    msg.exec()
                    return
            self.sheets_inventory.add_sheet(new_sheet)
            self.sheets_inventory.save()
            self.sync_changes()
            self.sort_sheets()
            self.update_stock_costs()

    def order_status_button_sheets_in_inventory(self, sheet: Sheet, button: OrderStatusButton) -> None:
        if button.isChecked():  # Meaning there is not a order pending, and we want to set up a order pending
            select_date_dialog = SetOrderPendingDialog(
                f'Set an expected arrival time for "{sheet.get_name()}" and the number of sheets ordered',
                "Sheets Ordered:",
                self,
            )
            if select_date_dialog.exec():
                sheet.expected_arrival_time = select_date_dialog.get_selected_date()
                sheet.order_pending_quantity = select_date_dialog.get_order_quantity()
                sheet.order_pending_date = datetime.now().strftime("%Y-%m-%d")
                sheet.is_order_pending = True
                self.sheets_inventory.save()
                self.sync_changes()
                self.sort_sheets()
            else:
                button.setChecked(False)
                return
        elif not button.isChecked():  # Meaning there is a order pending, and we want to add the quantity we set.
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Add Sheet Quantity")
            msg_box.setText(f'Do you want to add the incoming sheet quantity for "{sheet.get_name()}"?\n\nThe number of sheets that will be added is: {sheet.order_pending_quantity}.')
            msg_box.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            response = msg_box.exec()
            if response == QMessageBox.StandardButton.Yes:
                modified_date: str = f"{os.getlogin().title()} added {sheet.order_pending_quantity} sheets via order pending at {datetime.now().strftime('%B %d %A %Y %I:%M:%S %p')}"
                sheet.quantity += sheet.order_pending_quantity
                sheet.order_pending_quantity = 0
                sheet.latest_change_quantity = modified_date
                sheet.is_order_pending = False
                sheet.has_sent_warning = False
                self.sheets_inventory.save()
                self.sync_changes()
                self.sort_sheets()
            else:
                button.setChecked(True)
                return

    def arrival_date_change_sheets_in_inventory(self, sheet: Sheet, arrival_date: QDateEdit) -> None:
        sheet.expected_arrival_time = arrival_date.date().toString("yyyy-MM-dd")
        self.sheets_inventory.save()
        self.sync_changes()

    def update_sheet_costs(self):
        self.category_tables[self.category].blockSignals(True)
        for sheet, table_items in self.table_sheets_widgets.items():
            cost_per_sheet = self.sheets_inventory.get_sheet_cost(sheet)
            table_item_cost_in_stock = cost_per_sheet * sheet.quantity
            table_items["cost"].setText(f"${cost_per_sheet:,.2f}")
            table_items["total_cost_in_stock"].setText(f"${table_item_cost_in_stock:,.2f}")
        self.category_tables[self.category].blockSignals(False)

    def set_custom_quantity_limit(self) -> None:
        current_table = self.category_tables[self.category]
        if sheets := self.get_selected_sheets():
            sheets_string = "".join(f"    {i + 1}. {sheet.get_name()}\n" for i, sheet in enumerate(sheets))
            set_custom_limit_dialog = SetCustomLimitDialog(
                self,
                f"Set a custom red and yellow quantity limit for each of the {len(sheets)} selected sheets:\n{sheets_string}",
                sheets[0].red_quantity_limit,
                sheets[0].yellow_quantity_limit,
            )
            if set_custom_limit_dialog.exec():
                for sheet in sheets:
                    sheet.red_quantity_limit = set_custom_limit_dialog.get_red_limit()
                    sheet.yellow_quantity_limit = set_custom_limit_dialog.get_yellow_limit()
                    if sheet.quantity <= sheet.red_quantity_limit:
                        self.set_table_row_color(current_table, self.table_sheets_widgets[sheet]["row"], "#3F1E25")
                    elif sheet.quantity <= sheet.yellow_quantity_limit:
                        self.set_table_row_color(current_table, self.table_sheets_widgets[sheet]["row"], "#413C28")
                    else:
                        self.set_table_row_color(current_table, self.table_sheets_widgets[sheet]["row"], "#2c2c2c")
                self.sheets_inventory.save()
                self.sync_changes()

    def update_stock_costs(self) -> None:
        self.clear_layout(self.gridLayout_sheet_prices)
        grand_total: float = 0.0
        i: int = 0
        for i, category in enumerate(self.sheets_inventory.get_categories()):
            category_total = self.sheets_inventory.get_category_stock_cost(category)
            lbl = QLabel(f"{category.name}:", self)
            self.gridLayout_sheet_prices.addWidget(lbl, i, 0)
            lbl = QLabel(f"${category_total:,.2f}", self)
            # lbl.setTextInteractionFlags(Qt.ItemFlag.TextSelectableByMouse)
            self.gridLayout_sheet_prices.addWidget(lbl, i, 1)
            grand_total += category_total
            i += 1
        lbl = QLabel("Total:", self)
        lbl.setStyleSheet("border-top: 1px solid grey; border-bottom: 1px solid grey")
        self.gridLayout_sheet_prices.addWidget(lbl, i + 1, 0)
        lbl = QLabel(f"${grand_total:,.2f}", self)
        lbl.setStyleSheet("border-top: 1px solid grey; border-bottom: 1px solid grey")
        self.gridLayout_sheet_prices.addWidget(lbl, i + 1, 1)

    def select_last_selected_item(self):
        current_table = self.category_tables[self.category]
        for sheet, table_items in self.table_sheets_widgets.items():
            if sheet.name == self.last_selected_sheet:
                current_table.selectRow(table_items["row"])
                current_table.scrollTo(current_table.model().index(table_items["row"], 0))

    def get_selected_sheets(self) -> list[Sheet]:
        selected_sheets: list[Sheet] = []
        selected_rows = self.get_selected_rows()
        selected_sheets.extend(sheet for sheet, table_items in self.table_sheets_widgets.items() if table_items["row"] in selected_rows)
        return selected_sheets

    def get_selected_sheet(self) -> Sheet:
        selected_row = self.get_selected_row()
        for sheet, table_items in self.table_sheets_widgets.items():
            if table_items["row"] == selected_row:
                self.last_selected_index = selected_row
                self.last_selected_sheet = sheet.name
                return sheet

    def get_selected_rows(self) -> list[int]:
        rows: set[int] = {item.row() for item in self.category_tables[self.category].selectedItems()}
        return list(rows)

    def get_selected_row(self) -> int:
        with contextlib.suppress(IndexError):
            return self.category_tables[self.category].selectedItems()[0].row()

    def set_table_row_color(self, table: SheetsTableWidget, row_index: int, color: str):
        for j in range(table.columnCount()):
            item = table.item(row_index, j)
            if not item:
                item = QTableWidgetItem()
                table.setItem(row_index, j, item)
            item.setBackground(QColor(color))

    def sort_sheets(self):
        self.sheets_inventory.sort_by_thickness()
        self.load_table()

    def save_current_tab(self):
        if self.finished_loading:
            self.parent.sheets_inventory_tab_widget_last_selected_tab_index = self.tab_widget.currentIndex()

    def restore_last_selected_tab(self):
        if self.tab_widget.currentIndex() == self.parent.sheets_inventory_tab_widget_last_selected_tab_index:
            self.sort_sheets()  # * This happens when the last selected tab is the first tab
        else:
            self.tab_widget.setCurrentIndex(self.parent.sheets_inventory_tab_widget_last_selected_tab_index)

    def save_category_tabs_order(self):
        self.settings_file.load_data()
        tab_order = self.settings_file.get_value("category_tabs_order")
        tab_order["Sheets in Inventory"] = self.tab_widget.get_tab_order()
        self.settings_file.set_value("category_tabs_order", tab_order)

    def save_scroll_position(self):
        if self.finished_loading:
            self.parent.save_scroll_position(self.category, self.category_tables[self.category])

    def restore_scroll_position(self):
        if scroll_position := self.parent.get_scroll_position(self.category):
            self.category_tables[self.category].verticalScrollBar().setValue(scroll_position)

    def sync_changes(self):
        self.parent.sync_changes()

    def open_group_menu(self, menu: QMenu) -> None:
        menu.exec(QCursor.pos())

    def clear_layout(self, layout: QVBoxLayout | QWidget) -> None:
        with contextlib.suppress(AttributeError):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self.clear_layout(item.layout())
