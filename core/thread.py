from loguru      import logger
from core.config import Settings
from db.insert   import insert_Flight_Record

import time, threading, queue
import os, json, httpx, csv

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
        file_CSV_Path  = os.path.join(settings.CSV_DIR_PATH, user + "-" + time + ".csv")
        file_JSON_Path = os.path.join(settings.JSON_DIR_PATH, user + "-" + time + ".json")

        record = byte.decode('utf-8')

        # Save csv
        try:
            with open(file_CSV_Path, "w+") as csv_File:
                csv_File.write(record)
        except Exception as err:
            logger.exception(f"Upload CSV from {user} => " + str(err))

        # Convert csv to dict
        csvTodict = []
        try:
            with open(file_CSV_Path, 'rt', encoding='UTF-8') as csv_File:
                csv_reader = csv.DictReader(csv_File)
                for csvRows in csv_reader:
                    csvTodict.append(csvRows)
        except Exception as err:
            logger.exception(f"Upload CSV from {user} => " + str(err))

        # Make web routing json body
        try:
            coordMiddle_lat = csvTodict[int(len(csvTodict) / 2)]["latitude"]
            coordMiddle_lng = csvTodict[int(len(csvTodict) / 2)]["longitude"]
            output_Json = { 'serial_id' : user, 'incomming_time' : time, 'middle_point' : { 'latitude' : coordMiddle_lat, 'longitude': coordMiddle_lng } ,'flight_record' :  csvTodict }
        except Exception as err:
            logger.exception(f"Make json from {user} => " + str(err))

        # Insert Cache DB
        dbInserted = insert_Flight_Record(user, time, coordMiddle_lat, coordMiddle_lng, user + "-" + time + ".json")
        if not dbInserted:
            logger.critical(f"Upload CSV from {user} => Insert DB Fail. [{user}|{time}|{coordMiddle_lat}|{coordMiddle_lng}|{user}-{time}.json].")
        
        # Store flight record(JSON)
        json_object = None
        try:
            with open(file_JSON_Path, 'wt', encoding = 'UTF-8') as json_File:
                json_object = json.dumps(output_Json, indent = 4, ensure_ascii = True)
                json_File.write(json_object)
        except Exception as err:
            logger.exception(f"Upload CSV from {user} => " + str(err))

        # httpx send http post for call another api
        post_Result = httpx.post(settings.POST_URL, json = json.loads(json_object))
        if post_Result.status_code != httpx.codes.OK:
            logger.error(f"HTTP POST to Web Service({user}) => Fail...." + post_Result.text)
        else:
            response_Error = json.loads(post_Result.text)['error']
            if(response_Error == ''):
                logger.success(f"HTTP POST to Web Service({user}) => Success....")
            else:
                logger.error(f"HTTP POST to Web Service({user}) => Fail...." + response_Error)

        logger.success(f"Upload CSV from {user} => Success....")
