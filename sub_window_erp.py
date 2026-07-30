from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QAbstractItemView,
    QHeaderView, QDateEdit,
    QLabel, QLineEdit, QPushButton, QMessageBox,
    QDialog, QFormLayout)
from db_helper import DB, DB_CONFIG
from ui_style import apply_common_style

HEADERS = [
    "관리번호", "분류", "자재명", "재고수량", "수량단위",
    "재고단가", "단가단위", "업데이트", "등록자"
]

class EditDialog(QDialog):
    DELETE_RESULT = 2

    def __init__(self, row_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("재고 정보 수정")

        self.inputs = []
        form = QFormLayout(self)

        for index, title in enumerate(HEADERS):
            line = QLineEdit(str(row_data[index]))
            self.inputs.append(line)
            form.addRow(title, line)

        # 관리번호는 수정 및 삭제의 기준값
        self.inputs[0].setReadOnly(True)

        button_box = QHBoxLayout()

        self.btn_save = QPushButton("수정 저장")
        self.btn_save.clicked.connect(self.accept)

        self.btn_delete = QPushButton("삭제")
        self.btn_delete.clicked.connect(self.delete_item)

        button_box.addWidget(self.btn_save)
        button_box.addWidget(self.btn_delete)
        form.addRow(button_box)

    def delete_item(self):
        answer = QMessageBox.question(
            self,
            "재고 정보 삭제",
            "정말 이 재고 정보를 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )

        if answer == QMessageBox.Yes:
            self.done(self.DELETE_RESULT)

    def values(self):
        return [input_box.text().strip() for input_box in self.inputs]


class SubWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 조회")
        self.db = DB(**DB_CONFIG)

        central = QWidget()
        central.setObjectName("contentArea")
        self.setCentralWidget(central)

        apply_common_style(self)

        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(30, 25, 30, 30)

        title_label = QLabel("OO기업 품질보증팀 재고 정보")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)

        notice_label = QLabel(
            "재고 정보 표 값 클릭: 수정 및 삭제\n헤더 클릭: 정렬"
        )

        vbox.addWidget(title_label)
        vbox.addWidget(notice_label)

        # 재고 추가 영역
        add_box = QHBoxLayout()
        self.inputs = []

        for title in HEADERS:
            if title == "업데이트":
                input_box = QDateEdit()
                input_box.setDisplayFormat("yyyy-MM-dd")
                input_box.setCalendarPopup(True)
                input_box.setDate(QDate.currentDate())
                input_box.setToolTip("날짜 형식: YYYY-MM-DD")
            else:
                input_box = QLineEdit()
                input_box.setPlaceholderText(title)

            self.inputs.append(input_box)
            add_box.addWidget(input_box)

        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.add_erp)
        add_box.addWidget(self.btn_add)

        # 재고 검색 영역
        search_box = QHBoxLayout()
        search_box.addWidget(QLabel("검색어"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("관리번호, 분류 또는 자재명")
        self.search_input.returnPressed.connect(self.search_erp)

        self.btn_search = QPushButton("검색")
        self.btn_search.clicked.connect(self.search_erp)

        self.btn_all = QPushButton("전체 조회")
        self.btn_all.clicked.connect(self.load_erp)

        search_box.addWidget(self.search_input)
        search_box.addWidget(self.btn_search)
        search_box.addWidget(self.btn_all)

        # 재고 목록
        self.table = QTableWidget()
        self.table.setColumnCount(len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)

        # 열 제목을 클릭할 때마다 오름차순/내림차순 정렬
        self.table.setSortingEnabled(True)

        # 각 열이 테이블의 가로 폭을 모두 사용하도록 설정
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.cellClicked.connect(self.edit_erp)

        vbox.addLayout(add_box)
        vbox.addLayout(search_box)
        vbox.addWidget(self.table)

        self.load_erp()

    def show_rows(self, rows):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for column_index, value in enumerate(row_data):
                self.table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(str(value))
                )

        self.table.setSortingEnabled(True)

    def load_erp(self):
        rows = self.db.fetch_erp()
        self.show_rows(rows)

    def search_erp(self):
        keyword = self.search_input.text().strip()

        if not keyword:
            self.load_erp()
            return

        rows = self.db.search_erp(keyword)
        self.show_rows(rows)

    def add_erp(self):
        values = [input_box.text().strip() for input_box in self.inputs]

        if not all(values):
            QMessageBox.warning(self, "입력 오류", "모든 항목을 입력하세요.")
            return

        try:
            values[3] = int(values[3])     # 재고수량
            values[5] = int(values[5])     # 재고단가
        except ValueError:
            QMessageBox.warning(
                self,
                "입력 오류",
                "재고수량과 재고단가는 숫자로 입력하세요."
            )
            return

        ok = self.db.insert_erp(*values)

        if ok:
            QMessageBox.information(self, "완료", "재고 정보가 추가되었습니다.")

            for input_box in self.inputs:
                input_box.clear()

            self.load_erp()
        else:
            QMessageBox.critical(self, "실패", "재고 정보 추가 중 오류가 발생했습니다.")

    def edit_erp(self, row, column):
        row_data = []

        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            row_data.append(item.text())

        dialog = EditDialog(row_data, self)
        result = dialog.exec_()

        # 삭제 버튼을 눌렀고, 삭제 확인까지 완료한 경우
        if result == EditDialog.DELETE_RESULT:
            관리번호 = row_data[0]
            ok = self.db.delete_erp(관리번호)

            if ok:
                QMessageBox.information(self, "완료", "재고 정보가 삭제되었습니다.")
                self.search_erp()
            else:
                QMessageBox.critical(self, "실패", "재고 정보 삭제 중 오류가 발생했습니다.")

            return

        # 수정 창에서 취소한 경우
        if result != QDialog.Accepted:
            return

        values = dialog.values()

        if not all(values):
            QMessageBox.warning(self, "입력 오류", "모든 항목을 입력하세요.")
            return

        try:
            values[3] = int(values[3])  # 재고수량
            values[5] = int(values[5])  # 재고단가
        except ValueError:
            QMessageBox.warning(
                self,
                "입력 오류",
                "재고수량과 재고단가는 숫자로 입력하세요."
            )
            return

        ok = self.db.update_erp(*values)

        if ok:
            QMessageBox.information(self, "완료", "재고 정보가 수정되었습니다.")
            self.search_erp()
        else:
            QMessageBox.critical(self, "실패", "재고 정보 수정 중 오류가 발생했습니다.")