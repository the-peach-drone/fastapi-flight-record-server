from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn, logging
import API.Upload_CSV     as UploadAPI
import Server.server_Init as server_Init

# App init
app = FastAPI()

# Logger
fileLogger = logging.getLogger('ServerFileLog')

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
    server_Init.init_Server()
    uvicorn.run(app, host="0.0.0.0", port=5555)