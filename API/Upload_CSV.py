from fastapi  import APIRouter, File, UploadFile, HTTPException
from datetime import datetime
from loguru   import logger

import csv as CSV
import os, json, httpx

import DB.flight_DB as Database
import CONFIG.ServerConfig as Config

# FastAPI Router
router = APIRouter()

# Server Setting
settings = Config.Settings()

# FastAPI Server Method
@router.post("/upload_csv/{user}")
async def csvUpload(user, csv: UploadFile = File(...)):
    # Check Filename
    if csv.filename == '':
        logger.error(f"Upload CSV from {user} => File Name Missing.")
        raise HTTPException(status_code = 400, detail="File Name Missing.")
    
    # Check CSV
    if (not csv.filename.endswith(".csv")) and (not csv.filename.endswith(".CSV")):
        logger.error(f"Upload CSV from {user} => Not CSV File.")
        raise HTTPException(status_code = 400, detail="Not CSV File.")

    # Generate File Path
    file_Time      = datetime.now().strftime('%Y%m%d%H%M%S')
    file_CSV_Path  = os.path.join(settings.CSV_DIR_PATH, user + "-" + file_Time + ".csv")
    file_JSON_Path = os.path.join(settings.JSON_DIR_PATH, user + "-" + file_Time + ".json")

    # Save CSV
    try:
        with open(file_CSV_Path, "wb+") as file_object:
            file_object.write(csv.file.read())
    except Exception as err:
        logger.error(f"Upload CSV from {user} => " + str(err))
        raise HTTPException(status_code = 400, detail="Error in save CSV")

    # CSV convert to JSON
    csvTodict = []
    try:
        with open(file_CSV_Path, 'rt', encoding='UTF-8') as data_csv:
            csv_reader = CSV.DictReader(data_csv)
            for csvRows in csv_reader:
                csvTodict.append(csvRows)
    except Exception as err:
        logger.error(f"Upload CSV from {user} => " + str(err))
        raise HTTPException(status_code = 400, detail="Error in convert JSON")

    # Make JSON Body
    coordMiddle_lat = csvTodict[int(len(csvTodict) / 2)]["latitude"]
    coordMiddle_lng = csvTodict[int(len(csvTodict) / 2)]["longitude"]
    output_Json = { 'serial_id' : user, 'incomming_time' : file_Time, 'middle_point' : { 'latitude' : coordMiddle_lat, 'longitude': coordMiddle_lng } ,'flight_record' :  csvTodict }

    # Insert Cache DB
    dbInserted = Database.insert_Flight_Record(user, file_Time, coordMiddle_lat, coordMiddle_lng, user + "-" + file_Time + ".json")
    if dbInserted != True:
        logger.critical(f"Upload CSV from {user} => Insert DB Fail. [{user}|{file_Time}|{coordMiddle_lat}|{coordMiddle_lng}|{user}-{file_Time}.json].")

    # Store to JSON
    json_object = None
    try:
        with open(file_JSON_Path, 'wt', encoding='UTF-8') as data_json:
            json_object = json.dumps(output_Json, indent = 4, ensure_ascii = True)
            data_json.write(json_object)
    except Exception as err:
        logger.error(f"Upload CSV from {user} => " + str(err))
        raise HTTPException(status_code = 400, detail="Fail to store json.")
        
    # TODO : Send to another server
    post_Result = httpx.post(settings.POST_URL, json = json_object)
    if post_Result.status_code != httpx.codes.OK:
        logger.error(f"HTTP POST to Web Service => Fail..." + post_Result.text)
    else:
        logger.success(f"HTTP POST to Web Service => Success....")
    
    logger.success(f"Upload CSV from {user} => Success....")
    return 'CSV upload and Convert JSON Success.'