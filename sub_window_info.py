
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from db_helper import DB, DB_CONFIG
from PyQt5.QtCore import Qt

class SubWindow_info(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("버전 정보")


        label = QLabel(self)
        label.setFrameStyle(QFrame.Panel)
        label.setText("버전 정보: V1.0\n관리자: 김진태\n연락처: turtle950211@gmail.com")
        label.setAlignment(Qt.AlignCenter)
        label.resize(300, 100)


        