from loguru       import logger
from core.config  import Settings
from db.connector import con_DB

# Server Setting
settings = Settings()

def insert_Flight_Record(serial: str, time: str, lat: str, lng: str, filename: str):    
    table_name = settings.DB_TABLE
    sql_Create = f"""
                    INSERT INTO {table_name} (serial, incomming_time, mid_lat, mid_lng, flieName) VALUES(
                        '{serial}',
                        '{time}',
                        '{lat}', 
                        '{lng}',
                        '{filename}'
                    )
                 """
    try:
        connector = con_DB()
        cursor = connector.cursor()
        cursor.execute(sql_Create)
        connector.commit()
    except Exception as err:
        logger.error(str(err))
        return False
    finally:
        connector.close()

    return True

def get_Record_Serial():
    table_name = settings.DB_TABLE
    sql_Get = f"""
                    SELECT DISTINCT serial
                    FROM {table_name}
               """
    try:
        connector = con_DB()
        cursor = connector.cursor()
        cursor.execute(sql_Get)
        result = [item[0] for item in cursor.fetchall()]
    except Exception as err:
        logger.error(str(err))
        return None
    finally:
        connector.close()
    
    return result
