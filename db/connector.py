from loguru import logger
import sqlite3
import core.config as Config

settings = Config.Settings()

def con_DB():
    # DB connect
    try:
        connector = sqlite3.connect(settings.DB_PATH)
        connector.execute("PRAGMA cache_size=10000")
    except Exception as err:
        logger.error(str(err))

    return connector
