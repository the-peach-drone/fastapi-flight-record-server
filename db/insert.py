from loguru       import logger
from core.config  import Settings
from db.connector import con_DB

# Server Setting
settings = Settings()

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
        con = con_DB()
        con.execute(sql_Create)
        con.commit()
        con.close()
    except Exception as err:
        logger.error(str(err))
        return False

    return True
