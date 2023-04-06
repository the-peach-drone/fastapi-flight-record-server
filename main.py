from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru                  import logger

import uvicorn
import API.Upload_CSV as UploadAPI
import Server.server_Init as server_Init

# App init
app = FastAPI()

# Add API router
app.include_router(UploadAPI.router)

# CORS SET
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["GET", "POST"],
    allow_headers = ["*"]
)

@app.get('/')
def rootIndex():
    return "Please read API docs."

if __name__ == "__main__":
    isInited = server_Init.init_Server()
    if not isInited:
        logger.critical("server init failed. Please check log.")
    else:
        # Do not run with reload option
        logger.success("Server init success. Server Ready...")
        uvicorn.run("main:app", host="0.0.0.0", port=5555)
        logger.info("Server stop success. Closing Server...")