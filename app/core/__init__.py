import asyncio

from .ssh import SshMACS
from .database import SqlMACS

class ServerManager():
    def __init__(self):
        self._ssh = SshMACS()
        self._sql = SqlMACS()
    
    # ===================================== SSH ==================================
    async def NewSession(self, ip=None, port=22, name="root", password=None, keytxt=None, conf_id=None, session_name=None):
        return await self._ssh.create_session(ip, port, name, password, keytxt, conf_id, session_name)
    
    async def CloseSession(self, session_name):
        return await self._ssh.close_session(session_name)
    
    # ====================================== SQL ===================================
    async def InitStorage(self): #noReturn
        await self._sql.init_storage(), await self._sql.start_storage()
    
    async def CloseStorage(self):
        return await self._sql.close_storage()

    async def AddServer(self, title, ip, port, servname, password, keypath, keytxt):
        return await self._sql.add_server(title, ip, port, servname, password, keypath, keytxt)
    
    async def DelServer(self, conf_id):
        return await self._sql.del_server(conf_id)
    
    async def GetServer(self, conf_id, is_one):
        return await self._sql.get_server(conf_id, is_one)
    
    async def UpdServer(self, conf_id, updates):
        return await self._sql.update_server(conf_id, updates)