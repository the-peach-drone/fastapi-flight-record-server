from loguru import logger
import sqlite3
import core.ServerConfig as Config

settings = Config.Settings()

def con_DB():
    # DB connect
    try:
        connector = sqlite3.connect(settings.DB_PATH)
        connector.execute("PRAGMA cache_size=10000")
    except Exception as err:
        logger.error(str(err))

    return connector

def check_Table():
    sql_Check = """
                    SELECT COUNT(*) FROM sqlite_master Where name = "flightCache"
                """
    try:
        connector = con_DB()
        cursor = connector.cursor()
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
        connector = con_DB()
        connector.execute(sql_Create)
        connector.close()
    except Exception as err:
        logger.error(str(err))
        return False
    
    return True

def insert_Flight_Record(serial, time, lat, lng, filename):
    sql_Create = f"""
                    INSERT INTO flightCache (serial, incomming_time, mid_lat, mid_lng, flieName) VALUES(
                        '{serial}',
                        '{time}',
                        '{lat}', 
                        '{lng}',
                        '{filename}'
                    )
                 """
    try:
        connector = con_DB()
        connector.execute(sql_Create)
        connector.commit()
        connector.close()
    except Exception as err:
        logger.error(str(err))
        return False

    return True