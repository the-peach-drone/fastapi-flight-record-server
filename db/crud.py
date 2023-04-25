from loguru       import logger
from core.config  import Settings

# Server Setting
settings = Settings()

def insert_Flight_Record(connector, serial: str, time: str, lat: str, lng: str, filename: str):
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
        cursor = connector.cursor()
        cursor.execute(sql_Create)
        connector.commit()
    except Exception as err:
        logger.error(str(err))
        return False

    return True
