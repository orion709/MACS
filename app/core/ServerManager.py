import asyncio

from ssh import SshMACS
from sql import SqlMACS

class ServerManager():
    def __init__(self):
        self._ssh = SshMACS
        self._sql = SqlMACS
    
    # ===================================== SSH ==================================
    async def NewSession(self, ip=None, port=22, name=root, password=None, keytxt=None, conf_id=None, session_name=None):
        return self._ssh.create_session(ip, port, name, password, keytxt, conf_id, session_name)
    
    async def CloseSession(self, session_name):
        return self._ssh.close_session(session_name)
    
    # ====================================== SQL ===================================
    async def InitStorage(self):
        return self._sql.init_storage(self.SQLPassword)
