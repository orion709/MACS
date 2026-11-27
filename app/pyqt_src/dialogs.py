import asyncio

from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout,
    QInputDialog, QLineEdit, QSpinBox
)


async def open_dialog(dialog):
    result = asyncio.get_running_loop().create_future()

    def finished(code):
        if not result.done():
            result.set_result(code)

    dialog.finished.connect(finished)
    dialog.open()

    try:
        return await result
    finally:
        try:
            dialog.finished.disconnect(finished)
        except (TypeError, RuntimeError):
            pass


class AddServer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить сервер")

        self.title = QLineEdit()
        self.ip = QLineEdit()
        self.username = QLineEdit("root")

        self.port = QSpinBox()
        self.port.setRange(1, 65535)
        self.port.setValue(22)

        layout = QFormLayout(self)
        layout.addRow("Название", self.title)
        layout.addRow("IP / хост", self.ip)
        layout.addRow("Порт", self.port)
        layout.addRow("Логин", self.username)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def values(self):
        return (
            self.title.text().strip(),
            self.ip.text().strip(),
            self.port.value(),
            self.username.text().strip()
        )


async def ask_password(parent):
    dialog = QInputDialog(parent)
    dialog.setWindowTitle("SSH")
    dialog.setLabelText("Пароль (пусто для SSH-агента):")
    dialog.setTextEchoMode(QLineEdit.EchoMode.Password)

    if await open_dialog(dialog) != QDialog.DialogCode.Accepted:
        return None, False

    return dialog.textValue(), True
