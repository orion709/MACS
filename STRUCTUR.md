macs/
├── main.py                     # точка входа: QApplication + qasync + MainWindow
├── requirements.txt
├── pyproject.toml
├── README.md
├── .gitignore
│
├── app/
│   ├── __init__.py
│   ├── config.py               # пути, константы, версия, env
│   │
│   ├── core/                   # ⭐ ЯДРО — pure Python, никакого PyQt
│   │   ├── __init__.py
│   │   ├── events.py           # EventBus / сигналы (см. ниже про pyqtSignal)
│   │   ├── entities.py         # dataclass: Server, Credential, TabState, CommandTemplate
│   │   │
│   │   ├── ssh/
│   │   │   ├── __init__.py
│   │   │   ├── session.py      # SSHSession — одно TCP-соединение
│   │   │   ├── channel.py      # SSHChannel — независимый терминал (cat, tail, htop…)
│   │   │   ├── pool.py         # SessionPool: {server_id → SSHSession}
│   │   │   └── keys.py         # генерация пары ключей + автодеплой на сервер
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py     # aiosqlite connection, миграции
│   │   │   ├── schema.sql
│   │   │   └── repositories/
│   │   │       ├── __init__.py
│   │   │       ├── servers.py
│   │   │       ├── tabs.py
│   │   │       └── templates.py
│   │   │
│   │   └── security/
│   │       ├── __init__.py
│   │       ├── crypto.py       # AES через cryptography
│   │       └── keyring.py      # мастер-пароль / OS keychain
│   │
│   ├── models/                 # Qt-адаптеры над core (тонкие, без логики)
│   │   ├── __init__.py
│   │   ├── server_model.py     # QAbstractListModel → core.db.repositories.servers
│   │   ├── terminal_model.py   # для terminal widget
│   │   └── tab_model.py
│   │
│   ├── views/                  # GUI (PyQt6)
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   ├── server_list.py        # QListView + collapsible
│   │   │   ├── terminal.py           # ANSI-рендер (htop/btop)
│   │   │   ├── tabs.py               # QTabWidget
│   │   │   └── collapsible_panel.py
│   │   └── dialogs/
│   │       ├── __init__.py
│   │       ├── add_server.py
│   │       └── master_password.py
│   │
│   ├── controllers/            # перехват UI → вызовы core
│   │   ├── __init__.py
│   │   ├── main_controller.py
│   │   ├── server_controller.py
│   │   ├── terminal_controller.py
│   │   └── tab_controller.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── ansi.py             # парсер ANSI escape → rich text / цвета
│       └── logging.py
│
└── tests/
    ├── test_core/
    │   ├── test_ssh.py
    │   ├── test_crypto.py
    │   └── test_repositories.py
    ├── test_models/
    └── test_controllers/