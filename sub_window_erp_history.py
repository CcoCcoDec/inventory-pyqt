
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG

class SubWindow_history(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OO주식회사 품질보증팀 재고 관리 - 재고 이력")
        self.db = DB(**DB_CONFIG)