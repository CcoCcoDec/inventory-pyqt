# main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OO주식회사 품질보증팀 재고 관리")
        self.db = DB(**DB_CONFIG)

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        form_box = QHBoxLayout()
        self.input_관리번호 = QLineEdit()
        self.input_분류 = QLineEdit()
        self.input_자재명 = QLineEdit()
        self.input_재고수량 = QLineEdit()
        self.input_수량단위 = QLineEdit()
        self.input_재고단가 = QLineEdit()
        self.input_단가단위 = QLineEdit()
        self.input_업데이트 = QLineEdit()
        self.input_등록자 = QLineEdit()

        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.add_erp)

        form_box.addWidget(QLabel("관리번호"))
        form_box.addWidget(self.input_관리번호)
        form_box.addWidget(QLabel("분류"))
        form_box.addWidget(self.input_분류)        
        form_box.addWidget(QLabel("자재명"))
        form_box.addWidget(self.input_자재명)
        form_box.addWidget(QLabel("재고수량"))
        form_box.addWidget(self.input_재고수량)
        form_box.addWidget(QLabel("수량단위"))
        form_box.addWidget(self.input_수량단위)
        form_box.addWidget(QLabel("재고단가"))
        form_box.addWidget(self.input_재고단가)
        form_box.addWidget(QLabel("단가단위"))
        form_box.addWidget(self.input_단가단위)
        form_box.addWidget(QLabel("업데이트"))
        form_box.addWidget(self.input_업데이트)
        form_box.addWidget(QLabel("등록자"))
        form_box.addWidget(self.input_등록자)

        form_box.addWidget(self.btn_add)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["관리번호", "분류", "자재명", "재고수량", "수량단위", "재고단가", "단가단위", "업데이트", "등록자"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        vbox.addLayout(form_box)
        vbox.addWidget(self.table)

        self.load_erp()

    def load_erp(self):
        rows = self.db.fetch_erp()
        self.table.setRowCount(len(rows))
        for r, (관리번호, 분류, 자재명, 재고수량, 수량단위, 재고단가, 단가단위, 업데이트, 등록자) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(관리번호))
            self.table.setItem(r, 1, QTableWidgetItem(분류))
            self.table.setItem(r, 2, QTableWidgetItem(자재명))
            self.table.setItem(r, 3, QTableWidgetItem(str(재고수량)))
            self.table.setItem(r, 4, QTableWidgetItem(수량단위))
            self.table.setItem(r, 5, QTableWidgetItem(str(재고단가)))
            self.table.setItem(r, 6, QTableWidgetItem(단가단위))
            self.table.setItem(r, 7, QTableWidgetItem(str(업데이트)))
            self.table.setItem(r, 8, QTableWidgetItem(등록자))
        self.table.resizeColumnsToContents()

    def add_erp(self):
        관리번호 = self.input_관리번호.text().strip()
        분류 = self.input_분류.text().strip()
        자재명 = self.input_자재명.text().strip()
        재고수량 = self.input_재고수량.text().strip()
        수량단위 = self.input_수량단위.text().strip()
        재고단가 = self.input_재고단가.text().strip()
        단가단위 = self.input_단가단위.text().strip()
        업데이트 = self.input_업데이트.text().strip()
        등록자 = self.input_등록자.text().strip()

        ok = self.db.insert_erp(관리번호, 분류, 자재명, 재고수량, 수량단위, 재고단가, 단가단위, 업데이트, 등록자)

        if ok:
            QMessageBox.information(self, "완료", "추가되었습니다.")
            self.input_관리번호.clear()
            self.input_분류.clear()
            self.input_자재명.clear()
            self.input_재고수량.clear()
            self.input_수량단위.clear()
            self.input_재고단가.clear()
            self.input_단가단위.clear()
            self.input_업데이트.clear()
            self.input_등록자.clear()
            self.load_erp()

        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")