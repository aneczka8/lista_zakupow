import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from shopping_list_engine import *


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.file_name = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Shopping list")
        layout = QGridLayout()
        self.setLayout(layout)

        show_store_btn = QPushButton("Go to the store menu")
        show_store_btn.clicked.connect(self.switch_widget)
        layout.addWidget(show_store_btn, 1, 0)

        self.refresh_btn = QPushButton("Refresh the shopping list", self)
        self.refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(self.refresh_btn, 2, 0)

        self.save_list_btn = QPushButton("Save the list to a file", self)
        self.save_list_btn.clicked.connect(self.save_list)
        layout.addWidget(self.save_list_btn, 3, 0)

        self.read_list_btn = QPushButton("Read the list from a file", self)
        self.read_list_btn.clicked.connect(self.read_list)
        layout.addWidget(self.read_list_btn, 4, 0)

        shopping_list = create_shopping_list()
        self.shopping_list_listwidget = QListWidget()
        for index in range(0, len(shopping_list)):
            self.shopping_list_listwidget.insertItem(index, shopping_list[index])
        layout.addWidget(self.shopping_list_listwidget, 1, 1)
        self.shopping_list_listwidget.itemDoubleClicked.connect(self.delete_product)

        self.add_product_label = QLabel("Type new product into the list: ", self)
        layout.addWidget(self.add_product_label, 2, 1)

        self.new_product_line = QLineEdit()
        layout.addWidget(self.new_product_line, 3, 1)

        self.add_product_btn = QPushButton("Add product", self)
        self.add_product_btn.clicked.connect(self.launchStoreChoice)
        layout.addWidget(self.add_product_btn, 4, 1)

        self.delete_info_label = QLabel("To remove,  double click on the product.", self)
        layout.addWidget(self.delete_info_label, 0, 1)

    def refresh(self):
        shopping_list = create_shopping_list()
        self.shopping_list_listwidget.clear()
        for index in range(0, len(shopping_list)):
            item = shopping_list[index].replace('[','').replace(']','').replace("'","")
            if item:
                self.shopping_list_listwidget.insertItem(index, item)

    def delete_product(self, item):
        reply = QMessageBox.question(self, '', f'Are you sure you want to delete {item.text()} from the list?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_product(item.text())
            item_index = self.shopping_list_listwidget.currentRow()
            self.shopping_list_listwidget.takeItem(item_index)

    def launchFileNameInput(self):
        text, ok = QInputDialog.getText(self, 'File name', 'Type the file name')
        if ok:
            self.file_name = str(text)

    def switch_widget(self):
        stacked_widget.setCurrentIndex(1)

    def save_list(self):
        self.launchFileNameInput()
        save_file(self.file_name)

    def read_list(self):
        self.launchFileNameInput()
        if type(read_file(self.file_name)) == str:
            text = read_file(self.file_name)
            QMessageBox.warning(self, "Failed attempt", text)
        else:
            read_file(self.file_name)

    def add_product(self, store_index):
        shopping_list = create_shopping_list()
        if self.new_product_line.text():
            text = self.new_product_line.text()
            add_product(text, store_index)
            self.shopping_list_listwidget.insertItem(len(shopping_list), text)
            self.new_product_line.clear()

    def launchStoreChoice(self):
        pop = StoreChoice(self)
        pop.storeSelectedSignal.connect(self.add_product_to_store)
        pop.show()

    def add_product_to_store(self, store):
        shopping_list = create_shopping_list()
        if self.new_product_line.text():
            text = self.new_product_line.text()
            add_product(text, store)
            self.shopping_list_listwidget.insertItem(len(shopping_list), text)
            self.new_product_line.clear()


class StoreChoice(QDialog):
    storeSelectedSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(StoreChoice, self).__init__(parent)
        layout = QVBoxLayout(self)

        self.cb = QComboBox()
        stores = list(show_stores())
        self.cb.addItems(stores)
        layout.addWidget(self.cb)

        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.select_store)
        layout.addWidget(self.ok_btn)

    def select_store(self):
        selected_store = self.cb.currentIndex()
        self.storeSelectedSignal.emit(selected_store)
        self.close()


