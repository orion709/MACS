import os
from pathlib import Path

import aiosqlite
#import cryptography
# шифрование для будущего

# ~/.local/share/macs/macs.db

DATA_HOME = Path(os.environ.get("XDE_DATA_HOME", Path.home() / ".local" / "share").expanduser())
DB_DIR = DATA_HOME / "MACS"
DB_PATH = DB_DIR / "MACS.sql"

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

async def initBD():
    DB_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    DB_DIR.chmod(0o700)

    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(schema)
        await db.commit()
    
    DB_PATH.chmod(0o600)

    return DB_PATH

async def startBD():
    db = await aiosqlite.connect(DB_PATH)
    await db.execute("PRAGMA foreign_key = ON")

    return db