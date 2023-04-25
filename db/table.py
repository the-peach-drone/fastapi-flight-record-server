from loguru       import logger
from core.config  import Settings
from db.connector import con_DB

# Server Setting
settings = Settings()

def check_Table():
    sql_Check = """
                    SELECT COUNT(*) 
                    FROM information_schema.TABLES 
                    WHERE 
                        TABLE_SCHEMA = "{}" 
                        AND TABLE_NAME = "{}"
                """.format(settings.DB_NAME, settings.DB_TABLE)
    try:
        con    = con_DB()
        cursor = con.cursor()
        cursor.execute(sql_Check)
        result = cursor.fetchone()
    except Exception as err:
        logger.error(str(err))
        return False
    finally:
        con.close()
    
    if result[0] == 1:
        return True
    else:
        return False

def create_Table():
    sql_Create = """
                    CREATE TABLE {} (
                        id             integer primary key auto_increment,
                        serial         text    not null,
                        incomming_time text    not null,
                        mid_lat        text    not null, 
                        mid_lng        text    not null,
                        flieName       text    not null
                    )
                 """.format(settings.DB_TABLE)
    try:
        con = con_DB()
        cursor = con.cursor()
        cursor.execute(sql_Create)
    except Exception as err:
        logger.error(str(err))
        return False
    finally:
        con.close()
    
    return True
