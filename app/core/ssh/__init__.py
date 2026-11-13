import asyncio

from .SessionControl import close_ssh_session, create_ssh_session, create_process, reconnect_ssh

class SshMACS():
    def __init__(self):
        self.live_connections = {}

    async def create_session(self, ip, port, name, password, keytxt, conf_id, session_name):
        connect = await create_ssh_session(ip, port, name, password, keytxt)
        main_window = await create_process(connect)
        self._live_connections[conf_id] = [connect, [main_window]]
        # {conf_id: [conn; [windowslist]}
        reconnect = asyncio.create_task(reconnect_ssh(connect, ip, port, name, password, keytxt))
        return True



    async def close_session(self, session_name):
        return await close_ssh_session(session_name)