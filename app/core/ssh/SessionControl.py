import asyncio

import asyncssh

async def create_ssh_session(ip, port, name, password, keytxt):
    if keytxt:
        pkey = asyncssh.import_private_key(keytxt)
        conn = await asyncssh.connect(
            host=ip,
            port=port,
            username=name,
            client_keys=[pkey],
            known_hosts=None,
            connect_timeout=30,
            keepalive_count_max=2,
            keepalive_interval=15
        )
    else:
        conn = await asyncssh.connect(
            host=ip,
            port=port,
            username=name,
            password=password,
            known_hosts=None,
            connect_timeout=30,
            keepalive_count_max=2,
            keepalive_interval=15
        )
    return conn
    
async def reconnect_ssh(conn, ip, port, name, password, keytxt):
    while True:
        if await asyncssh.wait_close(conn):
            return await create_ssh_session(ip, port, name, password, keytxt)


async def close_ssh_session(session_name):
    pass


# ========================= processes =========================
async def create_process(conn):
    return await conn.create_process(
        term_type="xterm-256color",
        term_size=(80, 24),
        encoding=None
    )