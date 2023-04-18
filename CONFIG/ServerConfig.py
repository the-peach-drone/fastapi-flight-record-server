from pydantic import BaseSettings
import os, json, __main__

class Settings(BaseSettings):
    # Main Path
    MAIN_PATH     = os.path.dirname(os.path.realpath(__main__.__file__))

    # Json config
    config_Path = os.path.join(MAIN_PATH, "CONFIG", "config.json")
    config = json.load(open(config_Path))

    # DB Setting
    DB_NAME = config["db_name"]
    DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)), "Storage", DB_NAME)

    # Path Setting
    LOG_PATH      = os.path.join(MAIN_PATH,    "LOG")
    LOG_FILENAME  = os.path.join(LOG_PATH,     "FileServer.log")
    STORAGE_PATH  = os.path.join(MAIN_PATH,    "Storage")
    JSON_DIR_PATH = os.path.join(STORAGE_PATH, "JSON")
    CSV_DIR_PATH  = os.path.join(STORAGE_PATH, "CSV")

    # POST URL Setting
    POST_URL = config["api_url"]
