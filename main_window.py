# main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("회원 관리")
        self.db = DB(**DB_CONFIG)


        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)


        form_box = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_email = QLineEdit()
        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.add_member)

        form_box.addWidget(QLabel("이름"))
        form_box.addWidget(self.input_name)
        form_box.addWidget(QLabel("이메일"))
        form_box.addWidget(self.input_email)
        form_box.addWidget(self.btn_add)


        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "이메일"])
        self.table.setEditTriggers(self.table.NoEditTriggers)  # 표준 예시: 목록은 읽기 전용
        self.table.verticalHeader().setVisible(False)


        vbox.addLayout(form_box)
        vbox.addWidget(self.table)


        self.load_members()

    def load_members(self):
        rows = self.db.fetch_erp()
        self.table.setRowCount(len(rows))
        for r, (mid, name, email) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(mid)))
            self.table.setItem(r, 1, QTableWidgetItem(name))
            self.table.setItem(r, 2, QTableWidgetItem(email))
        self.table.resizeColumnsToContents()

    def add_member(self):
        name = self.input_name.text().strip()
        email = self.input_email.text().strip()
        if not name or not email:
            QMessageBox.warning(self, "오류", "이름과 이메일을 모두 입력하세요.")
            return
        ok = self.db.insert_erp(name, email)
        if ok:
            QMessageBox.information(self, "완료", "추가되었습니다.")
            self.input_name.clear()
            self.input_email.clear()
            self.load_members()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")