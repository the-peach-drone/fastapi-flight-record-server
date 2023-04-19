from loguru      import logger
from core.config import Settings

import sqlite3

# Server Setting
settings = Settings()

def con_DB():
    # DB connect
    try:
        connector = sqlite3.connect(settings.DB_PATH)
        connector.execute("PRAGMA cache_size=10000")
    except Exception as err:
        logger.error(str(err))

    return connector
