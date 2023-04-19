from loguru import logger

import core.config  as config
import db.connector as connector

settings = config.Settings()

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
        con = connector.con_DB()
        con.execute(sql_Create)
        con.commit()
        con.close()
    except Exception as err:
        logger.error(str(err))
        return False

    return True
