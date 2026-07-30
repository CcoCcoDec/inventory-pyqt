# login_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QColor
from ui_style import apply_common_style

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로그인")

        apply_common_style(self)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(
            base_dir,
            "assets",
            "erp_login_background.png"
        )

        self.background_image = QPixmap(image_path)

        self.db = DB(**DB_CONFIG)

        self.username = QLineEdit()
        self.username.setPlaceholderText("아이디")

        self.password = QLineEdit()
        self.password.setPlaceholderText("비밀번호")
        self.password.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("아이디", self.username)
        form.addRow("비밀번호", self.password)

        self.btn_login = QPushButton("로그인")
        self.btn_login.setFixedHeight(45)
        self.btn_login.clicked.connect(self.try_login)

        layout = QVBoxLayout()
        layout.setContentsMargins(350, 220, 350, 220)
        layout.addStretch()
        layout.addLayout(form)
        layout.addSpacing(15)
        layout.addWidget(self.btn_login)
        layout.addStretch()

        self.setLayout(layout)

    def try_login(self):
        uid = self.username.text().strip()
        pw = self.password.text().strip()
        if not uid or not pw:
            QMessageBox.warning(self, "오류", "아이디와 비밀번호를 모두 입력하세요.")
            return

        ok = self.db.verify_user(uid, pw)
        if ok:
            self.accept()
        else:
            QMessageBox.critical(self, "실패", "아이디 또는 비밀번호가 올바르지 않습니다.")

    def paintEvent(self, event):
        painter = QPainter(self)

        # 배경 이미지를 60% 투명도로 표시
        if not self.background_image.isNull():
            painter.setOpacity(0.6)

            scaled_image = self.background_image.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            x = (self.width() - scaled_image.width()) // 2
            y = (self.height() - scaled_image.height()) // 2

            painter.drawPixmap(x, y, scaled_image)

        painter.end()