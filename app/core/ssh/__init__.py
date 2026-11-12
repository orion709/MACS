import asyncio

from .SessionControl import close_ssh_session, create_ssh_session

class SshMACS():
    def __init__(self):
        self.live_connections = {}

    async def create_session(self, ip, port, name, password, keytxt, conf_id, session_name):
        connect = await create_ssh_session(ip, port, name, password, keytxt)
        pass
        self.live_connections[conf_id] = [connect, [windows]]
        # {conf_id: [conn; [window1]}



    async def close_session(self, session_name):
        return await close_ssh_session(session_name)