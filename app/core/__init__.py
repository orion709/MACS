from ssh import SshMACS
from sql import SqlMACS

class InfoMACS():
    def __init__(self):
        self._ssh = SshMACS
        self._sql = SqlMACS
    
    def NewSession(self):
        return self._ssh.create_session()
    
    def CloseSession(self):
        return self._ssh.close_session()