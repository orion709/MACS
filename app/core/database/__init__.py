import asyncio

from .startbase import initBD, startBD
from .server import add_server_sql, del_server_sql, get_server_sql

class SqlMACS():
    def __init__(self):
        self.password = None
        self._session = None
    
    async def init_storage(self):
        if await initBD():
            return True
    
    async def start_storage(self, bd_password):
        if bd_password:
            self.password = bd_password
        self._session = await startBD(self.password)
        return True

    async def add_server(self, title, ip, port, servname, password, keypath, keytxt): #не перепутаны
        #conf_id
        return await add_server_sql(self._session, title, ip, port, servname, password, keytxt, keypath)

    async def del_server(self, conf_id):
        #True False
        return await del_server_sql(self._session, conf_id)

    async def get_server(self, conf_id, is_one):
        #dick or list of dicks lol
        return await get_server_sql(self._session, conf_id, is_one)
