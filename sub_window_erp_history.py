from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton,
    QLineEdit, QHeaderView
)
from db_helper import DB, DB_CONFIG
from ui_style import apply_common_style


HEADERS = [
    "이력번호", "작업구분", "관리번호", "변경 전 값",
    "변경 후 값", "처리일시", "등록자"
]

class SubWindow_history(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 관리 이력")
        self.resize(1200, 600)

        self.db = DB(**DB_CONFIG)

        central = QWidget()
        central.setObjectName("contentArea")
        self.setCentralWidget(central)

        apply_common_style(self)

        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(30, 25, 30, 30)

        title_label = QLabel("OO기업 품질보증팀 재고 관리 이력")

        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)

        title_label.setFont(title_font)

        notice_label = QLabel(
            "추가, 수정, 삭제된 재고 정보의 처리일시와 등록자를 조회할 수 있습니다."
        )

        top_box = QHBoxLayout()

        top_box.addWidget(QLabel("관리번호"))

        self.management_input = QLineEdit()
        self.management_input.setPlaceholderText("관리번호 입력")
        self.management_input.returnPressed.connect(self.search_history)

        self.btn_search = QPushButton("조회")
        self.btn_search.clicked.connect(self.search_history)

        self.btn_refresh = QPushButton("전체 조회")
        self.btn_refresh.clicked.connect(self.load_history)

        top_box.addWidget(self.management_input)
        top_box.addWidget(self.btn_search)
        top_box.addWidget(self.btn_refresh)
        top_box.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        # 각 헤더 클릭 시 오름차순/내림차순 정렬
        self.table.setSortingEnabled(True)

        # 이력 내용이 긴 열을 넓게 표시
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )

        self.table.setColumnWidth(0, 70)   # 이력번호
        self.table.setColumnWidth(1, 80)   # 작업구분
        self.table.setColumnWidth(2, 100)  # 관리번호
        self.table.setColumnWidth(3, 260)  # 변경 전 값
        self.table.setColumnWidth(4, 260)  # 변경 후 값
        self.table.setColumnWidth(5, 150)  # 처리일시
        self.table.setColumnWidth(6, 100)  # 등록자

        vbox.addWidget(title_label)
        vbox.addWidget(notice_label)
        vbox.addLayout(top_box)
        vbox.addWidget(self.table)

        self.load_history()

    def show_history(self, rows):
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

    def load_history(self):
        self.management_input.clear()

        rows = self.db.get_history()
        self.show_history(rows)

    def search_history(self):
        관리번호 = self.management_input.text().strip()

        rows = self.db.get_history(관리번호)
        self.show_history(rows)