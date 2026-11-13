import asyncio

from .SessionControl import close_ssh_session, create_ssh_BEGINsession, create_process, reconnect_ssh

class SshMACS():
    def __init__(self):
        self._live_connections = {}
        # {conf_id: [conn; [windowslist]}

    async def create_session(self, ip, port, name, password, keytxt, conf_id, session_name):
        asyncio.create_task(await create_ssh_BEGINsession(self, ip, port, name, password, keytxt, conf_id, session_name))
        return True



    async def close_session(self, session_name):
        return await close_ssh_session(session_name)