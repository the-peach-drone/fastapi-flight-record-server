"""
실행방법

gunicorn --bind 0.0.0.0:5555 main:app --worker-class uvicorn.workers.UvicornWorker

"""
from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru                  import logger
from core.thread             import threadQueue
from core.init               import init_Server

import sys, __main__
import api.upload as upload

# App init, redoc & docs disable
app = FastAPI(docs_url=None, redoc_url=None)

# Add API router
app.include_router(upload.router)

# Data processing thread
thread = threadQueue()

# CORS SET
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["GET", "POST"],
    allow_headers = ["*"]
)

@app.on_event("startup")
def startup_server():
    # Server init
    try:
        isInited = init_Server()
        if not isInited:
            raise Exception('Server Init Fail.')
        else :
            # Data process thread start
            thread.start()
            logger.success("Server init success. Server Ready...")
    except Exception as err:
        sys.exit(4)

@app.on_event("shutdown")
def shutdown_server():
    # Data process thread end
    thread.event.set()

    logger.info("Server stop success. Closing Server...")
