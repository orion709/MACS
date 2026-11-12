import asyncio

from SessionControl import close_ssh_session, create_ssh_session

class SshMACS():
    def __init__(self):
        pass
    
    async def create_session(ip, port, name, password, keytxt, conf_id, session_name):
        return await create_ssh_session(ip, port, name, password, keytxt, conf_id, session_name)
    
    async def close_session(session_name):
        return await close_ssh_session(session_name)