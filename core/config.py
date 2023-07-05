from pydantic import BaseSettings
import os, __main__

class Settings(BaseSettings):
    # Singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        super().__init__()
    
    # Main Path
    MAIN_PATH = os.path.join("/", *os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[0:-1])

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
    DB_PORT  = os.environ.get('MARIADBPORT', '3306')

    # POST URL Setting
    POST_URL = os.environ.get('WEBAPIENDPOINT', 'API_URI')