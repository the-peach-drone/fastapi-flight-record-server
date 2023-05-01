from core.logger import CustomizeLogger
from db.table    import check_Table
from db.table    import create_Table
from core.config import Settings

import os, sys

# Server Setting
settings = Settings()

def init_Server():
    # Logger set
    config_path = os.path.join(settings.MAIN_PATH, "core", "logger_config.json")
    logger = CustomizeLogger.make_logger(config_path)

    # Python Version Check
    logger.info("Python version check... => " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro))
    if sys.version_info.major < 3: # Python 2
        logger.error("Please use Python 3.8 over")
        return False
    if sys.version_info.minor < 8: # Under Python 3.8
        logger.error("Please use Python 3.8 over")
        return False
    
    # if not exists log dir, make dir
    if not os.path.exists(settings.LOG_PATH): # Check Log Directory
        try:
            os.makedirs(settings.LOG_PATH)
        except OSError as err:
            logger.exception(f"Error in creating log directory. - {err}")
            return False

    # if not exists storage dir, make dir
    if not os.path.exists(settings.STORAGE_PATH):
        # Try to make directory
        try:
            os.makedirs(settings.STORAGE_PATH)
            os.makedirs(settings.CSV_DIR_PATH)
            os.makedirs(settings.JSON_DIR_PATH)
        except OSError as err:
            logger.exception(f"Error in creating directory. - {err}")
            return False
    
    if not os.path.exists(settings.CSV_DIR_PATH):
        # Try to make directory
        try:
            os.makedirs(settings.CSV_DIR_PATH)
        except OSError as err:
            logger.exception(f"Error in creating directory. - {err}")
            return False
    
    if not os.path.exists(settings.JSON_DIR_PATH):
        # Try to make directory
        try:
            os.makedirs(settings.JSON_DIR_PATH)
        except OSError as err:
            logger.exception(f"Error in creating directory. - {err}")
            return False

    # DB Init(Table Check)
    logger.info("Check Flight Cache Table...")
    if check_Table() == False:
        logger.error("Flight Cache Table not exist. Attemp to create table.")
        dbCreated = create_Table()
        if dbCreated != True:
            logger.critical("Flight Cache Table create fail.")
            return False
        else:
            logger.success("Flight Cache Table create success.")
            return True
    else:
        logger.success("Flight Cache Table check success.")
        return True
