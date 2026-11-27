import sys
import asyncio

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from app.core import ServerManager
from app.pyqt_src.gui import MainWindow


def main():
    print("1. Запуск", flush=True)

    app = QApplication(sys.argv)
    print("2. Qt работает", flush=True)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    print("3. Event loop создан", flush=True)

    manager = ServerManager()
    print("4. ServerManager создан", flush=True)

    with loop:
        print("5. Инициализация SQLite", flush=True)
        loop.run_until_complete(manager.InitStorage())

        print("6. Создание GUI", flush=True)
        window = MainWindow(manager)

        print("7. Показ окна", flush=True)
        window.show()

        print("8. Окно видимо:", window.isVisible(), flush=True)
        loop.create_task(window.load_servers())
        loop.run_forever()
        print("9. Event loop завершён", flush=True)


if __name__ == "__main__":
    main()