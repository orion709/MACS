import asyncio

import asyncssh

async def create_ssh_BEGINsession(manager, ip, port, name, password, keytxt, conf_id, session_name):
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
    main_wind = await conn.create_process(
        term_type="xterm-256color",
        term_size=(80, 24),
        encoding=None
    )
    manager._live_connections[conf_id] = [conn, [main_wind], True]
    await asyncssh.wait_closed(conn)
    if manager._live_connections[conf_id][3]:
        return await create_ssh_session(ip, port, name, password, keytxt)

# async def reconnect_ssh(conn, ip, port, name, password, keytxt):
#     await asyncssh.wait_closed(conn)
#     return await create_ssh_session(ip, port, name, password, keytxt)


async def close_ssh_session(session_name):
    pass


# ========================= processes =========================
# async def create_process(conn):
#     return await conn.create_process(
#         term_type="xterm-256color",
#         term_size=(80, 24),
#         encoding=None
#     )