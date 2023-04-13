from pydantic import BaseSettings
import os, __main__

class Settings(BaseSettings):
    # DB Setting
    DB_NAME = 'flightCache.db'
    DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)), "Storage", DB_NAME)

    # Path Setting
    MAIN_PATH     = os.path.dirname(os.path.realpath(__main__.__file__))
    LOG_PATH      = os.path.join(MAIN_PATH,    "LOG")
    LOG_FILENAME  = os.path.join(LOG_PATH,     "FileServer.log")
    STORAGE_PATH  = os.path.join(MAIN_PATH,    "Storage")
    JSON_DIR_PATH = os.path.join(STORAGE_PATH, "JSON")
    CSV_DIR_PATH  = os.path.join(STORAGE_PATH, "CSV")

    # POST URL Setting
    POST_URL = "http://127.0.0.1:11111/upload_json"
