from loguru       import logger
from core.config  import Settings

import time, threading, queue
import io, os, json, csv, requests

# Database import
from sqlalchemy import exc
from db import crud, models, schemas
from db.database import SessionLocal, engine

# Generate database schema
models.Base.metadata.create_all(bind=engine)

# Server Setting
settings = Settings()

# Data processing thread(Singleton)
class threadQueue(threading.Thread):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        super().__init__()
        self.data_Queue = queue.Queue()
        self.event = threading.Event()

    def run(self, *args, **kwargs):
        while True:
            time.sleep(0.01)
            if(self.event.is_set()):
                if(self.data_Queue.empty()):
                    return
            if(not self.data_Queue.empty()):
                data = self.data_Queue.get()
                self.__process_Data(data[0], data[1], data[2])

    def insert_Queue(self, user: str, time: str, record: bytes):
        self.data_Queue.put([user, time, record])

    def __process_Data(self, user: str, time: str, byte: bytes):
        file_CSV_Name = user + "-" + time + ".csv"
        file_CSV_Path  = os.path.join(settings.CSV_DIR_PATH, file_CSV_Name)

        file_JSON_Name = user + "-" + time + ".json"
        file_JSON_Path = os.path.join(settings.JSON_DIR_PATH, file_JSON_Name)

        # csv data decode
        record = byte.decode('utf-8')
        csv_data = io.StringIO(record)

        # Save flight record(CSV)
        try:
            with open(file_CSV_Path, "w+") as csv_File:
                csv_File.write(record)
        except Exception as err:
            logger.exception(f"Upload CSV from {user} => " + str(err))

        # Convert csv to list
        try:
            csvToList = []
            for csvRows in csv.DictReader(csv_data):
                csvToList.append(csvRows)
        except Exception as err:
            logger.exception(f"Upload CSV from {user} => " + str(err))

        # Make response json body
        try:
            output_Json = { 'serial_id' : user, 'flight_record' : csvToList }
            output_Object = json.dumps(output_Json, indent = 4, ensure_ascii = True)
        except Exception as err:
            logger.exception(f"Make json from {user} => " + str(err))
        
        # Save flight record(JSON)
        try:
            with open(file_JSON_Path, 'w+', encoding = 'UTF-8') as json_File:
                json_File.write(output_Object)
        except Exception as err:
            logger.exception(f"Upload CSV from {user} => " + str(err))

        # Insert DB
        try:
            db = SessionLocal()
            crud.create_record(db, schemas.Record(serial=user, incomming_time=time, fileName=file_JSON_Name))
        except exc.SQLAlchemyError as err:
            logger.critical(f"Upload CSV from {user} => Insert DB Fail. [{user}|{file_JSON_Name}]" + str(err))
        finally:
            db.close()
        
        # Python Requests module send POST
        response = requests.post(settings.POST_URL, json=output_Json)

        # POST response code check
        if not response.ok:
            logger.error(f"HTTP POST to Web Service({user}) => Fail...." + str(response.status_code) + response.text)
        else:
            res_Json_Body = response.json()
            if(res_Json_Body['error'] == ''):
                logger.info(response.text)
                logger.success(f"HTTP POST to Web Service({user}) => Success....")
            else:
                logger.error(f"HTTP POST to Web Service({user}) => Fail...." + res_Json_Body['error'])

        logger.success(f"Upload CSV from {user} => Success....")
