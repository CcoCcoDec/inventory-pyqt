# main_window.py

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG
from sub_window_erp import SubWindow
from sub_window_erp_history import SubWindow_history
from sub_window_info import SubWindow_info

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("erp")

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        form_box = QHBoxLayout()

        self.btn_search = QPushButton("재고 조회")
        self.btn_search.clicked.connect(self.open_subwindow)
        self.btn_history = QPushButton("재고 이력")
        self.btn_history.clicked.connect(self.open_subwindow_history)
        self.btn_info = QPushButton("버전 정보")
        self.btn_info.clicked.connect(self.open_subwindow_info)

        form_box.addWidget(self.btn_search)
        form_box.addWidget(self.btn_history)
        form_box.addWidget(self.btn_info)

        vbox.addLayout(form_box)

    def open_subwindow(self):
        self.sub = SubWindow()
        self.sub.show()

    def open_subwindow_history(self):
        self.sub = SubWindow_history()
        self.sub.show()        

    def open_subwindow_info(self):
        self.sub = SubWindow_info()
        self.sub.show()
        self.sub.resize(300, 100)

