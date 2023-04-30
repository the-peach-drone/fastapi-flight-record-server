from fastapi           import APIRouter, HTTPException
from loguru            import logger
from core.config       import Settings
from db.crud           import get_Record_Serial
from db.connector      import con_DB

# FastAPI Router
router = APIRouter()

# Server Setting
settings = Settings()

# Get Record Serial
@router.get("/get_serial")
async def getSerial():
    # DB connect
    try:
        connector = con_DB()
        serial_List = get_Record_Serial(connector)
    except Exception as err:
        logger.error(str(err))
        raise HTTPException(status_code = 503, detail="DB Connection Fail.")
    finally:
        connector.close()

    return serial_List
