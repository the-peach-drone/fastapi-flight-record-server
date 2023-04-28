from pydantic import BaseSettings
import os, json, __main__

class Settings(BaseSettings):
    # Main Path
    # MAIN_PATH     = os.path.dirname(os.path.realpath(__main__.__file__))
    # TODO : refactoring main path set
    MAIN_PATH = ""

    # Json config
    config_Path = os.path.join(MAIN_PATH, "core", "config.json")
    config      = json.load(open(config_Path))

    # Path Setting
    LOG_PATH      = os.path.join(MAIN_PATH,    "log")
    LOG_FILENAME  = os.path.join(LOG_PATH,     "FileServer.log")
    STORAGE_PATH  = os.path.join(MAIN_PATH,    "storage")
    JSON_DIR_PATH = os.path.join(STORAGE_PATH, "flight_json")
    CSV_DIR_PATH  = os.path.join(STORAGE_PATH, "flight_csv")

    # DB Setting
    DB_HOST  = config["db_host"]
    DB_USER  = config["db_user"]
    DB_PASS  = config["db_pass"]
    DB_PORT  = config["db_port"]
    DB_NAME  = config["db_name"]
    DB_TABLE = config["db_table"]

    # POST URL Setting
    POST_URL = config["api_url"]

    # POST TEST MODE
    SERVER_TEST_MODE = config["test_mode"]

    def setMainPath(self, path:str):
        self.MAIN_PATH = path
