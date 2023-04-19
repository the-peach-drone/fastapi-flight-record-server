from loguru import logger

import core.config  as config
import db.connector as connector

settings = config.Settings()

def check_Table():
    sql_Check = """
                    SELECT COUNT(*) FROM sqlite_master Where name = "flightCache"
                """
    try:
        con = connector.con_DB()
        cursor = con.cursor()
        cursor.execute(sql_Check)
        result = cursor.fetchone()
    except Exception as err:
        logger.error(str(err))
        return False
    
    if result[0] == 1:
        return True
    else:
        return False

def create_Table():
    sql_Create = """
                    CREATE TABLE flightCache (
                        id             integer primary key,
                        serial         text    not null,
                        incomming_time text    not null,
                        mid_lat        text    not null, 
                        mid_lng        text    not null,
                        flieName       text    not null
                    )
                 """
    try:
        con = connector.con_DB()
        con.execute(sql_Create)
        con.close()
    except Exception as err:
        logger.error(str(err))
        return False
    
    return True
