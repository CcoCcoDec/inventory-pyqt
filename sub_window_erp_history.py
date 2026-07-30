from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton
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

        self.btn_refresh = QPushButton("새로고침")
        self.btn_refresh.clicked.connect(self.load_history)

        top_box.addWidget(self.btn_refresh)
        top_box.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        vbox.addWidget(title_label)
        vbox.addWidget(notice_label)
        vbox.addLayout(top_box)
        vbox.addWidget(self.table)

        self.load_history()

    def load_history(self):
        rows = self.db.get_history()

        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for column_index, value in enumerate(row_data):
                self.table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(str(value))
                )

        self.table.resizeColumnsToContents()