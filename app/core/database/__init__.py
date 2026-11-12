import asyncio

from .startbase import initBD, startBD

class SqlMACS():
    def __init__(self):
        self.password = None
    
    async def init_storage(self):
        return await initBD()
    
    async def start_storage(self, bd_password):
        if bd_password:
            self.password = bd_password
        return await startBD(self.password)