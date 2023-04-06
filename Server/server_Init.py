import os, logging, logging.handlers
import DB.flight_DB as Database
import CONFIG.ServerConfig as Config

settings = Config.Settings()

LOG_FILENAME = os.path.join(settings.LOG_PATH, 'FileServer.log')

def set_Logger():
    # Check Log Directory
    if not os.path.exists(settings.LOG_PATH):
        try:
            os.makedirs(settings.LOG_PATH)
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
    if not os.path.exists(settings.STORAGE_PATH):
        # Try to make directory
        try:
            os.makedirs(settings.STORAGE_PATH)
            os.makedirs(settings.CSV_PATH)
            os.makedirs(settings.JSON_PATH)
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