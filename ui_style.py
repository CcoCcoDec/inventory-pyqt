from PyQt5.QtGui import QFont


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700


def apply_common_style(window):
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setFont(QFont("맑은 고딕", 10))

    window.setStyleSheet("""
        #contentArea {
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #b7dcf6,
                stop: 0.45 #d8edfb,
                stop: 1 #f4fbff
            );
        }

        QLabel {
            color: #173a5e;
            background: transparent;
        }

        QLineEdit, QDateEdit {
            background-color: rgba(255, 255, 255, 220);
            border: 1px solid #8ab7d8;
            border-radius: 5px;
            padding: 6px;
        }

        QLineEdit:focus, QDateEdit:focus {
            border: 2px solid #397fb5;
        }

        QPushButton {
            color: white;
            background-color: #397fb5;
            border: none;
            border-radius: 7px;
            padding: 8px 14px;
            font-family: "맑은 고딕";
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #28658f;
        }

        QPushButton:pressed {
            background-color: #1e4d70;
        }

        QTableWidget {
            background-color: rgba(255, 255, 255, 230);
            border: 1px solid #8ab7d8;
            gridline-color: #c5dceb;
            selection-background-color: #a9d2ee;
            selection-color: #173a5e;
        }

        QHeaderView::section {
            background-color: #6da7d1;
            color: white;
            padding: 6px;
            border: none;
            font-weight: bold;
        }
    """)