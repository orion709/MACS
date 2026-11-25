import asyncio

from .SessionControl import (
    create_ssh_session,
    create_process,
    close_ssh_session,
    reconnect_ssh,
)


class SshMACS:
    def __init__(self):
        self._live_connections = {}
        self._tasks = {}
        self._creating = set()

    async def create_session(
        self,
        ip,
        port,
        name,
        password,
        keytxt,
        conf_id,
        session_name,
    ):
        session_id = session_name if session_name is not None else conf_id

        if session_id is None:
            raise ValueError("Не указан идентификатор сессии")

        if (
            session_id in self._live_connections
            or session_id in self._creating
        ):
            raise ValueError("Сессия уже существует")

        self._creating.add(session_id)
        conn = None

        try:
            conn = await create_ssh_session(
                ip, port, name, password, keytxt
            )

            process = await create_process(conn)

            self._live_connections[session_id] = {
                "conf_id": conf_id,
                "conn": conn,
                "windows": [process],
                "status": "connected",
            }

            task = asyncio.create_task(
                reconnect_ssh(
                    self,
                    session_id,
                    ip,
                    port,
                    name,
                    password,
                    keytxt,
                )
            )

            self._tasks[session_id] = task
            return True

        except BaseException:
            if conn is not None:
                await close_ssh_session(conn)
            raise

        finally:
            self._creating.discard(session_id)

    async def close_session(self, session_name):
        session = self._live_connections.pop(
            session_name, None
        )

        task = self._tasks.pop(session_name, None)

        if task is not None:
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

        if session is None:
            return False

        conn = session["conn"]

        if conn is not None:
            await close_ssh_session(conn)

        session["status"] = "closed"
        session["windows"].clear()

        return True

    async def send_input(self, session_name, data, window=0):
        session = self._live_connections[session_name]

        if session["status"] != "connected":
            raise ConnectionError("SSH-сессия не подключена")

        process = session["windows"][window]

        if isinstance(data, str):
            data = data.encode("utf-8")

        process.stdin.write(data)
        await process.stdin.drain()

    async def read_output(
        self,
        session_name,
        window=0,
        size=4096,
    ):
        session = self._live_connections[session_name]

        if session["status"] != "connected":
            raise ConnectionError("SSH-сессия не подключена")

        process = session["windows"][window]

        return await process.stdout.read(size)

    def get_session(self, session_name):
        return self._live_connections.get(session_name)

    def get_sessions(self):
        return {
            session_id: {
                "conf_id": session["conf_id"],
                "status": session["status"],
                "windows": len(session["windows"]),
            }
            for session_id, session in self._live_connections.items()
        }

    async def close_all(self):
        for session_id in list(self._live_connections):
            await self.close_session(session_id)
