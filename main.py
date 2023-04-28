"""
실행방법

gunicorn --bind 0.0.0.0:5555 main:app --worker-class uvicorn.workers.UvicornWorker

"""
from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru                  import logger
from core.thread             import threadQueue
from core.init               import init_Server
from threading               import Event

import sys, os, __main__
import api.upload as upload
import api.getUser as getUser

# App init
app = FastAPI()

# Add API router
app.include_router(upload.router)
app.include_router(getUser.router)

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
    main_path = os.path.dirname(os.path.realpath(__file__))

    # Server init
    try:
        isInited = init_Server(main_path)
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

@app.get('/')
def rootIndex():
    return "Please read API docs."
