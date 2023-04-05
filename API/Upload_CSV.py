from fastapi  import APIRouter, File, UploadFile, HTTPException
from datetime import datetime

import csv as CSV
import os, json, __main__, logging

import DB.flight_DB as Database

# Logger
fileLogger = logging.getLogger('ServerFileLog')

# FastAPI Router
router = APIRouter()

JSON_DIR = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)), "Storage", "JSON")
CSV_DIR  = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)), "Storage", "CSV")

# FastAPI Server Method
@router.post("/upload_csv/{user}")
async def csvUpload(user, csv: UploadFile = File(...)):
    # Check Filename
    if csv.filename == '':
        fileLogger.error(f"{user} => Upload CSV - File Name Missing.")
        raise HTTPException(status_code = 400, detail="File Name Missing.")
    
    # Check CSV
    if (not csv.filename.endswith(".csv")) and (not csv.filename.endswith(".CSV")):
        fileLogger.error(f"{user} => Upload CSV - Not CSV File.")
        raise HTTPException(status_code = 400, detail="Not CSV File.")

    # Generate File Name
    file_Time = datetime.now().strftime('%Y%m%d%H%M%S')
    file_CSV = os.path.join(CSV_DIR, user + "-" + file_Time + ".csv")
    file_JSON = os.path.join(JSON_DIR, user + "-" + file_Time + ".json")

    # Save CSV
    try:
        with open(file_CSV, "wb+") as file_object:
            file_object.write(csv.file.read())
    except EnvironmentError as err:
        fileLogger.critical(f"{user} =>Upload CSV(CSV Save) - " + str(err))

    # CSV convert to JSON
    csvTodict = []
    try:
        with open(file_CSV, 'rt', encoding='UTF-8') as data_csv:
            csv_reader = CSV.DictReader(data_csv)
            for csvRows in csv_reader:
                csvTodict.append(csvRows)
    except EnvironmentError as err:
        fileLogger.critical(f"{user} => Upload CSV(CSV convert to JSON) - "+ str(err))

    # Make JSON Body
    coordMiddle_lat = csvTodict[int(len(csvTodict) / 2)]["latitude"]
    coordMiddle_lng = csvTodict[int(len(csvTodict) / 2)]["longitude"]
    output_Json = { 'serial_id' : user, 'incomming_time' : file_Time, 'middle_point' : { 'latitude' : coordMiddle_lat, 'longitude': coordMiddle_lng } ,'flight_record' :  csvTodict }

    Database.insert_Flight_Record(user, file_Time, coordMiddle_lat, coordMiddle_lng, user + "-" + file_Time + ".json")

    # Store to JSON
    try:
        with open(file_JSON, 'wt', encoding='UTF-8') as data_json:
            json_object = json.dumps(output_Json, indent = 4, ensure_ascii = True)
            data_json.write(json_object)
    except EnvironmentError as err:
        fileLogger.critical(f"{user} => Upload CSV(Save JSON) - " + str(err))
        
    # TODO : Send to another server
    
    fileLogger.info(f"{user} => Upload CSV - Flight Record upload success.")
    return 'CSV upload and Convert JSON Success.'