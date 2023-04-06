from loguru import logger
import os, logging
import DB.flight_DB as Database
import CONFIG.ServerConfig as Config

settings = Config.Settings()

def init_Server():
    # Logger Set
    # Check Log Directory
    if not os.path.exists(settings.LOG_PATH):
        try:
            os.makedirs(settings.LOG_PATH)
        except OSError as err:
            logger.critical(f"Error in creating log directory. - {err}")
            return False
        
    # Disable uvicorn logger
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_error.disabled = True
    uvicorn_access.disabled = True

    # Loguru file handler add
    logger.add(sink=settings.LOG_FILENAME, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} - {message}", rotation="12:00")

    logger.info("Server Init Start...")

    # Upload Dir Check
    if not os.path.exists(settings.STORAGE_PATH):
        # Try to make directory
        try:
            os.makedirs(settings.STORAGE_PATH)
            os.makedirs(settings.CSV_DIR_PATH)
            os.makedirs(settings.JSON_DIR_PATH)
        except OSError as err:
            logger.error(f"Error in creating directory. - {err}")
            return False

    # DB Init(Table Check)
    logger.info("Check Flight Cache Table...")
    if Database.check_Table() == False:
        logger.error("Flight Cache Table not exist. Attemp to create table.")
        dbCreated = Database.create_Table()
        if dbCreated != True:
            logger.critical("Flight Cache Table create fail.")
            return False
        else:
            logger.success("Flight Cache Table create success.")
            return True
    else:
        logger.success("Flight Cache Table check success.")
        return True