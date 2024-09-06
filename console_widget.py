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
        self.console.append(message)
class ConsoleLogger:
    def __init__(self, console_widget):
        self.console_widget = console_widget

    def write(self, message):
        if message.strip():  # Avoid logging empty messages
            self.console_widget.log(message)

    def flush(self):
        pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConsoleWidget()
    window.show()
    sys.exit(app.exec())