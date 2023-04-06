from fastapi  import APIRouter, File, UploadFile, HTTPException
from datetime import datetime

import csv as CSV
import os, json, logging

import DB.flight_DB as Database
import CONFIG.ServerConfig as Config

# Logger
fileLogger = logging.getLogger('ServerFileLog')

# FastAPI Router
router = APIRouter()
settings = Config.Settings()

# FastAPI Server Method
@router.post("/upload_csv/{user}")
async def csvUpload(user, csv: UploadFile = File(...)):
    # Check Filename
    if csv.filename == '':
        fileLogger.error(f"{user} => File Name Missing.")
        raise HTTPException(status_code = 400, detail="File Name Missing.")
    
    # Check CSV
    if (not csv.filename.endswith(".csv")) and (not csv.filename.endswith(".CSV")):
        fileLogger.error(f"{user} => Not CSV File.")
        raise HTTPException(status_code = 400, detail="Not CSV File.")

    # Generate File Name
    file_Time = datetime.now().strftime('%Y%m%d%H%M%S')
    file_CSV = os.path.join(settings.CSV_PATH, user + "-" + file_Time + ".csv")
    file_JSON = os.path.join(settings.JSON_PATH, user + "-" + file_Time + ".json")

    # Save CSV
    try:
        with open(file_CSV, "wb+") as file_object:
            file_object.write(csv.file.read())
    except Exception as err:
        fileLogger.critical(f"{user} => " + str(err))
        raise HTTPException(status_code = 400, detail="Error in save CSV")

    # CSV convert to JSON
    csvTodict = []
    try:
        with open(file_CSV, 'rt', encoding='UTF-8') as data_csv:
            csv_reader = CSV.DictReader(data_csv)
            for csvRows in csv_reader:
                csvTodict.append(csvRows)
    except Exception as err:
        fileLogger.critical(f"{user} => "+ str(err))
        raise HTTPException(status_code = 400, detail="Error in convert JSON")

    # Make JSON Body
    coordMiddle_lat = csvTodict[int(len(csvTodict) / 2)]["latitude"]
    coordMiddle_lng = csvTodict[int(len(csvTodict) / 2)]["longitude"]
    output_Json = { 'serial_id' : user, 'incomming_time' : file_Time, 'middle_point' : { 'latitude' : coordMiddle_lat, 'longitude': coordMiddle_lng } ,'flight_record' :  csvTodict }

    # Insert Cache DB
    dbInserted = Database.insert_Flight_Record(user, file_Time, coordMiddle_lat, coordMiddle_lng, user + "-" + file_Time + ".json")
    if dbInserted != True:
        fileLogger.critical(f"{user} => Fail insert cache DB[{user} {file_Time} {coordMiddle_lat} {coordMiddle_lng} {user}-{file_Time}.json]. Please insert data later.")

    # Store to JSON
    try:
        with open(file_JSON, 'wt', encoding='UTF-8') as data_json:
            json_object = json.dumps(output_Json, indent = 4, ensure_ascii = True)
            data_json.write(json_object)
    except Exception as err:
        fileLogger.critical(f"{user} => " + str(err))
        raise HTTPException(status_code = 400, detail="Not CSV File.")
        
    # TODO : Send to another server
    
    fileLogger.info(f"{user} => Flight Record upload success.")
    return 'CSV upload and Convert JSON Success.'