import asyncio
import aiosqlite

async def add_server_sql(session, title, ip, port, servername, password, keypath, key):
    async with session.execute(
        "INSERT INTO SERVERS (TITLE, SERVER_IP, SERVER_PORT, SERVER_NAME, SERVER_PASSWORD, SERVER_KEY_NAME, SERVER_KEY_FULL) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, ip, port, servername, password, keypath, key)
    ) as new_conf_id:
        conf_id = new_conf_id.lastrowid
    await session.commit()
    return conf_id
    
async def del_server_sql(session, conf_id):
    async with session.execute(
        "DELETE FROM SERVERS WHERE CONFIG_ID = ?",
        (conf_id,)
    ) as delserv:
        is_deleted = delserv.rowcount > 0
    await session.commit()
    return is_deleted        

async def get_server_sql(session, conf_id, one):
    if one:
        async with session.execute(
            "SELECT * FROM SERVERS WHERE CONFIG_ID = ?",
            (conf_id,)
        ) as cursor:
            try:
                return dict(await cursor.fetchone())
            except:
                return None
    else:
        async with session.execute("SELECT * FROM SERVERS") as cursor:
            return [dict(row) for row in await cursor.fetchall()]
