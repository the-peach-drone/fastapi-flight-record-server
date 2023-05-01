from pydantic import BaseSettings
from pathlib  import Path
import os, __main__

class Settings(BaseSettings):
    # Singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        super().__init__()
        # Get parent dir path
        pathList = os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)
        pathList.pop()
        self.MAIN_PATH = os.path.join("/", *pathList)
    
    # Main Path
    MAIN_PATH = ""

    # Path Setting
    LOG_PATH      = os.path.join(MAIN_PATH,    "log")
    LOG_FILENAME  = os.path.join(LOG_PATH,     "FileServer.log")
    STORAGE_PATH  = os.path.join(MAIN_PATH,    "storage")
    JSON_DIR_PATH = os.path.join(STORAGE_PATH, "flight_json")
    CSV_DIR_PATH  = os.path.join(STORAGE_PATH, "flight_csv")

    # DB Setting
    DB_HOST  = os.environ.get('MARIADBHOST', 'localhost')
    DB_USER  = os.environ.get('MARIADBUSER', 'USER')
    DB_PASS  = os.environ.get('MARIADBPASS', 'PASS')
    DB_PORT  = os.environ.get('MARIADBPORT',  3306)
    DB_NAME  = os.environ.get('MARIADBNAME',  'DB_NAME')
    DB_TABLE = os.environ.get('MARIADBTABLE', 'DB_TABLE_NAME')

    # POST URL Setting
    POST_URL = os.environ.get('WEBAPIENDPOINT', 'API_URI')

    # POST TEST MODE
    SERVER_TEST_MODE = os.environ.get('APISERVERTEST', True)