from loguru      import logger
from core.config import Settings

import pymysql

# Server Setting
settings = Settings()

def con_DB():
    # DB connect
    try:
        connector = pymysql.connect(host=settings.DB_HOST,
                                    user=settings.DB_USER,
                                    password=settings.DB_PASS,
                                    db=settings.DB_NAME,
                                    charset='utf8')
    except Exception as err:
        logger.error(str(err))

    return connector
