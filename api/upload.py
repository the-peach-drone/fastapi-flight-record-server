from fastapi           import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import PlainTextResponse
from datetime          import datetime
from loguru            import logger
from core.thread       import threadQueue

# FastAPI Router
router = APIRouter()

# Data processing thread
thread = threadQueue()

# Upload Flight record
@router.post("/upload_csv/{user}")
async def csvUpload(user, csv: UploadFile = File(...)):
    # Check Filename
    if csv.filename == '':
        logger.error(f"Upload CSV from {user} => File Name Missing.")
        raise HTTPException(status_code = 400, detail="File Name Missing.")
    
    # Check CSV
    if (not csv.filename.endswith(".csv")) and (not csv.filename.endswith(".CSV")):
        logger.error(f"Upload CSV from {user} => Not CSV File.")
        raise HTTPException(status_code = 400, detail="Not CSV File.")

    # Generate File Path
    file_Time = datetime.now().strftime('%Y%m%d%H%M%S')

    # Read csv request
    file_CSV = await csv.read()

    # Insert thread
    thread.insert_Queue(user, file_Time, file_CSV)

    return PlainTextResponse("ok")
