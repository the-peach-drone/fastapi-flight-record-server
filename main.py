from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru                  import logger
from core.thread             import threadQueue
from core.init               import init_Server
from threading               import Event

import uvicorn
import api.upload as upload

# App init
app = FastAPI()

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
    # Data process thread start
    thread.start()

    logger.success("Server init success. Server Ready...")

@app.on_event("shutdown")
def shutdown_server():
    # Data process thread end
    thread.event.set()

    logger.info("Server stop success. Closing Server...")

@app.get('/')
def rootIndex():
    return "Please read API docs."

if __name__ == "__main__":
    isInited = init_Server()
    if not isInited:
        logger.critical("server init failed. Please check log.")
    else:
        # Do not run with reload option
        uvicorn.run("main:app", host="0.0.0.0", port=5555)
