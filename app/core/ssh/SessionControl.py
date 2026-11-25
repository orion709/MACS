import asyncio
import asyncssh


async def create_ssh_session(ip, port, name, password, keytxt):
    options = {
        "host": ip,
        "port": port,
        "username": name,
        "connect_timeout": 30,
        "keepalive_count_max": 2,
        "keepalive_interval": 15,
    }

    if keytxt:
        private_key = asyncssh.import_private_key(keytxt)
        options["client_keys"] = [private_key]
    else:
        options["password"] = password

    return await asyncssh.connect(**options)


async def create_process(conn):
    return await conn.create_process(
        term_type="xterm-256color",
        term_size=(80, 24),
        encoding=None,
    )


async def close_ssh_session(conn):
    if conn is None:
        return False

    conn.close()
    await conn.wait_closed()
    return True


async def reconnect_ssh(
    manager,
    session_id,
    ip,
    port,
    name,
    password,
    keytxt,
):
    session = manager._live_connections[session_id]

    while True:
        # Ожидаем разрыва текущего соединения.
        await session["conn"].wait_closed()

        session["status"] = "reconnecting"
        session["conn"] = None
        session["windows"] = []

        delay = 2

        while True:
            new_conn = None

            try:
                new_conn = await create_ssh_session(
                    ip, port, name, password, keytxt
                )

                new_process = await create_process(new_conn)

                session["conn"] = new_conn
                session["windows"] = [new_process]
                session["status"] = "connected"

                # Продолжаем следить за новым соединением.
                break

            except asyncio.CancelledError:
                if new_conn is not None:
                    new_conn.close()
                    await new_conn.wait_closed()
                raise

            except (OSError, asyncssh.Error, TimeoutError):
                if new_conn is not None:
                    new_conn.close()
                    await new_conn.wait_closed()

                await asyncio.sleep(delay)
                delay = min(delay * 2, 30)
