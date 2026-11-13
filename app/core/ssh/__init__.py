import asyncio

from .SessionControl import close_ssh_session, create_ssh_BEGINsession

class SshMACS():
    def __init__(self):
        self._live_connections = {}
        self._tasks = {}
        # {conf_id: [conn; [windowslist]}

    async def create_session(self, ip, port, name, password, keytxt, conf_id, session_name):
        task = asyncio.create_task(create_ssh_BEGINsession(self, ip, port, name, password, keytxt, conf_id, session_name))
        self._tasks[conf_id] = task
        return True



    async def close_session(self, session_name):
        return await close_ssh_session(session_name)