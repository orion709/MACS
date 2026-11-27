import re

from PyQt6.QtWidgets import QPlainTextEdit, QLineEdit, QVBoxLayout, QWidget


ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


class Terminal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.output.setStyleSheet(
            "QPlainTextEdit { background: #101318; color: #d8dee9; "
            "font: 13px monospace; }"
        )
        layout.addWidget(self.output, 1)

        self.command = QLineEdit()
        self.command.setPlaceholderText("Команда...")
        self.command.setEnabled(False)
        layout.addWidget(self.command)

    def print_text(self, text):
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(ANSI.sub("", text))
        self.output.setTextCursor(cursor)

    def clear(self):
        self.output.clear()
