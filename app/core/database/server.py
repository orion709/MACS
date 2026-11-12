import asyncio
import aiosqlite

async def add_server_sql(self, session, title, ip, port, servername, password, keypath, key):
    async with sessio.execute(
        "INSERT INTO SERVERS (TITLE, SERVER_IP, SERVER_PORT, SERVER_NAME, SERVER_PASSWORD, SERVER_KEY_PATH, SERVER_KEY_FULL) VALUES (?, ?, ?, ?, ?, ?, ?)"
        (title, ip, port, servername, password, keypath, key)
    ) as new_conf_id:
        conf_id = new_conf_id.lastrowid
    await session.commit()
    return conf_id
    
async def del_server_sql(self, session, conf_id):
    pass

async def get_server_sql(self, session, conf_id):
    pass