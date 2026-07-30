# main_window.py

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui_style import apply_common_style
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG
from sub_window_erp import SubWindow
from sub_window_erp_history import SubWindow_history
from sub_window_info import SubWindow_info

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OO기업 품질보증팀 ERP")

        central = QWidget()
        central.setObjectName("contentArea")
        self.setCentralWidget(central)

        apply_common_style(self)

        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(70, 50, 70, 70)

        title_label = QLabel("OO기업 품질보증팀 재고 정보")

        title_font = QFont("맑은 고딕", 22)
        title_font.setBold(True)

        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignLeft)

        vbox.addWidget(title_label)
        vbox.addStretch(2)

        self.btn_search = QPushButton("재고 조회")
        self.btn_search.clicked.connect(self.open_subwindow)

        self.btn_history = QPushButton("재고 이력")
        self.btn_history.clicked.connect(self.open_subwindow_history)

        self.btn_info = QPushButton("버전 정보")
        self.btn_info.clicked.connect(self.open_subwindow_info)

        buttons = [
            self.btn_search,
            self.btn_history,
            self.btn_info
        ]

        for button in buttons:
            button.setFixedSize(360, 65)
            vbox.addWidget(button, alignment=Qt.AlignHCenter)
            vbox.addSpacing(15)

        vbox.addStretch(3)

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

