import os, sys, logging, logging.handlers, __main__

import DB.flight_DB as Database

MAIN_PATH = os.path.dirname(os.path.realpath(__main__.__file__))

LOG_PATH     = os.path.join(MAIN_PATH, "LOG")
STORAGE_PATH = os.path.join(MAIN_PATH, "Storage")
JSON_DIR     = os.path.join(STORAGE_PATH, "JSON")
CSV_DIR      = os.path.join(STORAGE_PATH, "CSV")

LOG_FILENAME = os.path.join(LOG_PATH, 'FileServer.log')

def set_Logger():
    # Check Log Directory
    if not os.path.exists(LOG_PATH):
        try:
            os.makedirs(LOG_PATH)
        except OSError:
            print("Error in creating dir")
            return
    
    # File Logger Set
    fileLogger = logging.getLogger('ServerFileLog')
    fileLogger.setLevel(logging.INFO)

    file_Handler = logging.handlers.TimedRotatingFileHandler(
        filename=LOG_FILENAME, when='midnight', interval=1, encoding='utf-8'
    )
    file_Handler.suffix = '%Y%m%d'

    fileLogger.addHandler(file_Handler)
    file_Formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s'
    )
    file_Handler.setFormatter(file_Formatter)

    fileLogger.info("Logger Setting Complete.")

def init_Server():
    # Logger Set
    set_Logger()
    fileLogger = logging.getLogger('ServerFileLog')

    # Upload Dir Check
    if not os.path.exists(STORAGE_PATH):
        # Try to make directory
        try:
            os.makedirs(STORAGE_PATH)
            os.makedirs(CSV_DIR)
            os.makedirs(JSON_DIR)
        except OSError:
            fileLogger.info("Error in creating directory.")

    # DB Init(Table Check)
    if Database.check_Table() == False:
        fileLogger.info("Flight Cache Table not exist. Attemp to create table.")
        dbCreated = Database.create_Table()
        if dbCreated != True:
            fileLogger.critical("Flight Cache Table create fail. Server Terminate.")
            return
        else:
            fileLogger.info("Flight Cache Table success.")
    else:
        fileLogger.info("Flight Cache Table exist.")