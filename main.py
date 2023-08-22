import sys
import random

from PySide6 import QtWidgets, QtCore, QtGui
from functools import partial
from helpers import load_yaml, save_yaml

class ProxyStyle(QtWidgets.QProxyStyle):
    def subElementRect(self, e, opt, widget):
        c = super().subElementRect(e, opt, widget)
        if e == QtWidgets.QStyle.SE_ItemViewItemCheckIndicator:
            c.moveCenter(opt.rect.center())
        return c
class MainWindow(QtWidgets.QWidget):
    def __init__(self, checkbox_data, ischild=False):
        super().__init__()
        self.checkbox_data = checkbox_data

        # Create the main window
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setFixedSize(430, 550)
        self.main_window.setWindowTitle("Main Window")

        # Create a vertical layout for the main window
        main_layout = QtWidgets.QVBoxLayout(self)
        self.widget = QtWidgets.QWidget()
        self.main_window.setLayout(main_layout)
        self.create_scrollable_table(main_layout)

        # Create an empty window display
        closed_window = QtWidgets.QMainWindow()
        closed_window.setWindowTitle("Closed Window")
        closed_window.resize(300, 100)

        if not ischild:
            # Draws a category
            # Label to show drawed category
            self.category_button = QtWidgets.QPushButton("Draw Category")
            self.category_button.setFixedSize(120, 30)
            self.category_label = QtWidgets.QLabel()
            self.category_button.clicked.connect(partial(self.draw_category, 'category', self.category_label))
            main_layout.addWidget(self.category_button, alignment = QtCore.Qt.AlignCenter)
            main_layout.addWidget(self.category_label)

            # Draws a subcategory
            # and Label to show drawed subcategory
            self.category_button = QtWidgets.QPushButton("Draw subcategory")
            self.category_button.setFixedSize(120, 30)
            self.task_label = QtWidgets.QLabel()
            self.category_button.clicked.connect(partial(self.draw_category, 'subcategory', self.task_label))
            main_layout.addWidget(self.category_button, alignment = QtCore.Qt.AlignCenter)
            main_layout.addWidget(self.task_label)

            # Draws a task
            # and Label to show drawed task
            self.category_button = QtWidgets.QPushButton("Draw Task")
            self.category_button.setFixedSize(120, 30)
            self.task_label = QtWidgets.QLabel()
            self.category_button.clicked.connect(partial(self.draw_category, 'task', self.task_label))
            main_layout.addWidget(self.category_button, alignment = QtCore.Qt.AlignCenter)
            main_layout.addWidget(self.task_label)


            # Saves data
            self.category_button = QtWidgets.QPushButton("Save data")
            self.category_button.setFixedSize(120, 30)
            self.category_button.clicked.connect(self.save_data)
            main_layout.addWidget(self.category_button, alignment = QtCore.Qt.AlignCenter)

            #exit program
            self.category_button = QtWidgets.QPushButton("Exit")
            self.category_button.setFixedSize(120, 30)
            self.category_button.clicked.connect(self.exit)
            main_layout.addWidget(self.category_button, alignment = QtCore.Qt.AlignCenter)

        self.setLayout(main_layout)

    def draw_category(self, txt_label, label):
        if txt_label == 'category':
            data = self.checkbox_data
        else:
            data = self.drawed
        categories = [category for category in data if category['state']]
        if categories:
            selected_category = random.choice(categories)
            label.setText(f"Selected {txt_label}: {selected_category['name']}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            print(f"Selected {txt_label}:", selected_category['name'])

            if txt_label == 'category':
                self.drawed = selected_category['subcategories']
        else:
            print(f"No {txt_label} selected.")

    def save_data(self, event:QtGui.QCloseEvent):
        question = QtWidgets.QMessageBox.question(self, "Question","Do you want to save data?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if question == QtWidgets.QMessageBox.StandardButton.Yes:
            save_yaml({'categories':self.checkbox_data})
            QtWidgets.QMessageBox.information(self, "Information","Data has been saved!", QtWidgets.QMessageBox.Ok)
            print("data has been saved!")
        if question == QtWidgets.QMessageBox.StandardButton.No:
            QtWidgets.QMessageBox.information(self, "Information","Data has not been saved!", QtWidgets.QMessageBox.Ok)
            print("data has not been saved!")

    def exit(self, event:QtGui.QCloseEvent):
        close_app = QtWidgets.QMessageBox.question(self, "Close App","Do you want to close app?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if close_app == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()

    def create_scrollable_table(self, main_layout:QtWidgets.QVBoxLayout):

         # Create a scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_widget = QtWidgets.QWidget()

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        # Create a vertical layout for the scrollable area
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        # Create a table with checkboxes and buttons
        #TODO: add second checkbox for "HasRead"
        self.table_widget = QtWidgets.QTableWidget(0, 3)
        self.table_widget.setHorizontalHeaderLabels([' Use ', 'HasRead', 'Title'])
        self.table_widget.horizontalHeader().setMinimumSectionSize(15)
        self.table_widget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeToContents)
       
        

        # Add checkbox data
        data = self.checkbox_data
        for row_id, obj in enumerate(data):
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self._style = ProxyStyle(self.style())
            self.setStyle(self._style)

            checkbox_item = QtWidgets.QTableWidgetItem()
            checkbox_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            checkbox_item.setCheckState(QtCore.Qt.Checked if obj['state'] else QtCore.Qt.Unchecked)
            self.table_widget.setItem(row_position, 0, checkbox_item)

            has_read_item = QtWidgets.QTableWidgetItem()
            has_read_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            has_read_item.setCheckState(QtCore.Qt.Checked if obj['hasRead'] else QtCore.Qt.Unchecked)
            self.table_widget.setItem(row_position, 1, has_read_item)

            clickable_button = QtWidgets.QPushButton(obj['name'])
            clickable_button.setFixedWidth(250)
            clickable_button.clicked.connect(partial(self.show_window, row_id))
            self.table_widget.setCellWidget(row_position, 2, clickable_button)

        scroll_layout.addWidget(self.table_widget)
        main_layout.addWidget(scroll_area)
        self.table_widget.cellChanged.connect(self.checkbox_state_changed)

    def checkbox_state_changed(self, row, column):
        checkbox_item = self.table_widget.item(row, 0)
        state = checkbox_item.checkState()
        self.checkbox_data[row]['state'] = state == QtCore.Qt.Checked

        button_widget = self.table_widget.cellWidget(row, 2)
        button_text = button_widget.text()
        print(button_text, self.checkbox_data[row]['state'])

    def show_window(self, row: int):
        if 'subcategories' in self.checkbox_data[row]:
            data = self.checkbox_data[row]['subcategories']
        elif 'tasks' in self.checkbox_data[row]:
            data = self.checkbox_data[row]['tasks']
        else:
            return
        new_window = MainWindow(data, ischild=True)
        new_window.display_main_window()

    def display_main_window(self):
        self.main_window.setCentralWidget(self)
        self.main_window.show()


def run_app():
    data = load_yaml()
    app = QtWidgets.QApplication([])

    # Create an instance of the CustomWindow class
    window = MainWindow(data['categories'])

    # Call the display_main_window method to show the main window
    window.display_main_window()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()