import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QSizePolicy
import sys
from PyQt6.QtGui import QFont


class ConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;  /* Dark background color */
                color: #20a67f;             /* Green text color */
                font-family: Consolas;       /* Monospaced font */
                font-size: 12px;             /* Font size */
            }
        """)
        self.console.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.console.setMinimumSize(260, 100)  # Minimum width and height
        self.console.setMaximumSize(520, 200)  # Maximum width and height
        layout.addWidget(self.console)
        self.setLayout(layout)
    def log(self, message):
        formatted_message = f'<span style="color:#20a67f;">{message}</span>'  # Green text
        self.console.append(formatted_message)
    def alert(self, message):
        formatted_message = f'<span style="color:#ee3140;">{message}</span>'  # Red text
        self.console.append(formatted_message)
    def notify(self, message):
        formatted_message = f'<span style="color:#e69629;">{message}</span>'  # Yellow text
        self.console.append(formatted_message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConsoleWidget()
    window.show()
    sys.exit(app.exec())