class StoreView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        stores = list(show_stores())

        self.stores_groupbox = QGroupBox("Your stores")
        stores_layout = QVBoxLayout()
        self.stores_groupbox.setLayout(stores_layout)

        self.stores_btn_group = QButtonGroup(self)

        self.deleting_groupbox = QGroupBox("")
        deleting_layout = QVBoxLayout()
        self.deleting_groupbox.setLayout(deleting_layout)

        self.del_btn_group = QButtonGroup(self)

        for index in range(0, len(stores)):
            btn = QPushButton(f"{stores[index]}", self)
            btn.clicked.connect(lambda _, text=stores[index]: self.chosen_store(text))
            stores_layout.addWidget(btn)
            self.stores_btn_group.addButton(btn, index)

            del_btn = QPushButton("-")
            del_btn.clicked.connect(lambda _, del_btn=del_btn: self.delete_store(del_btn))                  
            deleting_layout.addWidget(del_btn)
            self.del_btn_group.addButton(del_btn, index)          

        layout.addWidget(self.stores_groupbox, 0, 0, len(stores), 1)
        layout.addWidget(self.deleting_groupbox, 0, 1, len(stores), 1)

        self.delete_info_label = QLabel("To delete,  double click on the product.", self)
        layout.addWidget(self.delete_info_label, 0, 2)

        store_list = create_store_list(stores[0])
        self.store_list_listwidget = QListWidget()
        for index in range(0, len(self.store_list_listwidget)):
            item = shopping_list[index].replace('[','').replace(']','').replace("'","")
            self.store_list_listwidget.insertItem(index, item)
        self.store_list_listwidget.addItems(store_list)
        layout.addWidget(self.store_list_listwidget, 1, 2, len(stores), 1)
        self.store_list_listwidget.itemDoubleClicked.connect(self.delete_product)

        self.add_store_btn = QPushButton("Add store", self)
        self.add_store_btn.clicked.connect(self.add_store)
        layout.addWidget(self.add_store_btn, len(stores) + 1, 0)

        self.add_product_label = QLabel("Type new product into the list:: ", self)
        layout.addWidget(self.add_product_label, len(stores) + 1, 2)

        self.new_product_line = QLineEdit()
        layout.addWidget(self.new_product_line, len(stores) + 2, 2)

        self.add_product_btn = QPushButton("Add product", self)
        self.add_product_btn.clicked.connect(self.add_product_to_store)
        layout.addWidget(self.add_product_btn, len(stores) + 3, 2)

        exit_btn = QPushButton("Go back to the main menu")
        exit_btn.clicked.connect(self.switch_widget)
        layout.addWidget(exit_btn, len(stores) + 4, 2)
        self.setLayout(layout)

    def delete_product(self, item):
        reply = QMessageBox.question(self, '', f'Are you sure you want to delete {item.text()} from the list?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_product(item.text())
            item_index = self.store_list_listwidget.currentRow()
            self.store_list_listwidget.takeItem(item_index)

    def add_store(self):
        text, ok = QInputDialog.getText(self, 'Store addition', 'Type a store name')
        if ok:
            store_name = str(text)
            btn = QPushButton(store_name, self)
            del_btn = QPushButton("-", self)
            self.stores_groupbox.layout().insertWidget(self.stores_groupbox.layout().count(), btn)
            self.deleting_groupbox.layout().insertWidget(self.deleting_groupbox.layout().count(), del_btn)
            self.stores_btn_group.addButton(btn)
            self.del_btn_group.addButton(del_btn)
            btn.clicked.connect(lambda: self.chosen_store(btn))
            del_btn.clicked.connect(lambda: self.delete_store(del_btn))
            add_store(store_name)

    def add_product_to_store(self, store):
        shopping_list = create_shopping_list()
        if self.new_product_line.text():
            text = self.new_product_line.text()
            add_product(text, store)
            self.store_list_listwidget.insertItem(len(shopping_list), text)
            self.new_product_line.clear()

    def chosen_store(self, store_name):
        store_shopping_list = create_store_list(store_name)
        self.store_list_listwidget.clear()
        for index in range(0, len(store_shopping_list)):
            item = store_shopping_list[index].replace('[','').replace(']','').replace("'","")
            self.store_list_listwidget.insertItem(index, item)

    def delete_store(self, del_btn):
        btn_id = self.del_btn_group.id(del_btn)
        store_button = self.stores_btn_group.button(btn_id)
        if store_button is not None:
            self.del_btn_group.removeButton(del_btn)
            self.stores_btn_group.removeButton(store_button)
            delete_store(store_button.text())
            if not self.stores_btn_group.buttons():
                self.store_list_listwidget.clear()

        stores_layout = self.stores_groupbox.layout()
        deleting_layout = self.deleting_groupbox.layout()
        stores_layout.removeWidget(store_button)
        deleting_layout.removeWidget(del_btn)
        store_button.deleteLater()
        del_btn.deleteLater()

    def switch_widget(self):
        stacked_widget.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    widget1 = MainView()
    widget2 = StoreView()
    stacked_widget.addWidget(widget1)
    stacked_widget.addWidget(widget2)

    stacked_widget.setCurrentIndex(0)
    stacked_widget.show()

    sys.exit(app.exec_())