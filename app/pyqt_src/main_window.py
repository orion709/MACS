import asyncio

from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QLineEdit, QMainWindow,
    QMenu, QMessageBox, QToolButton, QVBoxLayout, QWidget
)

from .dialogs import AddServer, ask_password, open_dialog
from .terminal import Terminal


class MainWindow(QMainWindow):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.current_id = None
        self.reader_task = None
        self.work_tasks = set()
        self.busy = False
        self.closing = False

        self.setWindowTitle("MACS")
        self.resize(960, 620)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        top = QHBoxLayout()

        self.server_menu = QMenu(self)
        self.server_button = QToolButton()
        self.server_button.setText("Серверы")
        self.server_button.setMenu(self.server_menu)
        self.server_button.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

        self.status = QLineEdit("Disconnected")
        self.status.setReadOnly(True)
        self.status.setMaximumWidth(145)

        top.addWidget(self.server_button)
        top.addStretch()
        top.addWidget(self.status)
        layout.addLayout(top)

        self.terminal = Terminal(self)
        self.terminal.command.returnPressed.connect(self.send_command)
        layout.addWidget(self.terminal, 1)

    def run_task(self, coro):
        task = asyncio.create_task(coro)
        self.work_tasks.add(task)
        task.add_done_callback(self.work_tasks.discard)
        return task

    async def load_servers(self):
        if self.closing:
            return

        self.server_menu.clear()

        try:
            servers = await self.manager.GetServer(None, False)

            for server in servers:
                conf_id = server["CONFIG_ID"]
                action = self.server_menu.addAction(server["TITLE"])
                action.triggered.connect(
                    lambda checked=False, sid=conf_id:
                    self.run_task(self.connect_server(sid))
                )
        except Exception as exc:
            self.terminal.print_text(f"Ошибка БД: {exc}\n")

        self.server_menu.addSeparator()
        action = self.server_menu.addAction("+ Добавить сервер")
        action.triggered.connect(
            lambda: self.run_task(self.add_server())
        )

    async def add_server(self):
        if self.busy or self.closing:
            return

        dialog = AddServer(self)
        if await open_dialog(dialog) != dialog.DialogCode.Accepted:
            return

        title, ip, port, username = dialog.values()

        if not all((title, ip, username)):
            QMessageBox.warning(self, "Ошибка", "Заполни все поля")
            return

        try:
            conf_id = await self.manager.SaveServer(
                title, ip, port, username
            )
            await self.load_servers()
            await self.connect_server(conf_id)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if not self.closing:
                QMessageBox.critical(self, "Ошибка", str(exc))

    async def stop_reader(self):
        task = self.reader_task
        self.reader_task = None

        if task is None:
            return

        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    async def connect_server(self, conf_id):
        if self.busy or self.closing:
            return

        self.busy = True
        self.server_button.setEnabled(False)
        self.terminal.command.setEnabled(False)

        try:
            password, accepted = await ask_password(self)

            if not accepted or self.closing:
                return

            await self.stop_reader()

            if self.current_id is not None:
                await self.manager.CloseSession("main")
                self.current_id = None

            self.status.setText("Connecting")
            self.terminal.clear()

            await self.manager.ConnectSavedServer(
                conf_id, password or None
            )

            self.current_id = conf_id
            self.status.setText("Connected")
            self.terminal.command.setEnabled(True)
            self.terminal.command.setFocus()

            self.reader_task = asyncio.create_task(
                self.read_terminal(conf_id)
            )

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.status.setText("Error")
            if not self.closing:
                QMessageBox.critical(self, "SSH", str(exc))
        finally:
            self.busy = False
            if not self.closing:
                self.server_button.setEnabled(True)

    async def read_terminal(self, conf_id):
        old_process = None

        while not self.closing and self.current_id == conf_id:
            session = self.manager.GetSession()

            if session is None:
                break

            state = session["status"]
            self.status.setText(state.capitalize())

            if state != "connected" or not session["windows"]:
                self.terminal.command.setEnabled(False)
                old_process = None
                await asyncio.sleep(0.2)
                continue

            process = session["windows"][0]

            if process is not old_process:
                old_process = process
                self.terminal.command.setEnabled(True)
                self.terminal.print_text("\n[SSH connected]\n")

            try:
                data = await asyncio.wait_for(
                    process.stdout.read(4096), timeout=0.4
                )
                if data:
                    self.terminal.print_text(
                        data.decode("utf-8", errors="replace")
                    )
                else:
                    await asyncio.sleep(0.2)
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                self.terminal.print_text(
                    f"\nОшибка чтения: {exc}\n"
                )
                await asyncio.sleep(0.5)

    def send_command(self):
        text = self.terminal.command.text()

        if not text or self.current_id is None:
            return

        self.terminal.command.clear()
        self.run_task(self.send_input(text))

    async def send_input(self, text):
        try:
            await self.manager._ssh.send_input("main", text + "\n")
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.terminal.print_text(f"\nОшибка ввода: {exc}\n")

    async def shutdown(self):
        try:
            await self.stop_reader()

            for task in list(self.work_tasks):
                task.cancel()

            await asyncio.gather(
                *self.work_tasks, return_exceptions=True
            )
            await self.manager._ssh.close_all()
            await self.manager.CloseStorage()
        finally:
            QApplication.instance().quit()

    def closeEvent(self, event):
        event.ignore()

        if self.closing:
            return

        self.closing = True
        self.setEnabled(False)
        asyncio.create_task(self.shutdown())
