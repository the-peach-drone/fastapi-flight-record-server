from loguru import logger
from Server.custom_logger import CustomizeLogger
import os, sys, logging
import DB.flight_DB as Database
import CONFIG.ServerConfig as Config

settings = Config.Settings()

def init_Server():
    # Logger set
    config_path = os.path.join(settings.MAIN_PATH, "Server", "logging_config.json")
    logger = CustomizeLogger.make_logger(config_path)

    # Python Version Check
    logger.info("Python version check... => " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro))
    if sys.version_info.major < 3: # Python 2
        logger.error("Please use Python 3.8 over")
        return False
    if sys.version_info.minor < 8: # Under Python 3.8
        logger.error("Please use Python 3.8 over")
        return False
    
    # Logger Set
    if not os.path.exists(settings.LOG_PATH): # Check Log Directory
        try:
            os.makedirs(settings.LOG_PATH)
        except OSError as err:
            logger.critical(f"Error in creating log directory. - {err}")
            return False

    # Disable uvicorn logger
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_error.propagate = False
    uvicorn_access.propagate = False

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